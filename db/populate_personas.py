import os
import json
import sqlite3
from persona_generator.extractor import extract_coverage_areas, extract_people, extract_beats

def populate(db_path, schema_dir):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for fname in os.listdir(schema_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(schema_dir, fname)
        with open(path) as f:
            persona = json.load(f)
        # Fill missing fields using extractor (dummy for now)
        corpus_path = f"./db/journalists/corpus/{persona['journalist_id']}/"
        text = ""
        if os.path.exists(corpus_path):
            for file in os.listdir(corpus_path):
                with open(os.path.join(corpus_path, file)) as cf:
                    text += cf.read() + "\n"
        # Extract and fill
        persona['geographic_profile']['coverage_areas'] = extract_coverage_areas(text)
        persona['expertise_profile']['primary_beats'] = extract_beats(text)
        # Save to DB
        c.execute("INSERT OR REPLACE INTO journalists (journalist_id, name, persona_json) VALUES (?, ?, ?)",
                  (persona['journalist_id'],
                   persona['basic_info']['name']['display'],
                   json.dumps(persona)))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate("./db/journalists.sqlite", "./db/journalists/schema")