from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import sqlite3
import json
from press_release_nlp.summarizer import generate_objective_summary, generate_biased_summary
from press_release_nlp.grader import grade_press_release
from rag_pipeline.index import search
from api.logger import get_logger

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
logger = get_logger()

SQLITE_PATH = os.getenv("SQLITE_PATH", "./db/journalists.sqlite")
CHROMADB_PATH = os.getenv("CHROMADB_PATH", "./db/chromadb")

def get_journalist_persona(journalist_id):
    conn = sqlite3.connect(SQLITE_PATH)
    c = conn.cursor()
    c.execute("SELECT persona_json FROM journalists WHERE journalist_id=?", (journalist_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_press_release", methods=["POST"])
def submit_press_release():
    data = request.json
    press_release = data["press_release"]
    journalist_ids = data["journalist_ids"]

    logger.info("Received press release submission")
    # 1. Objective summary
    objective_summary = generate_objective_summary(press_release)
    logger.info("Objective summary generated")

    biased_summaries = {}
    knowledge_base_insights = {}
    grades = {}
    final_responses = {}

    for jid in journalist_ids:
        persona = get_journalist_persona(jid)
        if not persona:
            continue
        # 2. Biased summary
        biased_summaries[jid] = generate_biased_summary(press_release, persona)
        # 3. RAG insights
        insights = search(press_release, jid, CHROMADB_PATH)
        knowledge_base_insights[jid] = insights
        # 4. Grading
        grades[jid] = grade_press_release(press_release, persona)
        # 5. Final response: LLM prompt
        from openai import ChatCompletion
        prompt = (
            f"Persona traits:\n{json.dumps(persona.get('content_analysis',{}))}\n"
            f"Objective summary: {objective_summary}\n"
            f"Biased summary: {biased_summaries[jid]}\n"
            f"Knowledge base insights: {insights}\n"
            "Compose your critical response as this journalist."
        )
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        final_responses[jid] = response['choices'][0]['message']['content']
        logger.info(f"Completed analysis for journalist {jid}.")

    return jsonify({
        "objective_summary": objective_summary,
        "biased_summaries": biased_summaries,
        "knowledge_base_insights": knowledge_base_insights,
        "grades": grades,
        "final_responses": final_responses
    })

@app.route("/journalists", methods=["GET"])
def get_journalists():
    conn = sqlite3.connect(SQLITE_PATH)
    c = conn.cursor()
    c.execute("SELECT journalist_id, name, persona_json FROM journalists")
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        persona = json.loads(row[2])
        result.append({
            "journalist_id": row[0],
            "name": row[1],
            "topic_preferences": persona.get("expertise_profile", {}).get("topic_preferences", []),
            "coverage_areas": persona.get("geographic_profile", {}).get("coverage_areas", []),
            "fairness_index": persona.get("crisis_management_profile", {}).get("fairness_index", None)
        })
    return jsonify(result)

# For serving static files (CSS, JS) in frontend
@app.route('/static/<path:filename>')
def frontend_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)