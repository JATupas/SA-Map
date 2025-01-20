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
    const professionSelect = document.getElementById("profession");
    const otherProfessionInput = document.getElementById("otherProfession").value.trim();
    const affiliation = document.getElementById("affiliation").value.trim();

    // Determine the final profession value
    let profession = professionSelect.value === "Others" ? otherProfessionInput : professionSelect.value;

    // Log values to the console
    console.log("Full Name:", fullName);
    console.log("Birthdate:", birthdate);
    console.log("Email:", email);
    console.log("Profession:", profession);
    console.log("Affiliated Agency:", affiliation);
}

// Attach an event listener to the form submission
document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting by default
  
    const birthdateInput = document.getElementById('birthdate').value;
  
    let errorMessage = ''; // Initialize the error message
  
    // Validate the birthdate (at least 18 years old)
    const birthdate = new Date(birthdateInput);
    const today = new Date();
    const eighteenYearsAgo = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());
  
    if (birthdate > eighteenYearsAgo) {
      errorMessage += 'You must be at least 18 years old.\n';
    }
  
    // Display the error message if there are errors
    if (errorMessage) {
      alert(errorMessage); // Display the error messages in an alert
    } else {
      alert('Form submitted successfully!');
      // You can submit the form here if needed (e.g., via AJAX or traditional submission)
      e.target.submit(); // Uncomment if you want the form to submit
    }
  });
  
