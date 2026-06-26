# 🎓 EduGenie AI – Smart Faculty Copilot for Higher Education

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![IBM Watsonx.ai](https://img.shields.io/badge/IBM-Watsonx.ai-blue.svg)](https://www.ibm.com/watsonx)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered academic productivity web application designed to transform faculty productivity in Higher Education Institutions (HEIs) by automating academic document generation and providing intelligent teaching assistance using IBM Watsonx.ai Granite models with a sophisticated multi-agent architecture.

## ✨ Features

### 📚 Academic Document Generation
- **📖 Lesson Plans** - Comprehensive teaching plans with objectives, outcomes, and methodologies
- **📝 Question Papers** - University-style examination papers with Bloom's taxonomy mapping
- **📚 Assignments** - Detailed assignments with evaluation criteria and rubrics
- **🎯 Course Outcomes** - Well-defined COs with PO-CO mapping
- **📊 Assessment Rubrics** - Professional rubrics with performance levels

### 📄 Administrative Documents
- **📄 Meeting Minutes** - Professional meeting documentation with action items
- **📢 Notices/Circulars** - Official institutional communications
- **📧 Official Emails** - Well-structured professional emails
- **📋 Event Reports** - Comprehensive workshop and seminar reports

### 🎓 Teaching Assistance
- **🌸 Bloom's Taxonomy Assistant** - Guidance on applying learning taxonomies
- **💡 Project Idea Generator** - Innovative project suggestions for students
- **🎓 Career Guidance** - Personalized career advice and certification recommendations
- **💬 AI Chat Assistant** - Instant answers to academic queries

## 🤖 Multi-Agent Architecture (Agentic AI)

EduGenie AI demonstrates advanced Agentic AI through specialized agents:

1. **Planner Agent** - Intelligently routes requests to appropriate specialized agents
2. **Lesson Plan Agent** - Generates teaching materials and schedules
3. **Assessment Agent** - Creates evaluations, question papers, and rubrics
4. **Academic Writing Agent** - Drafts official documents and communications
5. **Course Outcome Agent** - Defines learning outcomes with taxonomy mapping
6. **Student Mentor Agent** - Provides project ideas and career guidance
7. **AI Chat Agent** - Handles general academic queries

Each agent collaborates seamlessly to deliver precise, contextually appropriate results.

## 🚀 Technology Stack

- **Backend**: Python Flask 3.0.0
- **AI Engine**: IBM Watsonx.ai with Granite 13B Chat v2 model
- **Frontend**: Bootstrap 5.3.2, HTML5, CSS3, JavaScript
- **Icons**: Bootstrap Icons
- **Fonts**: Google Fonts (Inter)

## 📋 Prerequisites

- Python 3.8 or higher
- IBM Cloud account with Watsonx.ai access
- IBM Cloud API Key
- IBM Watsonx.ai Project ID

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "EduGenie AI – Smart Faculty Copilot"
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# IBM Watsonx.ai Configuration
IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### 5. Get IBM Cloud Credentials

1. **Create IBM Cloud Account**: Visit [IBM Cloud](https://cloud.ibm.com/)
2. **Create Watsonx.ai Project**:
   - Navigate to IBM Watsonx.ai
   - Create a new project
   - Note your Project ID
3. **Generate API Key**:
   - Go to IBM Cloud Dashboard
   - Navigate to "Manage" → "Access (IAM)" → "API keys"
   - Create a new API key
   - Copy and save the key securely

## 🎯 Customization

### Agent Instructions

Edit the `AGENT_INSTRUCTIONS` section in `app.py` to customize:

```python
AGENT_INSTRUCTIONS = {
    "institution": {
        "name": "Your University Name",
        "department": "Your Department",
        "address": "Your Address",
        "phone": "Your Phone",
        "email": "your@email.com",
        "website": "www.youruniversity.edu"
    },
    "academic": {
        "session": "2024-2025",
        "semester": "Odd Semester",
        "university_type": "Autonomous/Affiliated",
        "accreditation": "NAAC A+ Grade"
    },
    "response_style": {
        "tone": "professional, helpful, and academically rigorous",
        "language": "formal academic English",
        "format": "well-structured with clear headings",
        "length": "comprehensive yet concise"
    },
    # ... more customization options
}
```

### Branding

Customize colors and branding in `AGENT_INSTRUCTIONS`:

```python
"branding": {
    "primary_color": "#2563eb",
    "secondary_color": "#7c3aed",
    "accent_color": "#059669",
    "logo_text": "EduGenie AI"
}
```

## 🏃 Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Production Mode

**Using Gunicorn (Linux/macOS):**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Using Waitress (Windows):**

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 📁 Project Structure

```
EduGenie AI – Smart Faculty Copilot/
├── app.py                      # Main Flask application with multi-agent system
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your environment variables (create this)
├── README.md                  # This file
├── templates/                 # HTML templates
│   ├── base.html             # Base template with navigation
│   ├── index.html            # Landing page with hero section
│   ├── dashboard.html        # Faculty dashboard
│   └── feature.html          # Individual feature pages
└── static/                    # Static assets
    ├── css/
    │   └── style.css         # Custom styles
    ├── js/
    │   └── main.js           # JavaScript functionality
    └── images/               # Image assets
```

## 🎨 Features Overview

### Dashboard
- Real-time statistics (documents generated, AI interactions, time saved)
- Quick access to all 13 features
- Recent activity tracking
- AI chat quick access

### Document Generation
Each feature provides:
- Simple input forms with only necessary fields
- AI-powered content generation using IBM Granite
- Professional formatting
- Copy, download, and print options
- Real-time generation with loading indicators

### Multi-Agent Coordination
- Intelligent request routing by Planner Agent
- Specialized agents for different document types
- Seamless collaboration between agents
- Context-aware responses

## 🔒 Security Features

- Environment variable-based configuration
- Secure API key storage
- Session management
- Input validation
- Error handling

## 🌐 Deployment

### Deploy to IBM Cloud

1. Install IBM Cloud CLI
2. Login to IBM Cloud:
   ```bash
   ibmcloud login
   ```
3. Create Cloud Foundry app:
   ```bash
   ibmcloud cf push edugenie-ai
   ```

### Deploy to Heroku

1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Deploy:
   ```bash
   heroku create edugenie-ai
   git push heroku main
   ```

### Deploy to AWS/Azure/GCP

Follow standard Flask deployment procedures for your chosen platform.

## 📊 Usage Examples

### Generate a Lesson Plan

1. Navigate to Dashboard
2. Click "Generate Lesson Plan"
3. Fill in:
   - Subject Name
   - Course Code
   - Semester
   - Credits
   - Teaching Hours
   - Topic/Unit
4. Click "Generate with AI"
5. Review, copy, download, or print the generated lesson plan

### Create a Question Paper

1. Click "Generate Question Paper"
2. Provide:
   - Subject and Course Code
   - Semester
   - Total Marks and Duration
   - Exam Type
3. AI generates a complete question paper with:
   - Multiple sections (A, B, C)
   - Bloom's taxonomy mapping
   - Proper mark distribution

### Get Career Guidance

1. Click "Student Career Guidance"
2. Enter:
   - Field of Study
   - Current Level
   - Areas of Interest
   - Career Goals
3. Receive comprehensive guidance including:
   - Career paths
   - Required skills
   - Certifications
   - Action plan

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **IBM Watsonx.ai** for providing the Granite AI models
- **Bootstrap** for the responsive UI framework
- **Flask** for the lightweight web framework

## 📧 Support

For support, email: support@edugenie.ai (replace with your actual support email)

## 🔮 Future Enhancements

- [ ] PDF export functionality
- [ ] Document templates library
- [ ] Collaborative editing
- [ ] Integration with LMS platforms
- [ ] Mobile application
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Document version control
- [ ] Team collaboration features

## 📈 Version History

- **v1.0.0** (2024) - Initial release
  - Multi-agent architecture
  - 13 core features
  - IBM Watsonx.ai integration
  - Responsive web interface

## 🎯 Key Benefits

✅ **Save Time** - Automate repetitive academic tasks
✅ **Improve Quality** - AI-powered professional documents
✅ **Increase Productivity** - Focus on teaching, not paperwork
✅ **Ensure Consistency** - Standardized document formats
✅ **Stay Current** - Modern teaching methodologies
✅ **Easy Customization** - Adapt to your institution's needs

---

**Made with ❤️ for Higher Education Institutions**

**Powered by IBM Watsonx.ai Granite Models**