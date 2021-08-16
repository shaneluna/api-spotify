from datetime import datetime, timedelta
import base64
import requests
from urllib.parse import urlencode

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        if self.client_id is None or self.client_secret is None:
            raise Exception("client_id or client_secret not set")
        client_creds_b64 = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        return {
            'Authorization': f'Basic {self.get_client_credentials()}'
        }
    
    def get_token_data(self):
        return {
            'grant_type': 'client_credentials'
        }

    def perform_auth(self):
        r = requests.post(self.token_url, data=self.get_token_data(), headers=self.get_token_headers())
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client")
        data = r.json()
        # access token
        self.access_token = data['access_token']
        # expiration
        now = datetime.now()
        token_expires_in = data['expires_in']
        token_expires_on = now + timedelta(seconds=token_expires_in)
        self.access_token_expires = token_expires_on
        self.access_token_did_expire = now > token_expires_on # False
        return True

    def get_access_token(self):
        now = datetime.now()
        if self.access_token is None or self.access_token_expires < now:
            self.perform_auth()
            return self.get_access_token()
        return self.access_token

    def search(self, query, search_type='artist,track', market=None, limit=20, offset=0):
        access_token = self.get_access_token()
        endpoint = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        data = urlencode({
            'q': query,
            'type': search_type,
            'limit': limit,
            'offset': 0
        })
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()

    def search_album(self, query):
        return self.search(query, search_type='album')

    def search_artist(self, query):
        return self.search(query, search_type='artist')

    def search_playlist(self, query):
        return self.search(query, search_type='playlist')

    def search_track(self, query):
        return self.search(query, search_type='track')

    def search_show(self, query):
        return self.search(query, search_type='show')

    def search_episode(self, query):
        return self.search(query, search_type='episode')
    