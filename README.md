# AI Resume Analyzer

An intelligent resume analysis tool powered by Groq's LLaMA3 and LangChain.

## Features

- 📄 Parse PDF, DOCX, and TXT resumes
- 🎯 Match against job descriptions
- 📊 Generate match scores (0-100%)
- 💡 Identify skill gaps and strengths
- 📚 Create personalized learning roadmaps
- 📈 Visualize skill profiles
- 🤖 ATS compatibility checking

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq (LLaMA3-70B)
- **Framework**: LangChain
- **Parsing**: PyPDF2, python-docx, pdfplumber
- **Visualization**: Plotly, Pandas
- **Language**: Python 3.9+

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ai-resume-analyzer
cd ai-resume-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY