from dotenv import load_dotenv
import os

print("Checking environment setup...")

# Try to load the .env file
load_dotenv()
print("\n1. Checking .env file:")
env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_path):
    print("✓ .env file found at:", env_path)
else:
    print("✗ .env file not found at:", env_path)

# Check if API key is set
print("\n2. Checking OPENAI_API_KEY:")
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print("✓ OPENAI_API_KEY is set")
    print("✓ Key starts with:", api_key[:5] + "..." + api_key[-4:])
else:
    print("✗ OPENAI_API_KEY not found in environment variables")

print("\nMake sure your .env file contains:")
print("OPENAI_API_KEY=sk-...</your-key-here>...") 