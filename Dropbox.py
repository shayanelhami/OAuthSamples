import json
import urllib.request
from urllib.parse import urlencode
import uuid
import webbrowser
from DummyWebServer import DummyServer, Messages


def get_access_token(app_info):
    # get access code
    qs = urlencode({
        'response_type': 'code',
        'client_id': app_info['key'],
        'redirect_uri': app_info['callback'],
        # we are not going to check it later (DANGEROUS!)
        'state': uuid.uuid1()
    })

    dummy_server = DummyServer("localhost", 8000)
    dummy_server.start()

    webbrowser.open("https://www.dropbox.com/1/oauth2/authorize?" + qs)

    code = Messages.get()
    dummy_server.stop()

    # exchange code for an access token
    data = urlencode({
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': app_info['callback'],
        'client_id': app_info['key'],
        'client_secret': app_info['secret']
    })

    # make a POST request

    # note: we could put the client's (app) key and secret in Authorization header
    # with "Authorization: Basic base64" or in the POST data. The latter is simpler and
    # we go with it.
    req = urllib.request.Request('https://api.dropbox.com/1/oauth2/token', data.encode())
    response_text = urllib.request.urlopen(req).read().decode()
    token_info = json.loads(response_text)

    if token_info['token_type'] != 'bearer':
        raise Exception("token_type is not bearer")

    return token_info['access_token']


def get_personal_info(access_token):

    # a POST request with Authorization
    req = urllib.request.Request('https://api.dropbox.com/1/account/info')
    req.add_header('Authorization', 'Bearer ' + access_token)
    response_text = urllib.request.urlopen(req).read().decode()
    info = json.loads(response_text)
    return info['display_name'], info['email']

if __name__ == "__main__":

    ''' - Dropbox is very similar to Linkedin
        - It doesn't need scope
    '''

    my_app = {
        'key': '<--your app key-->',
        'secret': '<--your app secret-->',
        'callback': 'http://localhost:8000/'
    }

    token = get_access_token(my_app)
    name, email = get_personal_info(token)
    print("Logged-in as " + email)
