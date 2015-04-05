import json
from urllib.parse import urlencode
from urllib.request import urlopen
import webbrowser
from DummyWebServer import DummyServer, Messages


def get_access_token(app_info):
    # get access code
    qs = urlencode({
        'client_id': app_info['id'],
        'redirect_uri': app_info['callback'],
        'scope': 'email'
        # no state check here, therefore prone to CSRF attack
    })

    dummy_server = DummyServer("localhost", 8000)
    dummy_server.start()

    webbrowser.open("https://www.facebook.com/dialog/oauth?" + qs)

    code = Messages.get()
    dummy_server.stop()

    # exchange code for an access token
    qs = urlencode({
        'client_id': app_info['id'],
        'redirect_uri': app_info['callback'],
        'code': code,
        'client_secret': app_info['secret']
    })

    response_text = urlopen("https://graph.facebook.com/v2.3/oauth/access_token?" + qs).read().decode()
    token_info = json.loads(response_text)

    if token_info['token_type'] != 'bearer':
        raise Exception("token_type is not bearer")

    return token_info['access_token']


def get_personal_info(access_token):
    # apparently facebook doesn't make use of Authorization header and accept the token as query string
    response_text = urlopen('https://graph.facebook.com/v2.3/me?access_token=' + access_token).read().decode()
    info = json.loads(response_text)
    return info['name'], info['email']


if __name__ == "__main__":

    ''' - Facebook uses OAuth2
        - But doesn't send information we need (ex. email) during authorization process
            therefore we need to grab the access token and make an extra API call
    '''
    my_app = {
        'id': '<--your app id-->',
        'secret': '<--your app secret-->',
        'callback': 'http://localhost:8000/'
    }

    token = get_access_token(my_app)
    name, email = get_personal_info(token)
    print("Logged-in as " + email)
