document.addEventListener('DOMContentLoaded', function() {
    // Handle Declustering Method Dropdown
    document.querySelectorAll('.dm-option-list .option').forEach(function(option) {
        option.addEventListener('click', function() {
            const selectedValue = option.getAttribute('data-value');
            document.querySelector('.dm-select .select').textContent = selectedValue;
            document.getElementById('declustering-method').value = selectedValue;
        });
    });

    // Handle Time Method Dropdown
    document.querySelectorAll('.tm-option-list .option').forEach(function(option) {
        option.addEventListener('click', function() {
            const selectedValue = option.getAttribute('data-value');
            document.querySelector('.tm-select .select').textContent = selectedValue;
            document.getElementById('time-method').value = selectedValue;
        });
    });

    const declusterButton = document.getElementById('decluster-button');
    const doneButton = document.getElementById('done_button');
    const popup = document.getElementById('loading-popup');
    const loadingSpinner = document.querySelector('.loading-spinner');

    declusterButton.addEventListener('click', function() {
        const form = document.getElementById('catalog-declustering-form');
        const formData = new FormData(form);

        // Show the loading popup
        popup.style.display = 'flex';
        processing = true;

        fetch('/catalog_declustering_tool/', {
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
    const inputFileField = document.getElementById('input-file-path');
    const declusteringMethodField = document.querySelector('.declustering-method-group .dm-select');
    const timeMethodField = document.querySelector('.time-method-group .tm-select');
    const outputFolderField = document.getElementById('output-file-path');
    const defaultTitle = 'About';
    const defaultDescription = 'Lorem ipsum dolor sit amet consectetur. Vestibulum urna pulvinar aliquam volutpat. Sed libero egestas felis faucibus id nunc. Integer dui amet sagittis sed et consequat. Non tempus tempor aliquet lacus potenti aliquam.';

    // Function to reset to default about content
    function resetAboutCard() {
        aboutTitle.textContent = defaultTitle;
        aboutDescription.textContent = defaultDescription;
    }

    // Input file focus event
    inputFileField.addEventListener('focus', function() {
        aboutTitle.textContent = 'Input File Information';
        aboutDescription.textContent = 'The EQ Events that will be declustered must be transferred to the Aegean_ExtendedCat1.csv file provided.';
    });

    // Declustering method focus event
    declusteringMethodField.addEventListener('focus', function() {
        aboutTitle.textContent = 'Declustering Method Information';
        aboutDescription.textContent = 'Select a method for declustering the earthquake catalog. Options include Gardner-Knopoff or Afteran.';
    });

    // Time-space window method focus event
    timeMethodField.addEventListener('focus', function() {
        aboutTitle.textContent = 'Time-Space Window Information';
        aboutDescription.textContent = 'Select the time-space window method, such as Gardner-Knopoff, Urhammer, or Gruenthal, to determine the declustering parameters.';
    });

    // Output folder focus event
    outputFolderField.addEventListener('focus', function() {
        aboutTitle.textContent = 'Output Folder Information';
        aboutDescription.textContent = 'The output folder will store the results of the declustering process.';
    });

    // Reset when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.CDT-input-group') && 
            !e.target.closest('.declustering-method-group') && 
            !e.target.closest('.time-method-group') && 
            !e.target.closest('.CDT-output-group')) {
            resetAboutCard();
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    let dmOptions = document.querySelectorAll('.declustering-method-group .option');
    let dmSelectEle = document.querySelector('.declustering-method-group .select');
    let dmOptionList = document.querySelector('.dm-option-list');
    let dmDropdown = document.querySelector('.dm-select');

    let tmOptions = document.querySelectorAll('.time-method-group .option');
    let tmSelectEle = document.querySelector('.time-method-group .select');
    let tmOptionList = document.querySelector('.tm-option-list');
    let tmDropdown = document.querySelector('.tm-select');

    function toggleDropdown(optionList) {
        optionList.classList.toggle('active');
    }

    function selectOption(selectEle, optionList, option) {
        selectEle.innerText = option.innerText;
        optionList.classList.toggle('active');
    }

    dmDropdown.addEventListener('click', function() {
        toggleDropdown(dmOptionList);
    });

    tmDropdown.addEventListener('click', function() {
        toggleDropdown(tmOptionList);
    });

    dmOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            selectOption(dmSelectEle, dmOptionList, this);
        });
    });

    tmOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            selectOption(tmSelectEle, tmOptionList, this);
        });
    });
});