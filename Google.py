import json
import urllib.request
from urllib.parse import urlencode
import uuid
import webbrowser
from DummyWebServer import DummyServer, Messages
import JWT


def get_access_token(client_info):
    # get access code
    qs = urlencode({
        'response_type': 'code',
        'client_id': client_info['id'],
        'redirect_uri': client_info['callback'],
        'scope': 'profile email',
        # to prevent consent screen appear every time:
        'approval_prompt': 'auto',
        # we are not going to check it later (DANGEROUS!)
        'state': uuid.uuid1()
    })

    dummy_server = DummyServer("localhost", 8000)
    dummy_server.start()

    webbrowser.open("https://accounts.google.com/o/oauth2/auth?" + qs)

    code = Messages.get()
    dummy_server.stop()

    # exchange code for an access token
    data = urlencode({
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': client_info['callback'],
        'client_id': client_info['id'],
        'client_secret': client_info['secret']
    })

    # make a POST request
    req = urllib.request.Request('https://www.googleapis.com/oauth2/v3/token', data.encode())
    response_text = urllib.request.urlopen(req).read().decode()
    token_info = json.loads(response_text)

    # Google happens to be sending the email in a JWT (JSON Web Token) with the rest of the tokens
    # we can extract it now or just leave it to another API call to get the email
    jwt = JWT.decode(token_info['id_token'])

    return jwt['email'], token_info['access_token']


def get_personal_info(access_token):
    # a POST request with Authorization
    req = urllib.request.Request('https://www.googleapis.com/plus/v1/people/me')
    req.add_header('Authorization', 'Bearer ' + access_token)
    response_text = urllib.request.urlopen(req).read().decode()
    info = json.loads(response_text)
    return info['displayName']


if __name__ == "__main__":

    ''' - Google uses OAuth2
        - Google+ API must be enabled for the app (but user doesn't need to have Google+ account)
        - It sends some information in form of a JWT we can use it to avoid making an extra API call
    '''

    my_client = {
        'id': '<--your client id-->',
        'secret': '<--your client secret-->',
        'callback': 'http://localhost:8000/'
    }

    email, token = get_access_token(my_client)
    # if the goal was to get the email we were done here
    print(email)
    # but let's make an API call to get the display name too
    display_name = get_personal_info(token)
    print(display_name)

