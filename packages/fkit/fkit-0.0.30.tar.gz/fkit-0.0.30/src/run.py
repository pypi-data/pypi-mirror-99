import docker, os, json, re, configparser
from src import create, log, common, project
myLogger = log.Logger()

def run(lName, file):
    if toolName is None:
        myLogger.error_logger("Please select the tool name")
        return

    if file is None or not os.path.exists(file):
        myLogger.error_logger("Please select the correct tool ini file")
        return

    param = {
        'projectId': project.getProjectId(),
        'toolName': toolName.split(':')[0],
        'version': toolName.split(':')[1]
    }
    toolVersionEntity = common.get(url=common.get_cloud_base_url() + '/tool/toolversion/info', params=param)
    if toolVersionEntity is None:
        myLogger.error_logger("Please enter the correct tool version ID")
        return
    cmd = toolVersionEntity['cmd']
    pattern = re.compile('#{.*?}')
    params = pattern.findall(cmd)

    config = configparser.ConfigParser()
    config.read(file, encoding='utf-8')
    inputPortNames = config.options('input')
    outputPath = config.get('output', 'outdir').replace('"', '')

    for i, param in enumerate(params):
        for toolCmdParam in toolVersionEntity['params']:
            if toolCmdParam['index'] == i:
                if toolCmdParam['type'] == 0 or toolCmdParam['type'] == 1:
                    cmd = cmd.replace(param, toolCmdParam['prefix'] + toolCmdParam['paramValue'], 1)

                if toolCmdParam['type'] == 2:
                    cmdParam = toolCmdParam['prefix']
                    for inputPort in toolVersionEntity['inputs']:
                        if inputPort['dir'] == toolCmdParam['paramKey']:
                            if inputPort['inCmd'] == 1:
                                for portName in inputPortNames:
                                    if portName == inputPort['name']:
                                        if inputPort['type'] == 0:
                                            filePath = config.get('input', portName)
                                            filePath = filePath.replace('"', '')
                                            (path, filename) = os.path.split(filePath)
                                            cmdParam = cmdParam + '/input/' + inputPort['dir'] + '/' + filename
                                        else:
                                            files = json.loads(config.get('input', portName))
                                            for file in files:
                                                (path, filename) = os.path.split(file)
                                                cmdParam = cmdParam + '/input/' + inputPort['dir'] + '/' + filename + ' '
                            else:
                                cmdParam = cmdParam + '/input/' + inputPort['dir'] + '/'


                    cmd = cmd.replace(param, cmdParam, 1)

                if toolCmdParam['type'] == 3:
                    if (not os.path.exists(outputPath + '/' + toolCmdParam['paramKey'])):
                        os.mkdir(outputPath + '/' + toolCmdParam['paramKey'])
                    cmdParam = toolCmdParam['prefix']
                    for outputPort in toolVersionEntity['outputs']:
                        if outputPort['dir'] == toolCmdParam['paramKey']:
                            if outputPort['inCmd'] == 1:
                                cmdParam = cmdParam + '/output/' + outputPort['dir'] + '/' + outputPort['namePattern']
                            else:
                                cmdParam = cmdParam + '/output/' + outputPort['dir'] + '/'



                    cmd = cmd.replace(param, cmdParam, 1)


    cmd = cmd.replace("\r\n", " ")
    cmd = cmd.replace("\n", " ")
    cmd = cmd.replace("\r", " ")
    auth = common.get(url=common.get_cloud_base_url() + '/tool/pass')
    client = docker.from_env(timeout=1000000)
    client.images.pull(repository=common.get_docker_registry() + '/' + toolVersionEntity['path'],
                       tag="latest",
                       auth_config={'username': auth['account'], 'password': auth['password']})
    image = client.images.get(common.get_docker_registry() + '/' + toolVersionEntity['path'] + ':latest')
    image.tag(repository=toolVersionEntity['name'], tag=str(toolVersionEntity['version']))
    client.images.remove(common.get_docker_registry() + '/' + toolVersionEntity['path'] + ':latest')


    mountList = []
    for inputPortName in inputPortNames:
        line = config.get('input', inputPortName)

        inputDir = ''
        for input in toolVersionEntity['inputs']:
            if input['name'] == inputPortName:
                inputDir = input['dir']
        if line.startswith('['):
            pathList = json.loads(line)
            for path in pathList:
                (path, filename) = os.path.split(path)
                mountList.append({
                    path: {'bind': '/input/' + inputDir + '/', 'mode': 'rw'}
                })
        else:
            line = line.replace('"', '')
            (path, filename) = os.path.split(line)
            mountList.append({
                path: {'bind': '/input/' + inputDir + '/', 'mode': 'rw'}
            })

    mountList.append({
        outputPath: {'bind': '/output', 'mode': 'rw'}
    })

    volumes = {}
    for mountFile in mountList:
        for key in mountFile:
            volumes[key] = mountFile[key]

    container = client.containers.run(image=toolVersionEntity['name'] + ':' + str(toolVersionEntity['version']),
                                      auto_remove=True,
                                      stdout=True,
                                      stderr=True,
                                      command=["/bin/sh", "-c", cmd],
                                      detach=True,
                                      volumes=volumes,
                                      working_dir='/',
                                      privileged=True
                                      )
    for line in container.logs(stream=True):
        print(line)

    result = container.wait()
    exit_code = result["StatusCode"]
    if exit_code != 0:
        myLogger.error_logger('run failed')

    print('run successful')