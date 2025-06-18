import requests

def test_end_to_end():
    url = "http://localhost:5000/submit_press_release"
    data = {
        "press_release": "Acme Corp announced a new product today.",
        "journalist_ids": ["journalist1"]
    }
    resp = requests.post(url, json=data)
    assert resp.status_code == 200
    result = resp.json()
    assert "objective_summary" in result
    assert "biased_summaries" in result
    assert "final_responses" in result