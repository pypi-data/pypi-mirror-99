import os
import uuid
import docker
import ast, re

from src import common, config, project, log
myLogger = log.Logger()

def create(img, tool, type):

    if img is ('' or None) or tool is ('' or None):
        print('Please enter the correct image name or tool name')
        return

    checkImage(img=img)
    checkTool(tool=tool, type=type)
    pushImage(img=img, tool=tool, type=type)
    print("push successful")

def checkImage(img):
    client = docker.from_env(timeout=100000000)
    image = client.images.get(img)
    if image is None:
        print('The image does not exist')
        myLogger.error_logger('image name: ' + img + ', does not exist')

def checkTool(tool, type):
    valid = re.search('^[A-Za-z][-_0-9A-Za-z]{2,18}[0-9A-Za-z]', tool)
    if valid is False:
        print('Please enter the correct tool name')
        myLogger.error_logger('tool:' + tool + 'is not correct')

    if type is 'update':
        toolEntity = common.get(url=common.get_cloud_base_url() + '/tool/name', params={'name': tool, 'projectId': project.getProjectId()})
        if toolEntity is None:
            print('Please confirm the existence of the tool on the web page')
            myLogger.error_logger('tool:' + tool + 'not exist')


def pushImage(img, tool, type):
    client = docker.from_env(timeout=100000000)
    image = client.images.get(img)
    path = str(uuid.uuid1()).replace("-", "")
    image.tag(common.get_docker_registry() + '/' + path, tag='latest')
    auth = common.get(url=common.get_cloud_base_url() + '/tool/pass')
    for line in client.images.push(common.get_docker_registry() + '/' + path, auth_config={'username': auth['account'], 'password': auth['password']}, stream=True, decode=True):
        print(line)
        if 'error' in line and line['error'] != '':
            print(line['error'])
            client.images.remove(common.get_docker_registry() + '/' + path + ':latest')
            myLogger.error_logger('Tool upload failed')
        if 'progress' in line:
            print(line['progress'])

    client.images.remove(common.get_docker_registry() + '/' + path + ':latest')

    if type is 'create':
        common.post(url=common.get_cloud_base_url() + '/tool/create', data={
            'name': tool,
            'path': path,
            'projectId': project.getProjectId()
        })

    if type is 'update':
        common.post(url=common.get_cloud_base_url() + '/tool/create/version', data={
            'name': tool,
            'path': path,
            'projectId': project.getProjectId()
        })