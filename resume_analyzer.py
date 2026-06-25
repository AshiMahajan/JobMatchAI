# resume_analyzer.py

from section_parser import extract_sections
from skill_extractor import extract_skills


def analyze_resume(text):

    sections = extract_sections(text)

    results = {}

    for section_name, section_text in sections.items():

        results[section_name] = extract_skills(section_text)

    return results