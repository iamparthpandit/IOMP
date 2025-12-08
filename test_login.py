import requests
import json

# Test login API
url = 'http://localhost:5000/api/auth/login'
data = {
    'email': 'student001@techvista.edu',
    'password': 'password123'
}

print(f"Testing login with: {data['email']}")
print(f"URL: {url}\n")

try:
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
