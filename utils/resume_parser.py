import os
from io import BytesIO
import PyPDF2
import docx

def extract_text_from_pdf(file_bytes):
    """Extract text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            # Add newline to prevent pages from gluing together
            text += (page.extract_text() or "") + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def parse_resume(file_path):
    """Parse resume file and extract text based on extension."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        try:
            with open(file_path, 'rb') as f:
                return extract_text_from_pdf(f.read())
        except Exception as e:
            return f"Error reading file: {str(e)}"
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading TXT: {str(e)}"
    else:
        return "Unsupported file format"

def extract_project_section(text):
    """
    Extracts the 'Projects' section from the resume text using line-based heuristics.
    """
    # Normalize text
    lines = text.split('\n')
    
    # Common headers for project sections
    project_headers = [
        'projects', 'academic projects', 'personal projects', 'key projects', 
        'technical projects', 'project experience', 'projects undertaken',
        'selected projects', 'major projects', 'professional projects',
        'project details', 'projects summary', 'key initiatives', 
        'development experience', 'significant projects'
    ]
    
    # Common headers for other sections (to find the end of projects)
    # Added more specific "Experience" variations to avoid false positives inside text
    other_headers = [
        'education', 'skills', 'technical skills', 'key skills', 'skills & achievements',
        'experience', 'work experience', 'employment', 'professional experience',
        'achievements', 'certifications', 'awards', 'languages', 'interests',
        'references', 'declaration', 'summary', 'profile', 'objective', 
        'competitive programming', 'courses', 'publications', 'patents',
        'extra-curricular', 'leadership', 
        # Internship headers to ensure strict separation
        'internships', 'internship', 'industrial training', 
        'in-plant training', 'vocational training'
    ]
    
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        # Clean line for checking: lowercase, remove non-alphanumeric at ends
        line_clean = line.strip().lower()
        # Remove common header suffixes/prefixes like delimiters
        line_clean = line_clean.strip(':-|•* #')
        
        if not line_clean:
            continue
            
        # Check start
        if start_idx == -1:
            # We look for exact match or strong containment for headers
            if any(line_clean == h for h in project_headers):
                start_idx = i + 1
                continue
            
            # Allow "Projects: <Description>" to trigger start, but keep the description
            for h in project_headers:
                if line_clean.startswith(h) and len(line_clean) < len(h) + 5: # "Projects:"
                     start_idx = i + 1
                     break

        # Check end
        if start_idx != -1:
            # If we hit another header, stop
            is_header = False
            for h in other_headers:
                # Exact match
                if line_clean == h:
                    is_header = True
                    break
                
                # Starts with header (e.g., "Education Details")
                # BUT be careful: "Experience with Python" is NOT "Experience" header
                if line_clean.startswith(h):
                    # Check if the rest is just generic characters or short
                    remainder = line_clean[len(h):].strip()
                    if not remainder or remainder in [':', '-', '|']:
                        is_header = True
                        break
                    
                    # If it's a known multi-word header like "Work Experience", startswith is fine
                    # But for single words like "Experience", we need to be careful
                    if ' ' in h: 
                         if len(line_clean) < len(h) + 10:
                             is_header = True
                             break
                    else:
                        # For single word headers, ensure it's not a sentence
                        if len(line_clean.split()) <= 3: 
                            is_header = True
                            break

            if is_header:
                # Double check: is this line too long to be a header?
                if len(line_clean) > 40:
                    is_header = False

                if is_header:
                    end_idx = i
                    break
                
    if start_idx != -1:
        if end_idx == -1:
            end_idx = len(lines)
        
        # Post-processing: remove empty lines from start/end
        section_lines = lines[start_idx:end_idx]
        while section_lines and not section_lines[0].strip():
            section_lines.pop(0)
        while section_lines and not section_lines[-1].strip():
            section_lines.pop()
            
        return "\n".join(section_lines).strip()
        
    return ""

def extract_internship_section(text):
    """
    Extracts the 'Internship' or 'Training' section from the resume text.
    """
    # Normalize text
    lines = text.split('\n')
    
    # Common headers for internship sections
    internship_headers = [
        'internships', 'internship experience', 'industrial training', 
        'in-plant training', 'vocational training', 'apprenticeship',
        'summer internship', 'winter internship', 'work history', 
        'professional experience', 'experience' # Generic fallback
    ]
    
    # Common headers for OTHER sections (to find the end)
    other_headers = [
        'education', 'skills', 'technical skills', 'key skills', 
        'projects', 'academic projects', 'achievements', 'certifications', 
        'awards', 'languages', 'interests', 'references', 'declaration', 
        'summary', 'profile', 'objective'
    ]
    
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        line_clean = line.strip().lower().strip(':-|•* #')
        
        if not line_clean:
            continue
            
        # Check start
        if start_idx == -1:
            if any(line_clean == h for h in internship_headers):
                start_idx = i + 1
                continue
            
            # Check for "Experience" combined with "Intern" in the same line?
            # Or reliance on specific headers. 
            # If "Experience" header is found, we might want to check if the content *looks* like internship
            # But let's stick to headers for now.
            for h in internship_headers:
                 if line_clean.startswith(h) and len(line_clean) < len(h) + 10:
                     start_idx = i + 1
                     break

        # Check end
        if start_idx != -1:
            is_header = False
            for h in other_headers:
                if line_clean == h:
                    is_header = True
                    break
                
                if line_clean.startswith(h):
                    remainder = line_clean[len(h):].strip()
                    if not remainder or remainder in [':', '-', '|']:
                        is_header = True
                        break
                    if ' ' in h: 
                         if len(line_clean) < len(h) + 10:
                             is_header = True
                             break
                    else:
                        if len(line_clean.split()) <= 3: 
                            is_header = True
                            break

            if is_header:
                if len(line_clean) > 40: is_header = False
                if is_header:
                    end_idx = i
                    break
                
    if start_idx != -1:
        if end_idx == -1:
            end_idx = len(lines)
        
        section_lines = lines[start_idx:end_idx]
        while section_lines and not section_lines[0].strip():
            section_lines.pop(0)
        while section_lines and not section_lines[-1].strip():
            section_lines.pop()
            
        return "\n".join(section_lines).strip()
        
    return ""
