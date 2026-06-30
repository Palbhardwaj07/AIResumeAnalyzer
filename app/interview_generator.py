from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class InterviewGenerator:
    """Generate interview questions based on resume and job description"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.api_key,
            temperature=0.5,
            max_tokens=4096
        )
    
    def generate_questions(self, resume_text, job_description, job_role):
        """Generate interview questions"""
        
        prompt = PromptTemplate(
            input_variables=["resume", "job_description", "job_role"],
            template="""
            Based on the following resume and job description, generate 15 interview questions.
            
            **Resume:**
            {resume}
            
            **Job Description:**
            {job_description}
            
            **Role:** {job_role}
            
            Generate questions in these categories:
            
            1. **Technical Questions (4 questions)** - Based on required skills from the job description
            2. **Behavioral Questions (4 questions)** - STAR format questions about past experiences
            3. **Problem-Solving Questions (3 questions)** - Scenario-based questions
            4. **Culture-Fit Questions (2 questions)** - Company culture and values
            5. **Role-Specific Questions (2 questions)** - Based on the specific job role
            
            Format each question clearly with its category.
            Make questions specific, challenging, and relevant to the role.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "resume": resume_text[:3000],
                "job_description": job_description[:3000],
                "job_role": job_role
            })
            
            questions = result.content if hasattr(result, 'content') else str(result)
            return questions
        except Exception as e:
            return f"Error generating questions: {str(e)}"