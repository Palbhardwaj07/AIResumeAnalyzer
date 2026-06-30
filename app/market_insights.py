from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class MarketInsights:
    """Get job market insights and trends"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.api_key,
            temperature=0.3,
            max_tokens=4096
        )
    
    def get_market_trends(self, job_role, location="Global"):
        """Get current market trends for a role"""
        
        prompt = PromptTemplate(
            input_variables=["job_role", "location"],
            template="""
            Provide current market insights for {job_role} in {location}.
            
            Include:
            1. **Demand Level:** (High/Medium/Low) and why
            2. **Growth Rate:** (Projected growth %)
            3. **Top Skills in Demand:** (List with explanations)
            4. **Salary Trends:** (Current average and expected growth)
            5. **Remote Work:** (Percentage of remote opportunities)
            6. **Top Industries:** (Industries hiring most)
            7. **Emerging Skills:** (Skills becoming important)
            8. **Certifications:** (Most valuable certifications)
            
            Format with clear sections.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "job_role": job_role,
                "location": location
            })
            
            insights = result.content if hasattr(result, 'content') else str(result)
            return insights
        except Exception as e:
            return f"Error getting market insights: {str(e)}"
    
    def get_company_insights(self, company_name):
        """Get insights about a specific company"""
        
        prompt = PromptTemplate(
            input_variables=["company_name"],
            template="""
            Provide insights about {company_name} as an employer.
            
            Include:
            1. **Company Culture:** (Describe culture and values)
            2. **Interview Process:** (Typical process)
            3. **Employee Reviews:** (Common pros and cons)
            4. **Tech Stack:** (If tech company)
            5. **Perks & Benefits:** (What they offer)
            6. **Career Growth:** (Opportunities for advancement)
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({"company_name": company_name})
            insights = result.content if hasattr(result, 'content') else str(result)
            return insights
        except Exception as e:
            return f"Error getting company insights: {str(e)}"