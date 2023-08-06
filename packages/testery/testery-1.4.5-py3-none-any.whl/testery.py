import click
import json
import requests
import time
import sys
import os
import mimetypes
import tempfile
from zipfile import ZipFile
from requests_toolbelt.multipart.encoder import MultipartEncoder
import xml.etree.ElementTree as ET

# we have to do this right now because of how our S3 buckets are named. This should be removed once we've fixed that
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

def get_api_url(is_dev):
    if is_dev:
        return 'https://api.dev.testery.io/api'
    return 'https://api.testery.io/api'

def report_test_run(test_run, output):
    if output == "teamcity":
        report_teamcity_test_run(test_run)
    elif output == "json":
        print(test_run)
    else:
        report_pretty_test_run(test_run)

def report_pretty_test_run(test_run):
    if test_run['status'] == 'SUBMITTED':
        print("Waiting for test run to start")
    elif test_run['totalCount'] == 0 and test_run['status'] == 'RUNNING':
        print("Getting list of tests to run")
    elif test_run['totalCount'] == 0:
        print("No tests run")
    elif test_run['ignoredCount'] == 0:
        if test_run['status'] == 'RUNNING':
            text = "Running"
        else:
            text = "Completed"
        print("%s: %s of %s pass with %s fail" % (text, test_run['passCount'], test_run['totalCount'], test_run['failCount']))
    else:
        if test_run['status'] == 'RUNNING':
            text = "Running"
        else:
            text = "Completed"
        print("%s: %s of %s pass with %s fail and %s ignored" % (text, test_run['passCount'], test_run['totalCount'], test_run['failCount'], test_run['ignoredCount']))
    

def report_teamcity_test_run(test_run):
    if test_run['status'] == 'FAIL':
        print("##teamcity[buildProblem description='%s: %s passing, %s failing out of %s total']" % (
            test_run['status'], test_run['passCount'], test_run['failCount'], test_run['totalCount']))
    else:
        print("##teamcity[buildStatus text='%s: %s passing, %s failing out of %s total']" % (
            test_run['status'], test_run['passCount'], test_run['failCount'], test_run['totalCount']))

def api_wait_test_run(api_url, token, test_run_id, output, fail_on_failure):
    headers['Authorization'] = "Bearer " + token

    test_run = requests.get(api_url + '/test-runs/' + str(test_run_id), headers=headers).json()

    report_test_run(test_run, output)

    while test_run['status'] not in ['PASS', 'FAIL', 'CANCELED']:
        time.sleep(15)
        test_run = requests.get(api_url + '/test-runs/' + str(test_run_id), headers=headers).json()
        report_test_run(test_run, output)

    if (test_run['status'] == 'FAIL' or test_run['status'] == 'CANCELED') and fail_on_failure:
        sys.exit(1)

def api_wait_deploy(api_url, token, deploy_id, output, fail_on_failure):
    headers['Authorization'] = "Bearer " + token

    test_runs = requests.get(api_url + '/test-runs/by-deploy/' + str(deploy_id), headers=headers).json()

    for test_run in test_runs:
        click.echo("Waiting for test run: %s" % test_run['id'])
        api_wait_test_run(api_url, token, test_run['id'], output, fail_on_failure)
    
    click.echo("All test runs for deployment #%s are complete." % deploy_id)


@click.group()
def cli():
    """
    Testery CLI\n
    Kick off test runs from your CI/CD platform and run them on Testery's next-generation, cloud-based testing grid.
    """
    pass


@click.command('verify-token')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', help='Your Testery API token.')
def verify_token(testery_dev, token):
    """
    Verifies your username and authentication token are valid.
    """
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)

    response = requests.get(api_url + '/account', headers=headers)

    if response.status_code == 200:
        print("Valid token")
    else:
        print("Invalid token")


@click.command('create-test-run')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--git-ref', default=None, help='The git commit hash of the build being tested.')
@click.option('--git-branch', default=None, help='The git branch whose latest commit you wnat to run.')
@click.option('--test-name', default=None, help='The name you want to use on the Git status.')
@click.option('--wait-for-results', is_flag=True, help='If set, the command will poll until the test run is complete.')
@click.option('--project', default=None, help='Legacy option. Use --project-key instead.')
@click.option('--project-key', default=None, help='The project key.')
@click.option('--environment', default=None, help="Legacy option. Use --environment-key instead.")
@click.option('--environment-key', default=None, help='Which environment you would like to run your tests against.')
@click.option('--include-tags', help='List of tags that should be run.')
@click.option('--exclude-tags', help='List of tags that should excluded from the test run.')
@click.option('--copies', default=1, type=int, help='The number of copies of the tests to submit.')
@click.option('--build-id', default=None, help='A unique identifier that identifies this build in your system.')
@click.option('--output', default='pretty', help='The format for outputting results [json,pretty,teamcity]')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
@click.option("--include-all-tags", is_flag=True, help='When set, overrides the testery.yml and runs all available tags.')
@click.option("--parallelize-by-file", is_flag=True, help='Pass this flag if you want the test run to parallelize by file/feature.')
@click.option("--parallelize-by-test", is_flag=True, help='Pass this flag if you want the test run to parallelize by test/scenario.')
@click.option("--timeout-minutes", default=None, type=int, help='The maximum number of minutes this test run can take before it is killed automatically.')
@click.option("--test-timeout-seconds", default=None, type=int, help='The maximum number of seconds a test can take before it is killed automatically.')
@click.option("--runner-count", default=None, type=int, help='Specify number of parallel runners to use in for this testrun.')
@click.option('--variable', help='A variable to add to the enviroment. Specified as "KEY=VALUE". To encrypt value, pass in "secure:KEY=VALUE", Multiple variables can be provided.', multiple=True)
@click.option('--test-filter-regex', help='A regular expression to be used for filtering tests.', multiple=True)
def create_test_run(testery_dev, token, git_ref, git_branch, test_name, wait_for_results, output, project, project_key, environment, environment_key, include_tags, exclude_tags, copies, build_id, fail_on_failure, include_all_tags, parallelize_by_file, parallelize_by_test, runner_count, variable, timeout_minutes, test_timeout_seconds, test_filter_regex):
    """
    Submits a Git-based test run to the Testery platform.
    """
    test_run_request = {"project": project_key or project, "environment": environment_key or environment}
    api_url = get_api_url(testery_dev)

    if(test_run_request["project"] == None):
        raise Exception("You must specify a project key with the --project-key option")

    if(test_run_request["environment"] == None):
        raise Exception("You must specify an environment key with the --environment-key option")

    if git_ref:
        test_run_request['ref'] = git_ref

    if git_branch:
        test_run_request['branch'] = git_branch

    if build_id:
        test_run_request['buildId'] = build_id

    if test_name:
        test_run_request['testName'] = test_name

    if include_tags:
        test_run_request['includeTags'] = include_tags.split(',')

    if exclude_tags:
        test_run_request['excludedTags'] = exclude_tags.split(',')

    if parallelize_by_file:
        test_run_request['parallelizeByFile'] = True

    if parallelize_by_test:
        test_run_request['parallelizeByFile'] = False

    if timeout_minutes:
        test_run_request['timeoutMinutes'] = timeout_minutes

    if test_timeout_seconds:
        test_run_request['testTimeoutSeconds'] = test_timeout_seconds 

    if runner_count:
        test_run_request['runners'] = runner_count

    if include_all_tags:
        test_run_request['includeTags'] = []

    if copies:
        test_run_request['copies'] = copies


    if test_filter_regex:
        testFilters = []
        for filter in test_filter_regex:
            f = "Regex: " + filter
            testFilters.append(f)
        test_run_request["testFilters"]=testFilters

    handle_variables(variable, test_run_request)

    print(test_run_request)

    headers['Authorization'] = "Bearer " + token
    test_run_response = requests.post(api_url + '/test-run-requests-build',
                                      headers=headers,
                                      json=test_run_request)

    if test_run_response.status_code != 201:
        if test_run_response.status_code == 404:
            message = "Failed to create test run for project " + project + ". Please make sure you have the correct project key and environment key."
        else:
            message = "Failed to create test run, status code: " + str(test_run_response.status_code)

        raise Exception(message)
    else:
        test_run = test_run_response.json()

        test_run_id = str(test_run['id'])

        click.echo("test_run_id: %s" % test_run_id)

        if wait_for_results:
            api_wait_test_run(api_url, token, test_run_id, output, fail_on_failure)

@click.command('create-environment')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--name', required=True, help='The display name for the environment.')
@click.option('--key', required=True, help='An identifier for the environment. This is used when creating test runs to indicate where tests should run.')
@click.option('--pipeline-stage', default=None, help='The name of a pipeline stage to associate this environment to.')
@click.option('--variable', help='A variable to add to the enviroment. Specified as "KEY=VALUE". To encrypt value, pass in "secure:KEY=VALUE", Multiple variables can be provided.', multiple=True)
def create_environment(testery_dev, token, key, name, variable, pipeline_stage):
    """
    Creates an environment where tests can be run.
    """
    headers['Authorization'] = "Bearer " + token

    environment_request = {"key": key, "name": name}
    api_url = get_api_url(testery_dev)

    if pipeline_stage:
        stages_response = requests.get(api_url + '/pipeline-stages', headers=headers)

        stages = stages_response.json()
        pipeline_stage_id = None

        for stage in stages:
            if stage['name'].lower() == pipeline_stage.lower():
                pipeline_stage_id = stage['id']
                
        if pipeline_stage_id:
            environment_request['pipelineStageId'] = pipeline_stage_id
        else:
            stageNames = map(lambda s: s['name'], stages) 
            message = "Could not find pipeline stage with name '" + pipeline_stage + "'. Known names: " + ', '.join(stageNames)
            raise Exception(message)

    handle_variables(variable, environment_request)

    print(environment_request)

    headers['Authorization'] = "Bearer " + token
    response = requests.post(api_url + '/environments',
                                      headers=headers,
                                      json=environment_request)

    print(response.json())

@click.command('create-schedule')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--git-ref', default=None, help='The git commit hash of the tests you want to run. Defaults to latest.')
@click.option('--git-branch', default=None, help='The git branch whose latest commit you want to run.')
@click.option('--build-id', default=None, help='The build id you want to run if not running the latest.')
@click.option('--schedule-name', required=True, default=None, help='The name for the schedule.')
@click.option('--schedule-type', required=True, default=None, type=click.Choice(['interval','deploy']), help='Select schedule type of "interval" to run on a schedule or "deploy" to run when a deploy is created.')
@click.option('--cron', default=None, help='The cron expression for the schedule. Requires --schedule-type interval')
@click.option('--priority', default=None, type=int, help='The priority to assign to test runs from this schedule.')
@click.option('--project-key', required=True, help='The project key.')
@click.option('--environment-key', required=True, default=None, help='Environment key for the environment where tests should run.')
@click.option('--include-tags', help='List of tags that should be run.')
@click.option('--exclude-tags', help='List of tags that should excluded from the test run.')
@click.option('--copies', default=1, type=int, help='The number of copies of the tests to submit.')
@click.option('--output', default='pretty', help='The format for outputting results [json,pretty,teamcity]')
@click.option('--on-deploy', is_flag=True, help='Pass this flag to trigger schedule when another project is deployed. Requires one or more --deploy-project.')
@click.option("--include-all-tags", is_flag=True, help='When set, overrides the testery.yml and runs all available tags.')
@click.option("--parallelize-by-file", is_flag=True, help='Pass this flag if you want the test run to parallelize by file/feature.')
@click.option("--parallelize-by-test", is_flag=True, help='Pass this flag if you want the test run to parallelize by test/scenario.')
@click.option("--follow-test-run", is_flag=True, help='Pass this flag if you want to be notified of test run events.')
@click.option("--timeout-minutes", default=None, type=int, help='The maximum number of minutes this test run can take before it is killed automatically.')
@click.option('--test-filter-regex', help='A regular expression to be used for filtering tests.', multiple=True)
@click.option("--test-timeout-seconds", default=None, type=int, help='The maximum number of seconds a test can take before it is killed automatically.')
@click.option("--run-specific-version", default=None, is_flag=True, help='Pass this flag to run a specific version of the tests instead of the latest. Used with --branch, --build-id, and --commit.')
@click.option("--retry-failed-tests", default=False, is_flag=True, help='Pass this flag to automatically retry tests.')
@click.option("--runner-count", default=None, type=int, help='Specify number of parallel runners to use in for this testrun.')
@click.option('--variable', help='A variable to add to the enviroment. Specified as "KEY=VALUE". To encrypt value, pass in "secure:KEY=VALUE", Repeat switch to add values.', multiple=True)
@click.option('--deploy-project', help='Project key for project that should start schedules. Repeat to provide additional projects.', multiple=True)
@click.option('--deploy-on-any-project', is_flag=True, help='When specified, test run will fire when any project is deployed.')

def create_schedule(testery_dev, token, git_ref, git_branch, build_id, priority, run_specific_version, schedule_name, project_key, cron, follow_test_run, on_deploy, schedule_type, environment_key, include_tags, exclude_tags, copies, output, include_all_tags, parallelize_by_file, parallelize_by_test, runner_count, variable, timeout_minutes, test_timeout_seconds, test_filter_regex, deploy_project, retry_failed_tests, deploy_on_any_project):
    """
    Creates a test run schedule.
    """

    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)
    environments_response = requests.get(api_url + '/environments', headers=headers)

    schedule_request = {
        "branch": git_branch,
        "buildName": build_id,
        "copies": 1,
        "cron": cron,
        "defaultToParallelizeByFile": parallelize_by_file,
        "environmentId": find_environment_by_key(api_url, token, environment_key)['id'],
        "followTestRun": follow_test_run,
        "latestDeploy": not run_specific_version,
        "name": schedule_name,
        "onDeploy": on_deploy,
        "projectId": find_project_by_key(api_url, token, project_key)['id'],
        "retryFailedTests": retry_failed_tests,
        "scheduleType": schedule_type,
        "testFilters": [],
        "testName": None
    }

    if git_branch:
        schedule_request['branch'] = git_branch

    if git_ref:
        schedule_request['commit'] = git_ref

    if build_id:
        schedule_request['buildName'] = build_id

    if include_tags:
        schedule_request['includeTags'] = include_tags.split(',')

    if exclude_tags:
        schedule_request['excludedTags'] = exclude_tags.split(',')
    
    if parallelize_by_file:
        schedule_request['parallelizeByFile'] = True

    if parallelize_by_test:
        schedule_request['parallelizeByFile'] = False

    if priority:
        schedule_request["priority"]: priority

    if timeout_minutes:
        schedule_request['timeoutMinutes'] = timeout_minutes

    if test_timeout_seconds:
        schedule_request['testTimeoutSeconds'] = test_timeout_seconds 

    if runner_count:
        schedule_request['maxRunners'] = runner_count

    if include_all_tags:
        schedule_request['includeTags'] = []

    if copies:
        schedule_request['copies'] = copies


    if test_filter_regex:
        testFilters = []
        for filter in test_filter_regex:
            f = "Regex: " + filter
            testFilters.append(f)
        schedule_request["testFilters"]=testFilters

    if deploy_project or deploy_on_any_project:
        deployedProjectIds = []

        if (deploy_on_any_project):
            print( "Deploy on any project")
            deployedProjectIds.append(0)
        else:
            print("Deploy on specific project")
            for project_key in deploy_project:
                deployedProjectIds.append(find_project_by_key(api_url, token, project_key)['id'])

        schedule_request["deployedProjectIds"]=deployedProjectIds

    handle_variables(variable, schedule_request)

    print(json.dumps(schedule_request, indent=1))

    headers['Authorization'] = "Bearer " + token
    schedule_response = requests.post(api_url + '/schedules', headers=headers, json=schedule_request)
    
    if schedule_response.status_code != 201:
        if schedule_response.status_code == 500:
            result = schedule_response.json()
            message = str(result['message'])
        else:
            message = "Failed to create schedule, status code: " + str(schedule_response.status_code)
        raise Exception(message)
    else:
        schedule = schedule_response.json()
        schedule_id = str(schedule['id'])
        click.echo("schedule_id: %s" % schedule_id)


@click.command('delete-environment')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--key', required=True, help='An identifier for the environment. This is used when creating test runs to indicate where tests should run.')
def delete_environment(testery_dev, token, key):
    """
    Deletes an environment.
    """
    
    # Look up environment id by key.
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)
    environments_response = requests.get(api_url + '/environments', headers=headers)

    environments = environments_response.json()

    for environment in environments:
        if environment['key'] == key:
            print('DELETE %s/environments/%s' % (api_url, environment['id']))
            response = requests.delete(api_url + '/environments/' + str(environment['id']),headers=headers)
            print(response)

@click.command('delete-schedule')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--name', required=True, help='Name of the schedule to remove.')
def delete_schedule(testery_dev, token, name):
    """
    Deletes a schedule.
    """
    
    # Look up by key.
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)
    response = requests.get(api_url + '/schedules', headers=headers)

    schedules = response.json()

    for schedule in schedules:
        if schedule['name'] == name:
            print('DELETE %s/schedules/%s' % (api_url, schedule['id']))
            response = requests.delete(api_url + '/schedules/' + str(schedule['id']),headers=headers)
            print(response)

def find_environment_by_key(api_url, token, environment_key):
    environments_response = requests.get(api_url + '/environments', headers=headers)

    environments = environments_response.json()

    for environment in environments:
        if environment['key'] == environment_key:
            return environment
    
    raise Exception("Environment with key not found: " + environment_key)

def find_project_by_key(api_url, token, project_key):
    response = requests.get(api_url + '/projects', headers=headers)

    projects = response.json()

    for project in projects:
        if project['key'] == project_key:
            return project
    
    raise Exception("Project with key not found: " + project_key)    

def handle_variables(variables, request):
    if variables:
        vars = []
        for var in variables:
            (vkey,vval) = var.split("=")

            if vkey.startswith("secure:"):
                vkey = vkey.replace("secure:","")
                encrypted=True
            else:
                encrypted=False

            v = {"key": vkey, "value": vval, "encrypted": encrypted}
            vars.append(v)
        request["variables"]=vars

@click.command('update-environment')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--name', required=True, help='The display name for the environment.')
@click.option('--key', required=True, help='An identifier for the environment. This is used when creating test runs to indicate where tests should run.')
@click.option('--variable', help='A variable to add to the enviroment. Specified as "KEY=VALUE". To encrypt value, pass in "secure:KEY=VALUE", Multiple variables can be provided.', multiple=True)
@click.option('--create-if-not-exists', is_flag=True, default=False, help='If passed in, environment will be created if not present. Otherwise command will fail.')
def update_environment(testery_dev, token, key, name, variable, create_if_not_exists):
    """
    Updates an environment where tests can be run.
    """
    environment_request = {"key": key, "name": name}

    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)
    
    environments_response = requests.get(api_url + '/environments', headers=headers)

    environments = environments_response.json()

    print(environments)

    environment = next(iter([environment for environment in environments if environment['key']==key]), None)

    if not environment and not create_if_not_exists:
        raise Exception("Environment not found by key and --create-if-not-exists flag was not set: " + key)

    headers['Authorization'] = "Bearer " + token
    
    if environment:
        environment["name"]=name
        handle_variables(variable, environment)
        print("Updating environment: " + key)
        print(environment)
        response = requests.patch(api_url + '/environments/' + str(environment['id']), headers=headers, json=environment)
    else:
        environment_request = {"key": key, "name": name}
        handle_variables(variable, environment_request)
        print("Creating environment: " + key)
        response = requests.post(api_url + '/environments', headers=headers, json=environment_request)
    
    print(response)

@click.command('list-environments')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
def list_environments(testery_dev, token):
    """
    Returns a list of environments.
    """
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)
    response = requests.get(api_url + '/environments',
                                      headers=headers)

    print(json.dumps(response.json()))

@click.command('upload-build-artifacts')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--project', default=None, help='Legacy option. Use --project-key instead.')
@click.option('--project-key', default=None, help='The project key.')
@click.option('--branch', default=None, help='The Git branch the build came from.')
@click.option('--build-id', required=True, help='The build the artifact should be associated with.')
@click.option('--path', required=True, help='The path to the file or directory you want to upload.')
@click.option("--zip-dir", is_flag=True, help='Creates a zip file of the directory contents before uploading.')
def upload_build_artifacts(testery_dev, token, project, project_key, branch, build_id, path, zip_dir):
    """
    Uploads a file or directory of build artifacts and associates them with the specified build-id
    """
    if(project_key == None and project == None):
        raise Exception("You must specify a project key with the --project-key option")

    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)
    base_api_url = api_url + '/projects/' + (project_key or project) + '/upload-url?build=' + build_id

    if branch:
        base_api_url += '&branch=' + branch

    base_api_url += '&file='

    if os.path.isdir(path):
        if zip_dir:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_file = create_zip_file(path, temp_dir)
                upload_build_artifact_file(base_api_url, zip_file.filename, "")
        else:
            upload_build_artifact_dir(base_api_url, path, "")
    else:
        upload_build_artifact_file(base_api_url, path, "")


def create_zip_file(path, temp_dir):
    zip_file = ZipFile(os.path.join(temp_dir, str(time.time()) + '.zip'), 'w')
    len_path = len(path)
    with zip_file as zip_file:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, file_path[len_path:])
    return zip_file


def upload_build_artifact_dir(base_api_url, file_path, dir_path):
    for file in os.listdir(file_path):
        new_file_path = os.path.join(file_path, file)
        if os.path.isdir(new_file_path):
            dir_name = os.path.basename(new_file_path)
            upload_build_artifact_dir(
                base_api_url, new_file_path, dir_path + dir_name + '/')
        else:
            upload_build_artifact_file(base_api_url, new_file_path, dir_path)


def upload_build_artifact_file(base_api_url, file_path, dir_path):
    file = dir_path + os.path.basename(file_path)

    upload_result = requests.get(base_api_url + file, headers=headers)

    upload_url = upload_result.text

    if upload_result.status_code != 200 or upload_url == "invalid request":
        raise Exception("Could not upload artifacts. Make sure you specified the correct project key.")

    result = upload_file(
        upload_url, {'Accept': 'application/json'}, file_path, False)

    if result.status_code != 200:
        raise Exception("Got status code " + str(result.status_code) +
                        " when trying to upload file with path " + file_path)


@click.command('create-deploy')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', required=True, help='Your Testery API token.')
@click.option('--project', required=True, help='The project key of the repo being deployed.')
@click.option('--git-provider', default=None, help='The Git provider used for the repository that is being deployed. Should be GitHub or BitBucket')
@click.option('--git-owner', default=None, help='The organization owner in Git for the repository that is being deployed.')
@click.option('--git-repo', default=None, help='The repository name that is being deployed.')
@click.option('--build-id', default=None, help='The build the artifact should be associated with.')
@click.option('--environment', required=True, help='Which environment you would like to run your tests against.')
@click.option('--commit', default=None, help='The Git commit that was deployed.')
@click.option('--branch', default=None, help='The Git branch the deploy came from.')
@click.option('--wait-for-results', is_flag=True, help='If set, the command will poll until the all test runs triggered by the deploy (defined in Schedules) are complete.')
@click.option('--output', default='pretty', help='The format for outputting results [json,pretty,teamcity]')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
def create_deploy(testery_dev, token, project, git_provider, git_owner, git_repo, environment, commit, build_id, branch, wait_for_results, output, fail_on_failure):
    """
    Creates a deploy for a project and environment.
    """
    deploy_request = {"environment": environment, "project": project}
    api_url = get_api_url(testery_dev)

    if git_provider:
        deploy_request['gitProvider'] = git_provider
        deploy_request['gitOwner'] = git_owner
        deploy_request['gitRepo'] = git_repo

    if build_id:
        deploy_request['buildId'] = build_id

    if branch:
        deploy_request['branch'] = branch

    if commit:
        deploy_request['commit'] = commit

    print(deploy_request)

    headers['Authorization'] = "Bearer " + token
    deploy_response = requests.post(api_url + '/deploys', headers=headers, json=deploy_request)

    if deploy_response.status_code != 201:
        if deploy_response.status_code == 500:
            result = deploy_response.json()
            message = str(result['message'])
        else:
            message = "Failed to create deploy, status code: " + str(deploy_response.status_code)
        raise Exception(message)
    else:
        deploy = deploy_response.json()
        deploy_id = str(deploy['id'])
        click.echo("deploy_id: %s" % deploy_id)
    
    if wait_for_results:
        api_wait_deploy(api_url, token, deploy_id, output, fail_on_failure)


@click.command('cancel-test-run')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', help='Your Testery API token.')
@click.option('--test-run-id', help='The ID of the test run to cancel.')
def cancel_test_run(testery_dev, token, test_run_id):
    """
    Cancels a test run.
    """
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)

    test_run = requests.get(
        api_url + '/test-runs/' + str(test_run_id), headers=headers).json()

    if test_run['status'] not in ['PASS', 'FAIL', 'CANCELED']:

        test_run_response = requests.patch(api_url + '/test-runs/' + test_run_id,
                                           headers=headers,
                                           json={"status": "CANCELED"})

        print(test_run_response)

        test_run = test_run_response.json()

        print(test_run)


@click.command('add-file')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', help='Your Testery API token.')
@click.option('--test-run-id', help='The ID of the test run to add the file to.')
@click.option('--kind', help='The kind of file you are uploading. For an DotCover JSON file put DotCover')
@click.argument('file_path')
def add_file(testery_dev, token, test_run_id, file_path, kind):
    """
    Adds a file to a test run.
    """
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)
    url = api_url + '/test-runs/' + str(test_run_id) + '/add-file/' + kind
    result = upload_file(url, headers, file_path, True).json()

    print(result)


def upload_file(url, headers, file_path, for_add_file):
    file_name = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]

    if mime_type is None:
        mime_type = "text/plain"

    if for_add_file:
        data = MultipartEncoder(
            fields={'file': (file_name, open(file_path, 'rb'), mime_type)})
        headers['Content-Type'] = data.content_type
        return requests.post(url, headers=headers, data=data)
    else:
        headers['Content-Type'] = mime_type
        data = open(file_path, 'rb')
        return requests.put(url, data=data, verify=False)


@click.command('monitor-test-run')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', help='Your Testery API token.')
@click.option('--test-run-id', help='The ID for the test run you would like to monitor and wait for.')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
@click.option('--output', default='pretty', help='The format for outputting results [json,pretty,teamcity]')
def monitor_test_run(testery_dev, token, test_run_id, output, fail_on_failure):
    api_url = get_api_url(testery_dev)
    api_wait_test_run(api_url, token, test_run_id, output, fail_on_failure)

@click.command('monitor-test-runs')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', help='Your Testery API token.')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
@click.option('--output', default='pretty', help='The format for outputting results [json,pretty,teamcity]')
def monitor_test_runs(testery_dev, token, output, fail_on_failure):
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)

    if username is None:
        username = os.environ['TESTERY_USERNAME']

    if token is None:
        token = os.environ['TESTERY_TOKEN']

    while True:
        test_runs = requests.get(
            api_url + '/test-runs?page=0&limit=250', headers=headers).json()
        try:
            for test_run in test_runs:
                if test_run['status'] in ['PENDING', 'RUNNING', 'SUBMITTED']:
                    test_run_updated = requests.get(api_url + '/test-runs/' + str(
                        test_run['id']), headers=headers).json()
                    # print(test_run_updated)
                    print("Test run %s was %s and is now %s. There are %s passing out of %s with %s failing." % (
                        test_run.get('id'), test_run.get('status'), test_run_updated.get('status'), test_run_updated.get('passCount'), test_run_updated.get('totalCount'), test_run_updated.get('failCount')))
                    time.sleep(1)

            print('...')
            time.sleep(60)
        except TypeError:
            print("Invalid response: ", test_runs)
            return False


@click.command('load-users')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', help='Your Testery API token.')
@click.option("--user-file", help='List of email addresses to load as user accounts.')
def load_users(testery_dev, token, user_file):
    headers['Authorization'] = "Bearer " + token
    api_url = get_api_url(testery_dev)

    user_file_data = open(user_file, "r")

    for email in user_file_data:
        print("Adding %s to account" % email.rstrip())

        user_request = {"email": email.rstrip(), "roleType": "USER"}

        user_response = requests.post(
            api_url + '/user-roles', headers=headers, json=user_request)

        print(user_response)

    # while True:
    #     test_runs= requests.get(api_url + '/test-runs?page=0&limit=100', headers=headers).json()
    #     for test_run in test_runs:
    #         if test_run['status'] in ['PENDING','RUNNING','SUBMITTED']:
    #             test_run_updated = requests.get(api_url + '/test-runs/' + str(test_run['id']), headers=headers).json()
    #             # print(test_run_updated)
    #             print("Test run %s was %s and is now %s. There are %s passing out of %s with %s failing." % (test_run['id'], test_run['status'], test_run_updated['status'], test_run_updated['passCount'], test_run_updated['totalCount'], test_run_updated['failCount']))

    #     time.sleep(60)

@click.command('report-test-run', help='Outputs individual test results for the entire run to the specified destination in the specified format.')
@click.option('--testery-dev', is_flag=True, default=False, hidden=True)
@click.option('--token', help='Your Testery API token.')
@click.option('--test-run-id', help='The ID for the test run you would like to monitor and wait for.')
@click.option("--fail-on-failure", is_flag=True, help='When set, the testery command will return exit code 1 if there are test failures.')
@click.option('--output', default="sonarcube", help='The format for outputting results [sonarcube]')
@click.option('--outfile', default="results.xml", help='The filename to write the results to.')
def report_test_run_cmd(testery_dev, token, test_run_id, fail_on_failure, output, outfile):
    api_url = get_api_url(testery_dev)
    
    api_wait_test_run(api_url, token, test_run_id, output, fail_on_failure)
    
    headers['Authorization'] = "Bearer " + token

    test_run = requests.get(api_url + '/test-runs/' + str(test_run_id), headers=headers).json()

    test_run_results = requests.get(api_url + '/test-runs/' + str(test_run_id) + '/results', headers=headers).json()

    test_executions = ET.Element('testExecutions')
    test_executions.set('version','1')
    
    for test_run_result in test_run_results:

        file_node = ET.SubElement(test_executions, 'file')
        file_node.set('path', test_run_result.get('fileFilter'))

        test_case_node = ET.SubElement(file_node, 'testCase')
        test_case_node.set('name',test_run_result.get('name'))
        test_case_node.set('duration','{0:g}'.format(test_run_result.get('duration')))

        if test_run_result.get('stackTrace'):
            print("Stack trace: %s" % str(test_run_result.get('stackTrace')))

        if test_run_result.get('status') == 'FAIL':
            error_node = ET.SubElement(test_case_node, 'error')
            error_node.set('message', 'Failed')
            if test_run_result.get('stackTrace') is not None:
                error_text = test_run_result.get('error') + test_run_result.get('stackTrace')
            else:
                error_text = test_run_result.get('error')
            error_node.text = error_text
        elif test_run_result.get('status') == 'IGNORED':
            error_node.set('message', 'Skipped')
            error_node = ET.SubElement(test_case_node, 'skipped')
            error_node.text = "Test was marked as ignored."
        elif test_run_result.get('status') == 'PASS':
            # No error node needed
            pass 
        else:
            error_node.set('message', 'Unrecognized test status')
            error_node = ET.SubElement(test_case_node, 'error')
            error_node.text = "Unrecognized status: %s" % test_run_result.get('status') 

            

    # Write output

    xml_data = ET.tostring(test_executions)
    xml_file = open(outfile, "wb")
    xml_file.write(xml_data)

cli.add_command(create_environment)
cli.add_command(update_environment)
cli.add_command(delete_environment)

cli.add_command(create_schedule)
cli.add_command(delete_schedule)

cli.add_command(create_deploy)
cli.add_command(list_environments)
cli.add_command(cancel_test_run)
cli.add_command(create_test_run)
cli.add_command(report_test_run_cmd)
cli.add_command(add_file)
cli.add_command(monitor_test_run)
cli.add_command(monitor_test_runs)
cli.add_command(verify_token)
cli.add_command(load_users)
cli.add_command(upload_build_artifacts)

if __name__ == '__main__':
    cli()
