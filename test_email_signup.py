import requests
import random
import string

# 테스트 설정
API_URL = "http://127.0.0.1:8000"

def generate_random_email():
    """중복 방지를 위한 랜덤 이메일 생성"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@example.com"

def test_signup_and_email(real_email: str = None):
    """
    회원가입 API를 호출하여 Celery 이메일 발송 트리거 테스트
    real_email이 주어지면 해당 이메일로 가입을 시도합니다.
    """
    
    email = real_email if real_email else generate_random_email()
    password = "strong_password_123!"
    
    print(f"🚀 Testing Signup with email: {email}")
    
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{API_URL}/users/", json=payload)
        
        if response.status_code == 200:
            print("✅ Signup Successful!")
            print(f"   User ID: {response.json().get('email')}")
            print("   👉 Check your Celery Worker logs for email sending status.")
            if real_email:
                print(f"   👉 Check your inbox ({real_email}) for the welcome email.")
        else:
            print(f"❌ Signup Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API Server.")
        print("   Make sure 'uvicorn app.main:app --reload' is running locally.")

if __name__ == "__main__":
    import sys
    
    # 사용자 입력 받기
    print("--- 📧 Email Sending Test (Celery) ---")
    target_email = input("Enter a REAL email address to receive the test email (or press Enter for random): ").strip()
    
    if not target_email:
        target_email = None
        print("ℹ️ No email provided. Using random email (Email won't be delivered but Task will run).")
    
    test_signup_and_email(target_email)
