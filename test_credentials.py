"""
Test script to verify IBM Watsonx.ai credentials
Run this before starting the main application
"""

from dotenv import load_dotenv
import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
load_dotenv()

print("=" * 60)
print("EduGenie AI - Credentials Test")
print("=" * 60)

# Check environment variables
IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
IBM_WATSONX_PROJECT_ID = os.getenv('IBM_WATSONX_PROJECT_ID')
IBM_WATSONX_URL = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')

print("\n1. Checking Environment Variables...")
print("-" * 60)

if IBM_CLOUD_API_KEY:
    print(f"[OK] IBM_CLOUD_API_KEY: Set (length: {len(IBM_CLOUD_API_KEY)} characters)")
else:
    print("[ERROR] IBM_CLOUD_API_KEY: NOT SET")

if IBM_WATSONX_PROJECT_ID:
    print(f"[OK] IBM_WATSONX_PROJECT_ID: Set ({IBM_WATSONX_PROJECT_ID})")
else:
    print("[ERROR] IBM_WATSONX_PROJECT_ID: NOT SET")

print(f"[OK] IBM_WATSONX_URL: {IBM_WATSONX_URL}")

if not IBM_CLOUD_API_KEY or not IBM_WATSONX_PROJECT_ID:
    print("\n" + "=" * 60)
    print("[FAILED] ERROR: Missing credentials!")
    print("=" * 60)
    print("\nPlease follow these steps:")
    print("\n1. Create a .env file in the project root directory")
    print("2. Add your IBM Cloud credentials:")
    print("\n   IBM_CLOUD_API_KEY=your_api_key_here")
    print("   IBM_WATSONX_PROJECT_ID=your_project_id_here")
    print("   IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com")
    print("\n3. Get credentials from:")
    print("   - API Key: https://cloud.ibm.com/iam/apikeys")
    print("   - Project ID: https://dataplatform.cloud.ibm.com/wx/home")
    print("\nSee TROUBLESHOOTING.md for detailed instructions.")
    exit(1)

# Test IBM Watsonx.ai connection
print("\n2. Testing IBM Watsonx.ai Connection...")
print("-" * 60)

try:
    from ibm_watsonx_ai.foundation_models import Model
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    
    print("[OK] IBM Watsonx.ai library imported successfully")
    
    print("\nInitializing model...")
    model = Model(
        model_id="meta-llama/llama-3-3-70b-instruct",
        params={
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 50,
            GenParams.MIN_NEW_TOKENS: 10,
            GenParams.TEMPERATURE: 0.7,
        },
        credentials={
            "apikey": IBM_CLOUD_API_KEY,
            "url": IBM_WATSONX_URL
        },
        project_id=IBM_WATSONX_PROJECT_ID
    )
    
    print("[OK] Model initialized successfully!")
    
    print("\nTesting text generation...")
    response = model.generate_text(
        prompt="Say 'Hello from EduGenie AI!' in one sentence."
    )
    
    print(f"[OK] AI Response: {response}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] All tests passed!")
    print("=" * 60)
    print("\nYour IBM Watsonx.ai credentials are working correctly.")
    print("You can now run the application with: python app.py")
    
except ImportError as e:
    print(f"\n[ERROR] Import Error: {str(e)}")
    print("\nPlease install required packages:")
    print("  pip install -r requirements.txt")
    exit(1)
    
except Exception as e:
    print(f"\n[ERROR] Connection Error: {str(e)}")
    print("\n" + "=" * 60)
    print("[FAILED] Could not connect to IBM Watsonx.ai")
    print("=" * 60)
    print("\nPossible issues:")
    print("1. Invalid API Key - Generate a new one from IBM Cloud")
    print("2. Invalid Project ID - Check your Watsonx.ai project")
    print("3. Wrong region URL - Verify your IBM Cloud region")
    print("4. No internet connection - Check your network")
    print("5. Billing not enabled - Ensure IBM Cloud billing is active")
    print("6. API quota exceeded - Check your usage limits")
    print("\nFor detailed help, see TROUBLESHOOTING.md")
    exit(1)

# Made with Bob
