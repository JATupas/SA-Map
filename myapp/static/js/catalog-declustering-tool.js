document.addEventListener('DOMContentLoaded', function () {
    // Declustering Method Dropdown
    const dmOptions = document.querySelectorAll('.dm-option-list .option');
    const dmSelectEle = document.querySelector('.declustering-method-group .select');
    const dmOptionList = document.querySelector('.dm-option-list');
    const dmDropdown = document.querySelector('.dm-select');

    // Time Method Dropdown
    const tmOptions = document.querySelectorAll('.tm-option-list .option');
    const tmSelectEle = document.querySelector('.time-method-group .select');
    const tmOptionList = document.querySelector('.tm-option-list');
    const tmDropdown = document.querySelector('.tm-select');

    // Loading Popup and Decluster Button
    const declusterButton = document.getElementById('decluster-button');
    const popup = document.getElementById('loading-popup');

    // About Section Elements
    const aboutTitle = document.getElementById('about-title');
    const aboutDescription = document.getElementById('about-description');
    const inputFileField = document.getElementById('input-file-path');
    const outputFolderField = document.getElementById('output-file-path');

    const defaultTitle = 'About';
    const defaultDescription = 'Lorem ipsum dolor sit amet consectetur.';

    // Dropdown Functions
    function toggleDropdown(optionList) {
        optionList.classList.toggle('active');
    }

    function selectOption(selectEle, optionList, option) {
        selectEle.innerText = option.innerText;
        const inputField = optionList.closest('.declustering-method-group') 
            ? document.getElementById('declustering-method') 
            : document.getElementById('time-method');
        inputField.value = option.getAttribute('data-value');
        optionList.classList.remove('active');
    }

    // Add Event Listeners for Dropdowns
    if (dmDropdown && dmOptionList) {
        dmDropdown.addEventListener('click', function () {
            toggleDropdown(dmOptionList);
        });
        dmOptions.forEach(function (option) {
            option.addEventListener('click', function () {
                selectOption(dmSelectEle, dmOptionList, this);
            });
        });
    }

    if (tmDropdown && tmOptionList) {
        tmDropdown.addEventListener('click', function () {
            toggleDropdown(tmOptionList);
        });
        tmOptions.forEach(function (option) {
            option.addEventListener('click', function () {
                selectOption(tmSelectEle, tmOptionList, this);
            });
        });
    }

    // Decluster Button Event Listener
    if (declusterButton) {
        declusterButton.addEventListener('click', function () {
            const form = document.getElementById('catalog-declustering-form');
            const formData = new FormData(form);

            // Show the loading popup
            popup.style.display = 'flex';

            fetch('/catalog_declustering_tool/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.status === 'success' ? 'Calculation completed successfully!' : `Error: ${data.message}`);
                    popup.style.display = 'none'; // Close the popup
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred.');
                    popup.style.display = 'none'; // Close the popup
                });
        });
    }

    // About Card Reset
    function resetAboutCard() {
        aboutTitle.textContent = defaultTitle;
        aboutDescription.textContent = defaultDescription;
    }

    // Input Focus Event Listeners
    if (inputFileField) {
        inputFileField.addEventListener('focus', function () {
            aboutTitle.textContent = 'Input File Information';
            aboutDescription.textContent = 'The EQ Events must be in the specified format.';
        });
    }

    if (outputFolderField) {
        outputFolderField.addEventListener('focus', function () {
            aboutTitle.textContent = 'Output Folder Information';
            aboutDescription.textContent = 'The output folder stores declustering results.';
        });
    }

    // Reset About Section on Outside Click
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.CDT-input-group') &&
            !e.target.closest('.declustering-method-group') &&
            !e.target.closest('.time-method-group')) {
            resetAboutCard();
        }
    });
});
