import requests
import json

BASE_URL = 'http://localhost:5000'

def test_classroom_flow():
    # 1. Create Teacher
    teacher_email = "teacher_flow@example.com"
    teacher_password = "password123"
    
    # Register
    requests.post(f'{BASE_URL}/api/auth/register', json={
        'name': 'Flow Teacher',
        'email': teacher_email,
        'password': teacher_password,
        'role': 'teacher'
    })
    
    # Login
    response = requests.post(f'{BASE_URL}/api/auth/login', json={
        'email': teacher_email,
        'password': teacher_password
    })
    
    if response.status_code != 200:
        print("Login failed")
        return
        
    token = response.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    
    print("Login successful")
    
    # 2. Create Classroom
    response = requests.post(f'{BASE_URL}/api/classrooms', headers=headers, json={
        'name': 'Flow Class 101',
        'description': 'Testing flow'
    })
    
    if response.status_code != 201:
        print(f"Create classroom failed: {response.text}")
        return
        
    classroom_id = response.json()['id']
    print(f"Classroom created: {classroom_id}")
    
    # 3. Upload Material
    response = requests.post(f'{BASE_URL}/api/classrooms/{classroom_id}/materials', headers=headers, json={
        'title': 'Syllabus',
        'file_url': 'http://example.com/syllabus.pdf',
        'file_type': 'pdf'
    })
    
    if response.status_code != 201:
        print(f"Upload material failed: {response.text}")
        return
        
    print("Material uploaded")
    
    # 4. Create Assignment
    response = requests.post(f'{BASE_URL}/api/classrooms/{classroom_id}/assignments', headers=headers, json={
        'title': 'Homework 1',
        'description': 'Do the homework',
        'due_date': '2023-12-31T23:59'
    })
    
    if response.status_code != 201:
        print(f"Create assignment failed: {response.text}")
        return
        
    print("Assignment created")
    
    # 5. Get Details
    response = requests.get(f'{BASE_URL}/api/classrooms/{classroom_id}/details', headers=headers)
    
    if response.status_code != 200:
        print(f"Get details failed: {response.text}")
        return
        
    data = response.json()
    print(f"Details fetched for {data['name']}")
    print(f"Materials: {len(data['materials'])}")
    print(f"Assignments: {len(data['assignments'])}")
    
    if len(data['materials']) == 1 and len(data['assignments']) == 1:
        print("SUCCESS: Flow completed")
    else:
        print("FAILURE: Data mismatch")

if __name__ == '__main__':
    test_classroom_flow()
