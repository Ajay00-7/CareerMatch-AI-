import os
import json
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def train_models():
    print("Training Job Matching Models...")
    
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, 'data', 'job_roles.json')
    models_dir = os.path.join(project_root, 'models')
    
    # Load Data
    with open(data_path, 'r') as f:
        job_roles = json.load(f)
    
    # Prepare Corpus
    corpus = []
    job_titles = []
    
    for title, data in job_roles.items():
        # Combine required skills into a single string document
        skills_text = " ".join(data['required_skills'])
        # Weight important skills by repeating them? (Simple trick)
        # For now, just simple text
        corpus.append(skills_text)
        job_titles.append(title)
        
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Save Models
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    joblib.dump(vectorizer, os.path.join(models_dir, 'skill_vectorizer.pkl'))
    joblib.dump(tfidf_matrix, os.path.join(models_dir, 'job_skills_matrix.pkl'))
    
    print(f"Models saved to {models_dir}")
    print(f"Trained on {len(job_titles)} job roles.")

if __name__ == "__main__":
    train_models()
