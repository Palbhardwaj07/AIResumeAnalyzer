from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class CareerPathGenerator:
    """Generate career path recommendations"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            api_key=self.api_key,
            temperature=0.4,
            max_tokens=4096
        )
    
    def suggest_career_path(self, skills, experience, education, job_role, interests=""):
        """Suggest career paths"""
        
        prompt = PromptTemplate(
            input_variables=["skills", "experience", "education", "job_role", "interests"],
            template="""
            Based on the following profile, suggest a detailed career path:
            
            **Current Role:** {job_role}
            **Skills:** {skills}
            **Experience:** {experience}
            **Education:** {education}
            **Interests:** {interests}
            
            Provide a comprehensive career roadmap:
            
            1. **Short-Term (1-2 years):**
               - Immediate next roles to target
               - Skills to develop
               - Certifications to pursue
               - Projects to build
            
            2. **Mid-Term (3-5 years):**
               - Career trajectory
               - Leadership opportunities
               - Specialization options
               - Industry transitions if applicable
            
            3. **Long-Term (5-10 years):**
               - Senior leadership roles
               - Entrepreneurship options
               - Consulting opportunities
               - Industry influence potential
            
            4. **Alternative Paths:**
               - Different industries to consider
               - Related roles to explore
               - Adjacent career opportunities
            
            5. **Action Plan:**
               - Step-by-step guide
               - Timeline for each milestone
               - Resources needed
            
            Be realistic, specific, and actionable.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "skills": skills[:1000],
                "experience": experience,
                "education": education,
                "job_role": job_role,
                "interests": interests or "Not specified"
            })
            
            career_path = result.content if hasattr(result, 'content') else str(result)
            return career_path
        except Exception as e:
            return f"Error generating career path: {str(e)}"