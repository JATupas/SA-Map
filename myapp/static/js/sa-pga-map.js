// Get the input element and error message element
const faInput = document.getElementById("fainput");
const errorMessage = document.getElementById("error-message");

let rawData = {};

// Function to check if the value is 0
function validateInput() {
  const value = faInput.value;

  // Check if the value is 0
  if (value == 0) {
    errorMessage.style.display = "inline"; // Show the error message
    faInput.style.borderColor = "red"; // Change the border color to red
    return false; // Prevent further actions
  } else {
    errorMessage.style.display = "none"; // Hide the error message
    faInput.style.borderColor = ""; // Reset the border color
    return true; // Allow further actions
  }
}

// Call the validation function when the input value changes
faInput.addEventListener("input", validateInput);

document.addEventListener("DOMContentLoaded", () => {
  const latField = document.getElementById("current-lat");
  const lonField = document.getElementById("current-lon");
  const popup = document.getElementById("popup");

  const boundingBox = {
    minLat: 4,
    maxLat: 21,
    minLon: 116,
    maxLon: 127,
  };

  const showPopup = (message) => {
    popup.style.display = "flex";
    popup.innerHTML = `
            <div class="card">
                <p>${message}</p>
                <button id="closePopup">Close</button>
            </div>`;

    // Close popup event listener
    document.addEventListener("click", function handleClosePopup(event) {
      if (event.target && event.target.id === "closePopup") {
        popup.style.display = "none";
        document.removeEventListener("click", handleClosePopup);
      }
    });
  };

  const validateCoordinates = () => {
    const latValue = parseFloat(latField.value);
    const lonValue = parseFloat(lonField.value);

    if (!isNaN(latValue) && !isNaN(lonValue)) {
      if (
        latValue < boundingBox.minLat ||
        latValue > boundingBox.maxLat ||
        lonValue < boundingBox.minLon ||
        lonValue > boundingBox.maxLon
      ) {
        showPopup(
          "This point is outside of the Philippines, there is no available data for the selected coordinates."
        );
        document.getElementById("current-lat").value = "";
        document.getElementById("current-lon").value = "";
      }
    }
    // else {
    //     showPopup("Invalid input! Please enter numeric values for latitude and longitude.");
    //     document.getElementById("current-lat").value = "";
    //     document.getElementById("current-lon").value = "";
    // }
  };

  latField.addEventListener("change", validateCoordinates);
  lonField.addEventListener("change", validateCoordinates);
});

document.addEventListener("DOMContentLoaded", function () {
  const inputElement = document.getElementById("site");
  const faDiv = document.getElementById("fainput").parentElement;
  const fvDiv = document.getElementById("fvinput").parentElement;

  // Function to handle display of `faDiv` and `fvDiv` based on input value
  function updateVisibility() {
    if (inputElement.value.trim().toUpperCase() === "F") {
      faDiv.style.display = "block";
      fvDiv.style.display = "block";
    } else {
      faDiv.style.display = "none";
      fvDiv.style.display = "none";
    }
  }
  document.querySelectorAll(".site-option-list .option").forEach((option) => {
    option.addEventListener("click", function () {
      inputElement.value = option.dataset.value; // Update the hidden input
      updateVisibility(); // Update the visibility of faDiv and fvDiv
    });
  });

  // Run once on page load to set initial visibility
  updateVisibility();
});

$(document).ready(function () {
  // Initialize the map after the page has fully loaded
  var map = L.map("map").setView([13.41, 122.56], 6); // Set initial coordinates

  var marker = null; // Marker variable to store the current marker on the map

  // Add a tile layer to the map
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Function to convert Decimal Degrees to DMS
  function convertToDMS(decimalDegree) {
    const degrees = Math.floor(decimalDegree); // Extract degrees
    const minutesDecimal = Math.abs((decimalDegree - degrees) * 60); // Convert remaining to minutes
    const minutes = Math.floor(minutesDecimal); // Extract whole minutes
    const seconds = ((minutesDecimal - minutes) * 60).toFixed(5); // Convert remaining to seconds with 5 decimals
    return { degrees, minutes, seconds };
  }

  // Map click event
  map.on("click", function (e) {
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;

    // Update the latitude and longitude input fields
    document.getElementById("current-lat").value = lat;
    document.getElementById("current-lon").value = lon;

    // Update DMS fields for Latitude
    const latDMS = convertToDMS(lat);
    document.getElementById("lat-degrees").value = latDMS.degrees;
    document.getElementById("lat-minutes").value = latDMS.minutes;
    document.getElementById("lat-seconds").value = latDMS.seconds;

    // Update DMS fields for Longitude
    const lonDMS = convertToDMS(lon);
    document.getElementById("lon-degrees").value = lonDMS.degrees;
    document.getElementById("lon-minutes").value = lonDMS.minutes;
    document.getElementById("lon-seconds").value = lonDMS.seconds;

    // Check if the point is outside the Philippines
    if (lat < 4 || lat > 21 || lon < 116 || lon > 127) {
      // Show the popup over the entire map
      document.getElementById("popup").style.display = "flex";
      document.getElementById("popup").innerHTML = `
                <div class="card">
                    <p>This point is outside of the Philippines, there is no available data for the selected coordinates.</p>
                    <button id="closePopup">Close</button>
                </div>`;

      // Close popup event listener
      document.addEventListener("click", function (event) {
        if (event.target && event.target.id === "closePopup") {
          document.getElementById("popup").style.display = "none";
        }
      });
      document.getElementById("current-lat").value = "";
      document.getElementById("current-lon").value = "";
    }

    // If a marker exists, remove it
    if (marker) {
      map.removeLayer(marker);
    }

    // Add a new marker at the clicked location
    marker = L.marker([lat, lon]).addTo(map);
  });

  // Add functionality to the "Check Data" button (for AJAX to update site information)
  document.getElementById("check-data").addEventListener("click", function () {
    var lat = document.getElementById("current-lat").value;
    var lon = document.getElementById("current-lon").value;
    var site = document.getElementById("site").value;
    var fainput = document.getElementById("fainput").value;
    var fvinput = document.getElementById("fvinput").value;
    var latDegrees = document.getElementById("lat-degrees").value;
    var latMinutes = document.getElementById("lat-minutes").value;
    var latSeconds = document.getElementById("lat-seconds").value;

    var lonDegrees = document.getElementById("lon-degrees").value;
    var lonMinutes = document.getElementById("lon-minutes").value;
    var lonSeconds = document.getElementById("lon-seconds").value;

    document
      .getElementById("lat-dms")
      .querySelector("#lat-degrees").textContent = latDegrees;
    document
      .getElementById("lat-dms")
      .querySelector("#lat-minutes").textContent = latMinutes;
    document
      .getElementById("lat-dms")
      .querySelector("#lat-seconds").textContent = latSeconds;

    document
      .getElementById("lon-dms")
      .querySelector("#lon-degrees").textContent = lonDegrees;
    document
      .getElementById("lon-dms")
      .querySelector("#lon-minutes").textContent = lonMinutes;
    document
      .getElementById("lon-dms")
      .querySelector("#lon-seconds").textContent = lonSeconds;

    // Make sure lat, lon, and site values are available before sending AJAX
    if (lat && lon && site) {
      const popup = document.getElementById("loading-popup");
      popup.style.display = "flex";

      $.ajax({
        type: "POST",
        url: saPgaMapUrl, // Ensure this URL resolves correctly in Django
        data: {
          lat: lat,
          lon: lon,
          site: site, // Send the site value as well
          fainput: fainput,
          fvinput: fvinput,
          csrfmiddlewaretoken: csrfToken, // Include CSRF token if not exempted
        },
        success: function (response) {
          console.log("Data updated successfully");
          console.log(response); // Handle the response from the server
          // Optionally, you can handle any changes to the UI here (e.g., updating coordinates)
          document.getElementById("long").textContent =
            response.current_coord.at(0) || "0.0";
          document.getElementById("lat").textContent =
            response.current_coord.at(1) || "0.0";
          document.getElementById("site-class-info").textContent =
            response.site || site; // Assuming site class info is static for now

          // Optionally, populate other fields like SA₁, SMS, etc.
          document.getElementById("sa1-value").textContent =
            response.sa1 || "0.0";
          document.getElementById("sa02-value").textContent =
            response.sa02 || "0.0";
          document.getElementById("tl-value").textContent =
            response.tl || "0.0";
          document.getElementById("Fa-value").textContent =
            response.Fa || "0.0";
          document.getElementById("Fv-value").textContent =
            response.Fv || "0.0";
          document.getElementById("SMS-value").textContent =
            response.SMS || "0.0";
          document.getElementById("SM1-value").textContent =
            response.SM1 || "0.0";
          document.getElementById("SDS-value").textContent =
            response.SDS || "0.0";
          document.getElementById("SD1-value").textContent =
            response.SD1 || "0.0";
          document.getElementById("Ts-value").textContent =
            response.Ts || "0.0";
          document.getElementById("To-value").textContent =
            response.To || "0.0";

          if (response.image_base64) {
            document.getElementById("image-container").innerHTML =
              '<img src="data:image/png;base64,' +
              response.image_base64 +
              '" alt="SA-PGA Map Image">';
          }

          document.querySelector(".Home .site-info-card").style.display =
            "flex";
          var newLat = response.current_coord.lat || lat;
          var newLon = response.current_coord.lon || lon;
          if (marker) {
            map.removeLayer(marker); // Remove any existing marker
          }
          marker = L.marker([newLat, newLon]).addTo(map); // Add the new marker
          map.setView([newLat, newLon], 11); // Zoom in to the new marker
          popup.style.display = "none"; // Close the popup
          console.log("user registration data:", registrationData);
          // let userData = {
          //     full_name: "",
          //     birthdate: "",
          //     email: "",
          //     prc_license: "",
          //     profession: "",
          //     affiliation: "",
          // }

          // if(registrationData){
          //     userData = {...registrationData}
          // }

          const rawCalcData = {
            ...response,
            latDegrees: latDegrees,
            latMinutes: latMinutes,
            latSeconds: latSeconds,
            lonDegrees: lonDegrees,
            lonMinutes: lonMinutes,
            lonSeconds: lonSeconds,
            site: site,
          };

          rawData = rawCalcData;

          const overAllData = {
            registrationData: registrationData,
            calculationData: rawCalcData,
          };

          $.ajax({
            url: emailUrl,
            type: "POST",
            data: JSON.stringify(overAllData),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            headers: {
              "X-CSRFToken": csrfToken, // Add CSRF token to the request headers
            },
            success: function (response) {
              if (response.status === "error") {
                alert(response.message);
              }
              console.log("Email sent successfully:", response);
            },
            error: function (xhr, status, error) {
              console.error("Error sending email:", error);
            },
          });
        },
        error: function (xhr, status, error) {
          console.error("Error occurred while updating data:", error);
          console.log(xhr.responseText);
          alert("Error: " + error.message);
          popup.style.display = "none"; // Close the popup
        },
      });
    } else {
      alert("Please fill in all required fields before submitting.");
    }
  });
});

// Function to convert Decimal Degrees to DMS
function convertToDMS(decimalDegree) {
  const degrees = Math.floor(decimalDegree); // Extract degrees
  const minutesDecimal = Math.abs((decimalDegree - degrees) * 60); // Convert remaining to minutes
  const minutes = Math.floor(minutesDecimal); // Extract whole minutes
  const seconds = ((minutesDecimal - minutes) * 60).toFixed(5); // Convert remaining to seconds with 5 decimals
  return { degrees, minutes, seconds };
}

// Function to convert DMS to Decimal Degrees
function convertToDecimalDegrees(degrees, minutes, seconds) {
  const decimalDegrees = Math.abs(degrees) + minutes / 60 + seconds / 3600; // Convert DMS to decimal
  return degrees < 0 ? -decimalDegrees : decimalDegrees; // Handle negative degrees
}

// Update DMS fields when Decimal Degrees change
function updateDMSFields(lat, lon) {
  const latDMS = convertToDMS(lat);
  document.getElementById("lat-degrees").textContent = latDMS.degrees;
  document.getElementById("lat-minutes").textContent = latDMS.minutes;
  document.getElementById("lat-seconds").textContent = latDMS.seconds;

  const lonDMS = convertToDMS(lon);
  document.getElementById("lon-degrees").textContent = lonDMS.degrees;
  document.getElementById("lon-minutes").textContent = lonDMS.minutes;
  document.getElementById("lon-seconds").textContent = lonDMS.seconds;
}

// Update Decimal Degrees when DMS fields change
function updateDecimalFields() {
  const latDegrees = parseInt(
    document.getElementById("lat-degrees").value || 0,
    10
  );
  const latMinutes = parseFloat(
    document.getElementById("lat-minutes").value || 0
  );
  const latSeconds = parseFloat(
    document.getElementById("lat-seconds").value || 0
  );
  const latDecimal = convertToDecimalDegrees(
    latDegrees,
    latMinutes,
    latSeconds
  );
  document.getElementById("current-lat").value = latDecimal.toFixed(6);

  const lonDegrees = parseInt(
    document.getElementById("lon-degrees").value || 0,
    10
  );
  const lonMinutes = parseFloat(
    document.getElementById("lon-minutes").value || 0
  );
  const lonSeconds = parseFloat(
    document.getElementById("lon-seconds").value || 0
  );
  const lonDecimal = convertToDecimalDegrees(
    lonDegrees,
    lonMinutes,
    lonSeconds
  );
  document.getElementById("current-lon").value = lonDecimal.toFixed(6);
}

// Event Listeners for Decimal Degrees Fields
document.getElementById("current-lat").addEventListener("input", () => {
  const lat = parseFloat(document.getElementById("current-lat").value || 0);
  const lon = parseFloat(document.getElementById("current-lon").value || 0);
  updateDMSFields(lat, lon);
});

document.getElementById("current-lon").addEventListener("input", () => {
  const lat = parseFloat(document.getElementById("current-lat").value || 0);
  const lon = parseFloat(document.getElementById("current-lon").value || 0);
  updateDMSFields(lat, lon);
});

// Event Listeners for DMS Fields
const dmsFields = [
  "lat-degrees",
  "lat-minutes",
  "lat-seconds",
  "lon-degrees",
  "lon-minutes",
  "lon-seconds",
];
dmsFields.forEach((fieldId) => {
  document
    .getElementById(fieldId)
    .addEventListener("input", updateDecimalFields);
});

// Select radio buttons
const toggleDms = document.getElementById("toggle-dms"); // For DMS radio button
const toggleDecimal = document.getElementById("toggle-decimal"); // For Decimal Degrees radio button

// Select elements for the fields
const decimalFields = document.getElementById("decimal-degrees-fields");
const degminsecFields = document.getElementById("dms-fields");

// Set initial state based on the default checked radio button
decimalFields.style.display = "block"; // Display decimal degrees fields by default
degminsecFields.style.display = "none"; // Hide DMS fields initially

// Toggle functionality when radio button changes
toggleDms.addEventListener("change", () => {
  if (toggleDms.checked) {
    decimalFields.style.display = "none"; // Hide decimal degrees fields
    degminsecFields.style.display = "block"; // Show DMS fields
  }
});

toggleDecimal.addEventListener("change", () => {
  if (toggleDecimal.checked) {
    degminsecFields.style.display = "none"; // Hide DMS fields
    decimalFields.style.display = "block"; // Show decimal degrees fields
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const selectElement = document.querySelector(".site-select");
  const optionsList = document.querySelector(".site-option-list");
  const selectedValue = document.querySelector(".select");
  const inputElement = document.getElementById("site");

  selectElement.addEventListener("click", function () {
    optionsList.classList.toggle("show");
  });

  document.querySelectorAll(".site-option-list .option").forEach((option) => {
    option.addEventListener("click", function () {
      selectedValue.textContent = option.textContent;
      inputElement.value = option.dataset.value;
      optionsList.classList.remove("show");
    });
  });

  // Close the dropdown if clicking outside
  document.addEventListener("click", function (event) {
    if (!selectElement.contains(event.target)) {
      optionsList.classList.remove("show");
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const loadingPopup = document.getElementById("loading-popup");
  const siteInfoSection = document.getElementById("site-info-section");
  const checkDataButton = document.getElementById("check-data");
  const background = document.getElementById("background");

  // Function to update the background height based on the visibility of the site-info-section
  function updateBackgroundHeight() {
    if (siteInfoSection.classList.contains("visible")) {
      background.style.height = "1600px"; // Set height to 1600px when visible
    } else {
      background.style.height = "600px"; // Set height to 600px when hidden
    }
  }

  // Function to trigger auto-scroll after loading popup is hidden
  const observer = new MutationObserver(() => {
    if (loadingPopup.style.display === "none") {
      // Trigger simultaneous show of the background and site-info-section
      siteInfoSection.classList.add("visible"); // Make the section visible
      updateBackgroundHeight(); // Update the background height immediately

      // Auto-scroll to the "Site Information" section
      siteInfoSection.scrollIntoView({ behavior: "smooth" });

      observer.disconnect(); // Stop observing after the popup is hidden
    }
  });

  // Add click event listener to "Check Data" button
  checkDataButton.addEventListener("click", () => {
    // Hide the loading popup and show the site info section
    loadingPopup.style.display = "none";

    // Use visibility and opacity transition for a smooth reveal
    siteInfoSection.classList.add("visible"); // Make the section visible

    // Observe changes to the style attribute of the loading popup
    observer.observe(loadingPopup, {
      attributes: true,
      attributeFilter: ["style"],
    });
  });

  // Initial check to set the correct background height on page load
  updateBackgroundHeight();
});

const sendEmailToUser = () => {
  const data = {
    registrationData: registrationData,
    calculationData: rawData,
  };

  // ajax script to send send email to user

  $.ajax({
    url: userEmailUrl,
    type: "POST",
    data: JSON.stringify(data),
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    headers: {
      "X-CSRFToken": csrfToken, // Add CSRF token to the request headers
    },
    success: function (response) {
      if (response.status === "error") {
        alert(response.message);
      }
      alert(`Your results have been sent at ${response.email}`);
    },
    error: function (xhr, status, error) {
      console.error("Error sending email:", error);
    },
  });
};

const emailButton = document.getElementById("email-results");

emailButton.addEventListener("click", sendEmailToUser);
