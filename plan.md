# PersonaPress: Step-by-Step System Creation Plan

This plan provides a structured, actionable sequence for building PersonaPress as specified. It covers scaffolding, core code, and test stubs for each module.

---

## 1. Project Scaffolding

- Create the directory and file structure as described.
- Add minimal `__init__.py` files for module recognition.
- Add a `requirements.txt` for all dependencies.
- Add a placeholder `.env` for OpenAI API keys/configs.

---

## 2. Core Libraries & Utilities

- Implement `/press_release_nlp/utils.py`:
  - Text cleaning, tokenization, NER using spaCy.

- Implement logging setup in `/api/logger.py`.

---

## 3. NLP Modules

- `/press_release_nlp/summarizer.py`:
  - `generate_objective_summary(text: str) -> str`
  - `generate_biased_summary(text: str, persona: Dict) -> str`

- `/press_release_nlp/grader.py`:
  - `grade_press_release(text: str, persona: Dict) -> Dict[str, int]`

---

## 4. Persona Generation

- `/persona_generator/extractor.py`:
  - NLP extraction of places, people, beats, mapped to persona schema.

- `/persona_generator/builder.py`:
  - Build persona JSONs compliant with schema, auto-filling metadata.

---

## 5. Database

- `/db/init_db.py`:
  - Create SQLite DB and tables from schema.

- `/db/populate_personas.py`:
  - Load persona JSONs into DB, fill missing fields via extractor.

---

## 6. RAG Pipeline

- `/rag_pipeline/chunking/`:
  - Implement fixed-length, sentence-aware, and topic-aware chunkers.

- `/rag_pipeline/embedding/`:
  - OpenAI embedder (default).
  - `base.py` for alternative pluggable embedders.

- `/rag_pipeline/ingest.py`:
  - Ingest and index journalist corpora as vectors with ChromaDB.

- `/rag_pipeline/index.py`:
  - `search(query: str, journalist_id: str) -> List[str]`

---

## 7. API

- `/api/routes.py`:
  - `POST /submit_press_release`
  - `GET /journalists`

---

## 8. Testing

- `/tests/`:
  - Create test stubs for E2E, summarizer, RAG, grader.

---

## 9. Frontend

- Scaffold HTML/JS/CSS for:
  - Upload form
  - Persona selection
  - Results display (including persona introspection)

---

## 10. Integration & Logging

- Integrate all flows.
- Ensure logging at each processing stage.

---

## 11. Documentation

- Provide clear README.
- Comment code for clarity.

---

## 12. Final Review

- Run all tests.
- Verify system end-to-end.

---