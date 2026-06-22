# section_parser.py

import re

SECTION_HEADERS = {
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "technologies"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience"
    ],

    "projects": [
        "projects",
        "personal projects"
    ],

    "education": [
        "education"
    ],

    "certifications": [
        "certifications",
        "certificates"
    ]
}


def identify_section(line):

    clean = line.strip().lower()

    for section, headers in SECTION_HEADERS.items():

        if clean in headers:
            return section

    return None


def extract_sections(text):

    sections = {}

    current_section = "general"

    sections[current_section] = []

    for line in text.splitlines():

        section = identify_section(line)

        if section:
            current_section = section

            if current_section not in sections:
                sections[current_section] = []

            continue

        sections[current_section].append(line)

    return {
        key: "\n".join(value).strip()
        for key, value in sections.items()
    }