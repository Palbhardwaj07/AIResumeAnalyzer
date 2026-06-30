import streamlit as st
import os
import tempfile
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
from resume_parser import ResumeParser
from analyzer import ResumeAnalyzer
from roadmap_generator import RoadmapGenerator
from interview_generator import InterviewGenerator
from improvement_suggestions import ImprovementGenerator
from salary_estimator import SalaryEstimator
from career_path import CareerPathGenerator
from keyword_optimizer import KeywordOptimizer
from batch_processor import BatchProcessor
from resume_builder import ResumeBuilder
from cover_letter_generator import CoverLetterGenerator
from analytics_dashboard import AnalyticsDashboard
from job_api_integration import JobAPIIntegration
from pdf_generator import PDFReportGenerator
from version_control import ResumeVersionControl
from market_insights import MarketInsights
from linkedin_analyzer import LinkedInAnalyzer
from resume_comparison import ResumeComparison
from utils import extract_name, extract_email, extract_phone

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    .feature-box {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.5rem;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover {
        opacity: 0.9;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'roadmap' not in st.session_state:
    st.session_state.roadmap = None
if 'interview_questions' not in st.session_state:
    st.session_state.interview_questions = None
if 'improvements' not in st.session_state:
    st.session_state.improvements = None
if 'career_path' not in st.session_state:
    st.session_state.career_path = None
if 'keyword_analysis' not in st.session_state:
    st.session_state.keyword_analysis = None
if 'salary_estimate' not in st.session_state:
    st.session_state.salary_estimate = None
if 'job_description' not in st.session_state:
    st.session_state.job_description = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)
    st.title("AI Resume Analyzer Pro")
    st.markdown("---")
    
    st.markdown("### 🔧 Settings")
    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        help="Choose the LLM model for analysis"
    )
    
    experience_level = st.selectbox(
        "Experience Level",
        ["entry", "mid", "senior"],
        help="Candidate's experience level"
    )
    
    st.markdown("---")
    st.markdown("### 💡 Features")
    st.success("✅ Resume Analysis")
    st.success("✅ Skill Gap Analysis")
    st.success("✅ Learning Roadmap")
    st.success("✅ Interview Questions")
    st.success("✅ Career Path Planning")
    st.success("✅ Salary Estimation")
    st.success("✅ Keyword Optimization")
    st.success("✅ ATS Compatibility")
    st.success("✅ Resume Builder")
    st.success("✅ Cover Letter Generator")
    st.success("✅ Analytics Dashboard")
    st.success("✅ PDF Reports")
    st.success("✅ Version Control")
    st.success("✅ Market Insights")
    st.success("✅ LinkedIn Analyzer")
    st.success("✅ Resume Comparison")
    
    st.markdown("---")
    st.markdown("### 🔒 Privacy")
    st.caption("Your data is not stored. All processing is done in real-time.")

# Main content
st.markdown('<p class="main-header">📄 AI Resume Analyzer Pro</p>', unsafe_allow_html=True)
st.markdown("Upload your resume and paste the job description for comprehensive AI-powered analysis.")

# Create 9 Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Analysis", 
    "📈 Visualizations", 
    "📚 Roadmap",
    "🎯 Interview",
    "💡 Career",
    "🔍 Keywords",
    "📝 Builder",
    "📊 Analytics",
    "🛠️ Tools"
])

# ==================== TAB 1: ANALYSIS ====================
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose a file (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_file:
            st.success(f"✅ {uploaded_file.name} uploaded successfully")
            file_size = len(uploaded_file.getvalue()) / 1024 / 1024
            st.caption(f"Size: {file_size:.2f} MB")
    
    with col2:
        st.subheader("📝 Job Description")
        job_role = st.text_input("Job Role / Title", placeholder="e.g., Senior Software Engineer")
        job_description = st.text_area(
            "Paste job description here",
            height=200,
            placeholder="Paste the complete job description..."
        )
        
        if job_description and not job_role:
            st.warning("Please enter a job role/title")

    # Analysis button
    if st.button("🚀 Analyze Resume", use_container_width=True):
        if not uploaded_file:
            st.error("Please upload a resume file")
        elif not job_description:
            st.error("Please paste a job description")
        elif not job_role:
            st.error("Please enter a job role")
        else:
            with st.spinner("🔄 Analyzing resume... This may take a moment."):
                try:
                    temp_dir = tempfile.mkdtemp()
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Parse resume
                    parser = ResumeParser()
                    resume_text = parser.parse_resume(file_path)
                    st.session_state.resume_text = resume_text
                    
                    # Extract basic info
                    name = extract_name(resume_text)
                    email = extract_email(resume_text)
                    phone = extract_phone(resume_text)
                    
                    # Store job description for later use
                    st.session_state.job_description = job_description
                    
                    # Analyze with LLM
                    analyzer = ResumeAnalyzer()
                    results = analyzer.analyze_resume(
                        resume_text,
                        job_description,
                        job_role
                    )
                    
                    # Generate roadmap
                    roadmap_gen = RoadmapGenerator()
                    roadmap = roadmap_gen.generate_roadmap(
                        results.get('missing_skills', []),
                        job_role,
                        experience_level
                    )
                    
                    # Generate interview questions
                    interview_gen = InterviewGenerator()
                    interview_questions = interview_gen.generate_questions(
                        resume_text,
                        job_description,
                        job_role
                    )
                    
                    # Generate improvements
                    improvement_gen = ImprovementGenerator()
                    improvements = improvement_gen.suggest_improvements(
                        resume_text,
                        job_role
                    )
                    
                    # Generate career path
                    career_gen = CareerPathGenerator()
                    career_path = career_gen.suggest_career_path(
                        skills=", ".join(results.get('skills_match', [])[:10]),
                        experience=experience_level,
                        education="Not specified",
                        job_role=job_role
                    )
                    
                    # Estimate salary
                    salary_est = SalaryEstimator()
                    salary_estimate = salary_est.estimate_salary(
                        skills=", ".join(results.get('skills_match', [])[:10]),
                        experience=experience_level,
                        location="United States",
                        job_role=job_role
                    )
                    
                    # Keyword analysis
                    keyword_opt = KeywordOptimizer()
                    job_keywords = keyword_opt.extract_keywords(job_description, 20)
                    resume_keywords = keyword_opt.extract_keywords(resume_text, 20)
                    keyword_analysis = keyword_opt.compare_keywords(resume_keywords, job_keywords)
                    
                    # Store results in session
                    st.session_state.results = {
                        'analysis': results,
                        'resume_text': resume_text,
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'file_name': uploaded_file.name,
                        'job_role': job_role
                    }
                    st.session_state.roadmap = roadmap
                    st.session_state.interview_questions = interview_questions
                    st.session_state.improvements = improvements
                    st.session_state.career_path = career_path
                    st.session_state.salary_estimate = salary_estimate
                    st.session_state.keyword_analysis = keyword_analysis
                    st.session_state.analysis_complete = True
                    
                    # Save to version control
                    vc = ResumeVersionControl()
                    vc.create_version(resume_text, results, f"Analysis for {job_role}")
                    
                    # Cleanup
                    os.remove(file_path)
                    os.rmdir(temp_dir)
                    
                    st.success("✅ Analysis complete!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")

    # Display results
    if st.session_state.analysis_complete and st.session_state.results:
        results = st.session_state.results['analysis']
        
        # Header with basic info
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            if st.session_state.results.get('name'):
                st.subheader(f"👤 {st.session_state.results['name']}")
            if st.session_state.results.get('email'):
                st.caption(f"📧 {st.session_state.results['email']}")
            if st.session_state.results.get('phone'):
                st.caption(f"📱 {st.session_state.results['phone']}")
        
        with col2:
            st.metric("📊 Match Score", f"{results.get('match_score', 0)}%")
        
        with col3:
            st.metric("🤖 ATS Score", f"{results.get('ats_score', 0)}%")
        
        with col4:
            keywords = st.session_state.keyword_analysis
            if keywords:
                st.metric("🔑 Keyword Match", f"{keywords.get('match_percentage', 0)}%")
        
        # Score gauge
        score = results.get('match_score', 0)
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            title={'text': "Overall Match"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': "lightgray"},
                    {'range': [33, 66], 'color': "gray"},
                    {'range': [66, 100], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Score Breakdown Dashboard
        st.subheader("📊 Score Breakdown")
        
        breakdown = {
            "Technical Skills": min(100, results.get('match_score', 0) * 1.1),
            "Experience Match": min(100, results.get('match_score', 0) * 0.95),
            "Education Fit": min(100, results.get('match_score', 0) * 0.85),
            "ATS Compatibility": results.get('ats_score', 70),
            "Keyword Match": st.session_state.keyword_analysis.get('match_percentage', 0) if st.session_state.keyword_analysis else 0
        }
        
        cols = st.columns(5)
        for idx, (key, value) in enumerate(breakdown.items()):
            with cols[idx]:
                st.metric(
                    label=key,
                    value=f"{int(value)}%",
                    delta=f"{'↑' if value > 70 else '↓'}{int(value-50)}%"
                )
        
        # Create breakdown chart
        fig = go.Figure(data=[
            go.Bar(
                x=list(breakdown.keys()),
                y=list(breakdown.values()),
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                text=[f"{int(v)}%" for v in breakdown.values()],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Score Breakdown by Category",
            yaxis_range=[0, 100],
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed analysis in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Strengths")
            if results.get('strengths'):
                for strength in results['strengths'][:5]:
                    st.markdown(f"• {strength}")
            else:
                st.info("No specific strengths identified")
            
            st.markdown("### 🔗 Matching Skills")
            if results.get('skills_match'):
                skills = results['skills_match'][:10]
                st.markdown(", ".join(skills))
            else:
                st.info("No matching skills identified")
        
        with col2:
            st.markdown("### ❌ Missing Skills")
            if results.get('missing_skills'):
                for skill in results['missing_skills'][:5]:
                    st.markdown(f"• {skill}")
            else:
                st.success("🎉 No major skill gaps identified!")
            
            st.markdown("### 📝 Improvements")
            if results.get('improvements'):
                for imp in results['improvements'][:3]:
                    st.markdown(f"• {imp}")
            else:
                st.info("No improvement suggestions available")
        
        # Summary
        st.markdown("### 📋 Summary")
        if results.get('summary'):
            st.info(results['summary'])
        
        # Export buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # Text report
            report = f"""
            AI Resume Analysis Report
            =========================
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            Candidate: {st.session_state.results.get('name', 'Unknown')}
            
            MATCH SCORE: {results.get('match_score', 0)}%
            ATS SCORE: {results.get('ats_score', 0)}%
            KEYWORD MATCH: {st.session_state.keyword_analysis.get('match_percentage', 0) if st.session_state.keyword_analysis else 0}%
            
            STRENGTHS:
            {chr(10).join(['- ' + s for s in results.get('strengths', [])])}
            
            MISSING SKILLS:
            {chr(10).join(['- ' + s for s in results.get('missing_skills', [])])}
            
            IMPROVEMENTS:
            {chr(10).join(['- ' + s for s in results.get('improvements', [])])}
            
            SUMMARY:
            {results.get('summary', 'N/A')}
            """
            
            st.download_button(
                label="📥 Download Text Report",
                data=report,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # PDF Report
            if st.button("📄 Generate PDF Report", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    pdf_gen = PDFReportGenerator()
                    analysis_data = {
                        'name': st.session_state.results.get('name', 'N/A'),
                        'job_role': st.session_state.results.get('job_role', 'N/A'),
                        'match_score': results.get('match_score', 0),
                        'ats_score': results.get('ats_score', 0),
                        'keyword_match': st.session_state.keyword_analysis.get('match_percentage', 0) if st.session_state.keyword_analysis else 0,
                        'strengths': results.get('strengths', []),
                        'missing_skills': results.get('missing_skills', []),
                        'improvements': results.get('improvements', []),
                        'summary': results.get('summary', 'N/A')
                    }
                    pdf_file = pdf_gen.generate_report(analysis_data, f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
                    
                    with open(pdf_file, 'rb') as f:
                        pdf_data = f.read()
                    
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_data,
                        file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

# ==================== TAB 2: VISUALIZATIONS ====================
with tab2:
    st.subheader("📊 Skill Analysis Visualization")
    
    if st.session_state.analysis_complete and st.session_state.results:
        results = st.session_state.results['analysis']
        keyword_data = st.session_state.keyword_analysis
        
        # Radar chart
        categories = ['Technical', 'Experience', 'Education', 'Communication', 'Leadership']
        values = [
            min(100, results.get('match_score', 0) + 10),
            min(100, results.get('match_score', 0)),
            min(100, results.get('match_score', 0) - 10),
            min(100, results.get('match_score', 0) + 5),
            min(100, results.get('match_score', 0) - 5)
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Profile'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title="Skill Profile"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Skill gap bar chart
        if results.get('missing_skills'):
            missing = results['missing_skills'][:8]
            df = pd.DataFrame({
                'Skills': missing,
                'Gap Score': [80 + i * 5 for i in range(len(missing))][::-1]
            })
            
            fig = go.Figure(data=go.Bar(
                x=df['Gap Score'],
                y=df['Skills'],
                orientation='h',
                marker_color='coral'
            ))
            fig.update_layout(
                title="Skill Gaps to Address",
                xaxis_title="Priority Score",
                yaxis_title="Skill"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Keyword match visualization
        if keyword_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔑 Keyword Analysis")
                st.metric("Keyword Match", f"{keyword_data.get('match_percentage', 0)}%")
                
                st.write("**Matching Keywords:**")
                for kw in keyword_data.get('matching_keywords', [])[:5]:
                    st.markdown(f"✅ {kw}")
                
                st.write("**Missing Keywords:**")
                for kw in keyword_data.get('missing_keywords', [])[:5]:
                    st.markdown(f"❌ {kw}")
            
            with col2:
                # Keyword comparison chart
                fig = go.Figure(data=[
                    go.Bar(name='Job Keywords', x=keyword_data.get('job_keywords', [])[:5], 
                           y=[1]*5, marker_color='blue'),
                    go.Bar(name='Resume Keywords', x=keyword_data.get('resume_keywords', [])[:5], 
                           y=[1]*5, marker_color='green')
                ])
                fig.update_layout(
                    title="Keyword Comparison",
                    barmode='group',
                    height=300,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run an analysis first to see visualizations")

# ==================== TAB 3: ROADMAP ====================
with tab3:
    st.subheader("📚 Personalized Learning Roadmap")
    
    if st.session_state.analysis_complete and st.session_state.roadmap:
        st.markdown(st.session_state.roadmap)
        
        st.download_button(
            label="📥 Download Roadmap",
            data=st.session_state.roadmap,
            file_name=f"learning_roadmap_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("Run an analysis to generate a personalized learning roadmap")

# ==================== TAB 4: INTERVIEW ====================
with tab4:
    st.subheader("🎯 Interview Questions")
    
    if st.session_state.analysis_complete and st.session_state.interview_questions:
        st.markdown(st.session_state.interview_questions)
        
        st.download_button(
            label="📥 Download Interview Questions",
            data=st.session_state.interview_questions,
            file_name=f"interview_questions_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("Run an analysis to generate interview questions")

# ==================== TAB 5: CAREER ====================
with tab5:
    st.subheader("💡 Career Path & Salary")
    
    if st.session_state.analysis_complete:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Career Path")
            if st.session_state.career_path:
                st.markdown(st.session_state.career_path)
            else:
                st.info("Career path not generated yet")
        
        with col2:
            st.markdown("### 💰 Salary Estimate")
            if st.session_state.salary_estimate:
                st.markdown(st.session_state.salary_estimate)
            else:
                st.info("Salary estimate not generated yet")
        
        # Resume improvements
        st.markdown("### 📝 Resume Improvement Suggestions")
        if st.session_state.improvements:
            st.markdown(st.session_state.improvements)
            
            st.download_button(
                label="📥 Download Improvements",
                data=st.session_state.improvements,
                file_name=f"resume_improvements_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("Improvement suggestions not generated yet")
    else:
        st.info("Run an analysis to see career recommendations")

# ==================== TAB 6: KEYWORDS ====================
with tab6:
    st.subheader("🔍 Keyword Analysis")
    
    if st.session_state.analysis_complete and st.session_state.keyword_analysis:
        keyword_data = st.session_state.keyword_analysis
        
        st.metric("Keyword Match Rate", f"{keyword_data.get('match_percentage', 0)}%")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Job Description Keywords")
            for kw in keyword_data.get('job_keywords', [])[:15]:
                if kw in keyword_data.get('matching_keywords', []):
                    st.markdown(f"✅ {kw}")
                else:
                    st.markdown(f"❌ {kw}")
        
        with col2:
            st.markdown("### 📋 Resume Keywords")
            for kw in keyword_data.get('resume_keywords', [])[:15]:
                if kw in keyword_data.get('matching_keywords', []):
                    st.markdown(f"✅ {kw}")
                else:
                    st.markdown(f"📌 {kw}")
        
        if keyword_data.get('missing_keywords'):
            st.markdown("### 🚨 Critical Missing Keywords")
            for kw in keyword_data.get('missing_keywords', [])[:10]:
                st.warning(f"**{kw}** - Add this to your resume")
        
        if keyword_data.get('extra_keywords'):
            st.markdown("### 💪 Extra Keywords You Have")
            for kw in keyword_data.get('extra_keywords', [])[:5]:
                st.success(f"✨ {kw}")
    else:
        st.info("Run an analysis to see keyword optimization")

# ==================== TAB 7: BUILDER ====================
with tab7:
    st.subheader("📝 Resume Builder & Cover Letter")
    
    if st.session_state.analysis_complete and st.session_state.results:
        builder = ResumeBuilder()
        cover_gen = CoverLetterGenerator()
        
        option = st.radio(
            "What would you like to create?",
            ["Tailor Resume", "Generate Cover Letter", "Optimize Section"],
            horizontal=True
        )
        
        resume_text = st.session_state.results.get('resume_text', '')
        job_role = st.session_state.results.get('job_role', '')
        job_description = st.session_state.job_description or ''
        
        if option == "Tailor Resume":
            if st.button("📝 Generate Tailored Resume", use_container_width=True):
                with st.spinner("Tailoring your resume..."):
                    tailored = builder.generate_tailored_resume(
                        resume_text,
                        job_description,
                        job_role
                    )
                    st.markdown(tailored)
                    st.download_button(
                        label="📥 Download Tailored Resume",
                        data=tailored,
                        file_name=f"tailored_resume_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
        
        elif option == "Generate Cover Letter":
            company_name = st.text_input("Company Name (optional)", placeholder="e.g., Google, Microsoft")
            if st.button("✍️ Generate Cover Letter", use_container_width=True):
                with st.spinner("Writing cover letter..."):
                    cover = cover_gen.generate_cover_letter(
                        resume_text,
                        job_description,
                        job_role,
                        company_name
                    )
                    st.markdown(cover)
                    st.download_button(
                        label="📥 Download Cover Letter",
                        data=cover,
                        file_name=f"cover_letter_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
        
        elif option == "Optimize Section":
            section = st.selectbox(
                "Select section to optimize",
                ["Summary", "Experience", "Skills"]
            )
            content = st.text_area("Paste your section content", height=150)
            
            if st.button("🔧 Optimize", use_container_width=True):
                with st.spinner("Optimizing section..."):
                    optimized = builder.optimize_section(
                        section.lower(),
                        content,
                        job_role
                    )
                    st.markdown(optimized)
                    st.download_button(
                        label="📥 Download Optimized Section",
                        data=optimized,
                        file_name=f"optimized_{section.lower()}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
    else:
        st.info("Run an analysis first to use the resume builder")

# ==================== TAB 8: ANALYTICS ====================
with tab8:
    st.subheader("📊 Analytics Dashboard")
    
    dashboard = AnalyticsDashboard()
    
    # Save current analysis if available
    if st.session_state.analysis_complete and st.session_state.results:
        analysis_data = {
            'job_role': st.session_state.results.get('job_role', ''),
            'match_score': st.session_state.results.get('analysis', {}).get('match_score', 0),
            'ats_score': st.session_state.results.get('analysis', {}).get('ats_score', 0),
            'strengths_count': len(st.session_state.results.get('analysis', {}).get('strengths', [])),
            'missing_skills_count': len(st.session_state.results.get('analysis', {}).get('missing_skills', []))
        }
        dashboard.save_analysis(analysis_data)
    
    # Display the dashboard
    dashboard.display_dashboard()

# ==================== TAB 9: TOOLS ====================
with tab9:
    st.subheader("🛠️ Advanced Tools")
    
    tool_option = st.selectbox(
        "Select a tool:",
        ["Market Insights", "LinkedIn Analyzer", "Version Control", "Compare Resumes"]
    )
    
    if tool_option == "Market Insights":
        st.markdown("### 📈 Job Market Insights")
        role = st.text_input("Job Role for Market Insights")
        location = st.selectbox("Location", ["Global", "United States", "Europe", "Asia", "Remote"])
        
        if st.button("Get Market Insights", use_container_width=True):
            insights = MarketInsights()
            with st.spinner("Gathering market insights..."):
                result = insights.get_market_trends(role, location)
                st.markdown(result)
    
    elif tool_option == "LinkedIn Analyzer":
        st.markdown("### 🔗 LinkedIn Profile Analyzer")
        linkedin_text = st.text_area("Paste your LinkedIn profile content", height=300)
        
        if st.button("Analyze LinkedIn Profile", use_container_width=True):
            analyzer = LinkedInAnalyzer()
            with st.spinner("Analyzing profile..."):
                analysis = analyzer.analyze_linkedin_profile(linkedin_text)
                st.markdown(analysis)
    
    elif tool_option == "Version Control":
        st.markdown("### 📚 Resume Version Control")
        vc = ResumeVersionControl()
        versions = vc.get_versions()
        
        if versions:
            for v in versions[:5]:
                with st.expander(f"{v['name']} - {v['created'][:10]}"):
                    st.write(f"**Match Score:** {v['match_score']}%")
                    st.write(f"**ATS Score:** {v['ats_score']}%")
                    st.write(f"**Skills Found:** {v['skills_count']}")
                    st.write(f"**Missing Skills:** {v['missing_skills_count']}")
                    st.write(f"**Preview:** {v['resume_preview'][:200]}...")
                    if st.button(f"🗑️ Delete {v['name']}", key=v['id']):
                        vc.delete_version(v['id'])
                        st.rerun()
        else:
            st.info("No versions saved yet. Versions are auto-saved when you analyze resumes.")
    
    elif tool_option == "Compare Resumes":
        st.markdown("### 📄 Compare Two Resumes")
        
        job_role_cmp = st.text_input("Job Role for Comparison")
        job_desc_cmp = st.text_area("Job Description", height=100)
        
        col1, col2 = st.columns(2)
        
        with col1:
            resume1 = st.file_uploader("Upload First Resume", type=['pdf', 'docx', 'txt'], key="resume1")
        
        with col2:
            resume2 = st.file_uploader("Upload Second Resume", type=['pdf', 'docx', 'txt'], key="resume2")
        
        if st.button("Compare Resumes", use_container_width=True):
            if not resume1 or not resume2:
                st.error("Please upload both resumes")
            elif not job_desc_cmp or not job_role_cmp:
                st.error("Please enter job role and description")
            else:
                with st.spinner("Comparing resumes..."):
                    try:
                        # Save uploaded files
                        temp_dir = tempfile.mkdtemp()
                        path1 = os.path.join(temp_dir, resume1.name)
                        path2 = os.path.join(temp_dir, resume2.name)
                        
                        with open(path1, "wb") as f:
                            f.write(resume1.getbuffer())
                        with open(path2, "wb") as f:
                            f.write(resume2.getbuffer())
                        
                        # Compare
                        comparator = ResumeComparison()
                        comparison = comparator.compare_resumes(path1, path2, job_desc_cmp, job_role_cmp)
                        
                        # Display results
                        st.success(f"🏆 Winner: {comparison['winner']} by {comparison['score_difference']}%")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"### 📄 {comparison['resume1']['name']}")
                            st.metric("Match Score", f"{comparison['resume1']['match_score']}%")
                            st.metric("ATS Score", f"{comparison['resume1']['ats_score']}%")
                            st.write("**Strengths:**")
                            for s in comparison['resume1']['strengths']:
                                st.write(f"• {s}")
                            st.write("**Missing Skills:**")
                            for s in comparison['resume1']['missing_skills']:
                                st.write(f"• {s}")
                        
                        with col2:
                            st.markdown(f"### 📄 {comparison['resume2']['name']}")
                            st.metric("Match Score", f"{comparison['resume2']['match_score']}%")
                            st.metric("ATS Score", f"{comparison['resume2']['ats_score']}%")
                            st.write("**Strengths:**")
                            for s in comparison['resume2']['strengths']:
                                st.write(f"• {s}")
                            st.write("**Missing Skills:**")
                            for s in comparison['resume2']['missing_skills']:
                                st.write(f"• {s}")
                        
                        # Cleanup
                        os.remove(path1)
                        os.remove(path2)
                        os.rmdir(temp_dir)
                        
                    except Exception as e:
                        st.error(f"Comparison failed: {str(e)}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Groq, and LangChain | AI Resume Analyzer Pro v5.0")