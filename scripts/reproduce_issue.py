from utils.resume_parser import extract_project_section

# 1. Clean Sample Case (Should Work)
clean_resume = """
John Doe
Software Engineer

Experience:
Worked at Google

Projects:
1. E-commerce App: Built using React and Node.js.
2. AI Chatbot: Used Python and TensorFlow.

Education:
B.Tech in CS
"""

# 2. Messy/Real-world Case (Likely to Fail)
# - Case insensitive issues
# - Extra whitespace or characters
# - Header variations
messy_resume = """
John Doe
Software Developer

Professional Experience
Worked at Microsoft

KEY PROJECTS
* E-commerce App
Built using MERN stack. Did frontend and backend.
* AI Chatbot
Used Python.

Technical Skills
Python, Java
"""

# 3. Another tricky case
tricky_resume = """
Projects Undertaken:
1. Project A
2. Project B

Certifications:
AWS Certified
"""

print("--- Clean Case ---")
print(extract_project_section(clean_resume))
print("\n--- Messy Case ---")
print(extract_project_section(messy_resume))
print("\n--- Tricky Case ---")
print(extract_project_section(tricky_resume))
