import os
import PyPDF2
import pdfplumber
from docx import Document
from utils import clean_text

class ResumeParser:
    """Parse resumes from various formats"""
    
    @staticmethod
    def parse_pdf(file_path):
        """Extract text from PDF using multiple methods"""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                if text.strip():
                    return clean_text(text)
        except:
            pass
        
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return clean_text(text)
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def parse_docx(file_path):
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return clean_text(text)
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    @staticmethod
    def parse_text(file_path):
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return clean_text(file.read())
        except Exception as e:
            raise Exception(f"Error parsing TXT: {str(e)}")
    
    @staticmethod
    def parse_resume(file_path):
        """Parse resume based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return ResumeParser.parse_pdf(file_path)
        elif ext == '.docx':
            return ResumeParser.parse_docx(file_path)
        elif ext == '.txt':
            return ResumeParser.parse_text(file_path)
        else:
            raise Exception(f"Unsupported file format: {ext}")