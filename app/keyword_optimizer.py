from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class KeywordOptimizer:
    """Extract and optimize keywords from resumes and job descriptions"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            api_key=self.api_key,
            temperature=0.2,
            max_tokens=2048
        )
    
    def extract_keywords(self, text, num_keywords=20):
        """Extract important keywords from text"""
        
        prompt = PromptTemplate(
            input_variables=["text", "num_keywords"],
            template="""
            Extract the {num_keywords} most important keywords from the following text.
            Focus on:
            - Skills and technologies
            - Tools and platforms
            - Qualifications and certifications
            - Industry-specific terminology
            - Soft skills and attributes
            
            **Text:**
            {text}
            
            Return ONLY a comma-separated list of keywords, without any additional text.
            """
        )
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "text": text[:3000],
                "num_keywords": num_keywords
            })
            
            keywords_text = result.content if hasattr(result, 'content') else str(result)
            # Clean up the keywords
            keyword_list = [k.strip() for k in keywords_text.split(',') if k.strip()]
            return keyword_list[:num_keywords]
        except Exception as e:
            return []
    
    def compare_keywords(self, resume_keywords, job_keywords):
        """Compare and analyze keyword matching"""
        
        # Normalize for comparison
        job_keywords_lower = [k.lower() for k in job_keywords]
        resume_keywords_lower = [k.lower() for k in resume_keywords]
        
        # Find matching keywords
        matching = [k for k in job_keywords if k.lower() in resume_keywords_lower]
        
        # Find missing keywords
        missing = [k for k in job_keywords if k.lower() not in resume_keywords_lower]
        
        # Find extra resume keywords
        extra = [k for k in resume_keywords if k.lower() not in job_keywords_lower]
        
        # Calculate match percentage
        match_percentage = (len(matching) / len(job_keywords) * 100) if job_keywords else 0
        
        return {
            "job_keywords": job_keywords[:15],
            "resume_keywords": resume_keywords[:15],
            "matching_keywords": matching[:10],
            "missing_keywords": missing[:10],
            "extra_keywords": extra[:5],
            "match_percentage": round(match_percentage, 1)
        }