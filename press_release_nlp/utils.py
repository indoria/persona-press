import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    return " ".join(text.split())

def tokenize(text: str):
    doc = nlp(text)
    return [token.text for token in doc]

def get_named_entities(text: str):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]