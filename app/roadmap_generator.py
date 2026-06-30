from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

class RoadmapGenerator:
    """Generate learning roadmaps based on skill gaps"""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",  # <-- EXACTLY THIS
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.4,
            max_tokens=4096
        )
    
    def generate_roadmap(self, missing_skills, target_role, experience_level="mid"):
        """Generate a structured learning roadmap"""
        
        if not missing_skills:
            return "No missing skills identified. You're on the right track!"
        
        skills_text = ", ".join(missing_skills[:10])
        
        prompt_template = PromptTemplate(
            input_variables=["skills", "role", "experience"],
            template="""
            You are a senior career coach and technical mentor.
            
            Create a detailed 3-month learning roadmap for a {experience} level professional
            targeting a {role} role who needs to learn: {skills}
            
            Structure your response as:
            
            **MONTH 1: Foundation**
            - Week 1-2: [Specific topics with resources]
            - Week 3-4: [More topics]
            
            **MONTH 2: Advanced Concepts**
            - Week 5-6: [Topics]
            - Week 7-8: [Topics]
            
            **MONTH 3: Hands-on Projects**
            - Week 9-10: [Project suggestions]
            - Week 11-12: [Portfolio building]
            
            **Recommended Resources:**
            - Courses: [List specific courses]
            - Books: [List specific books]
            - Practice Platforms: [Platforms for practice]
            
            **Estimated Time Commitment:**
            [Hours per week recommendation]
            
            Make it specific, actionable, and realistic.
            """
        )
        
        # Create the chain using the new syntax
        chain = prompt_template | self.llm
        
        try:
            result = chain.invoke({
                "skills": skills_text,
                "role": target_role,
                "experience": experience_level
            })
            
            # Extract content from the result
            roadmap = result.content if hasattr(result, 'content') else str(result)
            return roadmap
        except Exception as e:
            return f"Error generating roadmap: {str(e)}"
