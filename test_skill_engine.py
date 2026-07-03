from skill_engine import SkillEngine

engine = SkillEngine()

skills = [

    "python3",

    "Amazon Web Services",

    "tf",

    "k8s",

    "docker"
]

print()

for skill in skills:

    print("=" * 60)

    print("Input :", skill)

    print("Canonical :", engine.normalize(skill))

    print("Description :")

    print(engine.describe(skill))

    print("Parent :", engine.infer_parent_skill(skill))

    print("Related :", engine.related_skills(skill))