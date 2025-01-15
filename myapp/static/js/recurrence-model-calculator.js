document.addEventListener('DOMContentLoaded', function() {
    // Update selected value from dropdown
    document.querySelectorAll('.ss-option-list .option').forEach(function(option) {
        option.addEventListener('click', function() {
            const selectedValue = option.getAttribute('data-value');
            document.querySelector('.ss-select .select').textContent = selectedValue;
            document.getElementById('seismic-source').value = selectedValue;
        });
    });

    const recurrenceButton = document.getElementById('recurrence_button');
    const doneButton = document.getElementById('done_button');
    const popup = document.getElementById('loading-popup');
    const loadingSpinner = document.querySelector('.loading-spinner');
    
    recurrenceButton.addEventListener('click', function() {
        const form = document.getElementById('recurrence-model-form');
        const formData = new FormData(form);

        // Show the loading popup
        popup.style.display = 'flex';
        processing = true;

        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value; 
        if (!csrfToken) {
            console.error("CSRF token not found!");
            return;
        }

        fetch('/recurrence_model_tool/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Recurrence Model Generated!');
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

    // Recurrence Model Inputs
    const specificSourcesInput = document.querySelector('.specific-sources-group #fault-file-path'); // Specific Sources Input File
    const rawEarthquakeInput = document.querySelector('.raw-earthquake-group #earthquake-file-path'); // Raw EQ Input File
    const rawFaultsInput = document.querySelector('.raw-faults-group #vertice-file-path'); // Raw Faults Input File
    const seismicSourceField = document.querySelector('.seismic-source-group .ss-select');
    const bufferSizeInput = document.querySelector('.buffer-size-group #buffer-size'); // Buffer Size
    const outputFileInput = document.querySelector('.output-group #output-file-path'); // Output File
    const grOutputFileInput = document.querySelector('.gr-output-group #gr-output-file-path'); // GR Output File

    const defaultTitle = 'About';
    const defaultDescription = 'Lorem ipsum dolor sit amet consectetur. Vestibulum urna pulvinar aliquam volutpat. Sed libero egestas felis faucibus id nunc. Integer dui amet sagittis sed et consequat. Non tempus tempor aliquet lacus potenti aliquam.';

    // Function to reset to default about content
    function resetAboutCard() {
        aboutTitle.textContent = defaultTitle;
        aboutDescription.textContent = defaultDescription;
    }

    // Specific Sources Input File focus event
    specificSourcesInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Specific Sources Input File';
        aboutDescription.textContent = 'This file should contain the seismic sources you want to consider in the model.';
    });
    specificSourcesInput.addEventListener('focus', function() {
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

    // Raw EQ Input File focus event
    rawEarthquakeInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Raw EQ Input File';
        aboutDescription.textContent = 'Input file containing the raw earthquake data for processing.';
    });

    // Raw Faults Input File focus event
    rawFaultsInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Raw Faults Input File';
        aboutDescription.textContent = 'This file should include multiple longitude and latitude vertices along the fault from one end to another.';
    });

    // Buffer Size focus event
    bufferSizeInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Buffer Size';
        aboutDescription.textContent = 'Set the buffer size to define the extent of the analysis area.';
    });

    seismicSourceField.addEventListener('focus', function() {
        aboutTitle.textContent = 'Seismic Source Classification';
        aboutDescription.textContent = 'Select the appropriate Seismic Source Classification';
    });


    // Output File focus event
    outputFileInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'Output File';
        aboutDescription.textContent = 'Specify the location where the output results will be saved.';
    });

    // GR Output File focus event
    grOutputFileInput.addEventListener('focus', function() {
        aboutTitle.textContent = 'GR Output File';
        aboutDescription.textContent = 'This file will contain the generated graphs based on the analysis.';
    });

    // Reset to default when clicking outside the input fields
    document.addEventListener('click', function(e) {
        if (
            !e.target.closest('.specific-sources-group') && 
            !e.target.closest('.raw-earthquake-group') && 
            !e.target.closest('.raw-faults-group') && 
            !e.target.closest('.seismic-source-group') && 
            !e.target.closest('.buffer-size-group') && 
            !e.target.closest('.output-group') && 
            !e.target.closest('.gr-output-group')
        ) {
            resetAboutCard();
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    let ssOptions = document.querySelectorAll('.seismic-source-group .option');
    let ssSelectEle = document.querySelector('.seismic-source-group .select');
    let ssOptionList = document.querySelector('.ss-option-list');
    let ssDropdown = document.querySelector('.ss-select');

    function toggleDropdown(optionList) {
        optionList.classList.toggle('active');
    }

    function selectOption(selectEle, optionList, option) {
        selectEle.innerText = option.innerText;
        optionList.classList.toggle('active');
    }

    ssDropdown.addEventListener('click', function() {
        toggleDropdown(ssOptionList);
    });

    ssOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            selectOption(ssSelectEle, ssOptionList, this);
        });
    });
});