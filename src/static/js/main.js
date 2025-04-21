// src/static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Code to handle book downloads and other client-side functionality
    const downloadLinks = document.querySelectorAll('.download-link');

    downloadLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const filePath = this.getAttribute('href');
            window.location.href = filePath; // Redirect to the file download
        });
    });
});