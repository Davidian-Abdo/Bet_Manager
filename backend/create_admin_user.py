import os
import sys
from dotenv import load_dotenv
import requests

# Load environment
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

def create_admin_user():
    BASE_URL = "https://camden-strangulative-freezingly.ngrok-free.dev"
    
    # ✅ CORRECT data matching your UserCreate schema
    user_data = {
        "full_name": "System Administrator",    # ← Must be "name", not "full_name"
        "email": "admin@betmanager.com",   # ← Correct
        "password": "admin123",            # ← Correct
        "role": "admin"                    # ← Must include role
    }
    
    print(f"🔧 Creating admin user at: {BASE_URL}/api/auth/register")
    print(f"📤 Sending: {user_data}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ Admin user created successfully!")
            print(f"🆔 User ID: {user_info.get('id')}")
            print(f"👤 Name: {user_info.get('full_name')}")
            print(f"📧 Email: {user_info.get('email')}")
            print(f"🎯 Role: {user_info.get('role')}")
            print(f"🔑 Password: admin123")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    create_admin_user()