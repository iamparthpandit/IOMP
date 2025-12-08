import requests
import json

# Test login with new credentials
test_users = [
    {'email': 'student001@techvista.edu', 'password': 'Student@2025'},
    {'email': 'principal@techvista.edu', 'password': 'Principal@2025'},
    {'email': 'cs.prof@techvista.edu', 'password': 'CsProf@2025'},
]

url = 'http://localhost:5000/api/auth/login'

for user in test_users:
    print(f"\nTesting: {user['email']}")
    print("-" * 60)
    
    try:
        response = requests.post(url, json=user, headers={'Content-Type': 'application/json'})
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS!")
            print(f"Name: {data['user']['name']}")
            print(f"Role: {data['user']['role']}")
            print(f"Token received: Yes")
        else:
            print(f"❌ FAILED: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
