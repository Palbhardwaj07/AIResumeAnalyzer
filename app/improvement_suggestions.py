from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class ImprovementGenerator:
    """Generate specific resume improvement suggestions"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.api_key,
            temperature=0.3,
            max_tokens=4096
        )
    
    def suggest_improvements(self, resume_text, job_role):
        """Suggest specific improvements with examples"""
        
        prompt = PromptTemplate(
            input_variables=["resume", "job_role"],
            template="""
            You are a professional resume writer and career coach. Analyze this resume for a {job_role} position.
            
            **Resume:**
            {resume}
            
            Provide specific, actionable improvement suggestions with examples:
            
            1. **Professional Summary:** 
               - Current version: [extract from resume]
               - Suggested version: [write improved version]
               - Explanation: [why this works better]
            
            2. **Experience Bullet Points:** 
               - Weak example: [extract weak bullet]
               - Improved example: [use STAR method]
               - Explanation: [what makes it better]
            
            3. **Skills Section:**
               - Missing skills to add: [list]
               - Skills to highlight: [list]
               - Skills to reorder: [suggest order]
            
            4. **Achievements:** 
               - How to quantify achievements
               - Examples of metrics to include
            
            5. **Formatting & Layout:**
               - Suggestions for better visual appeal
               - ATS-friendly formatting tips
            
            6. **Keywords for ATS:**
               - Important keywords missing
               - How to naturally incorporate them
            
            Make each suggestion specific and immediately actionable.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "resume": resume_text[:4000],
                "job_role": job_role
            })
            
            suggestions = result.content if hasattr(result, 'content') else str(result)
            return suggestions
        except Exception as e:
            return f"Error generating suggestions: {str(e)}"