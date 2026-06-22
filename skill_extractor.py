import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

with open("data/skills.txt", "r", encoding="utf-8") as f:
    skills = [line.strip().lower() for line in f if line.strip()]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

patterns = [nlp.make_doc(skill) for skill in skills]

matcher.add("SKILLS", patterns)

def extract_skills(text):
    doc = nlp(text)

    matches = matcher(doc)

    found_skills = set()

    for match_id, start, end in matches:
        skill = doc[start:end].text.lower()
        found_skills.add(skill)

    return sorted(found_skills)