document.addEventListener('DOMContentLoaded', function() {
    const professionOptions = document.querySelectorAll('.profession-group .option');
    const professionSelectEle = document.querySelector('.profession-group .select');
    const professionOptionList = document.querySelector('.profession-option-list');
    const professionDropdown = document.querySelector('.profession-select');
    const professionInput = document.getElementById('profession');
    const otherProfessionContainer = document.getElementById('otherProfessionContainer'); // Container for "Others"
    const otherProfessionInput = document.getElementById('otherProfession'); // Input for "Others"

    function toggleDropdown(optionList) {
        // Get the position of the profession dropdown
        const rect = professionSelectEle.getBoundingClientRect();
        const dropdownHeight = optionList.offsetHeight;

        // Add 10px space below the profession select element
        optionList.style.top = `${rect.bottom + window.scrollY + 10}px`; // Adjust for space
        optionList.classList.toggle('active');
    }

    function selectOption(selectEle, optionList, inputField, option) {
        const selectedValue = option.getAttribute('data-value');
        selectEle.innerText = option.innerText;
        inputField.value = selectedValue;
        optionList.classList.toggle('active');

        // Handle "Others, Please Specify" visibility
        if (selectedValue === "Others") {
            otherProfessionContainer.style.display = "block"; // Show container
            otherProfessionInput.required = true; // Make input required
        } else {
            otherProfessionContainer.style.display = "none"; // Hide container
            otherProfessionInput.required = false; // Remove required attribute
            otherProfessionInput.value = ""; // Clear input value
        }
    }

    // Toggle dropdown on click
    professionDropdown.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent the click event from bubbling up
        toggleDropdown(professionOptionList);
    });

    // Select an option and update input field
    professionOptions.forEach(function(option) {
        option.addEventListener('click', function(event) {
            selectOption(professionSelectEle, professionOptionList, professionInput, this);
            event.stopPropagation(); // Prevent the click event from bubbling up
        });
    });

    // Close the dropdown if clicked outside
    document.addEventListener('click', function(event) {
        if (!professionDropdown.contains(event.target) && !professionOptionList.contains(event.target)) {
            professionOptionList.classList.remove('active');
        }
    });

    // Initialize Flatpickr
    flatpickr("#birthdate", {
        dateFormat: "d/m/Y", // Customize the date format
        allowInput: true,    // Allow typing in the input field
    });

});





// function handleProfessionChange() {
//     // Get elements
//     const professionSelect = document.getElementById("profession");
//     const otherProfessionContainer = document.getElementById("otherProfessionContainer");
//     const otherProfessionInput = document.getElementById("otherProfession");

//     // Check if "Others" is selected
//     if (professionSelect.value === "Others") {
//         otherProfessionContainer.style.display = "block"; // Show container
//         otherProfessionInput.required = true; // Make input required
//     } else {
//         otherProfessionContainer.style.display = "none"; // Hide container
//         otherProfessionInput.required = false; // Remove required attribute
//         otherProfessionInput.value = ""; // Clear input value
//     }
// }

function handleFormSubmission(event) {
    event.preventDefault(); // Prevent default form submission

    // Get input values
    const fullName = document.getElementById("full_name").value.trim();
    const birthdate = document.getElementById("birthdate").value.trim();
    const email = document.getElementById("email").value.trim();
    const prcLicense = document.getElementById("prc_license").value.trim();
    const professionSelect = document.getElementById("profession");
    const otherProfessionInput = document.getElementById("otherProfession").value.trim();
    const affiliation = document.getElementById("affiliation").value.trim();

    // Determine the final profession value
    let profession = professionSelect.value === "Others" ? otherProfessionInput : professionSelect.value;

    // Log values to the console
    console.log("Full Name:", fullName);
    console.log("Birthdate:", birthdate);
    console.log("Email:", email);
    console.log("PRC License:", prcLicense);
    console.log("Profession:", profession);
    console.log("Affiliated Agency:", affiliation);
}


// // Attach event listeners
// document.addEventListener("DOMContentLoaded", function () {
//     document.getElementById('registerForm').addEventListener('submit', function(event) {
//         // Get form data
//         var formData = {
//             'full_name': document.getElementById('full_name').value,
//             'birthdate': document.getElementById('birthdate').value,
//             'email': document.getElementById('email').value,
//             'profession': document.getElementById('profession').value,
//             'affiliation': document.getElementById('affiliation').value
//         };

//         // Log the data to the console
//         console.log("Register Form Data:", formData);
        
//         // You can do additional logging or validation here if needed
//     });
// });

