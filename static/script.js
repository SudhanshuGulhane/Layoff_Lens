function searchQuery() {
    let query = document.getElementById("query").value.trim();
    let top_k = document.getElementById("top_k").value;

    if (!query || !top_k) {
        alert("Please enter both query and top_k!");
        return;
    }

    let apiUrl = `http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}&top_k=${top_k}`;

    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        let resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";

        if (data.results.length === 0) {
            resultsDiv.innerHTML = "<p>No results found.</p>";
            return;
        }

        data.results.forEach((res, index) => {
            let item = document.createElement("div");
            item.classList.add("result-item");

            // Construct the resources dropdown if links exist
            let resourcesDropdown = "";
            if (res.links && res.links.length > 0) {
                resourcesDropdown = `
                    <select class="resources-dropdown" onchange="openResource(this)">
                        <option selected disabled>Related Articles</option>
                        ${res.links.map((link, i) => `<option value="${link}">Resource Link ${i + 1}</option>`).join("")}
                    </select>
                `;
            }

            item.innerHTML = `
                <p><strong>Article: ${index+1}</strong> ${res.sentence}</p>
                <p>
                    <a href="${res.url}" target="_blank">Source</a>
                    ${resourcesDropdown}
                </p>
            `;
            resultsDiv.appendChild(item);
        });
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while fetching results.");
    });
}

function openResource(selectElement) {
    let selectedLink = selectElement.value;
    if (selectedLink) {
        window.open(selectedLink, "_blank");
    }
}