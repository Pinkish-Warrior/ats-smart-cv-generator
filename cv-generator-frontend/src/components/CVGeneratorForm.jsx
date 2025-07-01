import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { ArrowLeft, ArrowRight, Upload, FileText, User, Briefcase, GraduationCap, Award, Download, Eye, Loader2 } from 'lucide-react'

const CVGeneratorForm = ({ onBack }) => {
  const [currentStep, setCurrentStep] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [jobAnalysis, setJobAnalysis] = useState(null)
  const [generatedCvId, setGeneratedCvId] = useState(null)
  
  const [formData, setFormData] = useState({
    jobDescription: '',
    personalInfo: {
      fullName: '',
      email: '',
      phone: '',
      location: '',
      linkedin: ''
    },
    professionalSummary: '',
    workExperience: [
      {
        jobTitle: '',
        company: '',
        startDate: '',
        endDate: '',
        description: ''
      }
    ],
    education: [
      {
        degree: '',
        school: '',
        graduationDate: '',
        gpa: ''
      }
    ],
    skills: {
      technicalSkills: [],
      softSkills: [],
      languages: [],
      certifications: []
    }
  })

  const steps = [
    { number: 1, title: 'Job Description', icon: <Upload className="h-4 w-4" /> },
    { number: 2, title: 'Personal Info', icon: <User className="h-4 w-4" /> },
    { number: 3, title: 'Experience', icon: <Briefcase className="h-4 w-4" /> },
    { number: 4, title: 'Education & Skills', icon: <GraduationCap className="h-4 w-4" /> },
    { number: 5, title: 'Generate CV', icon: <FileText className="h-4 w-4" /> }
  ]

  const progress = (currentStep / steps.length) * 100

  const handleInputChange = (section, field, value, index = null) => {
    setFormData(prev => {
      if (index !== null) {
        // Handle array updates
        const newArray = [...prev[section]]
        newArray[index] = { ...newArray[index], [field]: value }
        return { ...prev, [section]: newArray }
      } else if (section === 'skills' && Array.isArray(prev[section][field])) {
        // Handle skills arrays
        const skillsArray = value.split(',').map(skill => skill.trim()).filter(skill => skill)
        return {
          ...prev,
          [section]: { ...prev[section], [field]: skillsArray }
        }
      } else if (typeof prev[section] === 'object') {
        // Handle nested objects
        return {
          ...prev,
          [section]: { ...prev[section], [field]: value }
        }
      } else {
        // Handle direct fields
        return { ...prev, [section]: value }
      }
    })
  }

  const addExperience = () => {
    setFormData(prev => ({
      ...prev,
      workExperience: [...prev.workExperience, {
        jobTitle: '',
        company: '',
        startDate: '',
        endDate: '',
        description: ''
      }]
    }))
  }

  const addEducation = () => {
    setFormData(prev => ({
      ...prev,
      education: [...prev.education, {
        degree: '',
        school: '',
        graduationDate: '',
        gpa: ''
      }]
    }))
  }

  const analyzeJobDescription = async () => {
    if (!formData.jobDescription.trim()) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/analyze-job', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_text: formData.jobDescription
        })
      })

      if (response.ok) {
        const result = await response.json()
        setJobAnalysis(result.analysis)
      }
    } catch (error) {
      console.error('Error analyzing job description:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const generateCV = async () => {
    setIsLoading(true)
    try {
      const userData = {
        personal_info: {
          full_name: formData.personalInfo.fullName,
          email: formData.personalInfo.email,
          phone: formData.personalInfo.phone,
          location: formData.personalInfo.location,
          linkedin: formData.personalInfo.linkedin
        },
        professional_summary: formData.professionalSummary,
        work_experience: formData.workExperience.map(exp => ({
          job_title: exp.jobTitle,
          company: exp.company,
          start_date: exp.startDate,
          end_date: exp.endDate,
          description: exp.description
        })),
        education: formData.education.map(edu => ({
          degree: edu.degree,
          school: edu.school,
          graduation_date: edu.graduationDate,
          gpa: edu.gpa
        })),
        skills: {
          technical_skills: formData.skills.technicalSkills,
          soft_skills: formData.skills.softSkills,
          languages: formData.skills.languages,
          certifications: formData.skills.certifications
        }
      }

      const response = await fetch('/api/generate-cv', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_data: userData,
          job_analysis: jobAnalysis
        })
      })

      if (response.ok) {
        const result = await response.json()
        setGeneratedCvId(result.cv_id)
      }
    } catch (error) {
      console.error('Error generating CV:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const downloadCV = () => {
    if (generatedCvId) {
      window.open(`/api/download-cv/${generatedCvId}`, '_blank')
    }
  }

  const nextStep = () => {
    if (currentStep === 1 && formData.jobDescription.trim()) {
      analyzeJobDescription()
    }
    if (currentStep === 4) {
      generateCV()
    }
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                Job Description Analysis
              </CardTitle>
              <CardDescription>
                Paste the job description to get personalized CV optimization suggestions
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="jobDescription">Job Description</Label>
                <Textarea
                  id="jobDescription"
                  placeholder="Paste the job description here..."
                  value={formData.jobDescription}
                  onChange={(e) => handleInputChange('jobDescription', null, e.target.value)}
                  rows={10}
                  className="mt-2"
                />
              </div>
              {jobAnalysis && (
                <div className="mt-6 p-4 bg-green-50 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-2">Analysis Complete!</h4>
                  <div className="space-y-2">
                    <div>
                      <span className="font-medium">Key Skills Found: </span>
                      {jobAnalysis.technical_skills?.slice(0, 5).map((skill, index) => (
                        <Badge key={index} variant="secondary" className="mr-1">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                    <div>
                      <span className="font-medium">Experience Level: </span>
                      <Badge variant="outline">{jobAnalysis.experience_level}</Badge>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )

      case 2:
        return (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Personal Information
              </CardTitle>
              <CardDescription>
                Enter your contact details and professional summary
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="fullName">Full Name *</Label>
                  <Input
                    id="fullName"
                    value={formData.personalInfo.fullName}
                    onChange={(e) => handleInputChange('personalInfo', 'fullName', e.target.value)}
                    placeholder="John Doe"
                  />
                </div>
                <div>
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.personalInfo.email}
                    onChange={(e) => handleInputChange('personalInfo', 'email', e.target.value)}
                    placeholder="john@example.com"
                  />
                </div>
                <div>
                  <Label htmlFor="phone">Phone</Label>
                  <Input
                    id="phone"
                    value={formData.personalInfo.phone}
                    onChange={(e) => handleInputChange('personalInfo', 'phone', e.target.value)}
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
                <div>
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    value={formData.personalInfo.location}
                    onChange={(e) => handleInputChange('personalInfo', 'location', e.target.value)}
                    placeholder="New York, NY"
                  />
                </div>
              </div>
              <div>
                <Label htmlFor="linkedin">LinkedIn Profile</Label>
                <Input
                  id="linkedin"
                  value={formData.personalInfo.linkedin}
                  onChange={(e) => handleInputChange('personalInfo', 'linkedin', e.target.value)}
                  placeholder="linkedin.com/in/johndoe"
                />
              </div>
              <div>
                <Label htmlFor="summary">Professional Summary</Label>
                <Textarea
                  id="summary"
                  value={formData.professionalSummary}
                  onChange={(e) => handleInputChange('professionalSummary', null, e.target.value)}
                  placeholder="Brief overview of your professional background and key strengths..."
                  rows={4}
                />
              </div>
            </CardContent>
          </Card>
        )

      case 3:
        return (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Briefcase className="h-5 w-5" />
                Work Experience
              </CardTitle>
              <CardDescription>
                Add your work experience, starting with the most recent
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {formData.workExperience.map((exp, index) => (
                <div key={index} className="p-4 border rounded-lg space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>Job Title</Label>
                      <Input
                        value={exp.jobTitle}
                        onChange={(e) => handleInputChange('workExperience', 'jobTitle', e.target.value, index)}
                        placeholder="Software Developer"
                      />
                    </div>
                    <div>
                      <Label>Company</Label>
                      <Input
                        value={exp.company}
                        onChange={(e) => handleInputChange('workExperience', 'company', e.target.value, index)}
                        placeholder="Tech Company Inc."
                      />
                    </div>
                    <div>
                      <Label>Start Date</Label>
                      <Input
                        value={exp.startDate}
                        onChange={(e) => handleInputChange('workExperience', 'startDate', e.target.value, index)}
                        placeholder="Jan 2020"
                      />
                    </div>
                    <div>
                      <Label>End Date</Label>
                      <Input
                        value={exp.endDate}
                        onChange={(e) => handleInputChange('workExperience', 'endDate', e.target.value, index)}
                        placeholder="Present"
                      />
                    </div>
                  </div>
                  <div>
                    <Label>Description & Achievements</Label>
                    <Textarea
                      value={exp.description}
                      onChange={(e) => handleInputChange('workExperience', 'description', e.target.value, index)}
                      placeholder="• Led development of web applications&#10;• Improved performance by 40%&#10;• Mentored junior developers"
                      rows={4}
                    />
                  </div>
                </div>
              ))}
              <Button onClick={addExperience} variant="outline" className="w-full">
                Add Another Experience
              </Button>
            </CardContent>
          </Card>
        )

      case 4:
        return (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <GraduationCap className="h-5 w-5" />
                  Education
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {formData.education.map((edu, index) => (
                  <div key={index} className="p-4 border rounded-lg space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label>Degree</Label>
                        <Input
                          value={edu.degree}
                          onChange={(e) => handleInputChange('education', 'degree', e.target.value, index)}
                          placeholder="Bachelor of Science in Computer Science"
                        />
                      </div>
                      <div>
                        <Label>School</Label>
                        <Input
                          value={edu.school}
                          onChange={(e) => handleInputChange('education', 'school', e.target.value, index)}
                          placeholder="University of Technology"
                        />
                      </div>
                      <div>
                        <Label>Graduation Date</Label>
                        <Input
                          value={edu.graduationDate}
                          onChange={(e) => handleInputChange('education', 'graduationDate', e.target.value, index)}
                          placeholder="2020"
                        />
                      </div>
                      <div>
                        <Label>GPA (Optional)</Label>
                        <Input
                          value={edu.gpa}
                          onChange={(e) => handleInputChange('education', 'gpa', e.target.value, index)}
                          placeholder="3.8"
                        />
                      </div>
                    </div>
                  </div>
                ))}
                <Button onClick={addEducation} variant="outline" className="w-full">
                  Add Another Education
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Award className="h-5 w-5" />
                  Skills
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Technical Skills</Label>
                  <Input
                    value={formData.skills.technicalSkills.join(', ')}
                    onChange={(e) => handleInputChange('skills', 'technicalSkills', e.target.value)}
                    placeholder="Python, JavaScript, React, Node.js, SQL"
                  />
                  <p className="text-sm text-gray-500 mt-1">Separate skills with commas</p>
                </div>
                <div>
                  <Label>Soft Skills</Label>
                  <Input
                    value={formData.skills.softSkills.join(', ')}
                    onChange={(e) => handleInputChange('skills', 'softSkills', e.target.value)}
                    placeholder="Leadership, Communication, Problem Solving"
                  />
                </div>
                <div>
                  <Label>Languages</Label>
                  <Input
                    value={formData.skills.languages.join(', ')}
                    onChange={(e) => handleInputChange('skills', 'languages', e.target.value)}
                    placeholder="English (Native), Spanish (Conversational)"
                  />
                </div>
                <div>
                  <Label>Certifications</Label>
                  <Input
                    value={formData.skills.certifications.join(', ')}
                    onChange={(e) => handleInputChange('skills', 'certifications', e.target.value)}
                    placeholder="AWS Certified Developer, Scrum Master"
                  />
                </div>
              </CardContent>
            </Card>
          </div>
        )

      case 5:
        return (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Generate Your CV
              </CardTitle>
              <CardDescription>
                Review your information and generate your ATS-optimized CV
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {jobAnalysis && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-semibold text-blue-800 mb-2">Optimization Suggestions</h4>
                  <ul className="text-sm text-blue-700 space-y-1">
                    {jobAnalysis.optimization_suggestions?.slice(0, 3).map((suggestion, index) => (
                      <li key={index}>• {suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {generatedCvId ? (
                <div className="text-center space-y-4">
                  <div className="p-6 bg-green-50 rounded-lg">
                    <h3 className="text-lg font-semibold text-green-800 mb-2">
                      CV Generated Successfully!
                    </h3>
                    <p className="text-green-700">
                      Your ATS-optimized CV is ready for download.
                    </p>
                  </div>
                  <Button onClick={downloadCV} size="lg" className="bg-green-600 hover:bg-green-700">
                    <Download className="mr-2 h-5 w-5" />
                    Download CV
                  </Button>
                </div>
              ) : (
                <div className="text-center">
                  <Button 
                    onClick={generateCV} 
                    size="lg" 
                    disabled={isLoading}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                        Generating CV...
                      </>
                    ) : (
                      <>
                        <FileText className="mr-2 h-5 w-5" />
                        Generate CV
                      </>
                    )}
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Button variant="ghost" onClick={onBack} className="flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Home
            </Button>
            <div className="flex items-center space-x-2">
              <FileText className="h-6 w-6 text-blue-600" />
              <span className="text-lg font-semibold">CV Generator</span>
            </div>
          </div>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="bg-white border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {currentStep} of {steps.length}
            </span>
            <span className="text-sm text-gray-500">
              {Math.round(progress)}% Complete
            </span>
          </div>
          <Progress value={progress} className="h-2" />
          <div className="flex justify-between mt-4">
            {steps.map((step) => (
              <div
                key={step.number}
                className={`flex items-center space-x-2 ${
                  step.number <= currentStep ? 'text-blue-600' : 'text-gray-400'
                }`}
              >
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    step.number <= currentStep
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {step.number <= currentStep ? step.icon : step.number}
                </div>
                <span className="text-sm font-medium hidden sm:block">
                  {step.title}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderStepContent()}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8">
          <Button
            variant="outline"
            onClick={prevStep}
            disabled={currentStep === 1}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Previous
          </Button>
          
          {currentStep < steps.length && (
            <Button
              onClick={nextStep}
              disabled={isLoading || (currentStep === 2 && !formData.personalInfo.fullName)}
              className="flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  Next
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          )}
        </div>
      </main>
    </div>
  )
}

export default CVGeneratorForm

