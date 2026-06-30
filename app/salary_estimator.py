from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class SalaryEstimator:
    """Estimate salary based on skills, experience, and location"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            api_key=self.api_key,
            temperature=0.3,
            max_tokens=2048
        )
    
    def estimate_salary(self, skills, experience, location, job_role):
        """Estimate salary range"""
        
        prompt = PromptTemplate(
            input_variables=["skills", "experience", "location", "job_role"],
            template="""
            Estimate the salary range for a {job_role} in {location}.
            
            **Skills:** {skills}
            **Years of Experience:** {experience}
            
            Provide a comprehensive salary analysis:
            
            1. **Salary Range:** Minimum and maximum (in USD)
            2. **Average Salary:** Median or average expected
            3. **Factors that Increase Salary:**
               - Specific skills that add value
               - Certifications that boost pay
               - Location premium if applicable
            4. **Comparison to Market:** 
               - How this compares to industry average
               - Percentile in the market
            5. **Negotiation Tips:**
               - What to ask for
               - How to justify higher salary
            
            Format as a clear, structured response.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "skills": skills[:1000],
                "experience": experience,
                "location": location,
                "job_role": job_role
            })
            
            salary_info = result.content if hasattr(result, 'content') else str(result)
            return salary_info
        except Exception as e:
            return f"Error estimating salary: {str(e)}"