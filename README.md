# ATS-Smart CV Generator

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Node](https://img.shields.io/badge/node-16+-green)

A full-stack application that analyzes job descriptions and generates ATS-optimized CVs tailored to specific job requirements.

## � Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[API Documentation](#-api-endpoints)** - Backend API reference
- **[Contributing Guidelines](#-contributing)** - How to contribute to the project
- **[License](LICENSE)** - MIT License information

## �🚀 Features

- **Job Description Analysis**: Uses NLP to extract keywords, skills, and requirements
- **ATS Optimization**: Tailors CV content to match job postings
- **Multi-step Form**: Progressive data collection with user-friendly interface
- **PDF Generation**: Professional CV output with customizable templates
- **Real-time Feedback**: Optimization suggestions based on job analysis
- **Responsive Design**: Modern UI with Tailwind CSS and Radix UI components

## 🏗️ Architecture

### Backend (Flask API)
- **Technology**: Python, Flask, SQLAlchemy
- **NLP**: NLTK for job description analysis
- **PDF Generation**: ReportLab for professional CV creation
- **Database**: SQLite for user data storage
- **API**: RESTful endpoints for frontend communication

### Frontend (React SPA)
- **Technology**: React, Vite, Tailwind CSS
- **Components**: Radix UI for consistent design
- **State Management**: React hooks for form data
- **Build Tool**: Vite for fast development and building

## 📁 Project Structure

```
ATS-Smart/
├── cv-generator-backend/          # Flask API server
│   ├── src/
│   │   ├── models/               # Database models
│   │   ├── routes/               # API endpoints
│   │   ├── services/             # Business logic
│   │   └── static/               # Static files
│   ├── app.py                    # Main application entry
│   └── requirements.txt          # Python dependencies
├── cv-generator-frontend/        # React application
│   ├── src/
│   │   ├── components/           # React components
│   │   └── assets/               # Static assets
│   ├── package.json              # Node.js dependencies
│   └── vite.config.js            # Vite configuration
└── README.md                     # Project documentation
```

## � Quick Start

**Want to get started immediately?** Check out our [Quick Start Guide](QUICK_START.md) for a 5-minute setup!

## �🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd cv-generator-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger')"
   ```

5. **Start the server**
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5002`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd cv-generator-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   Frontend will run on `http://localhost:5173`

## 🔄 Usage

1. **Access the application** at `http://localhost:5173`
2. **Enter job description** in Step 1 for analysis
3. **Fill personal information** in Steps 2-4
4. **Review and generate** your optimized CV in Step 5
5. **Download** the ATS-optimized PDF

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze-job` | POST | Analyze job description |
| `/api/generate-cv` | POST | Generate tailored CV |
| `/api/download-cv/{id}` | GET | Download CV PDF |
| `/api/health` | GET | Health check |

## 🔧 Configuration

### Backend Configuration
- **Port**: 5002 (configurable in `app.py`)
- **Database**: SQLite (configurable in `src/main.py`)
- **CORS**: Enabled for all origins (production: configure specific origins)

### Frontend Configuration
- **Port**: 5173 (configurable in `vite.config.js`)
- **API Proxy**: Points to backend at `http://localhost:5002`
- **Build Output**: `dist/` directory

## 🚀 Deployment

### Backend Deployment
```bash
# Production setup
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5002 app:app
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files
npm run preview
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NLTK** for natural language processing
- **ReportLab** for PDF generation
- **React** and **Vite** for the frontend framework
- **Tailwind CSS** and **Radix UI** for the design system

## 📞 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/ats-smart/issues) on GitHub.

---

**Made with ❤️ for job seekers everywhere**
