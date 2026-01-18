import json
import os
from .nlp_processor import NLPProcessor
from spacy.matcher import PhraseMatcher

class SkillExtractor:
    def __init__(self, nlp_processor):
        self.nlp = nlp_processor.nlp
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.taxonomy = self._load_taxonomy()
        self._initialize_matcher()

    def _load_taxonomy(self):
        """Load skills taxonomy from JSON file"""
        try:
            # Look for data in local data directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            data_path = os.path.join(project_root, 'data', 'skills_taxonomy.json')
            
            with open(data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _initialize_matcher(self):
        """Initialize Spacy PhraseMatcher with skills"""
        for category, skills in self.taxonomy.items():
            patterns = [self.nlp.make_doc(text) for text in skills]
            self.matcher.add(category, patterns)

    def extract_skills(self, doc):
        """
        Extract skills from Spacy Doc object.
        Returns:
            dict: {category: [skills]}
            list: flat list of all unique skills
        """
        found_skills = {}
        all_skills_set = set()

        matches = self.matcher(doc)
        
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]  # Category
            span = doc[start:end]
            skill_name = span.text
            
            # Add to category
            if string_id not in found_skills:
                found_skills[string_id] = set()
            found_skills[string_id].add(skill_name)
            
            # Add to flat list
            all_skills_set.add(skill_name)

        # Convert sets to lists for JSON serialization
        final_skills = {k: list(v) for k, v in found_skills.items()}
        
        return final_skills, list(all_skills_set)
