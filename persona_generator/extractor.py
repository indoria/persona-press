import spacy

nlp = spacy.load("en_core_web_sm")

def extract_coverage_areas(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
    return list(set(locations))

def extract_people(text):
    doc = nlp(text)
    people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return list(set(people))

def extract_beats(text):
    # Dummy: look for keywords
    beats = []
    keywords = ["politics", "sports", "business", "health", "science", "technology", "entertainment", "crime"]
    for k in keywords:
        if k in text.lower():
            beats.append(k)
    return beats