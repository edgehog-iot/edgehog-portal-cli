import requests
import pprint

from ep_operations.common import HEADERS, get_authorized_headers

LOGIN_IAPI_V1 = "{}/iapi/v1/auth/login"
LOGOUT_IAPI_V1 = "{}/iapi/v1/auth/logout"

LOGIN_API_V1 = "{}/api/v1/auth/login"
LOGOUT_API_V1 = "{}/api/v1/auth/logout"


def internal_login(uri: str, mail: str, password: str):
    return login(LOGIN_IAPI_V1.format(uri), mail, password)


def external_login(uri: str, mail: str, password: str):
    return login(LOGIN_API_V1.format(uri), mail, password)


def login(uri: str, mail: str, password: str):
    """
    Call to Login API
    :param uri: base API url
    :param mail: email needed for login
    :param password: password needed for login
    """
    body = {
        "email": mail,
        "password": password
    }
    try:
        login_request = requests.post(uri, headers=HEADERS, params=body)
        response_dict = login_request.json()
    except ValueError:
        print('Unable to reach the host')
        return ''

    if response_dict.get('success', False):
        return response_dict.get("access_token", "")
    else:
        print(uri)
        pprint.pprint(body, indent=4)
        print('Error in Login phase: {}'.format(response_dict.get("message", "No error message provided.")))
        print("Errors: ")
        pprint.pprint(response_dict.get('errors', []), indent=4)
        return ''


def internal_logout(uri: str, token: str):
    return logout(LOGOUT_IAPI_V1.format(uri), token)


def external_logout(uri: str, token: str):
    return logout(LOGOUT_API_V1.format(uri), token)


def logout(uri: str, token: str):
    """
    Call to Logout API
    :param uri: base API url
    :param token: token of the user to logout
    """

    headers = get_authorized_headers(token)

    login_request = requests.post(uri, headers=headers)
    response_dict = login_request.json()
    return response_dict.get('success', False)
