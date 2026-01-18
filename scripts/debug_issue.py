import sys
import os

# Create a mock of utils.resume_parser's extract_project_section to test it isolated
# Or import it if path allows
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.resume_parser import extract_project_section
from utils.job_matcher import JobMatcher

def debug():
    with open("debug_resume.txt", "r", encoding="utf-8") as f:
        text = f.read()

    print("--- FULL TEXT (Starting partial) ---")
    print(text[:200])
    print("...")

    print("\n--- EXTRACTING PROJECTS ---")
    project_section = extract_project_section(text)
    print(f"Extracted Length: {len(project_section)}")
    print(f"Extracted Content:\n'{project_section}'")

    if not project_section:
        print("FAILED: No project section extracted.")
        return

    matcher = JobMatcher()
    print("\n--- ANALYZING PROJECTS ---")
    # Mock extracted skills
    skills = ["Python", "Machine Learning", "NLP", "Data Analysis", "React.js"]
    analysis = matcher.analyze_projects(project_section, skills)
    
    print(f"Projects Found: {len(analysis)}")
    for p in analysis:
        print(f" - {p['name']} (Score: {p.get('score', 'N/A')})")

if __name__ == "__main__":
    debug()
