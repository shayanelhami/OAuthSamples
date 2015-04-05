import base64
import hashlib
import hmac
from urllib.parse import urlencode, quote, urlparse
from urllib.request import Request, urlopen


def percent_encode(value):
    # safe is used to convert / to %2F
    return quote(str(value), safe='')


def create_signature_base_string(method, api_end_point, oauth_parameters, normal_parameters):

    parameters = oauth_parameters.copy()
    parameters.update(normal_parameters)

    parameters_as_list = []
    for key in sorted(parameters.keys()):
        encoded_key = percent_encode(key)
        encoded_value = percent_encode(parameters[key])
        parameters_as_list.append("%s=%s" % (encoded_key, encoded_value))

    parameters_string = '&'.join(parameters_as_list)

    signature_base_string = '&'.join([
        method,
        percent_encode(api_end_point),
        percent_encode(parameters_string)
    ])

    return signature_base_string


def get_signature(method, api_end_point, oauth_parameters, normal_parameters, consumer_secret, token_secret):

    signature_base_string = create_signature_base_string(method, api_end_point, oauth_parameters, normal_parameters)

    # in case of a missing token_secret appending & is OK
    signing_key = percent_encode(consumer_secret) + '&' + percent_encode(token_secret)

    signed_binary = hmac.new(signing_key.encode(), signature_base_string.encode(), hashlib.sha1).digest()
    signed_string = base64.b64encode(signed_binary).decode()

    return percent_encode(signed_string)


def get_oauth_authorization_header(oauth_parameters):

    parameters_as_list = []
    for key in oauth_parameters.keys():
        parameters_as_list.append("%s=\"%s\"" % (key, oauth_parameters[key]))

    return "OAuth " + ', '.join(parameters_as_list)


def post_signed_request(api_end_point, oauth_parameters, normal_parameters, consumer_secret, token_secret=''):

    oauth_parameters['oauth_signature'] = get_signature(
        'POST',
        api_end_point,
        oauth_parameters,
        normal_parameters,
        consumer_secret,
        token_secret)

    print(get_oauth_authorization_header(oauth_parameters))
    body = urlencode(normal_parameters)

    req = Request(api_end_point, body.encode())
    req.add_header("Authorization", get_oauth_authorization_header(oauth_parameters))
    response_text = urlopen(req).read().decode()

    print("response body:\n%s" % response_text)
    return response_text
