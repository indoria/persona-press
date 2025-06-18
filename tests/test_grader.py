from press_release_nlp.grader import grade_press_release

def test_grade_press_release():
    text = "Acme Corp announced a new product today."
    persona = {}
    grades = grade_press_release(text, persona)
    assert all(0 <= v <= 100 for v in grades.values())