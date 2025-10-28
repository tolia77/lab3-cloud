import requests
from typing import Any, Dict, Optional
from app.settings import settings


class HttpClient:
    def __init__(self, base_url: str = None, api_key: Optional[str] = None, api_host: Optional[str] = None):
        self.base_url = base_url or settings.API_SPORTS_BASE_URL
        self.session = requests.Session()
        key = api_key or settings.API_SPORTS_KEY
        host = api_host or settings.API_SPORTS_HOST
        print(key)
        print(host)
        headers = {}
        if key:
            headers["x-apisports-key"] = key
        if host:
            headers["x-apisports-host"] = host
        self.session.headers.update(headers)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        resp = self.session.get(url, params=params, **kwargs)
        resp.raise_for_status()
        return resp.json()
