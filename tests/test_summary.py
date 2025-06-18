import pytest
from press_release_nlp.summarizer import generate_objective_summary, generate_biased_summary

def test_objective_summary():
    text = "Acme Corp announced a new product today."
    summary = generate_objective_summary(text)
    assert isinstance(summary, str)
    assert len(summary) > 0

def test_biased_summary():
    text = "Acme Corp announced a new product today."
    persona = {"expertise_profile": {}, "sentiment_analysis": {}, "topic_preferences": []}
    summary = generate_biased_summary(text, persona)
    assert isinstance(summary, str)
    assert len(summary) > 0