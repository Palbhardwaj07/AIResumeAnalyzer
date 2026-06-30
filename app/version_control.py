import json
import hashlib
from datetime import datetime
import os

class ResumeVersionControl:
    """Track and manage resume versions"""
    
    def __init__(self):
        self.versions_file = "resume_versions.json"
        self.load_versions()
    
    def load_versions(self):
        """Load existing versions"""
        if os.path.exists(self.versions_file):
            with open(self.versions_file, 'r') as f:
                self.versions = json.load(f)
        else:
            self.versions = []
    
    def save_versions(self):
        """Save versions to file"""
        with open(self.versions_file, 'w') as f:
            json.dump(self.versions, f, indent=2, default=str)
    
    def create_version(self, resume_text, analysis_results, version_name=""):
        """Create a new version"""
        version_id = hashlib.md5(resume_text.encode()).hexdigest()[:8]
        
        version = {
            'id': version_id,
            'name': version_name or f"Version {len(self.versions) + 1}",
            'created': datetime.now().isoformat(),
            'resume_preview': resume_text[:500] + "...",
            'match_score': analysis_results.get('match_score', 0),
            'ats_score': analysis_results.get('ats_score', 0),
            'skills_count': len(analysis_results.get('skills_match', [])),
            'missing_skills_count': len(analysis_results.get('missing_skills', []))
        }
        
        self.versions.append(version)
        self.save_versions()
        return version
    
    def get_versions(self):
        """Get all versions"""
        return sorted(self.versions, key=lambda x: x['created'], reverse=True)
    
    def delete_version(self, version_id):
        """Delete a specific version"""
        self.versions = [v for v in self.versions if v['id'] != version_id]
        self.save_versions()
    
    def compare_versions(self, id1, id2):
        """Compare two versions"""
        v1 = next((v for v in self.versions if v['id'] == id1), None)
        v2 = next((v for v in self.versions if v['id'] == id2), None)
        
        if not v1 or not v2:
            return None
        
        return {
            'score_change': v2['match_score'] - v1['match_score'],
            'skills_added': v2['skills_count'] - v1['skills_count'],
            'gaps_filled': v1['missing_skills_count'] - v2['missing_skills_count']
        }