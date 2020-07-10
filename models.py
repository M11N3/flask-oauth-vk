import json

from flask import Flask, redirect, url_for, request
from rauth import OAuth2Service

from config import OAUTH_CREDENTIALS


class VkSignIn(object):
    def __init__(self):
        credentials = OAUTH_CREDENTIALS['vk']
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.scope = credentials['scope']
        self.service = OAuth2Service(
            name='vk',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.vk.com/authorize',           
            access_token_url='https://oauth.vk.com/access_token',
            base_url='https://oauth.vk.com/'
        )
    
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope=self.scope,
            response_type='code',
            redirect_uri=self.get_callback_url())
        )
    
    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        return oauth_session.access_token

    def get_callback_url(self):
        return url_for('oauth_callback', _external=True)
        