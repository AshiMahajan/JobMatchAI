# Architecture Decisions

---

## ADR-001

### Decision

Use `skills.txt` for skill detection.

### Why

Detection vocabulary can grow to thousands of skills without making the Knowledge Base difficult to maintain.

### Alternative Considered

Store all skills in `knowledge_base.json`.

### Rejected Because

The Knowledge Base should represent enriched knowledge (aliases, categories, relationships), not every detectable skill.

---

## ADR-002

### Decision

Keep `/analyze` deterministic.

### Why

Fast, reproducible ATS scoring.

### Alternative

LLM-powered extraction for every request.

### Rejected Because

Higher latency, API cost, and non-deterministic results.

---

## ADR-003

### Decision

Introduce an offline Knowledge Evolution Engine.

### Why

Allow the vocabulary and Knowledge Base to evolve with the job market without affecting runtime performance.

### Planned Implementation

CrewAI + LLM periodically analyzes fresh job descriptions, proposes updates to `skills.txt`, and suggests enrichments for `knowledge_base.json`.