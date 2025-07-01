import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { FileText, Zap, Target, CheckCircle, Upload, Download, Eye } from 'lucide-react'
import CVGeneratorForm from './components/CVGeneratorForm'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('landing') // 'landing' or 'generator'

  const features = [
    {
      icon: <Target className="h-8 w-8 text-blue-600" />,
      title: "ATS Optimization",
      description: "Automatically optimize your CV to pass through Applicant Tracking Systems with keyword matching and proper formatting."
    },
    {
      icon: <Zap className="h-8 w-8 text-green-600" />,
      title: "Smart Analysis",
      description: "Upload job descriptions and get intelligent suggestions to tailor your CV for specific positions."
    },
    {
      icon: <FileText className="h-8 w-8 text-purple-600" />,
      title: "Professional Templates",
      description: "Choose from ATS-friendly templates designed to showcase your experience effectively."
    }
  ]

  const steps = [
    {
      icon: <Upload className="h-6 w-6" />,
      title: "Upload Job Description",
      description: "Paste or upload the job posting you're applying for"
    },
    {
      icon: <FileText className="h-6 w-6" />,
      title: "Fill Your Details",
      description: "Enter your personal information, experience, and skills"
    },
    {
      icon: <Eye className="h-6 w-6" />,
      title: "Preview & Optimize",
      description: "Review your ATS-optimized CV with real-time suggestions"
    },
    {
      icon: <Download className="h-6 w-6" />,
      title: "Download PDF",
      description: "Get your professional, ATS-ready CV in PDF format"
    }
  ]

  if (currentView === 'generator') {
    return <CVGeneratorForm onBack={() => setCurrentView('landing')} />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <FileText className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">CV Generator</h1>
            </div>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              ATS Optimized
            </Badge>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Create ATS-Optimized CVs That Get You
            <span className="text-blue-600"> Hired</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Generate professional resumes tailored to specific job descriptions. 
            Our AI-powered tool ensures your CV passes through Applicant Tracking Systems 
            and reaches hiring managers.
          </p>
          <Button 
            size="lg" 
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg"
            onClick={() => setCurrentView('generator')}
          >
            Generate My CV
            <FileText className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Why Choose Our CV Generator?
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h3>
          <div className="grid md:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <div key={index} className="text-center">
                <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <div className="text-blue-600">
                    {step.icon}
                  </div>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  {step.title}
                </h4>
                <p className="text-gray-600 text-sm">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-blue-600">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Ready to Create Your Perfect CV?
          </h3>
          <p className="text-blue-100 text-lg mb-8">
            Join thousands of job seekers who have successfully landed interviews 
            with our ATS-optimized CVs.
          </p>
          <Button 
            size="lg" 
            variant="secondary"
            className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 text-lg"
            onClick={() => setCurrentView('generator')}
          >
            Get Started Now
            <CheckCircle className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <FileText className="h-6 w-6 text-blue-400" />
            <span className="text-lg font-semibold">CV Generator</span>
          </div>
          <p className="text-gray-400">
            Create professional, ATS-optimized CVs that get you hired.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App

