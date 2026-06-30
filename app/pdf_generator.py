from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFReportGenerator:
    """Generate professional PDF reports of resume analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.add_custom_styles()
    
    def add_custom_styles(self):
        """Add custom styles for the report"""
        self.styles.add(ParagraphStyle(
            name='Heading1',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=12,
            textColor=colors.HexColor('#1a237e')
        ))
        self.styles.add(ParagraphStyle(
            name='Heading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=8,
            textColor=colors.HexColor('#0d47a1')
        ))
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leading=14
        ))
        self.styles.add(ParagraphStyle(
            name='ScoreStyle',
            parent=self.styles['Normal'],
            fontSize=18,
            textColor=colors.HexColor('#2e7d32'),
            alignment=1
        ))
    
    def generate_report(self, analysis_data, filename="resume_analysis_report.pdf"):
        """Generate a PDF report"""
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Title
        story.append(Paragraph("AI Resume Analysis Report", self.styles['Heading1']))
        story.append(Spacer(1, 0.25*inch))
        
        # Date
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.25*inch))
        
        # Candidate Info
        story.append(Paragraph(f"Candidate: {analysis_data.get('name', 'N/A')}", self.styles['Heading2']))
        story.append(Paragraph(f"Role: {analysis_data.get('job_role', 'N/A')}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.25*inch))
        
        # Scores Table
        scores_data = [
            ['Metric', 'Score'],
            ['Match Score', f"{analysis_data.get('match_score', 0)}%"],
            ['ATS Score', f"{analysis_data.get('ats_score', 0)}%"],
            ['Keyword Match', f"{analysis_data.get('keyword_match', 0)}%"]
        ]
        
        table = Table(scores_data, colWidths=[2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 0.25*inch))
        
        # Strengths
        story.append(Paragraph("Strengths", self.styles['Heading2']))
        for strength in analysis_data.get('strengths', [])[:5]:
            story.append(Paragraph(f"• {strength}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.25*inch))
        
        # Missing Skills
        story.append(Paragraph("Missing Skills", self.styles['Heading2']))
        for skill in analysis_data.get('missing_skills', [])[:5]:
            story.append(Paragraph(f"• {skill}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.25*inch))
        
        # Improvements
        story.append(Paragraph("Improvement Suggestions", self.styles['Heading2']))
        for improvement in analysis_data.get('improvements', [])[:3]:
            story.append(Paragraph(f"• {improvement}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.25*inch))
        
        # Summary
        story.append(Paragraph("Summary", self.styles['Heading2']))
        story.append(Paragraph(analysis_data.get('summary', 'N/A'), self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        return filename