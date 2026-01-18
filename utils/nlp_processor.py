import spacy
from spacy.matcher import PhraseMatcher
import re

class NLPProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            print("Downloading language model...")
            from spacy.cli import download
            download("en_core_web_md")
            self.nlp = spacy.load("en_core_web_md")

    def process_text(self, text):
        """
        Process text using Spacy pipeline.
        Returns: Doc object
        """
        # Clean text slightly before processing
        clean_text = re.sub(r'\s+', ' ', text).strip()
        return self.nlp(clean_text)

    def extract_entities(self, doc):
        """
        Extract standard entities like ORG, GPE, DATE, PERSON
        """
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        return entities

    def get_noun_chunks(self, doc):
        """
        Get noun chunks for potential implicit skills
        """
        return [chunk.text for chunk in doc.noun_chunks]
