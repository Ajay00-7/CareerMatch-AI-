import streamlit as st
import time
import os
import pandas as pd
import base64

from utils.resume_parser import parse_resume
from utils.nlp_processor import NLPProcessor
from utils.skill_extractor import SkillExtractor
from utils.job_matcher import JobMatcher
from utils.visualizations import plot_job_match_scores, plot_skills_radar, plot_skill_gap

# Page Config
st.set_page_config(
    page_title="CareerMatch AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS & Background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_video_as_bg(video_file):
    bin_str = get_base64_of_bin_file(video_file)
    page_bg = '''
    <style>
        /* Force Text Colors for Dark Theme */
        h1, h2, h3, h4, h5, h6, .main-header, .sub-header, label, .stMarkdown, p {
            color: #F8FAFC !important;
        }
        
        /* Video Background */
        .stApp {
            background: transparent;
        }
        #myVideo {
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%; 
            min-height: 100%;
            z-index: -2;
            object-fit: cover;
            opacity: 0.3;
        }
        
        /* Enhanced Gradient Overlay - Purple/Pink/Blue Theme */
        .content-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg,
                rgba(124, 58, 237, 0.15) 0%,
                rgba(236, 72, 153, 0.12) 35%,
                rgba(14, 165, 233, 0.1) 70%,
                rgba(192, 38, 211, 0.15) 100%);
            z-index: -1;
        }
    
        /* Glass Cards - Purple Tint */
        div[data-testid="stMetric"],
        div[data-testid="stExpander"],
        div.css-1r6slb0, 
        .job-card,
        div[class*="stMarkdown"] div[style*="background"] {
            background: rgba(26, 11, 46, 0.65) !important;
            border: 1px solid rgba(167, 139, 250, 0.2) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 16px;
            padding: 24px;
            color: white;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        /* Sidebar - Deep Purple */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(26, 11, 46, 0.95) 0%, rgba(10, 1, 24, 0.98) 100%);
            border-right: 1px solid rgba(167, 139, 250, 0.2);
        }
        
        /* Headers - Purple/Pink/Blue Gradient */
        .main-header {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #a78bfa, #f472b6, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 30px rgba(167, 139, 250, 0.4));
        }
        .sub-header {
            font-size: 1.2rem;
            color: #e0e7ff !important;
            text-align: center;
            margin-bottom: 40px;
        }
        
        /* Buttons - Triple Gradient with Glow */
        .stButton>button {
            background: linear-gradient(135deg, #7c3aed 0%, #ec4899 50%, #c026d3 100%);
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.6), 0 0 40px rgba(236, 72, 153, 0.3);
        }
        
        /* Container Spacing */
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
        }
        
        /* Tabs - Purple Theme */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(124, 58, 237, 0.2);
            border: 1px solid rgba(167, 139, 250, 0.3);
            color: #a78bfa;
            border-radius: 8px;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.4), rgba(236, 72, 153, 0.3));
            border-color: rgba(167, 139, 250, 0.5);
            color: #f8fafc !important;
        }
        
        /* Info/Warning/Error Boxes */
        .stAlert {
            background: rgba(26, 11, 46, 0.7) !important;
            border-left: 4px solid #7c3aed !important;
            border-radius: 8px;
        }
        
        /* Success Boxes - Green Gradient */
        .stSuccess, div[data-testid="stSuccess"] {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.15)) !important;
            border-left: 4px solid #10b981 !important;
            border-radius: 12px;
            color: #d1fae5 !important;
        }
        
        /* Info Boxes - Blue Gradient */
        .stInfo, div[data-testid="stInfo"] {
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(6, 182, 212, 0.15)) !important;
            border-left: 4px solid #0ea5e9 !important;
            border-radius: 12px;
            color: #e0f2fe !important;
        }
        
        /* Warning Boxes - Orange Gradient */
        .stWarning, div[data-testid="stWarning"] {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(251, 146, 60, 0.15)) !important;
            border-left: 4px solid #f59e0b !important;
            border-radius: 12px;
            color: #fef3c7 !important;
        }
        
        /* Metrics - Enhanced with Gradients */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.25), rgba(236, 72, 153, 0.2)) !important;
            border: 2px solid rgba(167, 139, 250, 0.3) !important;
            border-radius: 16px;
            padding: 20px !important;
            box-shadow: 0 0 30px rgba(124, 58, 237, 0.3), 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        div[data-testid="stMetricValue"] {
            color: #f472b6 !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #e0e7ff !important;
            font-weight: 600 !important;
        }
        
        /* File Uploader - Purple Style */
        div[data-testid="stFileUploader"] {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(192, 38, 211, 0.1));
            border: 2px dashed rgba(167, 139, 250, 0.4);
            border-radius: 16px;
            padding: 20px;
        }
        
        div[data-testid="stFileUploader"] label {
            color: #a78bfa !important;
            font-weight: 600 !important;
        }
        
        /* Subheaders - Gradient Text */
        .stMarkdown h2, .stMarkdown h3 {
            background: linear-gradient(135deg, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
        }
        
        /* Code Blocks - Purple Theme */
        code {
            background: rgba(124, 58, 237, 0.2) !important;
            color: #f472b6 !important;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(167, 139, 250, 0.3);
        }
        
        /* Progress Bars */
        .stProgress > div > div {
            background: linear-gradient(90deg, #7c3aed, #ec4899, #0ea5e9) !important;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.5);
        }
        
        /* Spinner */
        .stSpinner > div {
            border-top-color: #ec4899 !important;
            border-right-color: #7c3aed !important;
        }
        
        /* Text Input Fields */
        input, textarea, select {
            background: rgba(26, 11, 46, 0.6) !important;
            border: 2px solid rgba(167, 139, 250, 0.3) !important;
            color: #f8fafc !important;
            border-radius: 8px;
        }
        
        input:focus, textarea:focus, select:focus {
            border-color: #ec4899 !important;
            box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.2) !important;
        }
        
        /* Expander Headers */
        div[data-testid="stExpander"] summary {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(236, 72, 153, 0.2));
            border-radius: 12px;
            padding: 16px;
            color: #f8fafc !important;
            font-weight: 600;
            border: 1px solid rgba(167, 139, 250, 0.4);
        }
        
        /* Plotly Charts Background */
        .js-plotly-plot {
            background: rgba(26, 11, 46, 0.4) !important;
            border-radius: 16px;
            padding: 10px;
        }
        
        /* Dataframes */
        .dataframe {
            background: rgba(26, 11, 46, 0.6) !important;
            border: 1px solid rgba(167, 139, 250, 0.3) !important;
            border-radius: 12px;
        }
        
        .dataframe th {
            background: linear-gradient(135deg, #7c3aed, #ec4899) !important;
            color: white !important;
            font-weight: 600;
        }
        
        .dataframe td {
            color: #e0e7ff !important;
        }
        
        /* Markdown Lists */
        .stMarkdown li {
            color: #e0e7ff !important;
            margin-bottom: 8px;
        }
        
        .stMarkdown li::marker {
            color: #f472b6 !important;
        }
        
        /* Strong/Bold Text */
        strong, b {
            color: #f472b6 !important;
        }
        
        /* Links */
        a {
            color: #0ea5e9 !important;
            text-decoration: none;
            font-weight: 600;
        }
        
        a:hover {
            color: #f472b6 !important;
            text-decoration: underline;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(26, 11, 46, 0.5);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #7c3aed, #ec4899);
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #ec4899, #c026d3);
        }
        

        /* HIDE DEFAULT STREAMLIT ELEMENTS - AGGRESSIVE */
        .stAppDeployButton, [data-testid="stAppDeployButton"] {
            display: none !important;
            visibility: hidden !important;
        }
        [data-testid="stToolbar"] {
            visibility: hidden !important;
            height: 0px !important;
            display: none !important;
        }
        [data-testid="stHeader"] {
            visibility: hidden !important;
            background-color: transparent !important;
        }
        header {
            visibility: hidden !important;
            height: 0px !important;
        }
        #MainMenu {
            visibility: hidden !important;
            display: none !important;
        }
        footer {
            visibility: hidden !important;
            display: none !important;
        }
        .st-emotion-cache-16txtl3 {
            display: none !important;
        }
    </style>
    
    <video autoplay muted loop id="myVideo">
        <source src="data:video/mp4;base64,%s" type="video/mp4">
    </video>
    <div class="content-overlay"></div>
    ''' % bin_str
    st.markdown(page_bg, unsafe_allow_html=True)

# Initialize Components (Cached)
@st.cache_resource
def load_components():
    nlp = NLPProcessor()
    extractor = SkillExtractor(nlp)
    matcher = JobMatcher()
    return nlp, extractor, matcher

# Main App
def main():
    # Set Background Video
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(current_dir, 'dummy.mp4')
        if os.path.exists(video_path):
            set_video_as_bg(video_path)
    except Exception as e:
        print(f"Background video error: {e}")

    # Header
    st.markdown('<div class="main-header">🚀 CareerMatch AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent Resume Analysis & Job Matching powered by NLP</div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Configuration")
    st.sidebar.info("Application is running offline using Spacy & Scikit-Learn")
    
    uploaded_file = st.sidebar.file_uploader("Upload Resume", type=['pdf', 'docx', 'txt'])
    
    if st.sidebar.button("Reload Models"):
        st.cache_resource.clear()
        st.success("Cache cleared! Reloading models...")

    # Main Content
    if uploaded_file is not None:
        try:
            # Load AI Components
            with st.spinner('Loading AI Models... (First time may take a minute)'):
                nlp_processor, skill_extractor, job_matcher = load_components()

            # 1. Parse Resume
            with st.spinner('Parsing resume text...'):
                resume_text = parse_resume(uploaded_file)
            
            if not resume_text:
                st.error("Could not extract text from the file.")
                return

            # Display Resume Stats
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📄 **File:** {uploaded_file.name}")
            with col2:
                st.info(f"📝 **Word Count:** {len(resume_text.split())}")

            # 2. NLP Analysis
            doc = nlp_processor.process_text(resume_text)
            
            # 3. Extract Skills
            categorized_skills, all_skills = skill_extractor.extract_skills(doc)
            
            # Display Skills
            st.subheader("🧠 Extracted Skills")
            if all_skills:
                # Skill Tabs
                tabs = st.tabs(categorized_skills.keys())
                for i, (category, skills) in enumerate(categorized_skills.items()):
                    with tabs[i]:
                        st.write(", ".join([f"`{s}`" for s in skills]))
            else:
                st.warning("No technical skills were detected based on our taxonomy.")

            # 4. Job Matching
            st.markdown("---")
            st.subheader("🎯 Job Role Matching")
            
            matches = job_matcher.match_jobs(all_skills)
            
            if matches:
                top_match = matches[0]
                
                # Visualizations
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    fig_bar = plot_job_match_scores(matches)
                    if fig_bar: st.plotly_chart(fig_bar, use_container_width=True)
                    
                with col_viz2:
                    fig_pie = plot_skill_gap(top_match)
                    if fig_pie: st.plotly_chart(fig_pie, use_container_width=True)

                st.markdown("---")
                
                # Radar Chart
                st.subheader("📊 Skill Distribution")
                fig_radar = plot_skills_radar(all_skills, skill_extractor.taxonomy)
                if fig_radar:
                    st.plotly_chart(fig_radar, use_container_width=True)
                
                # Detailed Analysis for Top Match
                st.subheader(f"🏆 Top Match: {top_match['job_title']} ({top_match['score']}%)")
                st.write(f"**Description:** {top_match.get('description', '')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.success("✅ **Matched Skills**")
                    for s in top_match['matched_skills']:
                        st.markdown(f"- {s}")
                
                with c2:
                    st.error("⚠️ **Missing Skills**")
                    for s in top_match['missing_skills']:
                        st.markdown(f"- {s}")

            else:
                st.warning("No job matches found. Try adding more skills to your resume.")
                
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.exception(e)

    else:
        # Welcome Screen
        st.markdown("""
        ### How it works:
        1. **Upload your resume** (PDF, DOCX, or TXT) from the sidebar
        2. **Wait for analysis** - Our AI scans for skills and keywords
        3. **View Results** - See job matches, skill gaps, and analytics
        """)
        
        # Check if models exist
        if not os.path.exists("models/skill_vectorizer.pkl"):
            st.warning("⚠️ ML models not found. Please run `python models/train_model.py` to train the initial models for better accuracy.")

if __name__ == "__main__":
    main()
