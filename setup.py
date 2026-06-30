# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-resume-analyzer",
    version="2.0.0",
    author="Your Name",
    description="AI-powered resume analyzer using Groq and LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-resume-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "streamlit>=1.28.0",
        "langchain>=0.1.0",
        "langchain-groq>=0.1.0",
        "pypdf2>=3.0.0",
        "python-docx>=1.1.0",
        "python-dotenv>=1.0.0",
        "pdfplumber>=0.10.0",
        "plotly>=5.18.0",
        "pandas>=2.1.0",
    ],
)