"""
EduGenie AI – Smart Faculty Copilot for Higher Education
A Flask-based AI-powered academic productivity application using IBM Watsonx.ai Granite models
with multi-agent architecture demonstrating Agentic AI capabilities.
"""

from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-in-production')

# ============================================================================
# AGENT INSTRUCTIONS - CUSTOMIZE HERE
# ============================================================================
AGENT_INSTRUCTIONS = {
    "institution": {
        "name": "Sanatan Dharma College Ambala",
        "department": "Computer Science ",
        "address": "Jagadhari Road,Ambala Cantt, State - Haryana",
        "phone": "+91-1234567890",
        "email": "info@abcuniversity.edu",
        "website": "www.sdcollegeambala.ac.in"
    },
    "academic": {
        "session": "2026-2027",
        "semester": "Odd Semester (July-December)",
        "university_type": "Affiliated",
        "accreditation": "NAAC A++ Grade"
    },
    "response_style": {
        "tone": "professional, helpful, and academically rigorous",
        "language": "formal academic English",
        "format": "well-structured with clear headings and sections",
        "length": "comprehensive yet concise"
    },
    "document_templates": {
        "lesson_plan_format": "Standard university format with objectives, outcomes, teaching methodology, assessment, and resources",
        "question_paper_pattern": "University examination pattern with sections (A, B, C), marks distribution, and Bloom's taxonomy levels",
        "assignment_format": "Clear instructions, learning outcomes, evaluation criteria, and submission guidelines",
        "notice_format": "Official letterhead style with date, subject, body, and authority signature",
        "email_format": "Professional email with proper salutation, body, and closing"
    },
    "teaching_preferences": {
        "methodologies": ["Lecture", "Discussion", "Case Study", "Problem-Based Learning", "Flipped Classroom", "Project-Based Learning"],
        "ict_tools": ["PowerPoint", "Google Classroom", "Moodle", "Kahoot", "Mentimeter", "Virtual Labs"],
        "assessment_types": ["Formative", "Summative", "Continuous Assessment", "Peer Assessment", "Self Assessment"]
    },
    "blooms_taxonomy": {
        "levels": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"],
        "use_in_outcomes": True,
        "map_to_assessment": True
    },
    "branding": {
        "primary_color": "#2563eb",
        "secondary_color": "#7c3aed",
        "accent_color": "#059669",
        "logo_text": "EduGenie AI"
    },
    "safety_rules": {
        "no_plagiarism": True,
        "cite_sources": True,
        "ethical_guidelines": True,
        "data_privacy": True,
        "academic_integrity": True
    }
}

# ============================================================================
# IBM WATSONX.AI CONFIGURATION
# ============================================================================
IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
IBM_WATSONX_PROJECT_ID = os.getenv('IBM_WATSONX_PROJECT_ID')
IBM_WATSONX_URL = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')

# Model parameters
MODEL_ID = "meta-llama/llama-3-3-70b-instruct"
GENERATION_PARAMS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 2000,
    GenParams.MIN_NEW_TOKENS: 50,
    GenParams.TEMPERATURE: 0.7,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1
}

def get_watsonx_model():
    """Initialize and return IBM Watsonx.ai model"""
    try:
        model = ModelInference(
            model_id=MODEL_ID,
            params=GENERATION_PARAMS,
            credentials={
                "apikey": IBM_CLOUD_API_KEY,
                "url": IBM_WATSONX_URL
            },
            project_id=IBM_WATSONX_PROJECT_ID
        )
        return model
    except Exception as e:
        print(f"Error initializing Watsonx model: {str(e)}")
        return None

# ============================================================================
# MULTI-AGENT SYSTEM - AGENTIC AI ARCHITECTURE
# ============================================================================

class PlannerAgent:
    """
    Planner Agent - Routes requests to appropriate specialized agents
    Demonstrates intelligent task routing in Agentic AI
    """
    
    @staticmethod
    def route_request(user_request, feature_type):
        """Analyze request and route to appropriate agent"""
        routing_map = {
            "lesson_plan": "LessonPlanAgent",
            "question_paper": "AssessmentAgent",
            "assignment": "AssessmentAgent",
            "course_outcomes": "CourseOutcomeAgent",
            "rubric": "AssessmentAgent",
            "meeting_minutes": "AcademicWritingAgent",
            "notice": "AcademicWritingAgent",
            "email": "AcademicWritingAgent",
            "event_report": "AcademicWritingAgent",
            "blooms_taxonomy": "CourseOutcomeAgent",
            "project_ideas": "StudentMentorAgent",
            "career_guidance": "StudentMentorAgent",
            "chat": "AIChatAgent"
        }
        
        agent_name = routing_map.get(feature_type, "AIChatAgent")
        return agent_name

class LessonPlanAgent:
    """Specialized agent for generating lesson plans and teaching schedules"""
    
    @staticmethod
    def generate(data, model):
        """Generate comprehensive lesson plan"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""You are an expert academic curriculum designer for {inst['institution']['name']}, {inst['institution']['department']}.

Academic Session: {inst['academic']['session']}
Institution Type: {inst['academic']['university_type']}

Generate a comprehensive lesson plan with the following details:

Subject: {data.get('subject', 'N/A')}
Course Code: {data.get('course_code', 'N/A')}
Semester: {data.get('semester', 'N/A')}
Credits: {data.get('credits', 'N/A')}
Teaching Hours: {data.get('hours', 'N/A')} hours per week
Topic/Unit: {data.get('topic', 'N/A')}

Create a detailed lesson plan following this structure:

1. COURSE INFORMATION
   - Subject Name and Code
   - Semester and Credits
   - Teaching Hours

2. LESSON DETAILS
   - Unit/Topic Name
   - Duration
   - Prerequisites

3. LEARNING OBJECTIVES (Use Bloom's Taxonomy)
   - Cognitive objectives
   - Affective objectives
   - Psychomotor objectives (if applicable)

4. COURSE OUTCOMES (COs)
   - Map to Bloom's taxonomy levels
   - Align with program outcomes

5. TEACHING METHODOLOGY
   - Lecture topics and subtopics
   - Teaching methods: {', '.join(inst['teaching_preferences']['methodologies'])}
   - ICT tools: {', '.join(inst['teaching_preferences']['ict_tools'])}

6. LESSON PLAN (Week-wise breakdown)
   - Week number
   - Topics to be covered
   - Teaching method
   - Resources required

7. ASSESSMENT STRATEGY
   - Formative assessment methods
   - Summative assessment methods
   - Continuous evaluation

8. LEARNING RESOURCES
   - Textbooks
   - Reference books
   - Online resources
   - Video lectures

9. ASSIGNMENTS AND ACTIVITIES
   - In-class activities
   - Homework assignments
   - Projects

Format the output professionally with clear headings and proper academic structure."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating lesson plan: {str(e)}"

class AssessmentAgent:
    """Specialized agent for creating assessments, question papers, and rubrics"""
    
    @staticmethod
    def generate_question_paper(data, model):
        """Generate university-style question paper"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""You are an expert examination paper setter for {inst['institution']['name']}.

Generate a university examination question paper with the following specifications:

Subject: {data.get('subject', 'N/A')}
Course Code: {data.get('course_code', 'N/A')}
Semester: {data.get('semester', 'N/A')}
Total Marks: {data.get('marks', '100')}
Duration: {data.get('duration', '3')} hours
Exam Type: {data.get('exam_type', 'End Semester')}

Create a question paper following this structure:

HEADER:
{inst['institution']['name']}
{inst['institution']['department']}
{inst['academic']['session']}
{data.get('exam_type', 'End Semester')} Examination

Subject: {data.get('subject', 'N/A')}
Course Code: {data.get('course_code', 'N/A')}
Semester: {data.get('semester', 'N/A')}
Time: {data.get('duration', '3')} Hours
Maximum Marks: {data.get('marks', '100')}

INSTRUCTIONS TO CANDIDATES:
1. Attempt all questions
2. Figures to the right indicate full marks
3. Use of calculator is permitted/not permitted
4. Draw neat diagrams wherever necessary

SECTION A (Short Answer Questions - Remember/Understand Level)
- 10 questions × 2 marks = 20 marks
- Answer any 8 questions

SECTION B (Medium Answer Questions - Apply/Analyze Level)
- 6 questions × 5 marks = 30 marks
- Answer any 4 questions

SECTION C (Long Answer Questions - Analyze/Evaluate/Create Level)
- 5 questions × 10 marks = 50 marks
- Answer any 3 questions

For each question:
- Indicate Bloom's taxonomy level
- Indicate course outcome (CO) mapping
- Ensure questions cover entire syllabus
- Include variety: theoretical, numerical, case-based, design-based

Generate complete questions for all sections with proper academic rigor."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating question paper: {str(e)}"
    
    @staticmethod
    def generate_assignment(data, model):
        """Generate assignment"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""You are an expert faculty member at {inst['institution']['name']}.

Create a comprehensive assignment with the following details:

Subject: {data.get('subject', 'N/A')}
Topic: {data.get('topic', 'N/A')}
Semester: {data.get('semester', 'N/A')}
Marks: {data.get('marks', '20')}
Submission Deadline: {data.get('deadline', '2 weeks from assignment date')}

Structure the assignment as follows:

1. ASSIGNMENT HEADER
   - Institution name and department
   - Subject and course code
   - Assignment number and topic
   - Submission deadline

2. LEARNING OUTCOMES
   - What students will learn
   - Skills to be developed
   - Bloom's taxonomy level

3. ASSIGNMENT QUESTIONS/TASKS
   - Clear, specific questions or tasks
   - Mix of theoretical and practical
   - Progressive difficulty level

4. INSTRUCTIONS
   - Format requirements (word count, pages, etc.)
   - Submission format (PDF, hardcopy, etc.)
   - Citation style (APA, IEEE, etc.)
   - Plagiarism warning

5. EVALUATION CRITERIA
   - Rubric with marking scheme
   - Content quality (X marks)
   - Presentation (X marks)
   - Originality (X marks)
   - References (X marks)

6. RESOURCES
   - Recommended readings
   - Online resources
   - Reference materials

Make it academically rigorous and aligned with course outcomes."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating assignment: {str(e)}"
    
    @staticmethod
    def generate_rubric(data, model):
        """Generate assessment rubric"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""Create a detailed assessment rubric for:

Assessment Type: {data.get('assessment_type', 'Assignment')}
Subject: {data.get('subject', 'N/A')}
Total Marks: {data.get('marks', '20')}

Generate a comprehensive rubric with:

1. CRITERIA AND WEIGHTAGE
   - List all evaluation criteria
   - Assign marks to each criterion

2. PERFORMANCE LEVELS
   - Excellent (90-100%)
   - Good (75-89%)
   - Satisfactory (60-74%)
   - Needs Improvement (Below 60%)

3. DETAILED DESCRIPTORS
   - For each criterion, describe what constitutes each performance level
   - Be specific and measurable

4. SCORING GUIDE
   - How to calculate final score
   - Weightage distribution

Format as a professional rubric table with clear descriptions."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating rubric: {str(e)}"

class AcademicWritingAgent:
    """Specialized agent for academic documents, notices, emails, reports"""
    
    @staticmethod
    def generate_notice(data, model):
        """Generate official notice/circular"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""Generate an official notice/circular for {inst['institution']['name']}.

Type: {data.get('doc_type', 'Notice')}
Subject: {data.get('subject', 'N/A')}
Target Audience: {data.get('audience', 'All Faculty')}
Details: {data.get('details', 'N/A')}

Format:

{inst['institution']['name']}
{inst['institution']['department']}
{inst['institution']['address']}

Date: {datetime.now().strftime('%B %d, %Y')}

NOTICE/CIRCULAR

Subject: {data.get('subject', 'N/A')}

[Professional body text with all details]

[Closing remarks]

[Authority Name]
[Designation]
{inst['institution']['department']}

Use formal, professional language appropriate for official academic communication."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating notice: {str(e)}"
    
    @staticmethod
    def generate_email(data, model):
        """Generate official email"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""Draft a professional official email:

To: {data.get('recipient', 'N/A')}
Subject: {data.get('subject', 'N/A')}
Purpose: {data.get('purpose', 'N/A')}
Key Points: {data.get('details', 'N/A')}

Format:

Subject: {data.get('subject', 'N/A')}

Dear [Recipient],

[Professional email body with proper structure]

[Closing]

Best regards,
[Your Name]
[Your Designation]
{inst['institution']['department']}
{inst['institution']['name']}
Email: {inst['institution']['email']}
Phone: {inst['institution']['phone']}

Use professional, courteous tone."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating email: {str(e)}"
    
    @staticmethod
    def generate_meeting_minutes(data, model):
        """Generate meeting minutes"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""Generate professional meeting minutes:

Meeting Type: {data.get('meeting_type', 'Department Meeting')}
Date: {data.get('date', datetime.now().strftime('%B %d, %Y'))}
Attendees: {data.get('attendees', 'N/A')}
Agenda: {data.get('agenda', 'N/A')}

Format:

MINUTES OF MEETING

Institution: {inst['institution']['name']}
Department: {inst['institution']['department']}
Meeting Type: {data.get('meeting_type', 'N/A')}
Date: {data.get('date', 'N/A')}
Time: {data.get('time', 'N/A')}
Venue: {data.get('venue', 'N/A')}

ATTENDEES:
[List of attendees]

AGENDA:
[Agenda items]

DISCUSSIONS:
[Detailed discussion points]

DECISIONS TAKEN:
[List of decisions]

ACTION ITEMS:
[Action items with responsible persons and deadlines]

NEXT MEETING:
[Date and time]

[Chairperson Name]
Chairperson

[Secretary Name]
Secretary"""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating meeting minutes: {str(e)}"
    
    @staticmethod
    def generate_report(data, model):
        """Generate event/workshop report"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""Generate a comprehensive event report:

Event Type: {data.get('event_type', 'Workshop')}
Event Name: {data.get('event_name', 'N/A')}
Date: {data.get('date', 'N/A')}
Organizer: {data.get('organizer', inst['institution']['department'])}
Details: {data.get('details', 'N/A')}

Structure:

EVENT REPORT

1. EVENT DETAILS
   - Name, date, venue, duration
   - Organizing department
   - Coordinator details

2. OBJECTIVES
   - Purpose of the event
   - Target audience
   - Expected outcomes

3. EVENT DESCRIPTION
   - Detailed description of activities
   - Sessions conducted
   - Resource persons

4. PARTICIPANTS
   - Number of participants
   - Demographics

5. OUTCOMES
   - Learning outcomes
   - Feedback summary
   - Success metrics

6. PHOTOGRAPHS
   - [Mention photo documentation]

7. CONCLUSION
   - Summary
   - Future recommendations

Prepared by:
[Name]
[Designation]
{inst['institution']['department']}"""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating report: {str(e)}"

class CourseOutcomeAgent:
    """Specialized agent for course outcomes and Bloom's taxonomy"""
    
    @staticmethod
    def generate_course_outcomes(data, model):
        """Generate course outcomes with Bloom's taxonomy mapping"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""Generate comprehensive Course Outcomes (COs) for:

Subject: {data.get('subject', 'N/A')}
Course Code: {data.get('course_code', 'N/A')}
Semester: {data.get('semester', 'N/A')}
Credits: {data.get('credits', 'N/A')}

Create detailed course outcomes following this structure:

1. COURSE DESCRIPTION
   - Brief overview of the course
   - Prerequisites
   - Course relevance

2. COURSE OUTCOMES (COs)
   Generate 5-6 specific, measurable course outcomes using this format:
   
   CO1: [Action Verb] [Content] [Context]
   Bloom's Level: [Remember/Understand/Apply/Analyze/Evaluate/Create]
   
   Example:
   CO1: Analyze and design database schemas for real-world applications
   Bloom's Level: Analyze (Level 4)

3. CO-PO MAPPING
   Map each CO to Program Outcomes (POs):
   - PO1: Engineering Knowledge
   - PO2: Problem Analysis
   - PO3: Design/Development of Solutions
   - PO4: Modern Tool Usage
   - PO5: Communication
   
   Create a mapping matrix showing correlation strength (1-Weak, 2-Medium, 3-Strong)

4. BLOOM'S TAXONOMY DISTRIBUTION
   - Show distribution across taxonomy levels
   - Ensure higher-order thinking skills

5. ASSESSMENT METHODS
   - How each CO will be assessed
   - Formative and summative assessments

Use action verbs from Bloom's taxonomy:
- Remember: Define, List, Recall, Identify
- Understand: Explain, Describe, Summarize, Interpret
- Apply: Apply, Demonstrate, Implement, Use
- Analyze: Analyze, Compare, Examine, Differentiate
- Evaluate: Evaluate, Justify, Critique, Assess
- Create: Create, Design, Develop, Formulate"""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating course outcomes: {str(e)}"
    
    @staticmethod
    def blooms_taxonomy_guide(data, model):
        """Provide Bloom's taxonomy guidance"""
        prompt = f"""Provide comprehensive guidance on Bloom's Taxonomy for:

Topic: {data.get('topic', 'General')}
Level: {data.get('level', 'All levels')}

Explain:

1. BLOOM'S TAXONOMY OVERVIEW
   - Six cognitive levels
   - Progression from lower to higher order thinking

2. DETAILED LEVEL DESCRIPTIONS
   
   Level 1 - REMEMBER (Knowledge)
   - Definition and purpose
   - Action verbs: List, Define, Identify, Recall, Name, State
   - Example questions
   - Assessment methods
   
   Level 2 - UNDERSTAND (Comprehension)
   - Definition and purpose
   - Action verbs: Explain, Describe, Summarize, Interpret, Classify
   - Example questions
   - Assessment methods
   
   Level 3 - APPLY (Application)
   - Definition and purpose
   - Action verbs: Apply, Demonstrate, Implement, Use, Execute
   - Example questions
   - Assessment methods
   
   Level 4 - ANALYZE (Analysis)
   - Definition and purpose
   - Action verbs: Analyze, Compare, Examine, Differentiate, Organize
   - Example questions
   - Assessment methods
   
   Level 5 - EVALUATE (Evaluation)
   - Definition and purpose
   - Action verbs: Evaluate, Justify, Critique, Assess, Judge
   - Example questions
   - Assessment methods
   
   Level 6 - CREATE (Synthesis)
   - Definition and purpose
   - Action verbs: Create, Design, Develop, Formulate, Construct
   - Example questions
   - Assessment methods

3. PRACTICAL APPLICATION
   - How to write learning objectives
   - How to design assessments
   - How to create rubrics

4. EXAMPLES FOR YOUR TOPIC
   - Sample questions at each level
   - Activity suggestions"""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating Bloom's taxonomy guide: {str(e)}"

class StudentMentorAgent:
    """Specialized agent for student guidance, projects, and career advice"""
    
    @staticmethod
    def generate_project_ideas(data, model):
        """Generate project ideas for students"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""Generate innovative project ideas for students:

Domain: {data.get('domain', 'Computer Science')}
Level: {data.get('level', 'Undergraduate')}
Semester: {data.get('semester', 'N/A')}
Team Size: {data.get('team_size', '3-4 students')}
Duration: {data.get('duration', 'One semester')}

Provide 5-7 project ideas with the following structure for each:

PROJECT IDEA #1: [Catchy Title]

1. OVERVIEW
   - Brief description (2-3 sentences)
   - Problem statement
   - Target users

2. OBJECTIVES
   - Main goals of the project
   - Learning outcomes

3. TECHNOLOGY STACK
   - Programming languages
   - Frameworks and libraries
   - Tools and platforms
   - Database

4. KEY FEATURES
   - Core functionalities (5-7 features)
   - Innovative aspects

5. IMPLEMENTATION APPROACH
   - High-level architecture
   - Development phases
   - Timeline

6. LEARNING OUTCOMES
   - Technical skills gained
   - Soft skills developed
   - Industry relevance

7. DIFFICULTY LEVEL
   - Beginner/Intermediate/Advanced
   - Prerequisites

8. FUTURE ENHANCEMENTS
   - Scalability options
   - Advanced features

9. RESOURCES
   - Tutorials
   - Documentation
   - Similar projects for reference

10. INDUSTRY RELEVANCE
    - Real-world applications
    - Career opportunities

Make projects innovative, practical, and aligned with current industry trends."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating project ideas: {str(e)}"
    
    @staticmethod
    def career_guidance(data, model):
        """Provide career guidance to students"""
        prompt = f"""Provide comprehensive career guidance:

Student Profile:
- Field of Study: {data.get('field', 'Computer Science')}
- Current Level: {data.get('level', 'Undergraduate')}
- Interests: {data.get('interests', 'N/A')}
- Career Goals: {data.get('goals', 'N/A')}

Provide detailed guidance covering:

1. CAREER PATHS
   - List 5-7 career options in this field
   - For each career path:
     * Job description
     * Required skills
     * Typical roles and responsibilities
     * Career progression
     * Salary expectations (entry to senior level)

2. SKILLS DEVELOPMENT
   - Technical skills needed
   - Soft skills required
   - Certifications to pursue
   - Online courses and platforms

3. INDUSTRY TRENDS
   - Current market demand
   - Emerging technologies
   - Future outlook
   - Hot skills in demand

4. EDUCATION PATHWAY
   - Higher education options (Masters, PhD)
   - Specializations to consider
   - Top universities/institutions
   - Scholarships and funding

5. CERTIFICATIONS
   - Industry-recognized certifications
   - Vendor-specific certifications
   - Professional certifications
   - Timeline and costs

6. INTERNSHIP & EXPERIENCE
   - How to find internships
   - Building portfolio
   - Open source contributions
   - Networking strategies

7. JOB SEARCH STRATEGY
   - Resume building tips
   - Interview preparation
   - Job portals and platforms
   - Company research

8. ENTREPRENEURSHIP
   - Startup opportunities
   - Business ideas
   - Funding options
   - Resources for entrepreneurs

9. WORK-LIFE BALANCE
   - Industry work culture
   - Remote work opportunities
   - Freelancing options

10. ACTION PLAN
    - Short-term goals (6 months)
    - Medium-term goals (1-2 years)
    - Long-term goals (3-5 years)
    - Specific action items

Provide practical, actionable advice tailored to the student's profile."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error generating career guidance: {str(e)}"

class AIChatAgent:
    """General AI chat agent for academic queries"""
    
    @staticmethod
    def chat(message, model):
        """Handle general chat queries"""
        inst = AGENT_INSTRUCTIONS
        
        prompt = f"""You are EduGenie AI, an intelligent academic assistant for {inst['institution']['name']}.

Your role:
- Answer academic and teaching-related questions
- Provide helpful guidance to faculty members
- Suggest teaching strategies and methodologies
- Recommend educational resources
- Assist with academic planning

Tone: {inst['response_style']['tone']}
Language: {inst['response_style']['language']}

User Query: {message}

Provide a helpful, accurate, and professional response."""

        try:
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            return f"Error in chat: {str(e)}"

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html', config=AGENT_INSTRUCTIONS)

@app.route('/dashboard')
def dashboard():
    """Faculty dashboard"""
    # Initialize session data if not exists
    if 'documents_generated' not in session:
        session['documents_generated'] = 0
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    return render_template('dashboard.html', config=AGENT_INSTRUCTIONS)

@app.route('/feature/<feature_type>')
def feature_page(feature_type):
    """Individual feature pages"""
    feature_titles = {
        'lesson_plan': 'Generate Lesson Plan',
        'question_paper': 'Generate Question Paper',
        'assignment': 'Generate Assignment',
        'course_outcomes': 'Generate Course Outcomes',
        'rubric': 'Create Assessment Rubric',
        'meeting_minutes': 'Write Meeting Minutes',
        'notice': 'Create Notice/Circular',
        'email': 'Draft Official Email',
        'event_report': 'Generate Event Report',
        'blooms_taxonomy': "Bloom's Taxonomy Assistant",
        'project_ideas': 'Project Idea Generator',
        'career_guidance': 'Student Career Guidance',
        'chat': 'AI Chat Assistant'
    }
    
    title = feature_titles.get(feature_type, 'Feature')
    return render_template('feature.html', feature_type=feature_type, title=title, config=AGENT_INSTRUCTIONS)

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """API endpoint for content generation using multi-agent system"""
    try:
        data = request.json
        feature_type = data.get('feature_type')
        
        # Initialize Watsonx model
        model = get_watsonx_model()
        if not model:
            return jsonify({
                'success': False,
                'error': 'Failed to initialize AI model. Please check your API credentials.'
            }), 500
        
        # Step 1: Planner Agent routes the request
        agent_name = PlannerAgent.route_request(data, feature_type)
        
        # Step 2: Execute appropriate specialized agent
        result = None
        
        if agent_name == "LessonPlanAgent":
            result = LessonPlanAgent.generate(data, model)
        
        elif agent_name == "AssessmentAgent":
            if feature_type == "question_paper":
                result = AssessmentAgent.generate_question_paper(data, model)
            elif feature_type == "assignment":
                result = AssessmentAgent.generate_assignment(data, model)
            elif feature_type == "rubric":
                result = AssessmentAgent.generate_rubric(data, model)
        
        elif agent_name == "AcademicWritingAgent":
            if feature_type == "notice":
                result = AcademicWritingAgent.generate_notice(data, model)
            elif feature_type == "email":
                result = AcademicWritingAgent.generate_email(data, model)
            elif feature_type == "meeting_minutes":
                result = AcademicWritingAgent.generate_meeting_minutes(data, model)
            elif feature_type == "event_report":
                result = AcademicWritingAgent.generate_report(data, model)
        
        elif agent_name == "CourseOutcomeAgent":
            if feature_type == "course_outcomes":
                result = CourseOutcomeAgent.generate_course_outcomes(data, model)
            elif feature_type == "blooms_taxonomy":
                result = CourseOutcomeAgent.blooms_taxonomy_guide(data, model)
        
        elif agent_name == "StudentMentorAgent":
            if feature_type == "project_ideas":
                result = StudentMentorAgent.generate_project_ideas(data, model)
            elif feature_type == "career_guidance":
                result = StudentMentorAgent.career_guidance(data, model)
        
        elif agent_name == "AIChatAgent":
            message = data.get('message', '')
            result = AIChatAgent.chat(message, model)
        
        # Update session statistics
        if 'documents_generated' in session:
            session['documents_generated'] += 1
        else:
            session['documents_generated'] = 1
        
        # Store in chat history if it's a chat
        if feature_type == 'chat' and 'chat_history' in session and result:
            session['chat_history'].append({
                'timestamp': datetime.now().isoformat(),
                'message': data.get('message', ''),
                'response': result[:100] + '...' if len(str(result)) > 100 else str(result)
            })
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'content': result,
            'agent_used': agent_name,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat functionality"""
    try:
        data = request.json
        message = data.get('message', '')
        
        model = get_watsonx_model()
        if not model:
            return jsonify({
                'success': False,
                'error': 'Failed to initialize AI model.'
            }), 500
        
        response = AIChatAgent.chat(message, model)
        
        # Store in chat history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'response': response[:100] + '...' if len(response) > 100 else response
        })
        session.modified = True
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get user statistics"""
    return jsonify({
        'documents_generated': session.get('documents_generated', 0),
        'chat_messages': len(session.get('chat_history', [])),
        'last_activity': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
