[![Live Demo](https://img.shields.io/badge/demo-live-green.svg)](https://github.com/Ajay00-7/CareerMatch-AI-)

# 🎯 CareerMatch AI - Intelligent Resume Analysis & Job Matching

AI-powered resume analyzer that uses Natural Language Processing (NLP) and Machine Learning to extract skills, match job roles, and provide career recommendations.

## ✨ Features

- **Smart Resume Parsing**: Upload PDF, DOCX, or TXT files
- **AI-Powered Skill Extraction**: Uses spaCy NLP for intelligent skill detection
- **Job Role Matching**: Weighted algorithm matching your skills to top career paths
- **Skill Gap Analysis**: Identifies missing skills for your target roles
- **Personalized Recommendations**: Career advice and certification suggestions
- **Interactive Visualizations**: Charts showing skill distribution and match analysis
- **Beautiful UI**: Modern glassmorphism design with video background

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project**
```bash
cd "d:\CareerMatch AI"
```

2. **Create and activate virtual environment** (if not already done)
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

### Running the Application

#### Option 1: Flask Web App (Recommended - Modern UI)

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

#### Option 2: Streamlit App (Legacy Version)

```bash
streamlit run app_streamlit_old.py
```

Then open your browser to the URL shown in terminal (usually http://localhost:8501)

## 📱 Usage

1. **Upload Your Resume**
   - Click "Upload File" and select your PDF, DOCX, or TXT resume
   - OR paste your resume text directly
   - OR try the sample resume

2. **Analyze**
   - Click "Analyze Resume" button
   - Wait for AI processing (few seconds)

3. **View Results**
   - Resume strengths summary
   - Extracted skills by category
   - Top 3 job role matches with scores
   - Missing skills for each role
   - Personalized improvement recommendations
   - Visual charts and analytics

## 🏗️ Project Structure

```
CareerMatch AI/
├── app.py                     # Flask backend API (main application)
├── app.js                     # Frontend JavaScript logic
├── index.html                 # Main HTML page
├── styles.css                 # Application styles
├── app_streamlit_old.py       # Legacy Streamlit version
├── requirements.txt           # Python dependencies
├── dummy.mp4                  # Background video
│
├── utils/                     # Utility modules
│   ├── resume_parser.py       # PDF/DOCX text extraction
│   ├── nlp_processor.py       # spaCy NLP processing
│   ├── skill_extractor.py     # Skill extraction logic
│   ├── job_matcher.py         # Job matching algorithm
│   ├── visualizations.py      # Plotly charts (Streamlit only)
│   └── extract_colors.py      # Color extraction (unused)
│
├── data/                      # Data files
│   ├── job_roles.json         # Job role definitions
│   └── skills_taxonomy.json   # Skill categorization
│
└── models/                    # ML models
    ├── skill_vectorizer.pkl   # Trained vectorizer
    ├── job_skills_matrix.pkl  # Job-skill mappings
    └── train_model.py         # Model training script
```

## 🔧 Technology Stack

### Backend
- **Flask**: Web framework and REST API
- **spaCy**: NLP and text processing
- **scikit-learn**: Machine learning algorithms
- **NLTK**: Natural language toolkit

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **HTML5 & CSS3**: Modern web standards
- **PDF.js & Mammoth.js**: Client-side file parsing

### Data Processing
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **pandas & numpy**: Data manipulation

## 🎨 Features Breakdown

### Backend API Endpoints

- `GET /` - Serves the main application
- `POST /api/analyze` - Analyzes resume text and returns matches
- `POST /api/upload` - Handles file uploads and extracts text
- `GET /api/health` - Health check endpoint

### Skill Extraction
- Uses spaCy's NLP pipeline
- Custom skill taxonomy matching
- Context-aware skill detection
- Categorizes skills into domains

### Job Matching Algorithm
- Weighted scoring system
- Jaccard similarity calculation
- Missing skill identification
- Top 3 role recommendations

## 📊 Sample Output

```
Resume Summary:
Your resume demonstrates strong technical expertise with 14 identified skills.
You are an excellent match for Full Stack Developer roles with a 87% compatibility score.

Top Job Matches:
1. Full Stack Developer - 87%
2. Frontend Developer - 78%
3. Backend Developer - 72%

Recommendations:
- Focus on learning: kubernetes, terraform, aws to improve your job match
- Get AWS Certified Solutions Architect certification
- Learn DevOps fundamentals (Docker, CI/CD)
```

## 🔄 Development Notes

### Files Not Used in Flask Version
- `utils/visualizations.py` - Plotly charts (Streamlit only)
- `utils/extract_colors.py` - Color extraction utility (not needed)

These files are kept for the Streamlit version but can be removed if only using Flask.

### Customization

**Add New Job Roles**: Edit `data/job_roles.json`
```json
{
  "New Role": {
    "required_skills": ["skill1", "skill2"],
    "weight": {"skill1": 3, "skill2": 2}
  }
}
```

**Add New Skills**: Edit `data/skills_taxonomy.json`

## 🐛 Troubleshooting

### spaCy Model Not Found
```bash
python -m spacy download en_core_web_sm
```

### Port Already in Use
Change port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Change to any available port
```

### File Upload Not Working
- Check file size (max 10MB)
- Ensure file format is PDF, DOCX, or TXT
- Try pasting text directly instead

## 📝 License

This project is for educational and personal use.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📧 Support

For issues or questions, please check the troubleshooting section or review the code comments.

---

**Built with ❤️ using AI and modern web technologies**
