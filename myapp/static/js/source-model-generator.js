document.addEventListener('DOMContentLoaded', function() {
    const modelButton = document.getElementById('model_button');
    const popup = document.getElementById('loading-popup');
    let processing = false;

    modelButton.addEventListener('click', function() {
        const form = document.getElementById('source-model-form');
        const formData = new FormData(form);

        // Show the loading popup
        popup.style.display = 'flex';
        processing = true;

        fetch('/source_model_tool/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Source Model Generated!');
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

    // Source Model Inputs
    const faultInput = document.querySelector('.fault-group #fault-file-path'); // Fault Input File
    const earthquakeInput = document.querySelector('.earthquake-group #earthquake-file-path'); // Earthquake Input File
    const verticeInput = document.querySelector('.vertice-group #vertice-file-path'); // Vertice Input File
    const outputFileInput = document.querySelector('.output-group #output-file-path'); // Output File

    const defaultTitle = 'About';
    const defaultDescription = 'Lorem ipsum dolor sit amet consectetur. Vestibulum urna pulvinar aliquam volutpat. Sed libero egestas felis faucibus id nunc. Integer dui amet sagittis sed et consequat. Non tempus tempor aliquet lacus potenti aliquam.';

    // Function to reset to default about content
    function resetAboutCard() {
        aboutTitle.textContent = defaultTitle;
        aboutDescription.textContent = defaultDescription;
    }

    // Fault Input File focus event
    faultInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Specific Sources Input File';
        aboutDescription.innerHTML = `
            <p>The input file must contain basic information of each fault to be processed, the excel file must contain the following columns;</p>
            <ul>
                <li>name</li>
                <li>segment</li>
                <li>length (km)</li>
                <li>dip</li>
                <li>rake</li>
                <li>maxmag</li>
            </ul>
        `;
    });

    // Earthquake Input File focus event
    earthquakeInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Earthquake Input File';
        aboutDescription.textContent = 'Input file containing earthquake data relevant to the analysis.';
    });

    // Vertice Input File focus event
    verticeInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Vertice Input File';
        aboutDescription.textContent = 'This file should include multiple longitude and latitude vertices along the fault from one end to another.';
    });

    // Output File focus event
    outputFileInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Output File';
        aboutDescription.textContent = 'Specify the output location for the results of the source model analysis.';
    });

    // Reset to default when clicking outside the input fields
    document.addEventListener('click', function(e) {
        if (
            !e.target.closest('.fault-group') && 
            !e.target.closest('.earthquake-group') && 
            !e.target.closest('.vertice-group') && 
            !e.target.closest('.output-group')
        ) {
            resetAboutCard();
        }
    });
});