import datetime as dt
import json
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

import yaml

from redisbench_admin.run.common import extract_benchmark_tool_settings, prepare_benchmark_parameters, \
    merge_default_and_specific_properties_dictType, process_default_yaml_properties_file, get_start_time_vars
from redisbench_admin.run.redis_benchmark.redis_benchmark import redis_benchmark_from_stdout_csv_to_json, \
    redis_benchmark_ensure_min_version_local
from redisbench_admin.utils.local import (
    spinUpLocalRedis,
    getLocalRunFullFilename,
    isProcessAlive, checkDatasetLocalRequirements, )
from redisbench_admin.utils.remote import (
    extract_git_vars,
    validateResultExpectations,
)


def run_local_command_logic(args):
    (
        github_org_name,
        github_repo_name,
        github_sha,
        github_actor,
        github_branch,
        github_branch_detached,) = extract_git_vars()

    local_module_file = args.module_path

    logging.info("Retrieved the following local info:")
    logging.info("\tgithub_actor: {}".format(github_actor))
    logging.info("\tgithub_org: {}".format(github_org_name))
    logging.info("\tgithub_repo: {}".format(github_repo_name))
    logging.info("\tgithub_branch: {}".format(github_branch))
    logging.info("\tgithub_sha: {}".format(github_sha))

    return_code = 0
    files = []
    default_metrics = []
    exporter_timemetric_path = None
    defaults_filename = "defaults.yml"
    default_kpis = None
    if os.path.exists(defaults_filename):
        with open(defaults_filename, "r") as stream:
            logging.info(
                "Loading default specifications from file: {}".format(defaults_filename)
            )
            default_kpis, default_metrics, exporter_timemetric_path = process_default_yaml_properties_file(default_kpis,
                                                                                                           default_metrics,
                                                                                                           defaults_filename,
                                                                                                           exporter_timemetric_path,
                                                                                                           stream)

    if args.test == "":
        files = pathlib.Path().glob("*.yml")
        files = [str(x) for x in files]
        if defaults_filename in files:
            files.remove(defaults_filename)

        logging.info(
            "Running all specified benchmarks: {}".format(" ".join([str(x) for x in files]))
        )
    else:
        logging.info("Running specific benchmark in file: {}".format(args.test))
        files = [args.test]

    for usecase_filename in files:
        with open(usecase_filename, "r") as stream:
            dirname = os.path.dirname(os.path.abspath(usecase_filename))
            redis_process = None
            benchmark_config = yaml.safe_load(stream)
            kpis_keyname = "kpis"
            if default_kpis != None:
                merge_default_and_specific_properties_dictType(benchmark_config, default_kpis, kpis_keyname,
                                                               usecase_filename)

            test_name = benchmark_config["name"]
            # after we've spinned Redis, even on error we should always teardown
            # in case of some unexpected error we fail the test
            try:
                dirname = ".",
                # setup Redis
                # copy the rdb to DB machine
                dataset = None
                temporary_dir = tempfile.mkdtemp()
                logging.info(
                    "Using local temporary dir to spin up Redis Instance. Path: {}".format(
                        temporary_dir
                    )
                )
                checkDatasetLocalRequirements(benchmark_config, temporary_dir, dirname)

                redis_process = spinUpLocalRedis(
                    temporary_dir,
                    args.port,
                    local_module_file
                )
                if isProcessAlive(redis_process) is False:
                    raise Exception("Redis process is not alive. Failing test.")
                # setup the benchmark
                start_time, start_time_ms, start_time_str = get_start_time_vars()
                local_benchmark_output_filename = getLocalRunFullFilename(
                    start_time_str,
                    github_branch,
                    test_name,
                )
                logging.info(
                    "Will store benchmark json output to local file {}".format(
                        local_benchmark_output_filename
                    )
                )

                benchmark_min_tool_version, benchmark_min_tool_version_major, benchmark_min_tool_version_minor, benchmark_min_tool_version_patch, benchmark_tool = extract_benchmark_tool_settings(
                    benchmark_config)
                if benchmark_tool is not None:
                    logging.info("Detected benchmark config tool {}".format(benchmark_tool))
                else:
                    raise Exception("Unable to detect benchmark tool within 'clientconfig' section. Aborting...")

                if benchmark_tool is not None:
                    logging.info("Checking benchmark tool {} is accessible".format(benchmark_tool))
                    which_benchmark_tool = shutil.which(benchmark_tool)
                    if which_benchmark_tool is None:
                        raise Exception("Benchmark tool was not accesible. Aborting...")
                    else:
                        logging.info("Tool {} was detected at {}".format(benchmark_tool, which_benchmark_tool))

                if benchmark_tool not in args.allowed_tools.split(","):
                    raise Exception(
                        "Benchmark tool {} not in the allowed tools list [{}]. Aborting...".format(benchmark_tool,
                                                                                                   args.allowed_tools))

                if benchmark_min_tool_version is not None and benchmark_tool == "redis-benchmark":
                    redis_benchmark_ensure_min_version_local(benchmark_tool, benchmark_min_tool_version,
                                                             benchmark_min_tool_version_major,
                                                             benchmark_min_tool_version_minor,
                                                             benchmark_min_tool_version_patch)

                # prepare the benchmark command
                command, command_str = prepare_benchmark_parameters(benchmark_config, benchmark_tool, args.port,
                                                                    "localhost", local_benchmark_output_filename, False)

                # run the benchmark
                if benchmark_tool == 'redis-benchmark':
                    benchmark_client_process = subprocess.Popen(args=command, stdout=subprocess.PIPE,
                                                                stderr=subprocess.STDOUT)
                else:
                    benchmark_client_process = subprocess.Popen(args=command)
                (stdout, sterr) = benchmark_client_process.communicate()
                logging.info("Extracting the benchmark results")

                if benchmark_tool == 'redis-benchmark':
                    logging.info("Converting redis-benchmark output to json. Storing it in: {}".format(
                        local_benchmark_output_filename))
                    results_dict = redis_benchmark_from_stdout_csv_to_json(stdout.decode('ascii'), start_time_ms,
                                                                           start_time_str,
                                                                           overloadTestName="Overall")
                    with open(local_benchmark_output_filename, "w") as json_file:
                        json.dump(results_dict, json_file, indent=True)

                # check KPIs
                result = True
                with open(local_benchmark_output_filename, "r") as json_file:
                    results_dict = json.load(json_file)

                if "kpis" in benchmark_config:
                    result = validateResultExpectations(
                        benchmark_config, results_dict, result, expectations_key="kpis"
                    )
                    if result is not True:
                        return_code |= 1
            except:
                return_code |= 1
                logging.critical(
                    "Some unexpected exception was caught during remote work. Failing test...."
                )
                logging.critical(sys.exc_info())
        # tear-down
        logging.info("Tearing down setup")
        if redis_process is not None:
            redis_process.kill()
        logging.info("Tear-down completed")

    exit(return_code)
