document.addEventListener('DOMContentLoaded', function () {
    // Get all text input fields within the form
    var textInputs = document.querySelectorAll('#source-model-form input[type="text"]');

    // Loop through each input field and add event listeners
    textInputs.forEach(function(inputField) {
        // Function to clean the input value
        function cleanInput() {
            var inputValue = inputField.value;

            // Remove quotation marks and replace backslashes with forward slashes
            inputValue = inputValue.replace(/"/g, '').replace(/\\/g, '/');
            
            // Set the modified value back to the input field
            inputField.value = inputValue;
        }

        // Add 'input' event listener to handle typing
        inputField.addEventListener('input', cleanInput);
        
        // Add 'paste' event listener in case the user pastes content into the field
        inputField.addEventListener('paste', function(event) {
            // Delay cleaning until after the paste event is complete
            setTimeout(cleanInput, 0);
        });
    });
});
