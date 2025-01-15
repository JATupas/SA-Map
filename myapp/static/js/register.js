function handleProfessionChange() {
    // Get elements
    const professionSelect = document.getElementById("profession");
    const otherProfessionContainer = document.getElementById("otherProfessionContainer");
    const otherProfessionInput = document.getElementById("otherProfession");

    // Check if "Others" is selected
    if (professionSelect.value === "Others") {
        otherProfessionContainer.style.display = "block"; // Show container
        otherProfessionInput.required = true; // Make input required
    } else {
        otherProfessionContainer.style.display = "none"; // Hide container
        otherProfessionInput.required = false; // Remove required attribute
        otherProfessionInput.value = ""; // Clear input value
    }
}

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