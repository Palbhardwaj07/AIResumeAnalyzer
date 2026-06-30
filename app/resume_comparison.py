from resume_parser import ResumeParser
from analyzer import ResumeAnalyzer
from utils import extract_name
import tempfile
import os

class ResumeComparison:
    """Compare two resumes side by side"""
    
    def __init__(self):
        self.parser = ResumeParser()
        self.analyzer = ResumeAnalyzer()
    
    def compare_resumes(self, resume1_path, resume2_path, job_description, job_role):
        """Compare two resumes"""
        
        # Parse both resumes
        text1 = self.parser.parse_resume(resume1_path)
        text2 = self.parser.parse_resume(resume2_path)
        
        # Analyze both
        results1 = self.analyzer.analyze_resume(text1, job_description, job_role)
        results2 = self.analyzer.analyze_resume(text2, job_description, job_role)
        
        # Extract names
        name1 = extract_name(text1) or "Resume 1"
        name2 = extract_name(text2) or "Resume 2"
        
        # Comparison data
        comparison = {
            'resume1': {
                'name': name1,
                'match_score': results1.get('match_score', 0),
                'ats_score': results1.get('ats_score', 0),
                'strengths': results1.get('strengths', [])[:3],
                'missing_skills': results1.get('missing_skills', [])[:3],
                'skills_match': results1.get('skills_match', [])
            },
            'resume2': {
                'name': name2,
                'match_score': results2.get('match_score', 0),
                'ats_score': results2.get('ats_score', 0),
                'strengths': results2.get('strengths', [])[:3],
                'missing_skills': results2.get('missing_skills', [])[:3],
                'skills_match': results2.get('skills_match', [])
            },
            'winner': 'Resume 1' if results1.get('match_score', 0) > results2.get('match_score', 0) else 'Resume 2',
            'winner_score': max(results1.get('match_score', 0), results2.get('match_score', 0)),
            'score_difference': abs(results1.get('match_score', 0) - results2.get('match_score', 0))
        }
        
        return comparison
    
    def display_comparison(self, comparison):
        """Format comparison for display"""
        
        output = []
        output.append("=" * 60)
        output.append("RESUME COMPARISON REPORT")
        output.append("=" * 60)
        
        # Winner
        output.append(f"\n🏆 WINNER: {comparison['winner']} by {comparison['score_difference']}%")
        
        # Resume 1
        output.append("\n" + "=" * 30)
        output.append(f"📄 RESUME 1: {comparison['resume1']['name']}")
        output.append("=" * 30)
        output.append(f"Match Score: {comparison['resume1']['match_score']}%")
        output.append(f"ATS Score: {comparison['resume1']['ats_score']}%")
        output.append("\nStrengths:")
        for s in comparison['resume1']['strengths']:
            output.append(f"  • {s}")
        output.append("\nMissing Skills:")
        for s in comparison['resume1']['missing_skills']:
            output.append(f"  • {s}")
        
        # Resume 2
        output.append("\n" + "=" * 30)
        output.append(f"📄 RESUME 2: {comparison['resume2']['name']}")
        output.append("=" * 30)
        output.append(f"Match Score: {comparison['resume2']['match_score']}%")
        output.append(f"ATS Score: {comparison['resume2']['ats_score']}%")
        output.append("\nStrengths:")
        for s in comparison['resume2']['strengths']:
            output.append(f"  • {s}")
        output.append("\nMissing Skills:")
        for s in comparison['resume2']['missing_skills']:
            output.append(f"  • {s}")
        
        output.append("\n" + "=" * 60)
        output.append("END OF COMPARISON")
        output.append("=" * 60)
        
        return "\n".join(output)