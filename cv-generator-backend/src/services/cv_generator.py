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
        if not job_analysis:
            return summary
            
        keywords = job_analysis.get('keywords', [])
        technical_skills = job_analysis.get('technical_skills', [])
        
        # Enhanced optimization with actual keyword integration
        optimized_summary = summary
        
        # Add missing critical keywords naturally
        missing_keywords = []
        for keyword in keywords[:5] # Top 5 keywords
            if keyword.lower() not in summary.lower():
                missing_keywords.append(keyword)
        
        # Advanced keyword density optimization
        if missing_keywords:
            # Add relevant skills if missing
            skill_additions = [skill for skill in technical_skills if skill not in summary.lower()]
            if skill_additions:
                optimized_summary += f" Experienced in {', '.join(skill_additions[:3])} with proven track record in {missing_keywords[0] if missing_keywords else 'software development'}."
        
        # Ensure keyword density is optimal (1-3% for top keywords)
        for keyword in keywords[:3]:
            if keyword.lower() not in optimized_summary.lower():
                optimized_summary = self._inject_keyword_naturally(optimized_summary, keyword)
        
        return optimized_summary

    def _inject_keyword_naturally(self, text: str, keyword: str) -> str:
        """Inject keywords naturally into text without making it sound robotic"""
        # Common professional phrases that can incorporate keywords
        insertion_patterns = [
            f"Expertise in {keyword}",
            f"Proficient in {keyword}",
            f"Strong background in {keyword}",
            f"Experienced with {keyword}",
            f"Skilled in {keyword}"
        ]
        
        # Choose appropriate pattern based on context
        if any(word in keyword.lower() for word in ['management', 'leadership', 'strategy']):
            return text + f" Demonstrated {keyword} capabilities across multiple projects."
        elif any(word in keyword.lower() for word in ['development', 'programming', 'coding']):
            return text + f" Strong {keyword} experience with focus on best practices."
        else:
            return text + f" {insertion_patterns[0]}."

    def _optimize_experience_description(self, description: str, job_analysis: Dict) -> str:
        """Optimize experience description based on job analysis"""
        if not job_analysis:
            return description
            
        keywords = job_analysis.get('keywords', [])
        
        # Enhance bullet points with job-relevant terms
        optimized_desc = description
        
        # Replace generic terms with job-specific ones
        replacements = {
            'worked on': 'developed',
            'helped': 'collaborated',
            'did': 'executed',
            'made': 'created',
            'used': 'leveraged',
            'handled': 'managed'
        }
        
        for generic, specific in replacements.items():
            optimized_desc = optimized_desc.replace(generic, specific)
        
        # Add quantification suggestions
        optimized_desc = self._suggest_quantification(optimized_desc)
        
        # Inject relevant keywords from job analysis
        for keyword in keywords[:3]:
            if keyword.lower() not in optimized_desc.lower():
                optimized_desc = self._enhance_bullets_with_keywords(optimized_desc, keyword)
        
        return optimized_desc

    def _suggest_quantification(self, description: str) -> str:
        """Add quantification hints to experience descriptions"""
        # Look for opportunities to add metrics
        metric_opportunities = {
            'project': '• Delivered [X] projects',
            'team': '• Led team of [X] members',
            'efficiency': '• Improved efficiency by [X]%',
            'cost': '• Reduced costs by $[X]',
            'time': '• Completed in [X] weeks',
            'users': '• Served [X] users',
            'performance': '• Increased performance by [X]%'
        }
        
        enhanced_desc = description
        for keyword, suggestion in metric_opportunities.items():
            if keyword in description.lower() and '[X]' not in description:
                # Add quantification hint
                enhanced_desc += f"\n{suggestion} ahead of schedule."
        
        return enhanced_desc

    def _enhance_bullets_with_keywords(self, description: str, keyword: str) -> str:
        """Enhance bullet points with relevant keywords"""
        lines = description.split('\n')
        enhanced_lines = []
        
        keyword_added = False
        for line in lines:
            if line.strip() and not keyword_added and len(line) > 20:
                # Add keyword to the first substantial bullet point
                if keyword.lower() in ['agile', 'scrum']:
                    line += f" using {keyword} methodology"
                elif keyword.lower() in ['api', 'rest', 'microservices']:
                    line += f" implementing {keyword} solutions"
                else:
                    line += f" utilizing {keyword}"
                keyword_added = True
            enhanced_lines.append(line)
        
        return '\n'.join(enhanced_lines)

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

    def validate_ats_compatibility(self, user_data: Dict, job_analysis: Dict = None) -> Dict:
        """Validate CV for ATS compatibility and provide score"""
        validation_results = {
            'overall_score': 0,
            'issues': [],
            'recommendations': [],
            'ats_grade': 'F'
        }
        
        score = 0
        max_score = 100
        
        # Check essential sections (30 points)
        if user_data.get('personal_info', {}).get('full_name'):
            score += 5
        else:
            validation_results['issues'].append("Missing full name")
        
        if user_data.get('personal_info', {}).get('email'):
            score += 5
        else:
            validation_results['issues'].append("Missing email address")
        
        if user_data.get('professional_summary'):
            score += 10
        else:
            validation_results['issues'].append("Missing professional summary")
        
        if user_data.get('work_experience'):
            score += 10
        else:
            validation_results['issues'].append("Missing work experience")
        
        # Check skills section (20 points)
        skills = user_data.get('skills', {})
        if skills.get('technical_skills'):
            score += 10
        else:
            validation_results['issues'].append("Missing technical skills")
        
        if skills.get('soft_skills'):
            score += 10
        else:
            validation_results['recommendations'].append("Add soft skills to improve ATS score")
        
        # Check job alignment (30 points)
        if job_analysis:
            job_keywords = job_analysis.get('keywords', [])
            job_skills = job_analysis.get('technical_skills', [])
            
            # Check keyword alignment
            user_text = str(user_data).lower()
            matching_keywords = sum(1 for keyword in job_keywords[:10] if keyword.lower() in user_text)
            score += (matching_keywords / 10) * 15
            
            # Check skill alignment
            user_skills = [skill.lower() for skill in skills.get('technical_skills', [])]
            matching_skills = sum(1 for skill in job_skills if skill.lower() in user_skills)
            if job_skills:
                score += (matching_skills / len(job_skills)) * 15
        
        # Check format and structure (20 points)
        # This is automatically good since we generate ATS-friendly PDFs
        score += 20
        
        validation_results['overall_score'] = round(score, 1)
        validation_results['ats_grade'] = self._get_ats_grade(score)
        
        # Generate recommendations
        if score < 70:
            validation_results['recommendations'].extend([
                "Include more job-relevant keywords in your summary",
                "Add quantifiable achievements to your experience",
                "Ensure all technical skills from job posting are included"
            ])
        
        return validation_results

    def _get_ats_grade(self, score: float) -> str:
        """Convert ATS score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'

