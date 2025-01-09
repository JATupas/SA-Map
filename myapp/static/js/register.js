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

function handleProfessionChange() {
    const professionSelect = document.getElementById("profession");
    const otherProfessionContainer = document.getElementById("otherProfessionContainer");
    const otherProfessionInput = document.getElementById("otherProfession");

    if (professionSelect.value === "Others") {
        otherProfessionContainer.style.display = "block"; // Show container
        otherProfessionInput.required = true; // Make input required
    } else {
        otherProfessionContainer.style.display = "none"; // Hide container
        otherProfessionInput.required = false; // Remove required attribute
        otherProfessionInput.value = ""; // Clear input value
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const professionSelect = document.getElementById("profession");

    // Call handleProfessionChange initially to set the correct state
    handleProfessionChange();

    // Add event listener for the profession select element
    professionSelect.addEventListener("change", handleProfessionChange);

    // Handle form submission
    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = {
            'full_name': document.getElementById('full_name').value,
            'birthdate': document.getElementById('birthdate').value,
            'email': document.getElementById('email').value,
            'prc_license': document.getElementById('prc_license').value,
            'profession': document.getElementById('profession').value,
            'affiliation': document.getElementById('affiliation').value
        };

        console.log("Register Form Data:", formData);
    });
});

