#!/usr/bin/env python3
"""
API Test Script for Quiz System
Tests all API endpoints to ensure they work correctly
"""

import requests
import json
import time

# Base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data)
        else:
            print(f"[FAIL] Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"[OK] {method} {endpoint} - Status: {response.status_code}")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"   Response: {response.text[:200]}...")
            return True
        else:
            print(f"[FAIL] {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] {method} {endpoint} - Connection Error (Is the server running?)")
        return False
    except Exception as e:
        print(f"[FAIL] {method} {endpoint} - Error: {str(e)}")
        return False

def main():
    """Run all API tests"""
    print("Starting API Tests for Quiz System")
    print("=" * 50)
    
    tests = [
        # Health check
        ("GET", "/health/"),
        
        # Get all subjects
        ("GET", "/subjects/"),
        
        # Get specific subject
        ("GET", "/subjects/CSW351-AI/"),
        
        # Get questions
        ("GET", "/questions/"),
        ("GET", "/questions/?subject_code=CSW351-AI&level=easy&limit=5"),
        
        # Generate quiz
        ("POST", "/quiz/generate/", {
            "subject_code": "CSW351-AI",
            "level": "easy",
            "num_questions": 5
        }),
        
        # Submit quiz (using sample answers)
        ("POST", "/quiz/submit/", {
            "answers": [
                {"question_id": 1, "selected_answer": "A"},
                {"question_id": 2, "selected_answer": "B"}
            ]
        }),
        
        # Get statistics
        ("GET", "/stats/"),
    ]
    
    passed = 0
    total = len(tests)
    
    for method, endpoint, *data in tests:
        data = data[0] if data else None
        if test_endpoint(method, endpoint, data):
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! API is working correctly.")
    else:
        print("Some tests failed. Check the output above.")
    
    print("\nAPI Documentation: API_DOCUMENTATION.md")
    print("Browseable API: http://127.0.0.1:8000/api/")

if __name__ == "__main__":
    main()
