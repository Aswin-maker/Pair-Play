import httpx
import asyncio
import sys

BASE_URL = "http://localhost:8000"
TOKEN = "supersecretkey"

async def test_endpoints():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    async with httpx.AsyncClient() as client:
        # 1. Root
        try:
            resp = await client.get(f"{BASE_URL}/")
            print(f"GET /: {resp.status_code}")
            if resp.status_code != 200:
                print(resp.text)
                return False
        except Exception as e:
            print(f"Failed to connect to {BASE_URL}: {e}")
            return False

        # 2. Get Packages
        resp = await client.get(f"{BASE_URL}/packages/", headers=headers)
        print(f"GET /packages/: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)
            return False

        # 3. Search Packages
        resp = await client.post(f"{BASE_URL}/packages/search", headers=headers, json={"location": "Bali"})
        print(f"POST /packages/search: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)
            return False

        # 4. Send OTP
        resp = await client.post(f"{BASE_URL}/leads/send-otp", headers=headers, json={"phone": "+1234567890"})
        print(f"POST /leads/send-otp: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)
            return False

        # 5. Generate Invoice
        resp = await client.post(f"{BASE_URL}/payments/generate-invoice", headers=headers, json={
            "customer_name": "Test User",
            "email": "test@example.com",
            "phone": "+1234567890",
            "amount": 1000,
            "description": "Test Trip"
        })
        print(f"POST /payments/generate-invoice: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)
            return False
            
        # 6. AI Recommend
        resp = await client.post(f"{BASE_URL}/ai/recommend", headers=headers, json={"query": "beach vacation"})
        print(f"POST /ai/recommend: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)
            return False

    return True

if __name__ == "__main__":
    success = asyncio.run(test_endpoints())
    if success:
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Tests failed!")
        sys.exit(1)
