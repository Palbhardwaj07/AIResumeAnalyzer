# app/utils.py
import os
import json
import re
from datetime import datetime

def clean_text(text):
    """Clean extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def extract_email(text):
    """Extract email from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails[0] if emails else None

def extract_phone(text):
    """Extract phone number from text"""
    pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
    phones = re.findall(pattern, text)
    return '-'.join(phones[0]) if phones else None

def extract_name(text):
    """Extract likely name from text (simplified)"""
    # Usually name appears in first few lines
    lines = text.split('\n')[:5]
    for line in lines:
        line = line.strip()
        if len(line.split()) <= 3 and line:
            # Check if it contains common name patterns
            if not any(keyword in line.lower() for keyword in ['resume', 'cv', 'profile', 'contact']):
                return line
    return None

def save_uploaded_file(uploaded_file, save_dir="uploads"):
    """Save uploaded file to disk"""
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def parse_analysis_response(response_text):
    """Parse LLM response into structured format"""
    try:
        # Try to parse as JSON first
        return json.loads(response_text)
    except:
        # Fallback to text parsing
        result = {
            "match_score": 0,
            "skills_match": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "improvements": [],
            "ats_score": 0,
            "summary": ""
        }
        
        # Extract score
        score_match = re.search(r'(\d+)%', response_text)
        if score_match:
            result["match_score"] = int(score_match.group(1))
        
        # Extract sections
        sections = {
            "skills_match": ["skills match", "matching skills", "matched skills"],
            "missing_skills": ["missing skills", "gaps", "needs improvement"],
            "strengths": ["strengths", "strong points"],
            "weaknesses": ["weaknesses", "areas to improve"],
            "improvements": ["suggestions", "recommendations", "improvements"]
        }
        
        for key, patterns in sections.items():
            for pattern in patterns:
                pattern_match = re.search(
                    f"{pattern}:(.*?)(?=\n\n|\Z)", 
                    response_text, 
                    re.IGNORECASE | re.DOTALL
                )
                if pattern_match:
                    items = pattern_match.group(1).strip().split('\n')
                    result[key] = [item.strip(' -•') for item in items if item.strip()]
                    break
        
        return result
