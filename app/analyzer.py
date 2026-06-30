import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import json
import re
from utils import parse_analysis_response

load_dotenv()

class ResumeAnalyzer:
    """Analyze resumes using Groq LLM"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",  # <-- EXACTLY THIS
            api_key=self.api_key,
            temperature=0.3,
            max_tokens=4096
        )
    
    def analyze_resume(self, resume_text, job_description, job_role):
        """Analyze resume against job description"""
        
        prompt_template = PromptTemplate(
            input_variables=["resume", "job_description", "job_role"],
            template="""
            You are an expert HR recruiter and career coach. Analyze this resume for a {job_role} position.
            
            **Resume Content:**
            {resume}
            
            **Job Description:**
            {job_description}
            
            Please provide a comprehensive analysis in the following JSON format:
            
            {{
                "match_score": <score between 0-100>,
                "skills_match": ["list of matching skills found"],
                "missing_skills": ["list of skills missing from resume"],
                "strengths": ["key strengths of the candidate"],
                "weaknesses": ["areas needing improvement"],
                "improvements": ["specific suggestions to improve resume"],
                "ats_score": <ATS compatibility score 0-100>,
                "summary": "Brief overall assessment of candidate fit"
            }}
            
            Be specific and actionable. Base scores on objective criteria.
            """
        )
        
        # Create the chain using the new syntax
        chain = prompt_template | self.llm
        
        try:
            result = chain.invoke({
                "resume": resume_text[:5000],
                "job_description": job_description[:5000],
                "job_role": job_role
            })
            
            # Extract content from the result
            result_text = result.content if hasattr(result, 'content') else str(result)
            
            try:
                if "```json" in result_text:
                    json_str = result_text.split("```json")[1].split("```")[0]
                elif "```" in result_text:
                    json_str = result_text.split("```")[1].split("```")[0]
                else:
                    json_str = result_text
                
                analysis = json.loads(json_str.strip())
                return analysis
            except:
                return parse_analysis_response(result_text)
        except Exception as e:
            raise Exception(f"LLM analysis failed: {str(e)}")
