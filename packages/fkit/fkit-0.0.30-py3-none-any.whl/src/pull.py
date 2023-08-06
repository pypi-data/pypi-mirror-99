from src import common, config, project, log
import os, json, docker, configparser
myLogger = log.Logger()

def pull(toolName):
    toolNameArray = toolName.split(':')
    pullToolEntity = common.get(url=common.get_cloud_base_url() + '/tool/toolversion/info', params={'toolName': toolNameArray[0], 'version': toolNameArray[1], 'projectId': project.getProjectId()})
    if pullToolEntity is None:
        myLogger.error_logger('The tool version id error')

    auth = common.get(url=common.get_cloud_base_url() + '/tool/pass')
    client = docker.from_env(timeout=100000000)
    print("pulling, please wait")
    client.images.pull(repository=common.get_docker_registry() + '/' + pullToolEntity['path'],
                       tag="latest",
                       auth_config={'username': auth['account'], 'password': auth['password']})

    image = client.images.get(common.get_docker_registry() + '/' + pullToolEntity['path'] + ':latest')
    image.tag(repository=pullToolEntity['name'], tag=str(pullToolEntity['version']))
    client.images.remove(common.get_docker_registry() + '/' + pullToolEntity['path'] + ':latest')

    curPath = os.getcwd()
    config = configparser.ConfigParser()
    config.add_section('input')
    for input in pullToolEntity['inputs']:
        if input['type'] is 1:
            config.set('input', input['name'], '[]')
        else:
            config.set('input', input['name'], '')

    config.add_section('output')
    config.set('output', 'outdir', '')
    with open(curPath + '/run.ini', 'w+') as f:
        config.write(f)
    print("pull successful")
