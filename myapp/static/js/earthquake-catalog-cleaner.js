document.addEventListener('DOMContentLoaded', function() {
    const cleanButton = document.getElementById('clean_button');
    const popup = document.getElementById('loading-popup');
    let processing = false;

    cleanButton.addEventListener('click', function() {
        const form = document.getElementById('catalog-cleaning-form');  
        const formData = new FormData(form);

        // Show the loading popup
        popup.style.display = 'flex';
        processing = true;

        fetch('/catalog_cleaning_tool/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'success') {
                alert('Error: ' + data.message);
                popup.style.display = 'none';  // Close the popup
            }                             
            popup.style.display = 'none';  // Close the popup
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred.');
            popup.style.display = 'none';  // Close the popup
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const aboutTitle = document.getElementById('about-title');
    const aboutDescription = document.getElementById('about-description');
    const inputField = document.getElementById('input-file-path');
    const outputField = document.getElementById('output-file-path');
    const defaultTitle = 'About';
    const defaultDescription = 'Lorem ipsum dolor sit amet consectetur. Vestibulum urna pulvinar aliquam volutpat. Sed libero egestas felis faucibus id nunc. Integer dui amet sagittis sed et consequat. Non tempus tempor aliquet lacus potenti aliquam.';

    // Function to reset to default about content
    function resetAboutCard() {
        aboutTitle.textContent = defaultTitle;
        aboutDescription.innerHTML = `<p>${defaultDescription}</p>`;
    }

    // Input field focus event
    inputField.addEventListener('focus', function() {
        aboutTitle.textContent = 'Input Folder or File(s)';
        aboutDescription.innerHTML = `
            <p>The input will accept a folder, multiple files, or a single file. Each file may contain any number of columns, but it is necessary to pre-process them and retain the following important columns:</p>
            <ul>
                <li>AUTHOR</li>
                <li>DATE</li>
                <li>TIME</li>
                <li>LAT</li>
                <li>LON</li>
                <li>DEPTH</li>
                <li>MAG</li>
                <li>TYPE</li>
            </ul>
        `;
    });

    // Output field focus event
    outputField.addEventListener('focus', function() {
        aboutTitle.textContent = 'Output Folder Information';
        aboutDescription.innerHTML = '<p>The output folder will contain the processed data after cleaning the earthquake catalog.</p>';
    });

    // Reset when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.ECC-input-group') && !e.target.closest('.ECC-output-group')) {
            resetAboutCard();
        }
    });
});