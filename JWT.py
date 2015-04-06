import base64
import json

'''
    Simplest JWT decode possible. For a proper one use: PyJWT (https://github.com/jpadilla/pyjwt/)
'''


def base64url_decode(base64url):
    rem = len(base64url) % 4

    # put back the missing padding character
    if rem == 3:
        base64url += '='

    if rem == 2:
        base64url += '=='

    return base64.urlsafe_b64decode(base64url)


def decode(jwt):
    payload = jwt.rsplit('.')[1]
    decoded_string = base64url_decode(payload).decode()
    return json.loads(decoded_string)
