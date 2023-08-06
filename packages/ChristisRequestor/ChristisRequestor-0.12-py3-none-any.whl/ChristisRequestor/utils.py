import os

def get_christisAPI_address():
    return os.environ['CHRISTIS_API_ADDRESS']

def get_christisAPI_port():
    return os.environ['CHRISTIS_API_PORT']

def get_christisAPI_accessPoint():
    return "http://{0}:{1}".format(get_christisAPI_address(),get_christisAPI_port())

def get_LDAP_k8s_group():
    return os.environ['CHRISTIS_K8s_LDAP_GROUP']
    