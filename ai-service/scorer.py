"""
Candidate Scoring Algorithm

This module implements a multi-factor scoring system to rank internship candidates.
The score is on a 0-100 scale based on:
1. Skills match (40%)
2. CGPA (25%)
3. Projects (20%)
4. Experience (15%)
"""

# Target skills for the internship (customize based on JD)
TARGET_SKILLS = [
    'python', 'java', 'javascript', 'react', 'node.js', 'mongodb',
    'mysql', 'git', 'data structures', 'algorithms', 'rest'
]

# High-value skills that give bonus points
BONUS_SKILLS = [
    'docker', 'kubernetes', 'aws', 'machine learning', 'system design'
]

def calculate_skills_score(skills):
    """
    Calculate score based on skill match
    Returns: 0-100 score
    """
    if not skills:
        return 0
    
    skills_lower = [s.lower() for s in skills]
    
    # Base score: percentage of target skills matched
    matched_skills = sum(1 for target in TARGET_SKILLS if target.lower() in skills_lower)
    base_score = (matched_skills / len(TARGET_SKILLS)) * 80
    
    # Bonus: up to 20 points for high-value skills
    bonus_matched = sum(1 for bonus in BONUS_SKILLS if bonus.lower() in skills_lower)
    bonus_score = min(bonus_matched * 5, 20)
    
    return min(base_score + bonus_score, 100)

def calculate_cgpa_score(cgpa):
    """
    Calculate score based on CGPA
    Returns: 0-100 score
    
    Scoring logic:
    - CGPA >= 9.0: 100 points
    - CGPA 8.0-8.99: 85-99 points
    - CGPA 7.0-7.99: 70-84 points
    - CGPA < 7.0: 50-69 points
    """
    if not cgpa or cgpa <= 0:
        return 50  # Default if CGPA not provided
    
    if cgpa >= 9.0:
        return 100
    elif cgpa >= 8.0:
        return 85 + (cgpa - 8.0) * 15
    elif cgpa >= 7.0:
        return 70 + (cgpa - 7.0) * 15
    else:
        return max(50, 50 + (cgpa - 6.0) * 20)

def calculate_projects_score(projects):
    """
    Calculate score based on projects
    Returns: 0-100 score
    
    Scoring logic:
    - 0 projects: 30 points
    - 1 project: 60 points
    - 2 projects: 80 points
    - 3+ projects: 100 points
    """
    if not projects:
        return 30
    
    num_projects = len(projects)
    
    if num_projects >= 3:
        return 100
    elif num_projects == 2:
        return 80
    elif num_projects == 1:
        return 60
    else:
        return 30

def calculate_experience_score(experience):
    """
    Calculate score based on work experience/internships
    Returns: 0-100 score
    
    Scoring logic:
    - No experience: 50 points
    - 1 internship: 75 points
    - 2+ internships: 100 points
    """
    if not experience:
        return 50
    
    num_experiences = len(experience)
    
    if num_experiences >= 2:
        return 100
    elif num_experiences == 1:
        return 75
    else:
        return 50

def calculate_score(candidate_data):
    """
    Calculate overall AI score for a candidate
    
    Args:
        candidate_data (dict): Dictionary containing candidate information
        
    Returns:
        float: Score from 0-100
    """
    # Extract data
    skills = candidate_data.get('skills', [])
    cgpa = candidate_data.get('cgpa')
    projects = candidate_data.get('projects', [])
    experience = candidate_data.get('experience', [])
    
    # Calculate component scores
    skills_score = calculate_skills_score(skills)
    cgpa_score = calculate_cgpa_score(cgpa)
    projects_score = calculate_projects_score(projects)
    experience_score = calculate_experience_score(experience)
    
    # Weighted average (customizable weights)
    WEIGHTS = {
        'skills': 0.40,      # 40%
        'cgpa': 0.25,        # 25%
        'projects': 0.20,    # 20%
        'experience': 0.15   # 15%
    }
    
    final_score = (
        skills_score * WEIGHTS['skills'] +
        cgpa_score * WEIGHTS['cgpa'] +
        projects_score * WEIGHTS['projects'] +
        experience_score * WEIGHTS['experience']
    )
    
    # Round to 1 decimal place
    return round(final_score, 1)

def get_score_breakdown(candidate_data):
    """
    Get detailed breakdown of how the score was calculated
    Useful for explaining scoring to users
    
    Returns:
        dict: Breakdown of scores
    """
    skills = candidate_data.get('skills', [])
    cgpa = candidate_data.get('cgpa')
    projects = candidate_data.get('projects', [])
    experience = candidate_data.get('experience', [])
    
    breakdown = {
        'skills': {
            'score': calculate_skills_score(skills),
            'weight': '40%',
            'matched': sum(1 for s in skills if s.lower() in [t.lower() for t in TARGET_SKILLS])
        },
        'cgpa': {
            'score': calculate_cgpa_score(cgpa),
            'weight': '25%',
            'value': cgpa
        },
        'projects': {
            'score': calculate_projects_score(projects),
            'weight': '20%',
            'count': len(projects)
        },
        'experience': {
            'score': calculate_experience_score(experience),
            'weight': '15%',
            'count': len(experience)
        },
        'final_score': calculate_score(candidate_data)
    }
    
    return breakdown