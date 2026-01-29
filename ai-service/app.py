from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parser import parse_resume
from scorer import calculate_score

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'AI Service is running'})

@app.route('/parse-resume', methods=['POST'])
def parse_resume_endpoint():
    """
    Parse resume and extract structured data
    Expected input: { "resume_path": "/path/to/resume.pdf" }
    """
    try:
        data = request.get_json()
        resume_path = data.get('resume_path')
        
        if not resume_path:
            return jsonify({'error': 'resume_path is required'}), 400
        
        if not os.path.exists(resume_path):
            return jsonify({'error': 'Resume file not found'}), 404
        
        # Parse resume to extract structured data
        parsed_data = parse_resume(resume_path)
        
        # Calculate AI score based on extracted data
        ai_score = calculate_score(parsed_data)
        parsed_data['ai_score'] = ai_score
        
        return jsonify(parsed_data), 200
        
    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/score-candidate', methods=['POST'])
def score_candidate():
    """
    Calculate score for candidate data
    Expected input: candidate JSON object
    """
    try:
        candidate_data = request.get_json()
        score = calculate_score(candidate_data)
        
        return jsonify({'score': score}), 200
        
    except Exception as e:
        print(f"Error scoring candidate: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🤖 Starting AI Service...")
    print("📡 Service running on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)