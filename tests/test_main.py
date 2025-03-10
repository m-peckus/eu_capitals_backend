#!/usr/bin/env python3

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_fetch():
    response = requests.get(f"{BASE_URL}/fetch?city=Warsaw&country=Poland")
    assert response.status_code == 200
    print(response.json())

if __name__ == "__main__":
    test_fetch()