import os
import base64
from dotenv import load_dotenv

load_dotenv()

def generate_encryption_key():
    """Generate a 32-byte encryption key (for AES-256)"""
    key = os.urandom(32)  # AES-256 requires 32 bytes
    return base64.b64encode(key).decode('utf-8')  # Base64 encode the key

def generate_iv():
    """Generate a 16-byte initialization vector (IV) for AES"""
    iv = os.urandom(16)  # AES requires 16-byte IV
    return base64.b64encode(iv).decode('utf-8')  # Base64 encode the IV

def save_encryption_config_to_env():
    encryption_key = generate_encryption_key()
    iv = generate_iv()

    with open(".env", "a") as env_file:
        env_file.write(f"ENCRYPTION_KEY={encryption_key}\n")
        env_file.write(f"IV={iv}\n")

    # Print the generated values for confirmation
    print(f"Generated Encryption Key: {encryption_key}")
    print(f"Generated IV: {iv}")

# Call the function to save the keys to .env file
save_encryption_config_to_env()
