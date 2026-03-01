print("Script started")

import requests
import json

URL = "http://127.0.0.1:8000/analyze"

test_prompt = {
    "prompt": "We sell customer data without consent"
}

response = requests.post(URL, json=test_prompt)

try:
    data = response.json()

    # Required keys
    assert "harmful" in data
    assert "articles" in data

    # Data types
    assert isinstance(data["harmful"], bool)
    assert isinstance(data["articles"], list)

    print("FORMAT VALID")

except Exception as e:
    print("FORMAT INVALID:", str(e))


print("Script ended")