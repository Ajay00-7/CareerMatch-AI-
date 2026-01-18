from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



# Import existing utility modules
from utils.resume_parser import parse_resume, extract_project_section, extract_internship_section
from utils.nlp_processor import NLPProcessor
from utils.skill_extractor import SkillExtractor
from utils.job_matcher import JobMatcher
from utils.ai_coach import AICoach

# Initialize Flask app
app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for development

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize NLP components (cached globally)
nlp_processor = None
skill_extractor = None
job_matcher = None
ai_coach = None


def initialize_components():
    """Initialize NLP components on startup"""
    global nlp_processor, skill_extractor, job_matcher, ai_coach
    
    try:
        logger.info("Initializing NLP components...")
        nlp_processor = NLPProcessor()
        skill_extractor = SkillExtractor(nlp_processor)
        job_matcher = JobMatcher()
        ai_coach = AICoach()
        logger.info("NLP components initialized successfully!")
    except Exception as e:
        logger.error(f"Error initializing components: {e}")
        raise


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_summary(skills, top_matches):
    """Generate summary text for resume analysis"""
    skill_count = len(skills)
    if not top_matches:
        return f"Your resume demonstrates {skill_count} identified skills. Upload a more detailed resume for better job matching."
    
    top_match = top_matches[0]
    avg_match = sum(m['score'] for m in top_matches[:3]) / min(len(top_matches), 3)
    
    return f"Your resume demonstrates strong technical expertise with {skill_count} identified skills. You are an excellent match for {top_match['job_title']} roles with a {top_match['score']:.0f}% compatibility score. Your diverse skillset positions you well for {len(top_matches[:3])} different career paths with an average match rate of {avg_match:.0f}%. {'Your comprehensive skill portfolio is a significant strength.' if skill_count >= 12 else 'Consider expanding your skillset for broader opportunities.'}"


def generate_recommendations(top_matches, skills):
    """Generate personalized recommendations"""
    recommendations = []
    all_missing = set()
    
    # Collect missing skills from top 3 matches
    for match in top_matches[:3]:
        all_missing.update(match.get('missing_skills', []))
    
    missing_list = list(all_missing)
    
    # Skill recommendations
    if missing_list:
        top_missing = missing_list[:5]
        recommendations.append(f"Focus on learning: {', '.join(top_missing)} to improve your job match")
    
    # Certification recommendations
    certifications = {
        "aws": "Get AWS Certified Solutions Architect certification",
        "azure": "Consider Microsoft Azure Fundamentals certification",
        "machine learning": "Pursue Google ML Engineer or AWS ML Specialty certification",
        "kubernetes": "Earn Certified Kubernetes Administrator (CKA) certification",
        "python": "Get Python Institute PCEP or PCAP certification"
    }
    
    for skill in missing_list[:3]:
        if skill.lower() in certifications:
            recommendations.append(certifications[skill.lower()])
    
    # General recommendations
    if len(skills) < 10:
        recommendations.append("Expand your technical skillset - aim for 12-15 diverse skills")
    
    if not any('git' in s.lower() for s in skills):
        recommendations.append("Add version control (Git/GitHub) to your resume")
    
    if not any(s.lower() in ['docker', 'kubernetes', 'ci/cd'] for s in skills):
        recommendations.append("Learn DevOps fundamentals (Docker, CI/CD) for better opportunities")
    
    recommendations.append("Include quantifiable achievements in your projects")
    recommendations.append("Keep your resume updated with latest projects and technologies")
    
    return recommendations[:7]


def extract_education(resume_text):
    """Extract education information from resume"""
    education_keywords = [
        'bachelor', 'master', 'phd', 'doctorate', 'degree',
        'computer science', 'engineering', 'mba', 'b.tech', 'm.tech',
        'university', 'college', 'institute', 'graduation'
    ]
    
    education_info = []
    lines = resume_text.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        for keyword in education_keywords:
            if keyword in line_lower and len(line) < 150 and line.strip():
                education_info.append(line.strip())
                break
    
    # Remove duplicates and limit
    unique_education = list(dict.fromkeys(education_info))[:3]
    
    return '<br>'.join(unique_education) if unique_education else 'Education information not clearly specified'


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, videos, etc.)"""
    return send_from_directory('.', path)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and extract text"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Use PDF, DOCX, or TXT'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract text from file
        logger.info(f"Extracting text from {filename}")
        extracted_text = parse_resume(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            return jsonify({'error': 'Could not extract meaningful text from file'}), 400
        
        return jsonify({
            'success': True,
            'text': extracted_text,
            'filename': filename
        })
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume text and return job matches"""
    try:
        # Get resume text from request
        data = request.get_json()
        resume_text = data.get('resumeText', '').strip()
        target_role = data.get('target_role', '').strip()  # [NEW] Get target role
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        if len(resume_text) < 100:
            return jsonify({'error': 'Resume text is too short. Please provide a detailed resume.'}), 400
        
        logger.info("Processing resume with NLP...")
        
        # Process text with NLP
        doc = nlp_processor.process_text(resume_text)
        
        # Extract skills
        logger.info("Extracting skills...")
        categorized_skills, flat_skills = skill_extractor.extract_skills(doc)
        
        # Match jobs
        logger.info(f"Matching jobs... (Target: {target_role if target_role else 'None'})")
        job_matches = job_matcher.match_jobs(flat_skills, target_role if target_role else None)
        
        # Get top 5 matches (UPDATED FROM 3 TO 5 AS REQUESTED)
        top_matches = job_matches[:5]
        
        # Extract education
        education = extract_education(resume_text)

        # Extract and Analyze Projects
        logger.info("Analyzing projects...")
        project_text = extract_project_section(resume_text)
        project_analysis = job_matcher.analyze_projects(project_text, flat_skills)
        
        # Extract and Analyze Internships [NEW FEATURE]
        logger.info("Analyzing internships...")
        internship_text = extract_internship_section(resume_text)
        internship_analysis = job_matcher.analyze_internships(internship_text, flat_skills)

        # Generate summary and recommendations
        summary = generate_summary(flat_skills, top_matches)
        recommendations = generate_recommendations(top_matches, flat_skills)
        
        # Prepare response
        response = {
            'success': True,
            'skills': flat_skills,
            'categorizedSkills': categorized_skills,
            'jobMatches': top_matches,
            'education': education,
            'projectAnalysis': project_analysis,
            'internshipAnalysis': internship_analysis,
            'summary': summary,
            'recommendations': recommendations
        }
        
        logger.info(f"Analysis complete: {len(flat_skills)} skills, {len(top_matches)} job matches")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        return jsonify({'error': f'Error analyzing resume: {str(e)}'}), 500





@app.route('/api/chat', methods=['POST'])
def chat_with_coach():
    """Handle chat messages with AI Coach"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        response = ai_coach.generate_response(message, context)
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': f'Error processing chat: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'nlp_processor': nlp_processor is not None,
            'skill_extractor': skill_extractor is not None,
            'job_matcher': job_matcher is not None
        }
    })


if __name__ == '__main__':
    # Initialize components before starting server
    initialize_components()
    
    # Start Flask server
    logger.info("Starting Flask server...")
    logger.info("Application will be available at http://localhost:5000")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
