import os
import sys
from dotenv import load_dotenv

# Load environment
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

sys.path.append(current_dir)

def debug_password():
    password = "admin123"
    
    print(f"🔍 Debugging password: '{password}'")
    print(f"📏 Length: {len(password)} characters")
    print(f"💾 Size: {len(password.encode('utf-8'))} bytes")
    print(f"🔢 ASCII values: {[ord(c) for c in password]}")
    
    # Test what happens in security.py
    try:
        from backend.core.security import hash_password, pwd_context
        
        print(f"\n🔐 Testing with your security module...")
        
        # Test direct bcrypt
        print("Direct bcrypt test:")
        hashed = pwd_context.hash(password)
        print(f"✅ Hash successful: {hashed[:50]}...")
        
        # Test your hash_password function
        print("Your hash_password function:")
        hashed2 = hash_password(password)
        print(f"✅ Your function worked: {hashed2[:50]}...")
        
        # Verify they match
        print(f"🔍 Hashes match: {hashed == hashed2}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_password()