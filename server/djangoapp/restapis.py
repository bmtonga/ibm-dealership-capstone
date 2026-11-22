import os
from urllib.parse import quote
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:3030").rstrip("/")
SENTIMENT_URL = os.getenv("SENTIMENT_ANALYZER_URL", "http://localhost:5050").rstrip("/")


def get_request(endpoint, **params):
    response = requests.get(f"{BACKEND_URL}/{endpoint.lstrip('/')}", params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    response = requests.get(f"{SENTIMENT_URL}/analyze/{quote(text, safe='')}", timeout=15)
    response.raise_for_status()
    return response.json().get("sentiment", "neutral")


def post_review(data_dict):
    response = requests.post(f"{BACKEND_URL}/insert_review", json=data_dict, timeout=15)
    response.raise_for_status()
    return response.json()
