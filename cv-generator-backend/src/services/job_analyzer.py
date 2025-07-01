import re
import nltk
from collections import Counter
from typing import Dict, List, Set
try:
    import textract
except ImportError:
    textract = None
import io

class JobAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        
        # Common technical skills and keywords
        self.technical_skills = {
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'html', 'css',
            'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum', 'machine learning',
            'data analysis', 'project management', 'leadership', 'communication',
            'problem solving', 'teamwork', 'flask', 'django', 'mongodb', 'postgresql',
            'mysql', 'redis', 'elasticsearch', 'api', 'rest', 'graphql', 'microservices',
            'devops', 'ci/cd', 'jenkins', 'terraform', 'ansible', 'linux', 'bash',
            'typescript', 'vue.js', 'angular', 'spring', 'hibernate', 'junit',
            'pytest', 'testing', 'tdd', 'bdd', 'selenium', 'cypress'
        }
        
        # Experience level indicators
        self.experience_indicators = {
            'entry': ['entry', 'junior', 'associate', '0-2 years', 'graduate', 'intern'],
            'mid': ['mid', 'intermediate', '2-5 years', '3-5 years', 'experienced'],
            'senior': ['senior', 'lead', 'principal', '5+ years', '7+ years', 'expert', 'architect']
        }
        
        # Education requirements
        self.education_keywords = {
            'bachelor', 'master', 'phd', 'degree', 'computer science', 'engineering',
            'mathematics', 'statistics', 'certification', 'certified'
        }

    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from uploaded file"""
        try:
            if filename.lower().endswith('.txt'):
                return file_content.decode('utf-8')
            elif filename.lower().endswith(('.doc', '.docx')):
                return textract.process(io.BytesIO(file_content)).decode('utf-8')
            elif filename.lower().endswith('.pdf'):
                return textract.process(io.BytesIO(file_content)).decode('utf-8')
            else:
                # Try to decode as text
                return file_content.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Could not extract text from file: {str(e)}")

    def analyze_job_description(self, text: str) -> Dict:
        """Analyze job description and extract key information"""
        text = text.lower()
        
        # Extract keywords
        keywords = self._extract_keywords(text)
        
        # Extract technical skills
        technical_skills = self._extract_technical_skills(text)
        
        # Determine experience level
        experience_level = self._determine_experience_level(text)
        
        # Extract education requirements
        education_requirements = self._extract_education_requirements(text)
        
        # Extract soft skills
        soft_skills = self._extract_soft_skills(text)
        
        # Extract job title and company info
        job_info = self._extract_job_info(text)
        
        return {
            'keywords': keywords,
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'experience_level': experience_level,
            'education_requirements': education_requirements,
            'job_info': job_info,
            'optimization_suggestions': self._generate_optimization_suggestions(
                keywords, technical_skills, soft_skills
            )
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from job description"""
        # Remove common job posting boilerplate
        text = re.sub(r'(equal opportunity employer|eoe|benefits|salary|compensation)', '', text)
        
        # Tokenize and filter
        tokens = nltk.word_tokenize(text)
        
        # Filter out stop words and short words
        keywords = [word for word in tokens 
                   if word.isalpha() and len(word) > 2 and word not in self.stop_words]
        
        # Count frequency and return top keywords
        keyword_freq = Counter(keywords)
        return [word for word, count in keyword_freq.most_common(20)]

    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills mentioned in job description"""
        found_skills = []
        
        for skill in self.technical_skills:
            if skill in text:
                found_skills.append(skill)
        
        # Also look for common patterns
        patterns = [
            r'(\w+)\s+programming',
            r'(\w+)\s+development',
            r'(\w+)\s+framework',
            r'(\w+)\s+database'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            found_skills.extend(matches)
        
        return list(set(found_skills))

    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills from job description"""
        soft_skills_keywords = [
            'communication', 'leadership', 'teamwork', 'problem solving',
            'analytical', 'creative', 'detail oriented', 'organized',
            'time management', 'adaptable', 'collaborative', 'innovative',
            'critical thinking', 'presentation', 'interpersonal'
        ]
        
        found_skills = []
        for skill in soft_skills_keywords:
            if skill in text:
                found_skills.append(skill)
        
        return found_skills

    def _determine_experience_level(self, text: str) -> str:
        """Determine required experience level"""
        for level, indicators in self.experience_indicators.items():
            for indicator in indicators:
                if indicator in text:
                    return level
        return 'not_specified'

    def _extract_education_requirements(self, text: str) -> List[str]:
        """Extract education requirements"""
        requirements = []
        for keyword in self.education_keywords:
            if keyword in text:
                requirements.append(keyword)
        return list(set(requirements))

    def _extract_job_info(self, text: str) -> Dict:
        """Extract job title and company information"""
        # This is a simplified extraction - in a real application,
        # you might use more sophisticated NLP techniques
        lines = text.split('\n')
        
        job_title = ""
        company = ""
        
        # Look for common patterns in the first few lines
        for i, line in enumerate(lines[:5]):
            if any(word in line.lower() for word in ['position', 'role', 'job', 'title']):
                job_title = line.strip()
                break
        
        return {
            'job_title': job_title,
            'company': company
        }

    def _generate_optimization_suggestions(self, keywords: List[str], 
                                         technical_skills: List[str], 
                                         soft_skills: List[str]) -> List[str]:
        """Generate suggestions for CV optimization"""
        suggestions = []
        
        if technical_skills:
            suggestions.append(f"Highlight these technical skills: {', '.join(technical_skills[:5])}")
        
        if soft_skills:
            suggestions.append(f"Emphasize these soft skills: {', '.join(soft_skills[:3])}")
        
        if keywords:
            suggestions.append(f"Include these keywords naturally: {', '.join(keywords[:10])}")
        
        suggestions.extend([
            "Use action verbs to describe your achievements",
            "Quantify your accomplishments with numbers",
            "Tailor your professional summary to match the job requirements",
            "Ensure your CV format is ATS-friendly (simple, clean layout)",
            "Use standard section headings (Experience, Education, Skills)"
        ])
        
        return suggestions

