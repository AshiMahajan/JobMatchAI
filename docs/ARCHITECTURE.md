# 🏗️ JobMatch AI Architecture

## Overview

JobMatch AI is a modular backend platform designed to evolve from a traditional ATS (Applicant Tracking System) resume analyzer into a complete **Career Intelligence Platform**.

The architecture separates **skill detection**, **skill intelligence**, and **ATS analysis** into independent layers. This allows the system to remain deterministic, scalable, and easy to extend as new capabilities such as Career Intelligence, Resume Intelligence, and AI-assisted Knowledge Evolution are introduced.

---

# Design Principles

The architecture follows these principles:

- Single Responsibility Principle
- Modular Service Architecture
- Separation of Detection and Intelligence
- Deterministic ATS Analysis
- Extensible Knowledge Layer
- Offline AI-assisted Knowledge Evolution

---

# High-Level Architecture

![JobMatch AI Architecture](IMAGES/architecture_overview.png)

---

# Core Components

## Resume Service

### Responsibilities

- Parse uploaded resumes
- Extract resume text
- Generate canonical resume skills using the Skill Service

---

## Skill Extractor

### Responsibilities

- Detect technical skills from resumes and Job Descriptions
- Uses only `skills.txt`
- Performs detection only
- Does not perform categorization or normalization

### Input

- Resume Text
- Job Description

### Output

Example

```
Python
AWS
Docker
SQL
```

---

## Skill Engine

### Responsibilities

- Normalize detected skills
- Resolve aliases
- Enrich skills using the Knowledge Base
- Return canonical skill information
- Provide categories
- Provide related technologies

Example

```
Python

↓

Programming Language

↓

Related

FastAPI
Flask
TensorFlow
PyTorch
```

---

## Skill Service

The Skill Service acts as the orchestration layer between skill detection and skill intelligence.

### Responsibilities

- Invoke Skill Extractor
- Normalize detected skills
- Enrich skills
- Return canonical skill information

Every module within JobMatch AI interacts with skills through the Skill Service.

---

## ATS Engine

### Responsibilities

- Compare Resume Skills
- Compare Job Description Skills
- Calculate ATS Match Score
- Identify Matched Skills
- Identify Missing Skills
- Generate Recommendations

The ATS Engine is deterministic and does not depend on LLMs.

---

# Data Layer

## skills.txt

### Purpose

Acts as the project's skill vocabulary.

### Responsibilities

- Detect skills from text
- Fast vocabulary lookup
- Easy to expand

This file contains **only detectable skills** and no additional metadata.

---

## knowledge_base.json

### Purpose

Stores enriched information about known skills.

Example information

- Categories
- Aliases
- Parent Skills
- Related Technologies

The Knowledge Base is responsible for understanding skills, not detecting them.

---

## missing_skills.json

### Purpose

Tracks manually queried skills that are currently unknown to the Knowledge Base.

These entries can later be reviewed and incorporated into the Knowledge Base.

---

# Runtime Data Flow

## Resume Analysis (/analyze)

Resume PDF

↓

Resume Service

↓

Resume Text

↓

Skill Service

↓

Skill Extractor

↓

skills.txt

↓

Canonical Resume Skills

──────────────

Job Description

↓

Skill Service

↓

Skill Extractor

↓

skills.txt

↓

Canonical JD Skills

──────────────

ATS Engine

↓

ATS Score

Matched Skills

Missing Skills

Recommendations

---

## JD Skill Extraction (/extract-jd-skills)

Job Description

↓

Skill Service

↓

Skill Extractor

↓

skills.txt

↓

Detected Skills

↓

Skill Engine

↓

knowledge_base.json

↓

Enriched Skills

---

# Current Features

Current implementation includes:

- Resume Parsing
- Resume Skill Extraction
- Job Description Skill Extraction
- Skill Intelligence
- ATS Resume Matching
- Recommendation Engine
- Market Analysis
- Knowledge Base

---

# Future Architecture

## Career Intelligence

Planned capabilities

- Skill Details
- Technology Ecosystem
- Learning Roadmaps
- Market Demand
- Career Guidance
- Role Intelligence

---

## Resume Intelligence

Planned capabilities

- Hidden Skill Detection
- Resume Improvements
- Resume Optimization
- Resume Strength Analysis

---

## Knowledge Evolution Engine

The Knowledge Evolution Engine is designed as an **offline subsystem**.

Unlike runtime APIs, it is responsible for continuously improving JobMatch AI's vocabulary and Knowledge Base.

Planned workflow:

- Collect fresh Job Descriptions
- Analyze market trends
- Extract emerging technologies
- Compare with existing vocabulary
- Suggest new skills
- Suggest Knowledge Base enrichments

The runtime APIs remain deterministic and do not rely on LLMs.

---

# Responsibilities Summary

| Component | Responsibility |
|------------|----------------|
| Resume Service | Parse resumes and extract resume text |
| Skill Extractor | Detect known skills from text |
| Skill Engine | Normalize and enrich detected skills |
| Skill Service | Orchestrate extraction and enrichment |
| ATS Engine | Compare resume and JD skills |
| Knowledge Base | Store skill intelligence |
| Knowledge Evolution Engine | Keep vocabulary and knowledge updated |

---

# Architectural Decisions

The architecture intentionally separates:

## Skill Detection

Responsible for answering:

> **"Which known skills are present in this text?"**

Implemented using:

- `skills.txt`
- Skill Extractor

---

## Skill Intelligence

Responsible for answering:

> **"What do we know about this skill?"**

Implemented using:

- Skill Engine
- `knowledge_base.json`

---

## Knowledge Evolution

Responsible for answering:

> **"Which new technologies should JobMatch AI learn?"**

This is implemented as an offline AI-assisted pipeline using CrewAI and Large Language Models.

The runtime API is intentionally isolated from this process to ensure fast, deterministic, and reproducible ATS analysis.

---

# Guiding Philosophy

JobMatch AI separates **skill detection** from **skill intelligence**.

Detection should remain:

- Fast
- Lightweight
- Deterministic

Intelligence should remain:

- Rich
- Extensible
- Continuously evolving

This separation allows the platform to deliver reliable ATS analysis today while continuously improving its understanding of the technology landscape over time.