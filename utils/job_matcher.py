import json
import os
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    def __init__(self):
        self.job_roles = self._load_job_roles()
        self.models_loaded = False
        self.vectorizer = None
        self.job_vectors = None
        self.job_titles = []
        
        # Try to load pre-trained models
        self._load_models()

    def _load_job_roles(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_path = os.path.join(project_root, 'data', 'job_roles.json')
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def _load_models(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            models_dir = os.path.join(project_root, 'models')
            
            # Load vectorizer if exists
            vec_path = os.path.join(models_dir, 'skill_vectorizer.pkl')
            matrix_path = os.path.join(models_dir, 'job_skills_matrix.pkl')
            
            if os.path.exists(vec_path) and os.path.exists(matrix_path):
                self.vectorizer = joblib.load(vec_path)
                self.job_vectors = joblib.load(matrix_path)
                self.models_loaded = True
                self.job_titles = list(self.job_roles.keys())
        except Exception as e:
            print(f"Could not load ML models: {e}. Using rule-based fallback.")

    def match_jobs(self, extracted_skills, target_role=None):
        """
        Calculate job matches based on extracted skills.
        If target_role is provided, ensures it is included and prioritized.
        """
        matches = []
        
        # Method 1: ML-based strict matching (Cosine Similarity) - with error handling
        if self.models_loaded and len(extracted_skills) > 0:
            try:
                skill_text = " ".join(extracted_skills)
                user_vector = self.vectorizer.transform([skill_text])
                cosine_sims = cosine_similarity(user_vector, self.job_vectors).flatten()
                
                for i, score in enumerate(cosine_sims):
                    matches.append({
                        "job_title": self.job_titles[i],
                        "score": round(score * 100, 1),
                        "method": "ML"
                    })
            except Exception as e:
                # ML model failed, fall back to rule-based matching
                print(f"ML matching failed: {e}. Using rule-based matching.")
                self.models_loaded = False  # Disable ML for future calls
        
        # Method 2: Rule-based Weighted Matching (Fallback or Hybrid)
        # We calculate this anyway to get missing skills details
        rule_matches = []
        for role_name, role_data in self.job_roles.items():
            req_skills = [s.lower() for s in role_data['required_skills']]
            user_skills = [s.lower() for s in extracted_skills]
            
            matched = [s for s in req_skills if s in user_skills]
            missing = [s for s in req_skills if s not in user_skills]
            weights = role_data.get('weights', {})
            
            # Calculate weighted score
            score = 0
            total_weight = 0
            for skill in req_skills:
                # Default weight 1 if not specified, find actual case-sensitive key
                w = 1
                for k, v in weights.items():
                    if k.lower() == skill:
                        w = v
                        break
                
                total_weight += w
                if skill in user_skills:
                    score += w
            
            final_percentage = (score / total_weight * 100) if total_weight > 0 else 0
            
            # Penalize generic roles slightly to favor specific matches
            # If the role is generic, reduce score by 10% (multiply by 0.9)
            generic_roles = ["Software Engineer", "Software Developer", "Software Test Engineer", "Programmer"]
            if role_name in generic_roles:
                final_percentage *= 0.9
            
            rule_matches.append({
                "job_title": role_name,
                "score": round(final_percentage, 1),
                "matched_skills": matched,
                "missing_skills": missing,
                "description": role_data.get("description", "")
            })
            
        # If ML failed, use rule matches. If ML worked, valid logic would be to combine them.
        # For simplicity in this v1, we return the detailed rule-based matches matches 
        # but sorted by score
        
        sorted_matches = sorted(rule_matches, key=lambda x: x['score'], reverse=True)
        
        # --- TARGET ROLE PRIORITIZATION ---
        if target_role:
            target_role_lower = target_role.lower()
            target_match = None
            
            # Find the target role in the results
            for match in sorted_matches:
                if match['job_title'].lower() == target_role_lower:
                    target_match = match
                    break
            
            # If not found directly, try fuzzy match (simple containment)
            if not target_match:
                for match in sorted_matches:
                    if target_role_lower in match['job_title'].lower():
                        target_match = match
                        break
            
            if target_match:
                # Remove it from its current position
                sorted_matches.remove(target_match)
                # Mark it as target
                target_match['is_target'] = True
                # Insert at the very top (Index 0)
                sorted_matches.insert(0, target_match)
                
        return sorted_matches

    def analyze_projects(self, project_text, extracted_skills):
        """
        Analyze the projects section to provide detailed per-project feedback.
        Returns a list of project analysis objects.
        """
        if not project_text:
            return []

        # 1. Split Text into Individual Projects (Heuristic)
        import re
        
        # Normalize newlines
        text = project_text.replace('\r\n', '\n')
        
        # Heuristic: distinct projects often separated by double newlines or bullet points at start of line
        raw_projects = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 20]
        
        # If still 1 big block, try to split by lines that look like titles (short, capitalized) if followed by detail
        if len(raw_projects) <= 1:
            lines = text.split('\n')
            current_proj = []
            new_projects = []
            
            for line in lines:
                l = line.strip()
                if not l: continue
                
                # Heuristic 1: Line is short, capitalized, and looks like a title
                is_title_candidate = len(l) < 80 and l[0].isupper()
                # Heuristic 2: Line contains a pipe separator
                has_pipe = " | " in l
                # Heuristic 3: Line starts with project keywords
                starts_keyword = any(l.lower().startswith(k) for k in ["project", "title:", "system:"])
                
                # Heuristic 4: Bullet point logic (Crucial for splitting)
                is_bullet = l.startswith(('•', '-', '*', '1.', '2.', '3.'))
                
                # Heuristic 5: Previous block was substantial enough (> 2 lines) OR empty
                prev_proj_substantial = len(current_proj) >= 2
                
                is_new_start = False
                
                if has_pipe or starts_keyword:
                    is_new_start = True
                elif is_title_candidate and not is_bullet:
                    # If previous project has content, this might be a new title
                    if prev_proj_substantial or not current_proj:
                        is_new_start = True
                    # If current project is just 1 short line (maybe a previous false start title), treat this as continuation or new?
                    # Let's assume new start if it looks like a strong title
                    elif len(current_proj) == 1 and len(current_proj[0]) < 40:
                         # Ambiguous. But if previous line didn't end with punctuation and this one is Title Case...
                         pass

                # Force split on numbered lists if they look like project headers (e.g. "1. Project Name")
                if l[0].isdigit() and '.' in l[:3] and len(l) < 60:
                     is_new_start = True

                # Special case check: don't split if it's the very first line
                if not current_proj and not new_projects:
                    is_new_start = False

                if is_new_start and current_proj:
                    new_projects.append("\n".join(current_proj))
                    current_proj = [line]
                else:
                    current_proj.append(line)
            
            if current_proj:
                new_projects.append("\n".join(current_proj))
            
            # Filter garbage (reduced threshold)
            new_projects = [p for p in new_projects if len(p.strip()) > 15] # Reduced from 30
            
            if len(new_projects) > 1:
                raw_projects = new_projects

        # If splitting completely failed but text is long, default to single block
        if not raw_projects and len(project_text) > 50:
            raw_projects = [project_text]
            
        # [FIX] Deduplicate if the fallback strategy (re-splitting) appended to existing
        unique_projects = []
        seen_content = set()
        for p in raw_projects:
             norm = p.strip().lower()[:100] 
             if norm not in seen_content:
                  seen_content.add(norm)
                  unique_projects.append(p)
        raw_projects = unique_projects

        analysis_results = []

        for idx, p_text in enumerate(raw_projects):
            # Extract Title
            lines = p_text.split('\n')
            title = lines[0].strip()
            # If title is just a bullet or number, remove it
            title = re.sub(r'^[\*\-•\d\.\)]+\s*', '', title)
            # Remove trailing colons
            title = title.strip(':')
            
            if len(title) > 60: title = title[:60] + "..."
            
            description = " ".join([l.strip() for l in lines[1:]]) if len(lines) > 1 else p_text
            
            # Identify skills
            p_skills = [s for s in extracted_skills if s.lower() in p_text.lower()]
            
            # --- Analysis Logic ---
            
            # 1. Summary
            summary = f"A {len(p_skills)}-tech stack project."
            if "api" in p_text.lower(): summary = "API-driven backend system."
            elif "react" in p_text.lower() or "css" in p_text.lower(): summary = "Frontend user interface application."
            elif "data" in p_text.lower() or "model" in p_text.lower(): summary = "Data science / ML implementation."
            
            # 2. Advantages (Pros)
            advantages = []
            if len(p_skills) >= 3: advantages.append(f"Strong Tech Stack: Integrates {', '.join(p_skills[:3])}.")
            if any(k in p_text.lower() for k in ['users', 'clients', 'customers']): advantages.append("User-Centric: Addresses real-world user needs.")

            if any(k in p_text.lower() for k in ['fast', 'efficient', 'optimized', 'performance']): advantages.append("Performance: Focus on efficiency and optimization.")
            if any(k in p_text.lower() for k in ['secure', 'auth', 'protection']): advantages.append("Security: Implements security best practices.")
            if not advantages: advantages.append("Solid technical implementation.")

            # 3. Disadvantages (Cons / Improvements)
            disadvantages = []
            if not any(k in p_text.lower() for k in ['test', 'testing', 'unit', 'ci/cd']): disadvantages.append("No testing strategy mentioned (Unit/Integration tests).")
            if not any(k in p_text.lower() for k in ['deploy', 'hosted', 'aws', 'cloud', 'live']): disadvantages.append("Deployment status unclear (is it live?).")
            if not any(k in p_text.lower() for k in ['metric', 'kpi', 'result', 'improved by']): disadvantages.append("Lacks quantifiable impact metrics (e.g., 'improved X by Y%').")
            
            # 4. Role Relevance
            relevant_roles = set()
            for role_name, role_data in self.job_roles.items():
                req_skills = set(s.lower() for s in role_data['required_skills'])
                matched_proj_skills = set(s.lower() for s in p_skills).intersection(req_skills)
                if len(matched_proj_skills) >= 1:
                    relevant_roles.add(role_name)
            
            # Pick top 3 most relevant based on overlap count
            sorted_roles = sorted(list(relevant_roles), key=lambda r: len(set(self.job_roles[r]['required_skills']).intersection(set(p_text.lower().split()))), reverse=True)

            # Role detected (Restored)
            role_inferred = "Contributor / Developer"
            if "lead" in p_text.lower() or "led" in p_text.lower() or "managed" in p_text.lower():
                role_inferred = "Team Lead / Manager"
            elif "architect" in p_text.lower() or "designed" in p_text.lower():
                role_inferred = "System Architect / Core Developer"
            elif "support" in p_text.lower() or "maintained" in p_text.lower():
                role_inferred = "Maintenance & Support"

            # 5. Project Scoring & Tiering
            score = 60 # Base Score
            
            # Tech Stack Points (Max 20)
            score += min(len(p_skills) * 4, 20)
            
            # Impact Points (Max 10)
            if any(k in p_text.lower() for k in ['%', 'improved', 'increased', 'reduced', 'saved']):
                score += 10
            
            # Methodology Points (Max 10)
            if any(k in p_text.lower() for k in ['agile', 'scrum', 'kanban', 'ci/cd', 'testing']):
                score += 10
                
            # Role Points (Max 5)
            if role_inferred != "Contributor / Developer":
                score += 5
            
            # Tier Calculation
            if score >= 90: tier = "S"
            elif score >= 85: tier = "A"
            elif score >= 75: tier = "B"
            else: tier = "C"

            analysis_results.append({
                "name": title if len(title) > 3 else f"Project {idx + 1}",
                "summary": summary,
                "description": description[:200] + "..." if len(description) > 200 else description,
                "advantages": advantages,
                "disadvantages": disadvantages,
                "relevance": sorted_roles[:3],
                "tech_stack": p_skills,
                "score": score,
                "tier": tier
            })

        return analysis_results

    def analyze_internships(self, internship_text, extracted_skills):
        """
        Analyze internship/training section text.
        """
        if not internship_text:
            return []

        # 1. Normalize and Split (Reuse some logic from projects, but adapted)
        # Often internships are listed like:
        # "Role at Company (Date)"
        # "• Detail 1"
        import re
        text = internship_text.replace('\r\n', '\n')
        
        # Split by blocks that look like new entries
        # HEURISTIC: A line that is NOT a bullet, is Title Case, and has a date or location might be a header
        
        lines = text.split('\n')
        entries = []
        current_entry = []
        
        for line in lines:
            l = line.strip()
            if not l: continue
            
            is_bullet = l.startswith(('•', '-', '*', '1.', '>'))
            
            # Potential Header Detection:
            # - Not a bullet
            # - Has Company/Role keywords OR Dates
            # - Not too long
            is_header = False
            if not is_bullet:
                # Check for date patterns roughly (e.g. 2023, Jan '22, present)
                has_date = bool(re.search(r'\b(19|20)\d\d\b', l) or re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', l, re.I))
                if has_date or len(current_entry) > 2:
                    is_header = True
            
            if not current_entry:
                is_header = False # First line is always start
                
            if is_header and current_entry:
                entries.append("\n".join(current_entry))
                current_entry = [line]
            else:
                current_entry.append(line)
                
        if current_entry:
            entries.append("\n".join(current_entry))
            
        # Refine entries - remove short garbage
        entries = [e for e in entries if len(e) > 20]
        
        # fallback if single block
        if not entries and len(internship_text) > 30:
            entries = [internship_text]

        results = []
        for entry in entries:
            # Extract Role & Company
            first_line = entry.split('\n')[0].strip()
            role = "Intern / Trainee"
            company = "Unknown Company"
            
            # Simple heuristic: Split by 'at', ' in ', '|', ','
            separators = [' at ', ' in ', ' | ', ',', '@']
            for sep in separators:
                if sep in first_line:
                    parts = first_line.split(sep)
                    # Guess: Role usually first? "Software Intern at Google"
                    if len(parts) >= 2:
                        role = parts[0].strip()
                        company = parts[1].strip()
                        # Clean up company (remove date)
                        company = re.sub(r'\b(19|20)\d\d.*', '', company).strip(' ()-')
                        break
            
            if role == "Intern / Trainee" and len(first_line) < 50:
                role = first_line # Assume the whole line is the header
            
            # Skills used
            skills_used = [s for s in extracted_skills if s.lower() in entry.lower()]
            
            # Key Learnings (from bullets)
            description_lines = [line.strip().lstrip('•-* ') for line in entry.split('\n')[1:] if len(line.strip()) > 10]
            summary = " ".join(description_lines[:2]) if description_lines else entry[len(first_line):].strip()[:150] + "..."

            # Classification Logic
            entry_lower = entry.lower()
            role_lower = role.lower()
            
            # Default to Internship
            entry_type = "Internship"
            
            if any(k in entry_lower for k in ['in-plant', 'training', 'workshop', 'course', 'vocational', 'seminar', 'certification']):
                entry_type = "Training"
            elif "intern" in role_lower:
                entry_type = "Internship"
            elif "trainee" in role_lower: # Ambiguous, but usually training/internship
                 pass 

            results.append({
                "role": role,
                "company": company,
                "summary": summary,
                "skills_used": skills_used,
                "full_text": entry,
                "type": entry_type
            })
            
        return results
