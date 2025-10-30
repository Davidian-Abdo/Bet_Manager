import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path and load .env
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir  # Since this is in Bet_Manager folder
env_path = os.path.join(project_root, '.env')

print(f"Looking for .env at: {env_path}")
print(f".env exists: {os.path.exists(env_path)}")

# Load environment variables
load_dotenv(env_path)

# Check if key variables are loaded
print(f"DB_USER loaded: {os.getenv('DB_USER')}")
print(f"JWT_SECRET_KEY loaded: {bool(os.getenv('JWT_SECRET_KEY'))}")

try:
    from backend.core.security import hash_password
    print("✅ Successfully imported hash_password")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_password_hashing():
    test_passwords = [
        "admin123",  # Your current password
        "a" * 100,   # Very long password
        "test"       # Short password
    ]
    
    for pwd in test_passwords:
        print(f"\nTesting password: '{pwd}'")
        print(f"Length: {len(pwd)} chars, {len(pwd.encode('utf-8'))} bytes")
        try:
            hashed = hash_password(pwd)
            print(f"✅ Hashing successful: {hashed[:50]}...")
        except Exception as e:
            print(f"❌ Hashing failed: {e}")

if __name__ == "__main__":
    test_password_hashing() 