from urllib.parse import parse_qsl
import uuid
import time
import webbrowser
from DummyWebServer import DummyServer, Messages
from SignedRequest import post_signed_request


def get_request_token(consumer_key, consumer_secret, callback):

    print("requesting request token")

    oauth_parameters = {
        'oauth_consumer_key': consumer_key,
        'oauth_nonce': uuid.uuid1(),
        'oauth_signature_method': "HMAC-SHA1",
        'oauth_timestamp': int(time.time()),
        'oauth_version': "1.0"
    }

    normal_parameters = {
        'oauth_callback': callback
    }

    response_text = post_signed_request(
        "https://api.twitter.com/oauth/request_token",
        oauth_parameters,
        normal_parameters,
        consumer_secret)

    token_info = dict(parse_qsl(response_text))
    if token_info['oauth_callback_confirmed'] != 'true':
        raise Exception("oauth_callback_confirmed is not 'true'")

    return token_info['oauth_token'], token_info['oauth_token_secret']


def get_verifier(request_token):
    dummy_server = DummyServer("localhost", 8000)
    dummy_server.start()

    webbrowser.open("https://api.twitter.com/oauth/authenticate?oauth_token=" + request_token)

    # block here until verifier is back
    verifier = Messages.get()
    dummy_server.stop()
    return verifier


def get_access_token(verifier_token, request_token, token_secret, consumer_key, consumer_secret):

    print("requesting access token")

    oauth_parameters = {
        'oauth_consumer_key': consumer_key,
        'oauth_token': request_token,
        'oauth_nonce': uuid.uuid1(),
        'oauth_signature_method': "HMAC-SHA1",
        'oauth_timestamp': int(time.time()),
        'oauth_version': "1.0"
    }

    normal_parameters = {
        'oauth_verifier': verifier_token
    }

    response_text = post_signed_request(
        "https://api.twitter.com/oauth/access_token",
        oauth_parameters,
        normal_parameters,
        consumer_secret,
        token_secret)

    info = dict(parse_qsl(response_text))
    return info['user_id'], info['screen_name'], info['oauth_token'], info['oauth_token_secret']


if __name__ == "__main__":

    ''' - Twitter uses OAuth 1.0a
        - OAuth 1.0a expects every request to be signed
        - Instead of using consumer (client) key directly to get user's permission (as in
           OAuth2) we need to first get a temporary request-token
    '''

    consumer_info = {
        'key': '<--your app key-->',
        'secret': '<--your app secret-->'
    }

    # Step 1: get a temporary request-token
    temp_request_token, temp_request_secret = get_request_token(
        consumer_info['key'],
        consumer_info['secret'],
        callback="http://localhost:8000/")

    # Step 2: use the temporary request-token to ask user's permission
    token_verifier = get_verifier(temp_request_token)

    # Step 3: exchange the verifier for real access token
    # During the exchange Twitter sends back screen name and id so there is no need to make
    # an API call to get these information.
    user_id, screen_name, access_token, access_secret = get_access_token(
        token_verifier,
        temp_request_token,
        temp_request_secret,
        consumer_info['key'],
        consumer_info['secret'])

    print("Logged-in as " + screen_name)
