import requests
import json
import sys

# Configuration
BASE_URL = "http://127.0.0.1:8000"  # Testing against local backend
# BASE_URL = "https://web-production-e70e2.up.railway.app" # Uncomment to test production

def print_result(name, success, details):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} - {name}")
    print(f"Details: {details}")

def test_message_handler_ai():
    """Simulates the AI call in message_handler.ds"""
    print("\n--- Testing Message Handler (AI Recommendation) ---")
    url = f"{BASE_URL}/api/ai-recommend"
    payload = {"text": "I want a honeymoon trip to Bali under $2000"}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            if "recommendation" in data:
                print_result("AI Recommendation", True, f"Response: {data['recommendation'][:100]}...")
            else:
                print_result("AI Recommendation", False, f"Missing 'recommendation' key. Got: {data}")
        else:
            print_result("AI Recommendation", False, f"Status: {response.status_code}, Body: {response.text}")
    except Exception as e:
        print_result("AI Recommendation", False, f"Exception: {e}")

def test_context_handler_lead():
    """Simulates the Lead Creation in context_handler.ds"""
    print("\n--- Testing Context Handler (Create Lead) ---")
    url = f"{BASE_URL}/api/create-lead"
    payload = {
        "name": "Test User",
        "email": "test_user@example.com",
        "phone": "9998887776",
        "package_name": "Test Package via Script"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            # Expecting {"status": "lead_created"} or similar
            print_result("Create Lead", True, f"Response: {data}")
        else:
            print_result("Create Lead", False, f"Status: {response.status_code}, Body: {response.text}")
    except Exception as e:
        print_result("Create Lead", False, f"Exception: {e}")

def test_trigger_handler():
    """Trigger handler is purely client-side, but we can verify the server is up"""
    print("\n--- Testing Server Health (Prerequisite for Trigger Handler) ---")
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print_result("Server Health", True, f"Response: {response.json()}")
        else:
            print_result("Server Health", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Server Health", False, f"Exception: {e}")

if __name__ == "__main__":
    print(f"Testing against: {BASE_URL}")
    test_trigger_handler()
    test_message_handler_ai()
    test_context_handler_lead()
    print("\nDone.")
