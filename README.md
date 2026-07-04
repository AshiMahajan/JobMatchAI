# 🚀 JobMatch AI

> **An AI-powered Career Intelligence Platform for Resume Analysis, Skill Intelligence, and Career Growth.**

JobMatch AI is an open-source backend platform designed to go beyond traditional ATS (Applicant Tracking System) resume analyzers.

Instead of only telling users whether their resume matches a job description, JobMatch AI is being built to help professionals understand **why**, identify skill gaps, explore technology ecosystems, and continuously improve their career profile.

---

# ❓ The Problem

Most ATS tools answer only one question:

> **"Does my resume match this Job Description?"**

They rarely explain:

- Why the match is low
- Which skills are missing
- What technologies are commonly associated with a skill
- Which skills are currently in demand
- What should be learned next

JobMatch AI aims to solve these problems by combining deterministic ATS analysis with Career Intelligence.

---

# ✨ Current Features

### ✅ ATS Resume Analysis

- Upload resumes
- Compare resumes against Job Descriptions
- ATS match scoring
- Matched skill detection
- Missing skill identification
- Personalized recommendations

---

### ✅ Skill Extraction

Extract technical skills from Job Descriptions using a curated vocabulary.

---

### ✅ Skill Intelligence

Enrich detected skills with:

- Categories
- Aliases
- Parent skills
- Related technologies

---

### ✅ Knowledge Base

Separate:

- Skill Detection (`skills.txt`)
- Skill Intelligence (`knowledge_base.json`)

for better scalability and maintainability.

---

# 🛠️ Tech Stack

### Backend

- Python
- FastAPI

### NLP

- spaCy

### Data Validation

- Pydantic

### Future Integrations

- Docker
- AWS
- CrewAI
- Large Language Models (LLMs)

---

# 📈 Project Status

Current Version:

**v0.5 — Foundation Release**

Completed:

- ATS Engine
- Resume Parsing
- Skill Extraction
- Skill Intelligence
- Knowledge Base
- Unified Skill Pipeline

Currently Working On:

- Sprint 5.5 — Project Hardening

---

# 📚 Documentation

- 📖 [Architecture](docs/ARCHITECTURE.md)
- 🗺️ [Roadmap](ROADMAP.md)
- 📝 [Changelog](CHANGELOG.md)
- 🧠 [Architecture Decisions](docs/DECISIONS.md)
- 🔌 API Documentation *(coming soon)*
---

# 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/AshiMahajan/JobMatchAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the API

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

to explore the interactive Swagger API.

---

# 🎯 Vision

JobMatch AI is evolving into a **Career Intelligence Platform** capable of providing:

- ATS Resume Analysis
- Career Intelligence
- Resume Intelligence
- Market Trend Analysis
- Skill Gap Analysis
- Technology Ecosystem Mapping
- AI-assisted Knowledge Evolution

---

# 🤝 Contributing

Contributions, suggestions, and discussions are always welcome.

---

# 📜 License

This project is licensed under the MIT License.