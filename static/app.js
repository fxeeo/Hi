document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('district-search');
    const tableBody = document.getElementById('districts-table-body');

    if (searchInput && tableBody) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value;
            fetch(`/api/districts?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    tableBody.innerHTML = '';
                    data.forEach(district => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${district.name}</td>
                            <td>${district.risk_level}</td>
                            <td>${district.people_affected}</td>
                            <td>${district.relief_camps}</td>
                            <td>${district.trend}</td>
                        `;
                        tableBody.appendChild(row);
                    });
                })
                .catch(err => console.error("Failed to fetch districts:", err));
        });
    }
});
