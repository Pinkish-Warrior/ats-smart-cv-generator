from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from typing import Dict, List
import os
import uuid
from datetime import datetime

class CVGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for CV"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='CVHeader',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2563eb'),
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f2937'),
            borderWidth=1,
            borderColor=colors.HexColor('#e5e7eb'),
            borderPadding=6,
            spaceBefore=12,
            spaceAfter=6
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica-Bold',
            spaceBefore=6,
            spaceAfter=2
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#6b7280'),
            fontName='Helvetica-Oblique',
            spaceAfter=4
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CVBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ))

    def generate_cv(self, user_data: Dict, job_analysis: Dict = None) -> str:
        """Generate ATS-optimized CV and return file path"""
        # Create unique filename
        cv_id = str(uuid.uuid4())
        filename = f"cv_{cv_id}.pdf"
        filepath = os.path.join('/tmp', filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build CV content
        story = []
        story.extend(self._build_header(user_data))
        story.extend(self._build_professional_summary(user_data, job_analysis))
        story.extend(self._build_experience_section(user_data, job_analysis))
        story.extend(self._build_education_section(user_data))
        story.extend(self._build_skills_section(user_data, job_analysis))
        
        # Build PDF
        doc.build(story)
        
        return filepath

    def _build_header(self, user_data: Dict) -> List:
        """Build CV header with name and contact info"""
        story = []
        
        # Name
        name = user_data.get('personal_info', {}).get('full_name', 'Your Name')
        story.append(Paragraph(name, self.styles['CVHeader']))
        
        # Contact information
        contact_info = user_data.get('personal_info', {})
        contact_parts = []
        
        if contact_info.get('email'):
            contact_parts.append(contact_info['email'])
        if contact_info.get('phone'):
            contact_parts.append(contact_info['phone'])
        if contact_info.get('location'):
            contact_parts.append(contact_info['location'])
        if contact_info.get('linkedin'):
            contact_parts.append(f"LinkedIn: {contact_info['linkedin']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 12))
        return story

    def _build_professional_summary(self, user_data: Dict, job_analysis: Dict = None) -> List:
        """Build professional summary section"""
        story = []
        
        summary = user_data.get('professional_summary', '')
        if summary:
            story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader']))
            
            # Optimize summary based on job analysis
            if job_analysis:
                summary = self._optimize_summary(summary, job_analysis)
            
            story.append(Paragraph(summary, self.styles['CVBodyText']))
            story.append(Spacer(1, 12))
        
        return story

    def _build_experience_section(self, user_data: Dict, job_analysis: Dict = None) -> List:
        """Build work experience section"""
        story = []
        
        experiences = user_data.get('work_experience', [])
        if experiences:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader']))
            
            for exp in experiences:
                # Job title and company
                job_title = exp.get('job_title', '')
                company = exp.get('company', '')
                dates = f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}"
                
                story.append(Paragraph(f"{job_title}", self.styles['JobTitle']))
                story.append(Paragraph(f"{company} | {dates}", self.styles['Company']))
                
                # Job description/achievements
                description = exp.get('description', '')
                if description:
                    # Optimize description based on job analysis
                    if job_analysis:
                        description = self._optimize_experience_description(description, job_analysis)
                    
                    # Split into bullet points if not already
                    if not description.startswith('•'):
                        bullets = description.split('\n')
                        description = '\n'.join([f"• {bullet.strip()}" for bullet in bullets if bullet.strip()])
                    
                    story.append(Paragraph(description, self.styles['CVBodyText']))
                
                story.append(Spacer(1, 8))
        
        return story

    def _build_education_section(self, user_data: Dict) -> List:
        """Build education section"""
        story = []
        
        education = user_data.get('education', [])
        if education:
            story.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
            
            for edu in education:
                degree = edu.get('degree', '')
                school = edu.get('school', '')
                graduation_date = edu.get('graduation_date', '')
                gpa = edu.get('gpa', '')
                
                degree_line = degree
                if graduation_date:
                    degree_line += f" | {graduation_date}"
                if gpa:
                    degree_line += f" | GPA: {gpa}"
                
                story.append(Paragraph(degree_line, self.styles['JobTitle']))
                story.append(Paragraph(school, self.styles['Company']))
                story.append(Spacer(1, 6))
        
        return story

    def _build_skills_section(self, user_data: Dict, job_analysis: Dict = None) -> List:
        """Build skills section"""
        story = []
        
        skills = user_data.get('skills', {})
        if skills:
            story.append(Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader']))
            
            # Organize skills by category
            skill_categories = []
            
            if skills.get('technical_skills'):
                technical = skills['technical_skills']
                if job_analysis:
                    # Prioritize skills mentioned in job description
                    job_skills = job_analysis.get('technical_skills', [])
                    technical = self._prioritize_skills(technical, job_skills)
                skill_categories.append(f"<b>Technical:</b> {', '.join(technical)}")
            
            if skills.get('soft_skills'):
                soft = skills['soft_skills']
                if job_analysis:
                    # Prioritize soft skills mentioned in job description
                    job_soft_skills = job_analysis.get('soft_skills', [])
                    soft = self._prioritize_skills(soft, job_soft_skills)
                skill_categories.append(f"<b>Soft Skills:</b> {', '.join(soft)}")
            
            if skills.get('languages'):
                languages = skills['languages']
                skill_categories.append(f"<b>Languages:</b> {', '.join(languages)}")
            
            if skills.get('certifications'):
                certs = skills['certifications']
                skill_categories.append(f"<b>Certifications:</b> {', '.join(certs)}")
            
            for category in skill_categories:
                story.append(Paragraph(category, self.styles['CVBodyText']))
                story.append(Spacer(1, 4))
        
        return story

    def _optimize_summary(self, summary: str, job_analysis: Dict) -> str:
        """Optimize professional summary based on job analysis"""
        keywords = job_analysis.get('keywords', [])
        technical_skills = job_analysis.get('technical_skills', [])
        
        # This is a simplified optimization - in a real application,
        # you might use more sophisticated NLP techniques
        optimized_summary = summary
        
        # Add relevant keywords naturally (this is a basic implementation)
        # In practice, you'd want more sophisticated text generation
        
        return optimized_summary

    def _optimize_experience_description(self, description: str, job_analysis: Dict) -> str:
        """Optimize experience description based on job analysis"""
        # This is a placeholder for more sophisticated optimization
        # In practice, you might use NLP to rewrite descriptions to better match job requirements
        return description

    def _prioritize_skills(self, user_skills: List[str], job_skills: List[str]) -> List[str]:
        """Prioritize skills that match job requirements"""
        # Convert to lowercase for comparison
        job_skills_lower = [skill.lower() for skill in job_skills]
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        # Separate matching and non-matching skills
        matching_skills = []
        other_skills = []
        
        for skill in user_skills:
            if skill.lower() in job_skills_lower:
                matching_skills.append(skill)
            else:
                other_skills.append(skill)
        
        # Return matching skills first, then others
        return matching_skills + other_skills

    def get_cv_templates(self) -> List[Dict]:
        """Return available CV templates"""
        return [
            {
                'id': 'professional',
                'name': 'Professional',
                'description': 'Clean, ATS-friendly template suitable for most industries'
            },
            {
                'id': 'modern',
                'name': 'Modern',
                'description': 'Contemporary design with subtle styling'
            },
            {
                'id': 'minimal',
                'name': 'Minimal',
                'description': 'Ultra-clean template focused on content'
            }
        ]

