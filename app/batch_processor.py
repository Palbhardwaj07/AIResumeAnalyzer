import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from resume_parser import ResumeParser
from analyzer import ResumeAnalyzer
import pandas as pd
from datetime import datetime

class BatchProcessor:
    """Process multiple resumes at once"""
    
    def __init__(self):
        self.parser = ResumeParser()
        self.analyzer = ResumeAnalyzer()
    
    def process_single_resume(self, file_path, job_description, job_role):
        """Process a single resume"""
        try:
            resume_text = self.parser.parse_resume(file_path)
            results = self.analyzer.analyze_resume(resume_text, job_description, job_role)
            return {
                'file_name': os.path.basename(file_path),
                'match_score': results.get('match_score', 0),
                'ats_score': results.get('ats_score', 0),
                'strengths': len(results.get('strengths', [])),
                'missing_skills': len(results.get('missing_skills', [])),
                'status': 'success'
            }
        except Exception as e:
            return {
                'file_name': os.path.basename(file_path),
                'status': 'failed',
                'error': str(e)
            }
    
    def process_batch(self, file_paths, job_description, job_role, max_workers=4):
        """Process multiple resumes in parallel"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.process_single_resume, path, job_description, job_role): path 
                for path in file_paths
            }
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        return results
    
    def generate_comparison_report(self, results):
        """Generate a comparison report for batch processing"""
        df = pd.DataFrame(results)
        
        # Clean data for display
        if 'error' in df.columns:
            df['error'] = df['error'].fillna('')
        
        # Sort by match score
        if 'match_score' in df.columns:
            df = df.sort_values('match_score', ascending=False)
        
        return df