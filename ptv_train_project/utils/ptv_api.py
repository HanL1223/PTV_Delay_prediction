# Helper functions for signing and calling the PTV API
# utils/ptv_api.py
import hashlib
import hmac
import requests
import json
from urllib.parse import urlencode

# Load API credentials from secrets
def load_secrets(path="config/secrets.json"):
    with open(path) as f:
        return json.load(f)

def build_signed_url(endpoint_path: str, params: dict, dev_id: str, api_key: str) -> str:
    params["devid"] = dev_id
    query = urlencode(sorted(params.items()))
    raw_url = f"{endpoint_path}?{query}"
    signature = hmac.new(
        api_key.encode("utf-8"),
        raw_url.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()
    return f"https://timetableapi.ptv.vic.gov.au{raw_url}&signature={signature}"

def fetch_ptv_data(endpoint_path: str, params: dict, secrets_path="config/secrets.json"):
    creds = load_secrets(secrets_path)
    url = build_signed_url(endpoint_path, params, creds["DEV_ID"], creds["API_KEY"])
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
