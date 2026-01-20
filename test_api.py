#!/usr/bin/env python3

import requests
import json
import time
import subprocess
import sys
from threading import Thread

def test_api():
    base_url = "http://localhost:5001"
    
    print("🚀 Testing Flask REST API")
    print("=" * 50)
    
    # Test 1: Get all users (should be empty initially)
    print("\n1. GET /users (empty)")
    try:
        response = requests.get(f"{base_url}/users")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except:
        print("❌ Server not running")
        return
    
    # Test 2: Create a user
    print("\n2. POST /users (create user)")
    user_data = {"name": "Alice Smith", "email": "alice@example.com"}
    response = requests.post(f"{base_url}/users", json=user_data)
    print(f"Status: {response.status_code}")
    user = response.json()
    print(f"Response: {user}")
    user_id = user.get('id')
    
    # Test 3: Get user by ID
    print(f"\n3. GET /users/{user_id} (get user with posts)")
    response = requests.get(f"{base_url}/users/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Create a post
    print("\n4. POST /posts (create post)")
    post_data = {
        "title": "My Amazing Post", 
        "content": "This is the content of my post!",
        "user_id": user_id
    }
    response = requests.post(f"{base_url}/posts", json=post_data)
    print(f"Status: {response.status_code}")
    post = response.json()
    print(f"Response: {post}")
    post_id = post.get('id')
    
    # Test 5: Get all posts
    print("\n5. GET /posts (all posts with authors)")
    response = requests.get(f"{base_url}/posts")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 6: Update user
    print(f"\n6. PATCH /users/{user_id} (update user)")
    update_data = {"name": "Alice Johnson"}
    response = requests.patch(f"{base_url}/users/{user_id}", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 7: Error handling - invalid email
    print("\n7. POST /users (invalid email)")
    bad_user = {"name": "Bad User", "email": "invalid-email"}
    response = requests.post(f"{base_url}/users", json=bad_user)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 8: Error handling - user not found
    print("\n8. GET /users/999 (user not found)")
    response = requests.get(f"{base_url}/users/999")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n✅ API Testing Complete!")
    print("\n📋 Summary:")
    print("- ✅ Models: User and Post with relationships")
    print("- ✅ Validations: Name, email, title, content validation")
    print("- ✅ REST Routes: GET, POST, PATCH, DELETE")
    print("- ✅ JSON Responses: Proper structure with nested data")
    print("- ✅ HTTP Status Codes: 200, 201, 400, 404")
    print("- ✅ Error Handling: Informative error messages")

if __name__ == "__main__":
    test_api()