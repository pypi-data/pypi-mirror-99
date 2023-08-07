import os
import requests_cache
import datetime as dt
import xmltodict
from pathlib import Path

from patent_client import SETTINGS

cache_max_age = dt.timedelta(days=3)
cache_dir = "~/.patent_client"
CACHE_BASE = Path(cache_dir).expanduser()
CACHE_BASE.mkdir(exist_ok=True)

CACHE_CONFIG = dict(
    expire_after=cache_max_age,
    backend=requests_cache.backends.sqlite.DbCache(
        location=str(CACHE_BASE / "requests_cache")
    ),
    )

CLIENT_SETTINGS = SETTINGS["EpoOpenPatentServices"]
if os.environ.get("EPO_KEY", False):
    KEY = os.environ["EPO_KEY"]
    SECRET = os.environ["EPO_SECRET"]
else:
    KEY = CLIENT_SETTINGS["ApiKey"]
    SECRET = CLIENT_SETTINGS["Secret"]

NS = {
    "http://ops.epo.org": None,
    "http://www.epo.org/exchange": None,
    "http://www.epo.org/fulltext": None,
    "http://www.epo.org/register": None,
}

class OpsSession(requests_cache.CachedSession):
    def __init__(self, *args, key=None, secret=None, **kwargs):
        super(OpsSession, self).__init__(*args, **kwargs)
        self.key: str = key
        self.secret: str = secret
        self.expires: dt.datetime = dt.datetime.utcnow()
    
    def request(self, *args, **kwargs):
        response = super(OpsSession, self).request(*args, **kwargs)
        if response.status_code in (403, 400):
            auth_response = self.get_token()
            response = super(OpsSession, self).request(*args, **kwargs)
        return response
        
    def get_token(self):
        auth_url = "https://ops.epo.org/3.2/auth/accesstoken"
        response = super(OpsSession, self).request(
            'post',
            auth_url, auth=(self.key, self.secret), data={"grant_type": "client_credentials"}
        )
        data = response.json()
        self.expires = dt.datetime.fromtimestamp(int(data['issued_at']) / 1000) + dt.timedelta(seconds=int(data['expires_in']))
        self.headers['Authorization'] = f"Bearer {data['access_token']}"
        return response

session = OpsSession(
    key=KEY, 
    secret=SECRET,
    **CACHE_CONFIG
)