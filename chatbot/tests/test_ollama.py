import requests
import json
import os
import dotenv

dotenv.load_dotenv()


def test_ollama_api():
    url = os.getenv("OPENAI_API_BASE")
    payload = {
        "model": os.getenv("OPENAI_MODEL_NAME"),
        "prompt": "Hello, world!",
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        result = response.json()
        print("Success! Response:", result)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response'):
            print(f"Status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        print(f"Request URL: {url}")
        print(f"Request payload: {payload}")

if __name__ == "__main__":
    test_ollama_api()