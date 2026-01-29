import re
import pdfplumber
from docx import Document
import spacy

# Load spaCy model for NLP
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("⚠️  spaCy model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

# Common skills to look for
TECH_SKILLS = [
    'python', 'java', 'javascript', 'c++', 'c#', 'react', 'angular', 'vue',
    'node.js', 'express', 'django', 'flask', 'spring', 'mongodb', 'mysql',
    'postgresql', 'redis', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
    'git', 'html', 'css', 'typescript', 'sql', 'nosql', 'rest', 'graphql',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
    'data structures', 'algorithms', 'system design', 'agile', 'scrum'
]

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""

def extract_text(file_path):
    """Extract text based on file extension"""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def extract_email(text):
    """Extract email address using regex"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_phone(text):
    """Extract phone number using regex"""
    phone_pattern = r'(\+91[\-\s]?)?[6789]\d{9}'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else None

def extract_name(text):
    """Extract name from resume (first line heuristic or NLP)"""
    lines = text.strip().split('\n')
    # First non-empty line is often the name
    for line in lines:
        line = line.strip()
        if line and len(line.split()) <= 4 and len(line) > 3:
            return line
    
    # Fallback: use NLP to find PERSON entities
    if nlp:
        doc = nlp(text[:500])  # Check first 500 chars
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
    
    return "Unknown"

def extract_cgpa(text):
    """Extract CGPA/GPA from text"""
    # Look for patterns like "CGPA: 8.5" or "GPA: 3.8/4.0"
    cgpa_patterns = [
        r'cgpa[:\s]+(\d+\.?\d*)',
        r'gpa[:\s]+(\d+\.?\d*)',
        r'grade[:\s]+(\d+\.?\d*)',
    ]
    
    text_lower = text.lower()
    for pattern in cgpa_patterns:
        match = re.search(pattern, text_lower)
        if match:
            cgpa = float(match.group(1))
            # Normalize to 10-point scale if needed
            if cgpa <= 4.0:
                cgpa = cgpa * 2.5  # Convert 4.0 scale to 10.0 scale
            return round(cgpa, 2)
    
    return None

def extract_graduation_year(text):
    """Extract graduation year"""
    # Look for patterns like "2025" or "Expected: 2025"
    year_pattern = r'\b(20[2-3]\d)\b'
    years = re.findall(year_pattern, text)
    
    # Return the most recent year (likely graduation)
    if years:
        return max(int(year) for year in years)
    return None

def extract_college(text):
    """Extract college/university name"""
    # Common patterns for Indian institutes
    college_keywords = ['iit', 'nit', 'iiit', 'bits', 'vit', 'dtu', 'nsit', 
                       'university', 'institute of technology', 'college']
    
    lines = text.lower().split('\n')
    for line in lines:
        for keyword in college_keywords:
            if keyword in line:
                # Return the original case line
                original_line = text.split('\n')[lines.index(line)]
                return original_line.strip()
    
    return None

def extract_skills(text):
    """Extract technical skills from text"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in TECH_SKILLS:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def extract_projects(text):
    """Extract project names/descriptions"""
    projects = []
    
    # Look for section headers like "Projects", "Academic Projects"
    project_section_pattern = r'(?i)(projects?|academic projects?)[:\n](.+?)(?=\n\n|\nexperience|\neducation|$)'
    match = re.search(project_section_pattern, text, re.DOTALL)
    
    if match:
        project_text = match.group(2)
        # Split by bullet points or numbers
        project_lines = re.split(r'\n\s*[•\-\*\d\.]+\s*', project_text)
        for line in project_lines:
            line = line.strip()
            if line and len(line) > 10:
                projects.append(line[:100])  # Limit to 100 chars
    
    return projects[:3]  # Return top 3 projects

def extract_experience(text):
    """Extract work experience"""
    experience = []
    
    # Look for experience section
    exp_pattern = r'(?i)(experience|internship)[:\n](.+?)(?=\n\n|education|projects?|$)'
    match = re.search(exp_pattern, text, re.DOTALL)
    
    if match:
        exp_text = match.group(2)
        # Look for company names and durations
        exp_lines = re.split(r'\n\s*[•\-\*]+\s*', exp_text)
        for line in exp_lines:
            line = line.strip()
            if line and len(line) > 15:
                experience.append(line[:150])  # Limit to 150 chars
    
    return experience[:2]  # Return top 2 experiences

def parse_resume(file_path):
    """
    Main function to parse resume and extract all information
    Returns: Dictionary with structured candidate data
    """
    text = extract_text(file_path)
    
    if not text:
        raise ValueError("Could not extract text from resume")
    
    parsed_data = {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'college': extract_college(text),
        'degree': 'B.Tech Computer Science',  # Default, can be improved
        'graduation_year': extract_graduation_year(text),
        'cgpa': extract_cgpa(text),
        'skills': extract_skills(text),
        'projects': extract_projects(text),
        'experience': extract_experience(text)
    }
    
    return parsed_data