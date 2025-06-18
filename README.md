# PersonaPress

**PersonaPress** is an enterprise-grade AI platform for press release analysis, powered by retrieval-augmented generation (RAG) and a rich ecosystem of journalist personas. Upload a press release and receive nuanced critiques, summaries, and insights from AI personas—each with their own beats, writing styles, and knowledge bases.

---

## System Overview

- **Upload:** Users submit a press release.
- **Persona Analysis:** AI journalist personas analyze and respond, drawing on their unique knowledge, sentiment, and style.
- **RAG:** Persona-specific retrieval from ChromaDB with OpenAI LLMs via LangChain.
- **Evaluation:** Each persona grades, summarizes, and comments on the release.

---

## Tech Stack

- **Frontend:** Vanilla JS, HTML, CSS
- **Backend:** Python (Flask), spaCy, OpenAI, LangChain, ChromaDB, SQLite3
- **Testing & Logging:** Python logging, `unittest`/`pytest`

---

## Folder Structure

```
/press_release_nlp/
  summarizer.py
  grader.py
  utils.py
/rag_pipeline/
  chunking/
    fixed_length.py
    sentence_aware.py
    topic_aware.py
  embedding/
    openai_embedder.py
    base.py
  index.py
  ingest.py
/persona_generator/
  extractor.py
  builder.py
/db/
  init_db.py
  populate_personas.py
  create_embeddings.py
  journalists/
    schema/
    corpus/
/api/
  routes.py
  logger.py
/tests/
  test_end_to_end.py
  test_summary.py
  test_rag.py
  test_grader.py
```

---

## Key Pipeline

1. **Upload:** User submits a press release.
2. **Summarization:** 
   - Objective summary.
   - Biased summary per journalist persona (based on their expertise, sentiment, and preferences).
3. **RAG:** 
   - Persona-specific retrieval from ChromaDB (LangChain).
   - Query over each journalist's indexed corpus.
4. **Grading:** 
   - Each persona grades the press release (clarity, credibility, relevance) using persona-specific weights.
5. **Composition:** 
   - Final response crafted by OpenAI LLM, combining summaries, knowledge, and persona traits.

---

## API

### `POST /submit_press_release`

#### Input:
- `press_release` (str, required)
- `journalist_ids` (list of str, required)

#### Response:
```json
{
  "objective_summary": "...",
  "biased_summaries": {
    "journalist_1": "...",
    "journalist_2": "..."
  },
  "knowledge_base_insights": {
    "journalist_1": ["fact1", "quote1", "incident1"],
    "journalist_2": ["stat1", "event2"]
  },
  "grades": {
    "journalist_1": {
      "credibility": 82,
      "clarity": 74,
      "relevance": 90
    }
  },
  "final_responses": {
    "journalist_1": "LLM-composed critique...",
    "journalist_2": "Persona-aligned reaction..."
  }
}
```

### `GET /journalists`
- Returns list of journalist personas and their metadata.

---

## Components

### `/press_release_nlp/`
- **summarizer.py**: Generates objective and persona-biased summaries.
- **grader.py**: Grades press releases per persona's profile.
- **utils.py**: Text cleaning, tokenization, NER (spaCy).

### `/rag_pipeline/`
- **chunking/**: Strategies for splitting text.
- **embedding/**: Embedding interfaces (default: OpenAI).
- **index.py**: ChromaDB index management.
- **ingest.py**: Corpus ingestion and indexing.

### `/persona_generator/`
- **extractor.py**: Extracts persona traits from text.
- **builder.py**: Builds persona JSON files conforming to schema.

### `/db/`
- **init_db.py**: Initializes SQLite DB.
- **populate_personas.py**: Loads and fills persona schema.
- **create_embeddings.py**: Embeds journalist corpora into ChromaDB.

### `/api/`
- **routes.py**: Flask API endpoints.
- **logger.py**: Structured logging.

### `/tests/`
- Unit and end-to-end tests for all major components.

---

## Persona Schema

See `/db/journalists/schema/` for the full JSON schema.

---

## Setup

1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Initialize DB and embeddings**
   ```bash
   python db/init_db.py
   python db/populate_personas.py
   python db/create_embeddings.py
   ```

3. **Run the API**
   ```bash
   python -m app.routes
   ```

4. **Run tests**
   ```bash
   pytest tests/
   ```

---

## Notes

- All journalist corpora are in `.txt` files.
- Each processing stage is logged.
- The frontend will render persona traits for transparency.

---

## License

Enterprise/Proprietary – internal use only.

```