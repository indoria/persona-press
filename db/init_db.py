import sqlite3
import json
import os

def load_schema(path):
    with open(path) as f:
        return json.load(f)

def create_tables_from_schema(schema_file, db_path):
    schema = load_schema(schema_file)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Example: create a journalists table with basic fields
    c.execute('''
    CREATE TABLE IF NOT EXISTS journalists (
        journalist_id TEXT PRIMARY KEY,
        name TEXT,
        persona_json TEXT
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    SCHEMA_FILE = "./db/journalists/schema/sample_schema.json"
    DB_PATH = "./db/journalists.sqlite"
    create_tables_from_schema(SCHEMA_FILE, DB_PATH)