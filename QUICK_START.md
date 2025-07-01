# 🚀 Quick Start Guide

Get your ATS-Smart CV Generator up and running in minutes!

## 📋 Prerequisites

Before you start, make sure you have:

- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **Node.js 16+** ([Download here](https://nodejs.org/))
- **npm** (comes with Node.js)
- **Git** ([Download here](https://git-scm.com/))

## ⚡ 5-Minute Setup

### Option 1: Automated Setup (Recommended)

**For macOS/Linux:**

```bash
# Clone and run
git clone https://github.com/yourusername/ats-smart-cv-generator.git
cd ats-smart-cv-generator
./start.sh
```

**For Windows:**

```cmd
# Clone and run
git clone https://github.com/yourusername/ats-smart-cv-generator.git
cd ats-smart-cv-generator
start.bat
```

The script will automatically:

- ✅ Check prerequisites
- ✅ Set up virtual environments
- ✅ Install all dependencies
- ✅ Download NLTK data
- ✅ Start both servers
- ✅ Open the application in your browser

### Option 2: Manual Setup

If you prefer manual setup or need more control:

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ats-smart-cv-generator.git
cd ats-smart-cv-generator
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd cv-generator-backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Download required NLTK data (one-time setup)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger')"

# Start the backend server
python app.py
```

✅ **Backend should now be running on:** `http://localhost:5002`

### Step 3: Frontend Setup

Open a **new terminal** and run:

```bash
# Navigate to frontend directory (from project root)
cd cv-generator-frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

✅ **Frontend should now be running on:** `http://localhost:5173`

### Step 4: Access the Application

Open your browser and go to: <http://localhost:5173>

---

## 🎯 How to Use

### 1. **Job Description Analysis**

- Paste the job description you want to tailor your CV for
- Click "Analyze Job Description"
- The system will extract keywords and requirements

### 2. **Personal Information**

- Fill in your contact details
- Full Name, Email, Phone, Location, LinkedIn

### 3. **Work Experience**

- Add your work history
- Include job titles, companies, dates, and descriptions
- Use bullet points for achievements

### 4. **Education & Skills**

- Add your educational background
- List technical skills, soft skills, languages, certifications
- Separate multiple items with commas

### 5. **Generate CV**

- Review optimization suggestions
- Click "Generate CV"
- Download your ATS-optimized PDF

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'flask'`

```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem:** `LookupError: Resource punkt not found`

```bash
# Solution: Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

**Problem:** `Address already in use` (Port 5002)

```bash
# Solution: Kill process on port 5002
lsof -ti:5002 | xargs kill -9
# Or change port in app.py
```

### Frontend Issues

**Problem:** `command not found: npm`

- **Solution:** Install Node.js from [nodejs.org](https://nodejs.org/)

**Problem:** `Error: Cannot find module`

```bash
# Solution: Install dependencies
npm install
```

**Problem:** Port 5173 already in use

```bash
# Solution: Kill process or use different port
npm run dev -- --port 3000
```

### API Connection Issues

**Problem:** API calls failing

1. Ensure backend is running on port 5002
2. Check if `http://localhost:5002/api/health` returns a response
3. Verify proxy configuration in `cv-generator-frontend/vite.config.js`

---

## 🐳 Docker Alternative (Optional)

If you prefer using Docker:

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:5173
```

---

## 📚 Next Steps

- **Customize CV Templates**: Modify styling in `cv-generator-backend/src/services/cv_generator.py`
- **Add New Skills**: Extend the skills database in `job_analyzer.py`
- **Deploy to Production**: See deployment guides in the main README
- **Contribute**: Check out our [Contributing Guidelines](CONTRIBUTING.md)

---

## 🆘 Need Help?

- **Issues**: [Report bugs](https://github.com/yourusername/ats-smart-cv-generator/issues)
- **Discussions**: [Ask questions](https://github.com/yourusername/ats-smart-cv-generator/discussions)
- **Documentation**: [Full README](README.md)

---

## ✅ Verification Checklist

- [ ] Backend running on <http://localhost:5002>
- [ ] Frontend running on <http://localhost:5173>
- [ ] Can access application in browser
- [ ] Job analysis works (Step 1)
- [ ] Can fill out forms (Steps 2-4)
- [ ] Can generate and download CV (Step 5)

## Happy CV building! 🎉

