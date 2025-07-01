from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
from src.services.job_analyzer import JobAnalyzer
from src.services.cv_generator import CVGenerator

cv_bp = Blueprint('cv', __name__)

# Initialize services
job_analyzer = JobAnalyzer()
cv_generator = CVGenerator()

# Allowed file extensions for job descriptions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cv_bp.route('/analyze-job', methods=['POST'])
def analyze_job_description():
    """Analyze job description and extract keywords/requirements"""
    try:
        job_text = ""
        
        # Check if job description is provided as JSON
        if request.is_json:
            data = request.get_json()
            if 'job_text' in data:
                job_text = data['job_text']
        
        # Check if job description is provided as form data
        elif 'job_text' in request.form:
            job_text = request.form['job_text']
        
        # Check if job description is uploaded as file
        elif 'job_file' in request.files:
            file = request.files['job_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_content = file.read()
                job_text = job_analyzer.extract_text_from_file(file_content, filename)
            else:
                return jsonify({'error': 'Invalid file type. Please upload txt, pdf, doc, or docx files.'}), 400
        
        else:
            return jsonify({'error': 'No job description provided. Please provide job_text or job_file.'}), 400
        
        if not job_text.strip():
            return jsonify({'error': 'Job description is empty.'}), 400
        
        # Analyze job description
        analysis = job_analyzer.analyze_job_description(job_text)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to analyze job description: {str(e)}'}), 500

@cv_bp.route('/generate-cv', methods=['POST'])
def generate_cv():
    """Generate ATS-optimized CV based on user data and job analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_data = data.get('user_data', {})
        job_analysis = data.get('job_analysis', None)
        
        # Validate required user data
        if not user_data.get('personal_info', {}).get('full_name'):
            return jsonify({'error': 'Full name is required'}), 400
        
        # Generate CV
        cv_filepath = cv_generator.generate_cv(user_data, job_analysis)
        
        # Return CV file path and metadata
        return jsonify({
            'success': True,
            'cv_id': os.path.basename(cv_filepath).replace('.pdf', '').replace('cv_', ''),
            'message': 'CV generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate CV: {str(e)}'}), 500

@cv_bp.route('/download-cv/<cv_id>', methods=['GET'])
def download_cv(cv_id):
    """Download generated CV"""
    try:
        cv_filename = f"cv_{cv_id}.pdf"
        cv_filepath = os.path.join('/tmp', cv_filename)
        
        if not os.path.exists(cv_filepath):
            return jsonify({'error': 'CV not found'}), 404
        
        return send_file(
            cv_filepath,
            as_attachment=True,
            download_name=f"optimized_cv_{cv_id}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to download CV: {str(e)}'}), 500

@cv_bp.route('/templates', methods=['GET'])
def get_cv_templates():
    """Get available CV templates"""
    try:
        templates = cv_generator.get_cv_templates()
        return jsonify({
            'success': True,
            'templates': templates
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get templates: {str(e)}'}), 500

@cv_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'CV Generator API',
        'version': '1.0.0'
    })

# Sample data endpoint for testing
@cv_bp.route('/sample-data', methods=['GET'])
def get_sample_data():
    """Get sample user data for testing"""
    sample_data = {
        'personal_info': {
            'full_name': 'John Doe',
            'email': 'john.doe@email.com',
            'phone': '+1 (555) 123-4567',
            'location': 'New York, NY',
            'linkedin': 'linkedin.com/in/johndoe'
        },
        'professional_summary': 'Experienced software developer with 5+ years of experience in full-stack web development. Proficient in Python, JavaScript, and modern web frameworks. Strong problem-solving skills and experience working in agile environments.',
        'work_experience': [
            {
                'job_title': 'Senior Software Developer',
                'company': 'Tech Solutions Inc.',
                'start_date': 'Jan 2020',
                'end_date': 'Present',
                'description': '• Led development of web applications using React and Python Flask\n• Improved application performance by 40% through code optimization\n• Mentored junior developers and conducted code reviews\n• Collaborated with cross-functional teams to deliver projects on time'
            },
            {
                'job_title': 'Software Developer',
                'company': 'StartupXYZ',
                'start_date': 'Jun 2018',
                'end_date': 'Dec 2019',
                'description': '• Developed and maintained web applications using JavaScript and Node.js\n• Implemented RESTful APIs and database designs\n• Participated in agile development processes\n• Reduced bug reports by 30% through improved testing practices'
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Science in Computer Science',
                'school': 'University of Technology',
                'graduation_date': '2018',
                'gpa': '3.8'
            }
        ],
        'skills': {
            'technical_skills': ['Python', 'JavaScript', 'React', 'Node.js', 'Flask', 'SQL', 'Git', 'AWS', 'Docker'],
            'soft_skills': ['Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Time Management'],
            'languages': ['English (Native)', 'Spanish (Conversational)'],
            'certifications': ['AWS Certified Developer', 'Scrum Master Certified']
        }
    }
    
    return jsonify({
        'success': True,
        'sample_data': sample_data
    })

