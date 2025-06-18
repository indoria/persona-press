import json
from datetime import datetime

def build_persona_json(extracted_data: dict, base_schema: dict) -> dict:
    persona = base_schema.copy()
    persona['metadata']['created_at'] = datetime.utcnow().isoformat()
    persona['metadata']['confidence_level'] = 0.9
    persona['expertise_profile']['primary_beats'] = extracted_data.get("beats", [])
    persona['geographic_profile']['coverage_areas'] = extracted_data.get("coverage_areas", [])
    persona['relationship_tracking'] = extracted_data.get("relationship_tracking", {})
    # ...fill other fields as desired
    return persona

def save_persona_json(persona: dict, path: str):
    with open(path, "w") as f:
        json.dump(persona, f, indent=2)