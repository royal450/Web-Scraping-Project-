// Add form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const urlInput = document.getElementById('url');
            const elementsInput = document.getElementById('elements');
            
            if (!urlInput.value.trim()) {
                event.preventDefault();
                alert('Please enter a valid URL');
                return;
            }
            
            if (!elementsInput.value.trim()) {
                event.preventDefault();
                alert('Please enter CSS selectors');
                return;
            }
        });
    }
});
