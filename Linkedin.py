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
        'scope': 'r_basicprofile r_emailaddress',
        # we are not going to check it later (DANGEROUS!)
        'state': uuid.uuid1()
    })

    dummy_server = DummyServer("localhost", 8000)
    dummy_server.start()

    webbrowser.open("https://www.linkedin.com/uas/oauth2/authorization?" + qs)

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
    req = urllib.request.Request('https://www.linkedin.com/uas/oauth2/accessToken', data.encode())
    response_text = urllib.request.urlopen(req).read().decode()
    token_info = json.loads(response_text)
    # Linkedin does not send token_type, no checking
    return token_info['access_token']


def get_personal_info(access_token):

    # a POST request with Authorization
    req = urllib.request.Request('https://www.linkedin.com//v1/people/~:(first-name,last-name,email-address)')
    req.add_header('Authorization', 'Bearer ' + access_token)
    req.add_header('x-li-format', 'json')
    response_text = urllib.request.urlopen(req).read().decode()
    info = json.loads(response_text)
    return info['firstName'], info['lastName'], info['emailAddress']

if __name__ == "__main__":

    ''' - Linkedin uses OAuth2
        - Like Facebook it doesn't send information we need (ex. email) during authorization process
           So we need to make an API call
        - Unlike Facebook after we got hold of the access-token any API call must have an Authorization Bearer
           header
    '''
    my_app = {
        'key': '<--your app key-->',
        'secret': '<--your app secret-->',
        'callback': 'http://localhost:8000/'
    }

    token = get_access_token(my_app)
    firstName, lastName, email = get_personal_info(token)
    print("Logged-in as " + email)
