from behave import step

from misttests.config import safe_get_var
import requests
import random
import json

from random import randrange


@step(u'rbac members are initialized')
def initialize_rbac_members(context):
    BASE_EMAIL = context.mist_config['BASE_EMAIL']
    context.mist_config['MEMBER1_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))
    context.mist_config['MEMBER2_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))

    context.mist_config['ORG_NAME'] = "rbac_org_%d" % random.randint(1,200000)

    payload = {
        'email': context.mist_config['MEMBER1_EMAIL'],
        'password': context.mist_config['MEMBER1_PASSWORD'],
        'name': "Atheofovos Gkikas"
    }

    requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    return


@step(u'rbac members, organization and team are initialized')
def initialize_rbac_members(context):
    BASE_EMAIL = context.mist_config['BASE_EMAIL']
    context.mist_config['MEMBER1_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))

    payload = {
        'email': context.mist_config['MEMBER1_EMAIL'],
        'password': context.mist_config['MEMBER1_PASSWORD'],
        'name': "Atheofovos Gkikas"
    }
    requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }
    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    api_token = re.json()['token']
    headers = {'Authorization': api_token}

    payload = {
        'name': "Test Team"
    }
    requests.post(context.mist_config['MIST_URL'] + "/api/v1/org/" + context.mist_config['ORG_ID'] + "/teams", data=json.dumps(payload), headers=headers)

    return


@step(u'script "{script_name}" is added via API request')
def create_script_api_request(context, script_name):
    script_data = {'location_type':'inline','exec_type':'executable', 'name': script_name}
    bash_script = """#!/bin/bash\ntouch /root/dummy_file
    """
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }

    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))

    api_token = re.json()['token']
    headers = {'Authorization': api_token}

    script_data['script'] = bash_script

    requests.post(context.mist_config['MIST_URL'] + "/api/v1/scripts" , data=json.dumps(script_data), headers=headers)


@step(u'cloud "{cloud}" has been added via API request')
def add_docker_api_request(context, cloud):
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }

    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))
    api_token = re.json()['token']
    headers = {'Authorization': api_token}

    if cloud == 'Docker':

        payload = {
            'title': "Docker",
            'provider': "docker",
            'docker_host': safe_get_var('clouds/docker', 'host', context.mist_config['CREDENTIALS']['DOCKER']['host']),
            'docker_port': safe_get_var('clouds/docker', 'port', context.mist_config['CREDENTIALS']['DOCKER']['port']),
            'authentication': safe_get_var('clouds/docker', 'authentication', context.mist_config['CREDENTIALS']['DOCKER']['authentication']),
            'ca_cert_file': safe_get_var('clouds/docker', 'ca', context.mist_config['CREDENTIALS']['DOCKER']['ca']),
            'key_file': safe_get_var('clouds/docker', 'key', context.mist_config['CREDENTIALS']['DOCKER']['key']),
            'cert_file': safe_get_var('clouds/docker', 'cert', context.mist_config['CREDENTIALS']['DOCKER']['cert'])
        }

    elif cloud == 'Docker-Monitoring':

        payload = {
            'title': "Docker",
            'provider': "docker",
            'docker_host': safe_get_var('clouds/docker_monitoring', 'host',
                                        context.mist_config['CREDENTIALS']['DOCKER_MONITORING']['host']),
            'docker_port': safe_get_var('clouds/docker_monitoring', 'port',
                                        context.mist_config['CREDENTIALS']['DOCKER_MONITORING']['port']),
        }

    requests.post(context.mist_config['MIST_URL'] + "/api/v1/clouds", data=json.dumps(payload), headers=headers)


@step(u'Docker machine "{machine_name}" has been added via API request')
def create_docker_machine(context, machine_name):
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'org_id': context.mist_config['ORG_ID']
    }

    re = requests.post("%s/api/v1/tokens" % context.mist_config['MIST_URL'], data=json.dumps(payload))
    api_token = re.json()['token']
    headers = {'Authorization': api_token}

    re = requests.get(context.mist_config['MIST_URL'] + "/api/v1/clouds", headers=headers)

    for cloud in re.json():
        if 'docker' in cloud['provider']:
            cloud_id = cloud['id']
            break

    re = requests.get(context.mist_config['MIST_URL'] + "/api/v1/clouds/" + cloud_id + "/images", headers=headers)

    for image in re.json():
        if 'Ubuntu 14.04' in image['name']:
            image_id = image['id']
            break;

    if 'random' in machine_name:
        value_key = machine_name
        machine_name = machine_name.replace("random", str(randrange(1000)))
        context.mist_config[value_key] = machine_name

    payload = {
        'image': image_id,
        'name': machine_name,
        'provider': 'docker',
        'location': '',
        'size': ''
    }

    requests.post(context.mist_config['MIST_URL'] + "/api/v1/clouds/" + cloud_id + "/machines", data=json.dumps(payload), headers=headers)
