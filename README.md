# OAuthSamples
Demonstrates OAuth flow for several different provider

IMPORTANT NOTE: This project is for educational purposes only. 
Feel free to read it, teach it, experiment with it 
but it is NOT by any means ready for production. 
It is designed to be simple to read and simple to understand but 
it does NOT do most of the necessary error checking and 
does NOT provide protection against many hack scenarios like 
Cross-Site Request Forgery (CSRF). 

*DO NOT USE FOR PRODUCTION* or with real data.

Content
-------

You can find samples to learn about OAuth flow in the following providers:

- Twitter (most complex one as it is using OAuth 1.0a and that needs signing each request)
- Facebook (OAuth2 but in a peculiar way)
- Linkedin (OAuth2)
- Dropbox (OAuth2)

At the end of the authorization process each provider gives you an access-token. That is enough to
assume user is Authenticated successfully. Therefore you can use OAuth as a tool to do "Login with Twitter", 
"Login with Facebook", etc.

The same access-token can be used to make further API calls if you happen to need them 
(for example post to the user's twitter timeline)


Dummy Web Server
----------------

The samples are designed to run as command line (console) application for simplicity. Normally
these category of application in OAuth expect you to receive a PIN from provider and type it to proceed.

This is not probably the usual case. Most of the times you just have a web-server application that can redirect user 
back and forth in a web-browser.

To make it more similar to those scenarios and to avoid making the samples specific to a web framework
a DummyWebServer is added which is responsible for receiving certain tokens from providers and passing them 
to the next level. This simulates a part of the web server you would build for the same purpose. The rest of 
the code is a sequential process that could be understood easily. 


Setup
-----

In each case you need to follow instructions of each provider and create an App through their Developer Console. 
Find callback URL in each case and add http://localhost:8000/ (in case of Twitter http://127.0.0.1:8000/). Then 
copy and paste client id and secret to the code (sometime they call the *client* "consumer" or "app" and *id* is the same thing 
as "key")


Roadmap
-------
The plan is to add more samples for:
- Google
- Microsoft Azure Active Directory 