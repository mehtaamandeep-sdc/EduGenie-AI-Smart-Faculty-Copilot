# 🚀 Quick Start Guide - EduGenie AI

Get up and running with EduGenie AI in 5 minutes!

## ⚡ Quick Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your IBM Cloud credentials:

```env
IBM_CLOUD_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
FLASK_SECRET_KEY=your_random_secret_key_here
FLASK_ENV=development
```

### Step 3: Run the Application

```bash
python app.py
```

### Step 4: Open in Browser

Navigate to: **http://localhost:5000**

## 🔑 Getting IBM Cloud Credentials

### Get API Key:
1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Login/Sign up
3. Navigate to: **Manage → Access (IAM) → API keys**
4. Click **Create** and copy your API key

### Get Project ID:
1. Go to [IBM Watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Create or open a project
3. Go to **Manage → General**
4. Copy your **Project ID**

## 🎯 Customize Your Institution

Edit `app.py` and find the `AGENT_INSTRUCTIONS` section (around line 40):

```python
AGENT_INSTRUCTIONS = {
    "institution": {
        "name": "Your University Name",  # Change this
        "department": "Your Department",  # Change this
        "address": "Your Address",
        "phone": "+91-1234567890",
        "email": "info@youruniversity.edu",
        "website": "www.youruniversity.edu"
    },
    # ... more settings
}
```

## 📱 First Steps

1. **Visit Dashboard**: Click "Dashboard" in the navigation
2. **Try a Feature**: Click any feature card (e.g., "Generate Lesson Plan")
3. **Fill the Form**: Enter required details
4. **Generate**: Click "Generate with AI"
5. **Use Content**: Copy, download, or print the generated document

## 🎨 Features to Try

### For Teaching:
- 📖 Generate Lesson Plan
- 📝 Generate Question Paper
- 📚 Generate Assignment
- 🎯 Generate Course Outcomes

### For Administration:
- 📄 Write Meeting Minutes
- 📢 Create Notice/Circular
- 📧 Draft Official Email
- 📋 Generate Event Report

### For Students:
- 💡 Project Idea Generator
- 🎓 Student Career Guidance
- 🌸 Bloom's Taxonomy Assistant

### General:
- 💬 AI Chat Assistant

## 🔧 Troubleshooting

### Issue: "Failed to initialize AI model"
**Solution**: Check your IBM Cloud API key and Project ID in `.env`

### Issue: "Module not found"
**Solution**: Run `pip install -r requirements.txt`

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py` (last line): `app.run(port=5001)`

### Issue: Templates not loading
**Solution**: Ensure you're running from the project root directory

## 📚 Example Usage

### Generate a Lesson Plan:

1. Click "Generate Lesson Plan"
2. Fill in:
   - Subject: "Database Management Systems"
   - Course Code: "CS301"
   - Semester: "5th Semester"
   - Credits: "4"
   - Teaching Hours: "4 hours per week"
   - Topic: "SQL and Relational Algebra"
3. Click "Generate with AI"
4. Wait 10-15 seconds
5. Review and use the generated lesson plan!

## 🎓 Multi-Agent System

EduGenie AI uses 7 specialized AI agents:

1. **Planner Agent** → Routes your request
2. **Lesson Plan Agent** → Creates teaching materials
3. **Assessment Agent** → Generates evaluations
4. **Academic Writing Agent** → Drafts documents
5. **Course Outcome Agent** → Defines learning outcomes
6. **Student Mentor Agent** → Provides guidance
7. **AI Chat Agent** → Answers queries

Each agent is powered by **IBM Granite 13B Chat v2** model!

## 💡 Tips

✅ **Be Specific**: Provide detailed information for better results
✅ **Review Output**: Always review AI-generated content
✅ **Customize**: Edit the generated content as needed
✅ **Save Time**: Use templates for recurring tasks
✅ **Explore**: Try all 13 features to maximize productivity

## 🆘 Need Help?

- 📖 Read the full [README.md](README.md)
- 💬 Use the AI Chat Assistant in the app
- 🐛 Check the console for error messages
- 📧 Contact support (if available)

## 🎉 You're Ready!

Start generating professional academic documents with AI!

**Happy Teaching! 🎓**

---

**Powered by IBM Watsonx.ai Granite Models**