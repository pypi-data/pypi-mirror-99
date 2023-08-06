from ChristisRequestor.utils import get_christisAPI_accessPoint
from ChristisRequestor.utils import get_LDAP_k8s_group
import requests

def get_group_members(groupCN):
  christisApiAccessPoint = get_christisAPI_accessPoint()
  requestURL = "{0}/group/members/{1}".format(christisApiAccessPoint,groupCN)
  try:
    members = requests.get(requestURL,timeout=3)
    if( type(members.json())==dict and 'ErrorCode' in members.json()):
            return members.json()
  except requests.exceptions.HTTPError as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("HTTP Error:", e) }
    return Error
  except requests.exceptions.ConnectionError as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("Error Connectiong:", e) }
    return Error
  except requests.exceptions.Timeout as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("Timeout Error:", e) }
    return Error
  except requests.exceptions.RequestException as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("Another Error:", e) }
    return Error
  else:
    return { "StatusCode":members.status_code,"Response":members.json()}

def get_group_dn(groupCN):
  christisApiAccessPoint = get_christisAPI_accessPoint()
  requestURL = "{0}/group/dn/{1}".format(christisApiAccessPoint,groupCN)
  try:
    groupDN = requests.get(requestURL,timeout=3)
    if( type(groupDN.json())==dict and 'ErrorCode' in groupDN.json()):
            return groupDN.json()
  except requests.exceptions.HTTPError as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("HTTP Error:", e) }
    return Error
  except requests.exceptions.ConnectionError as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("Error Connectiong:", e) }
    return Error
  except requests.exceptions.Timeout as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("Timeout Error:", e) }
    return Error
  except requests.exceptions.RequestException as e:
    Error = { "ErrorCode":"600","ErrorMsg":"{0}:{1}".format("Another Error:", e) }
    return Error
  else:
    return { "StatusCode":groupDN.status_code,"Response":groupDN.json()}