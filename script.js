// script.js
function runSpeedTest() {
    fetch('/plot')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('results').innerHTML = `
            <p>Upload Speed: ${data.uploadSpeed} Mbps</p>
            <p>Download Speed: ${data.downloadSpeed} Mbps</p>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
