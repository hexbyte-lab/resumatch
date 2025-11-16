from flask import Blueprint, request, jsonify
from src.services.matcher import ResumeMatcher
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger("api")

# Create blueprint
api = Blueprint("api", __name__)

# Initialize matcher
matcher = ResumeMatcher()


@api.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({"status": "healthy", "message": "ResuMatch API is running"}), 200


@api.route("/analyze", methods=["POST"])
def analyze_resume():
    """
    Analyze resume against job description

    Expected JSON body:
    {
        "resume": "resume text here",
        "job_description": "job description text here"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400

        resume = data.get("resume", "").strip()
        job_description = data.get("job_description", "").strip()

        if not resume:
            return jsonify({"error": "Resume text is required"}), 400

        if not job_description:
            return jsonify({"error": "Job description is required"}), 400

        # Perform analysis
        result = matcher.analyze(resume, job_description)

        return jsonify({"success": True, "data": result}), 200

    except Exception as e:
        logger.error(f"Error in analyze: {str(e)}")
        return jsonify(
            {"error": "An error occurred during analysis", "details": str(e)}
        ), 500

@api.route("/analyze-file", methods=["POST"])
def analyze_file():
    """
    Analyze resume file against job description
    
    Expected form data:
    - resume_file: file upload (pdf, docx, txt)
    - job_description: text input string
    """
    from src.utils.file_processor import process_file # Import here to avoid circular imports
    
    try:
        # Check if file is present
        if 'resume_file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        file = request.files['resume_file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        job_description = request.form.get("job_description", "").strip()
        
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400
        
        try:
            resume_text = process_file(file)
        except Exception as e:
            return jsonify({"error": f"Could not extract text from file: {str(e)}"}), 400
        
        result = matcher.analyze(resume_text, job_description)
        
        return jsonify({
            "success": True,
            "data": result,
            'resume_preview': resume_text[:200] + '...' if len(resume_text) > 200 else resume_text
        }), 200
    except Exception as e:
        logger.error(f"Error in analyze_file: {str(e)}")
        return jsonify(
            {"error": "An error occurred during file analysis", "details": str(e)}
        ), 500