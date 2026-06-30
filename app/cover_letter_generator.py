from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class CoverLetterGenerator:
    """Generate professional cover letters"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.api_key,
            temperature=0.4,
            max_tokens=4096
        )
    
    def generate_cover_letter(self, resume_text, job_description, job_role, company_name=""):
        """Generate a cover letter"""
        
        prompt = PromptTemplate(
            input_variables=["resume", "job_description", "job_role", "company_name"],
            template="""
            Write a professional cover letter for a {job_role} position at {company_name}.
            
            **Candidate Background:**
            {resume}
            
            **Job Requirements:**
            {job_description}
            
            **Guidelines:**
            1. Professional and enthusiastic tone
            2. Highlight relevant experience
            3. Connect skills to job requirements
            4. Express interest in the company
            5. Show enthusiasm for the role
            6. Include a call to action
            7. Keep it to 3-4 paragraphs
            
            **Format:**
            - Professional header with contact info
            - Salutation
            - 3-4 paragraphs of content
            - Closing
            - Signature
            
            Provide ONLY the complete cover letter.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "resume": resume_text[:3000],
                "job_description": job_description[:3000],
                "job_role": job_role,
                "company_name": company_name or "Your Company"
            })
            
            cover_letter = result.content if hasattr(result, 'content') else str(result)
            return cover_letter
        except Exception as e:
            return f"Error generating cover letter: {str(e)}"