import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

matcher = PhraseMatcher(
    nlp.vocab,
    attr="LOWER"
)

# ---------------------------------------
# Load Skill Vocabulary
# ---------------------------------------

with open(
        "data/skills.txt",
        "r",
        encoding="utf-8"
) as f:

    skills = [

        line.strip()

        for line in f

        if line.strip()

    ]

patterns = [

    nlp.make_doc(skill)

    for skill in skills

]

matcher.add(
    "SKILLS",
    patterns
)

# ---------------------------------------
# Skill Extraction
# ---------------------------------------

def extract_skills(text: str):

    doc = nlp(text)

    matches = matcher(doc)

    found = set()

    for _, start, end in matches:

        found.add(

            doc[start:end].text

        )

    return sorted(found)