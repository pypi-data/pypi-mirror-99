from ChristisRequestor.utils import get_christisAPI_accessPoint
import requests

def get_user_email(userDN):
    christisApiAccessPoint = get_christisAPI_accessPoint()
    requestURL = "{0}/user/email/{1}".format(christisApiAccessPoint,userDN)
    try:
        email = requests.get(requestURL,timeout=3)
        if(type(email.json())==dict and 'ErrorCode' in email.json()):
            return email.json()
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
        return { "StatusCode":email.status_code,"Response":email.json()}

def get_user_cn(userDN):
    christisAPIAccessPoint = get_christisAPI_accessPoint()
    requestURL = "{0}/user/cn/{1}".format(christisAPIAccessPoint,userDN)
    try:
        userCN = requests.get(requestURL,timeout=3)
        if( type(userCN.json())==dict and 'ErrorCode' in userCN.json()):
            return userCN.json()
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
        return { "StatusCode":userCN.status_code,"Response":userCN.json()}
   
def get_user_membership(userDN):
    christisAPIAccessPoint = get_christisAPI_accessPoint()
    requestURL = "{0}/user/membership/{1}".format(christisAPIAccessPoint,userDN)
    try:
        userGroup = requests.get(requestURL,timeout=3)
        if( type(userGroup.json())==dict and 'ErrorCode' in userGroup.json()):
            return userGroup.json()
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
        return { "StatusCode":userGroup.status_code,"Response":userGroup.json()}
