from typing import Dict
from .utils import clean_text
import openai
import os

def generate_objective_summary(text: str) -> str:
    prompt = f"Summarize the following press release objectively:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def generate_biased_summary(text: str, persona: Dict) -> str:
    prompt = (
        f"You are a journalist with the following profile:\n"
        f"Expertise: {persona.get('expertise_profile','')}\n"
        f"Sentiment: {persona.get('sentiment_analysis','')}\n"
        f"Topic preferences: {persona.get('expertise_profile', {}).get('topic_preferences','')}\n"
        f"Summarize the press release through your lens:\n{text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']