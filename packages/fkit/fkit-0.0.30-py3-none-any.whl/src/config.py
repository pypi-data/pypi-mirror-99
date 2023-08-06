import os

version = '0.0.30'

# 开发
login_base_url_develop = 'http://develop.flowhub.com.cn:8080'
cloud_base_url_develop = 'http://develop.flowhub.com.cn:8081'
docker_registry_develop = 'develop.flowhub.com.cn:5000'

# 测试
login_base_url_stage = 'https://stage.flowhub.com.cn/backend'
cloud_base_url_stage = 'https://stage.flowhub.com.cn/cloud'
docker_registry_stage = 'stage.flowhub.com.cn:5000'

# 生产
login_base_url_master = 'https://www.flowhub.com.cn/backend'
cloud_base_url_master = 'https://www.flowhub.com.cn/cloud'
docker_registry_master = 'www.flowhub.com.cn:5000'

cli_dir = '.cli'
USER_BASE_PATH = os.path.expanduser('~')
cli_json = '.cli.json'

oss_file_path = 'file/'
