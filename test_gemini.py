import requests

response = requests.post(
    "http://localhost:8000/api/research/explore",
    json={"concept": "quantum computing", "domain": "computer science"}
)

print(f"Status Code: {response.status_code}")
try:
    print(response.json())
except Exception as e:
    print(f"Error decoding JSON: {e}")
    print(response.text)
