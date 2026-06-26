# 🔧 Troubleshooting Guide - EduGenie AI

## ❌ Error: "Failed to initialize AI model. Please check your API credentials"

This error occurs when the IBM Watsonx.ai credentials are missing or incorrect.

### Solution Steps:

#### 1. Check if .env file exists
```bash
# Windows
dir .env

# Linux/Mac
ls -la .env
```

If the file doesn't exist, create it:
```bash
cp .env.example .env
```

#### 2. Get IBM Cloud API Key

**Step-by-step:**

1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Login to your account
3. Click on **Manage** (top menu) → **Access (IAM)**
4. Click **API keys** in the left sidebar
5. Click **Create** button
6. Give it a name (e.g., "EduGenie AI")
7. Click **Create**
8. **IMPORTANT:** Copy the API key immediately (you won't see it again!)

#### 3. Get IBM Watsonx.ai Project ID

**Step-by-step:**

1. Go to [IBM Watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Login with the same IBM Cloud account
3. Click **Projects** in the left menu
4. Create a new project or open an existing one:
   - Click **New project**
   - Choose **Create an empty project**
   - Give it a name (e.g., "EduGenie AI Project")
   - Click **Create**
5. Once in the project, click **Manage** tab
6. Click **General** in the left sidebar
7. Copy the **Project ID** (it looks like: `12345678-1234-1234-1234-123456789abc`)

#### 4. Update .env file

Open `.env` file and add your credentials:

```env
# IBM Watsonx.ai Configuration
IBM_CLOUD_API_KEY=paste_your_api_key_here
IBM_WATSONX_PROJECT_ID=paste_your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Flask Configuration
FLASK_SECRET_KEY=change_this_to_any_random_string
FLASK_ENV=development
```

**Example:**
```env
IBM_CLOUD_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
IBM_WATSONX_PROJECT_ID=12345678-1234-1234-1234-123456789abc
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
FLASK_SECRET_KEY=my-super-secret-key-12345
FLASK_ENV=development
```

#### 5. Verify .env file is loaded

Add this test to check if environment variables are loaded:

```python
# Run this in Python console or create test.py
from dotenv import load_dotenv
import os

load_dotenv()

print("API Key:", os.getenv('IBM_CLOUD_API_KEY'))
print("Project ID:", os.getenv('IBM_WATSONX_PROJECT_ID'))
print("URL:", os.getenv('IBM_WATSONX_URL'))
```

If any value shows `None`, the .env file is not being loaded correctly.

#### 6. Restart the application

After updating .env:
```bash
# Stop the app (Ctrl+C)
# Start again
python app.py
```

### Common Issues:

#### Issue 1: .env file not in the correct location
**Solution:** Make sure .env is in the same directory as app.py

```
EduGenie AI – Smart Faculty Copilot/
├── app.py
├── .env          ← Must be here!
├── requirements.txt
└── ...
```

#### Issue 2: Spaces in .env file
**Wrong:**
```env
IBM_CLOUD_API_KEY = your_key_here
```

**Correct:**
```env
IBM_CLOUD_API_KEY=your_key_here
```

#### Issue 3: Quotes around values
**Wrong:**
```env
IBM_CLOUD_API_KEY="your_key_here"
```

**Correct:**
```env
IBM_CLOUD_API_KEY=your_key_here
```

#### Issue 4: Invalid API Key
**Solution:** Generate a new API key from IBM Cloud

#### Issue 5: Project not associated with Watsonx.ai
**Solution:** Make sure your project is created in Watsonx.ai, not just IBM Cloud

#### Issue 6: Wrong region URL
**Solution:** Check your IBM Cloud region:
- US South: `https://us-south.ml.cloud.ibm.com`
- EU Germany: `https://eu-de.ml.cloud.ibm.com`
- Japan Tokyo: `https://jp-tok.ml.cloud.ibm.com`

### Test Your Credentials

Create a file `test_credentials.py`:

```python
from dotenv import load_dotenv
import os
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Load environment variables
load_dotenv()

IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
IBM_WATSONX_PROJECT_ID = os.getenv('IBM_WATSONX_PROJECT_ID')
IBM_WATSONX_URL = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')

print("Testing IBM Watsonx.ai credentials...")
print(f"API Key: {'✓ Set' if IBM_CLOUD_API_KEY else '✗ Missing'}")
print(f"Project ID: {'✓ Set' if IBM_WATSONX_PROJECT_ID else '✗ Missing'}")
print(f"URL: {IBM_WATSONX_URL}")

if not IBM_CLOUD_API_KEY or not IBM_WATSONX_PROJECT_ID:
    print("\n❌ Error: Missing credentials in .env file")
    exit(1)

try:
    print("\nInitializing model...")
    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 100,
            GenParams.MIN_NEW_TOKENS: 10,
            GenParams.TEMPERATURE: 0.7,
        },
        credentials={
            "apikey": IBM_CLOUD_API_KEY,
            "url": IBM_WATSONX_URL
        },
        project_id=IBM_WATSONX_PROJECT_ID
    )
    
    print("✓ Model initialized successfully!")
    
    print("\nTesting generation...")
    response = model.generate_text(prompt="Hello, this is a test. Respond with 'Test successful!'")
    print(f"✓ Response: {response}")
    
    print("\n✅ All tests passed! Your credentials are working correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nPossible solutions:")
    print("1. Check if your API key is valid")
    print("2. Verify your Project ID is correct")
    print("3. Ensure your project has Watsonx.ai enabled")
    print("4. Check your internet connection")
    print("5. Verify you have access to IBM Watsonx.ai")
```

Run the test:
```bash
python test_credentials.py
```

### Still Having Issues?

1. **Check IBM Cloud Status**: Visit [IBM Cloud Status](https://cloud.ibm.com/status)
2. **Verify Billing**: Ensure your IBM Cloud account has billing enabled
3. **Check Quotas**: Verify you haven't exceeded API quotas
4. **Review Logs**: Check the Flask console for detailed error messages
5. **Contact Support**: Reach out to IBM Cloud support

### Quick Checklist

- [ ] .env file exists in project root
- [ ] IBM_CLOUD_API_KEY is set (no quotes, no spaces)
- [ ] IBM_WATSONX_PROJECT_ID is set (no quotes, no spaces)
- [ ] IBM_WATSONX_URL is correct for your region
- [ ] API key is valid and not expired
- [ ] Project exists in Watsonx.ai (not just IBM Cloud)
- [ ] Internet connection is working
- [ ] Application was restarted after updating .env

---

**Need more help?** Check the [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)