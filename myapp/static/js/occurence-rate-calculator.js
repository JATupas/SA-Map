document.addEventListener('DOMContentLoaded', function() {
    const calculateButton = document.getElementById('calculate-button');
    const popup = document.getElementById('loading-popup');

    calculateButton.addEventListener('click', function() {
        const form = document.getElementById('occurrence-rates-form');
        const formData = new FormData(form);

        // Show the loading popup
        popup.style.display = 'flex';
        processing = true;

        fetch('/calculate_occurrence_rates/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Calculation completed successfully!');
                popup.style.display = 'none';  // Close the popup
            } else {
                alert('Error: ' + data.message);
                popup.style.display = 'none';  // Close the popup
            }
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
    
    // Occurrence Rates Form Inputs
    const occurrenceInputFile = document.querySelector('.ORC-input-group #input-file-path'); // Occurrence Rates Input File
    const occurrenceOutputFile = document.querySelector('.ORC-output-group #output-file-path'); // Occurrence Rates Output File

    const defaultTitle = 'About';
    const defaultDescription = 'Lorem ipsum dolor sit amet consectetur. Vestibulum urna pulvinar aliquam volutpat. Sed libero egestas felis faucibus id nunc. Integer dui amet sagittis sed et consequat. Non tempus tempor aliquet lacus potenti aliquam.';

    // Function to reset to default about content
    function resetAboutCard() {
        aboutTitle.textContent = defaultTitle;
        aboutDescription.textContent = defaultDescription;
    }

    // Occurrence Rates Input File focus event
    occurrenceInputFile.addEventListener('focus', function() {
        aboutTitle.textContent = 'Input File Information (Occurrence Rates)';
        aboutDescription.textContent = 'The input file should contain the necessary seismic occurrence data in Excel format for processing.';
    });

    // Occurrence Rates Output File focus event
    occurrenceOutputFile.addEventListener('focus', function() {
        aboutTitle.textContent = 'Output File Information (Occurrence Rates)';
        aboutDescription.textContent = 'The output file will store the processed seismic occurrence rates in Excel format.';
    });

    // Reset to default when clicking outside the input fields
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.ORC-input-group') && !e.target.closest('.ORC-output-group')) {
            resetAboutCard();
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const aboutTitle = document.getElementById('about-title');
    const aboutDescription = document.getElementById('about-description');
    
    // Occurrence Rates Form Inputs
    const occurrenceInputFile = document.querySelector('.ORC-input-group #input-file-path'); // Occurrence Rates Input File
    const occurrenceOutputFile = document.querySelector('.ORC-output-group #output-file-path'); // Occurrence Rates Output File

    const defaultTitle = 'About';
    const defaultDescription = 'Lorem ipsum dolor sit amet consectetur. Vestibulum urna pulvinar aliquam volutpat. Sed libero egestas felis faucibus id nunc. Integer dui amet sagittis sed et consequat. Non tempus tempor aliquet lacus potenti aliquam.';

    // Function to reset to default about content
    function resetAboutCard() {
        aboutTitle.textContent = defaultTitle;
        aboutDescription.textContent = defaultDescription;
    }

    // Occurrence Rates Input File focus event
    occurrenceInputFile.addEventListener('focus', function() {
        aboutTitle.textContent = 'Input File';
        aboutDescription.innerHTML = `
            <p>This a compilation of multiple fault information combined into a single input file. The columns must include</p>
            <ul>
                <li>Fault Name</li>
                <li>a-value</li>
                <li>b-value</li>
                <li>Min Magnitude</li>
                <li>Max Magnitude</li>
                <li>Ocurrence</li>
            </ul>
        `;
    });

    // Occurrence Rates Output File focus event
    occurrenceOutputFile.addEventListener('focus', function() {
        aboutTitle.textContent = 'Output File Information (Occurrence Rates)';
        aboutDescription.textContent = 'The output file will store the processed seismic occurrence rates in Excel format.';
    });

    // Reset to default when clicking outside the input fields
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.ORC-input-group') && !e.target.closest('.ORC-output-group')) {
            resetAboutCard();
        }
    });
});