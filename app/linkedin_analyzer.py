import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class LinkedInAnalyzer:
    """Analyze LinkedIn profiles and suggest improvements"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.api_key,
            temperature=0.3,
            max_tokens=4096
        )
    
    def extract_profile_info(self, profile_text):
        """Extract key information from LinkedIn profile"""
        
        # Simple extraction patterns
        name = re.search(r'(?:Name|Profile):\s*(.+?)(?:\n|$)', profile_text)
        headline = re.search(r'(?:Headline|Title):\s*(.+?)(?:\n|$)', profile_text)
        experience = re.findall(r'(?:Experience|Work):\s*(.+?)(?:\n|$)', profile_text)
        skills = re.findall(r'(?:Skills|Expertise):\s*(.+?)(?:\n|$)', profile_text)
        
        return {
            'name': name.group(1) if name else "Not found",
            'headline': headline.group(1) if headline else "Not found",
            'experience': experience if experience else [],
            'skills': skills if skills else []
        }
    
    def analyze_linkedin_profile(self, profile_text):
        """Analyze LinkedIn profile and suggest improvements"""
        
        prompt = PromptTemplate(
            input_variables=["profile"],
            template="""
            Analyze this LinkedIn profile and provide specific improvements:
            
            **Profile:**
            {profile}
            
            Provide:
            1. **Profile Summary:** Suggest improvements to make it impactful
            2. **Headline:** Suggest a more compelling headline
            3. **Experience:** How to better describe achievements (use STAR method)
            4. **Skills:** Suggest skills to add or remove
            5. **Keywords:** Keywords to add for better searchability
            6. **Recommendations:** Overall tips to improve profile
            
            Be specific and actionable.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({"profile": profile_text[:4000]})
            analysis = result.content if hasattr(result, 'content') else str(result)
            return analysis
        except Exception as e:
            return f"Error analyzing LinkedIn profile: {str(e)}"