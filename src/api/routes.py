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
