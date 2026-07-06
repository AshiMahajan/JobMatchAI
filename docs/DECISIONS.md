# 🧠 Architecture Decisions

This document records important architectural decisions made during the development of JobMatch AI.

---

# ADR-001

## Decision

Use `skills.txt` as the skill detection vocabulary.

## Why

Skill detection should remain:

- Fast
- Deterministic
- Lightweight

## Alternative Considered

Store every detectable skill inside `knowledge_base.json`.

## Rejected Because

The Knowledge Base should focus on skill intelligence rather than vocabulary.

---

# ADR-002

## Decision

Separate Skill Detection from Skill Intelligence.

## Why

Detection and enrichment solve different problems.

Detection answers:

> Which skills exist?

Intelligence answers:

> What do we know about those skills?

---

# ADR-003

## Decision

Introduce the Skill Service.

## Why

Every module should use a single skill pipeline.

Benefits

- Reduced duplicate code
- Consistent normalization
- Easier maintenance

---

# ADR-004

## Decision

Keep the ATS Engine deterministic.

## Why

ATS analysis should produce identical results for identical inputs.

## Alternative Considered

Use an LLM during runtime.

## Rejected Because

- Higher latency
- Higher cost
- Non-deterministic output
- External dependency

---

# ADR-005

## Decision

Knowledge Evolution runs offline.

## Why

Runtime APIs should remain independent of AI services.

CrewAI and LLMs will periodically:

- Analyze fresh Job Descriptions
- Discover emerging technologies
- Suggest vocabulary updates
- Suggest Knowledge Base enrichments

---

# ADR-006

## Decision

Separate runtime from learning.

Runtime Responsibilities

- ATS Analysis
- Resume Parsing
- Skill Extraction
- Skill Intelligence

Offline Responsibilities

- Market Analysis
- Vocabulary Expansion
- Knowledge Base Evolution

---

# ADR-007

## Decision

Use a modular service architecture.

Services

- Resume Service
- Skill Service
- ATS Service
- Market Analysis Service

Benefits

- Loose coupling
- Easier testing
- Better scalability
- Clear responsibilities

---

# ADR-008

## Decision

JobMatch AI is a Career Intelligence Platform.

## Why

Traditional ATS tools only answer:

> Does my resume match?

JobMatch AI aims to answer:

- Why?
- What skills are missing?
- What should I learn?
- How is the market changing?
- Which technologies are related?

This vision guides all future architectural decisions.