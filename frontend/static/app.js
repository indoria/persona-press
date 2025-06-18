document.addEventListener("DOMContentLoaded", function () {
    const personaListDiv = document.getElementById("persona-list");
    const form = document.getElementById("press-release-form");
    const resultsSection = document.getElementById("results-section");
    const objectiveSummaryDiv = document.getElementById("objective-summary");
    const personaResultsDiv = document.getElementById("persona-results");
    const analyzeBtn = document.getElementById("analyze-btn");

    let personas = [];
    let selectedPersonas = new Set();

    // Fetch journalist personas
    fetch("/journalists")
        .then(res => res.json())
        .then(data => {
            personas = data;
            renderPersonaCards(personas);
        });

    function renderPersonaCards(personas) {
        personaListDiv.innerHTML = "";
        personas.forEach(persona => {
            const card = document.createElement("div");
            card.className = "persona-card";
            card.dataset.journalistId = persona.journalist_id;

            card.innerHTML = `
                <div class="name">${persona.name}</div>
                <div class="traits">
                    <strong>Topics:</strong> ${Array.isArray(persona.topic_preferences) 
                        ? persona.topic_preferences.map(t => t.topic).join(", ") 
                        : ""}
                </div>
                <div class="traits">
                    <strong>Coverage:</strong> ${Array.isArray(persona.coverage_areas) 
                        ? persona.coverage_areas.map(area => area.type || area).join(", ")
                        : ""}
                </div>
                <div class="fairness">Fairness: ${persona.fairness_index != null ? persona.fairness_index : "?"}</div>
            `;
            card.addEventListener("click", function () {
                if (selectedPersonas.has(persona.journalist_id)) {
                    selectedPersonas.delete(persona.journalist_id);
                    card.classList.remove("selected");
                } else {
                    selectedPersonas.add(persona.journalist_id);
                    card.classList.add("selected");
                }
            });
            personaListDiv.appendChild(card);
        });
    }

    // Form submit handler
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const text = document.getElementById("press-release-input").value.trim();
        if (!text) {
            alert("Please paste your press release.");
            return;
        }
        if (selectedPersonas.size === 0) {
            alert("Select at least one journalist persona.");
            return;
        }

        resultsSection.style.display = "none";
        personaResultsDiv.innerHTML = "";
        objectiveSummaryDiv.textContent = "";
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = "Analyzing...";

        fetch("/submit_press_release", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                press_release: text,
                journalist_ids: Array.from(selectedPersonas)
            })
        })
            .then(res => res.json())
            .then(data => {
                resultsSection.style.display = "block";
                objectiveSummaryDiv.textContent = data.objective_summary;
                renderPersonaResults(data);
            })
            .catch(() => alert("Error analyzing press release."))
            .finally(() => {
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = "Analyze";
            });
    });

    function renderPersonaResults(data) {
        personaResultsDiv.innerHTML = "";
        for (const jid in data.biased_summaries) {
            const persona = personas.find(p => p.journalist_id === jid);
            const block = document.createElement("div");
            block.className = "persona-analysis-block";

            block.innerHTML = `
                <h4>${persona ? persona.name : jid}</h4>
                <div class="analysis-section">
                    <span class="label">Biased Summary:</span>
                    <div class="result-content">${data.biased_summaries[jid]}</div>
                </div>
                <div class="analysis-section">
                    <span class="label">Knowledge Base Insights:</span>
                    <div class="result-content">${(data.knowledge_base_insights[jid] || []).map(i => `<li>${i}</li>`).join("")}</div>
                </div>
                <div class="analysis-section">
                    <span class="label">Grades:</span>
                    ${renderGradesTable(data.grades[jid])}
                </div>
                <div class="analysis-section">
                    <span class="label">Final Persona Response:</span>
                    <div class="result-content">${data.final_responses[jid]}</div>
                </div>
            `;
            personaResultsDiv.appendChild(block);
        }
    }

    function renderGradesTable(grades) {
        if (!grades) return "<div>No grades available.</div>";
        let html = `<table class="grades-table"><tr>`;
        for (const key in grades) html += `<th>${key.charAt(0).toUpperCase() + key.slice(1)}</th>`;
        html += `</tr><tr>`;
        for (const key in grades) html += `<td>${grades[key]}</td>`;
        html += `</tr></table>`;
        return html;
    }
});