from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class ResumeBuilder:
    """Build and customize resume templates"""
    
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
    
    def optimize_section(self, section_type, content, job_role):
        """Optimize a specific section of the resume"""
        
        prompts = {
            'summary': """
                Rewrite this professional summary for a {job_role} position.
                Make it impactful and ATS-friendly.
                
                Current Summary: {content}
                
                Requirements:
                - Start with strong action words
                - Include key skills
                - Show value proposition
                - Keep it to 3-4 sentences
                - Use industry keywords
                
                Provide ONLY the improved summary, no additional text.
            """,
            'experience': """
                Rewrite these experience bullet points for a {job_role} position.
                Use the STAR method (Situation, Task, Action, Result).
                
                Current Experience: {content}
                
                Requirements:
                - Start with action verbs
                - Include quantifiable achievements
                - Focus on results
                - Use industry keywords
                - Each bullet point should be 1-2 lines
                
                Provide ONLY the improved bullet points, no additional text.
            """,
            'skills': """
                Optimize this skills section for a {job_role} position.
                
                Current Skills: {content}
                
                Requirements:
                - Group by category (technical, soft, tools)
                - Prioritize relevant skills
                - Include industry-standard terms
                - Remove outdated or irrelevant skills
                
                Provide ONLY the optimized skills list, no additional text.
            """
        }
        
        prompt_template = PromptTemplate(
            input_variables=["content", "job_role"],
            template=prompts.get(section_type, prompts['summary'])
        )
        
        chain = prompt_template | self.llm
        
        try:
            result = chain.invoke({
                "content": content,
                "job_role": job_role
            })
            
            optimized = result.content if hasattr(result, 'content') else str(result)
            return optimized
        except Exception as e:
            return f"Error optimizing section: {str(e)}"
    
    def generate_tailored_resume(self, resume_text, job_description, job_role):
        """Generate a tailored resume for a specific job"""
        
        prompt = PromptTemplate(
            input_variables=["resume", "job_description", "job_role"],
            template="""
            You are a professional resume writer. Tailor this resume for a {job_role} position.
            
            **Original Resume:**
            {resume}
            
            **Job Description:**
            {job_description}
            
            Create a tailored version that:
            1. Highlights relevant experience
            2. Incorporates keywords from the job description
            3. Reorders skills to match job requirements
            4. Adapts the professional summary
            5. Quantifies achievements where possible
            6. Uses action verbs and STAR method
            
            Provide the complete tailored resume with clear sections.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "resume": resume_text[:4000],
                "job_description": job_description[:3000],
                "job_role": job_role
            })
            
            tailored = result.content if hasattr(result, 'content') else str(result)
            return tailored
        except Exception as e:
            return f"Error tailoring resume: {str(e)}"