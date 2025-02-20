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

        data.results.forEach(res => {
            let item = document.createElement("div");
            item.classList.add("result-item");
            item.innerHTML = `
                <p><strong>Sentence:</strong> ${res.sentence}</p>
                <p><a href="${res.url}" target="_blank">Read More</a></p>
            `;
            resultsDiv.appendChild(item);
        });
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while fetching results.");
    });
}