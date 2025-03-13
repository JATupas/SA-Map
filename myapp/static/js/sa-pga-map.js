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
  window.map = L.map("map", {
    center: [13.41, 121], 
    zoom: 6,
    minZoom: 6,
    maxZoom: 18,
    maxBounds: [
        [3.5, 114],  // Southwest corner (Lower-left of PH)
        [21.5, 127]  // Northeast corner (Upper-right of PH)
    ],
    maxBoundsViscosity: 1.0
  }); // Set initial coordinates

  var marker = null; // Marker variable to store the current marker on the map

  // Add a tile layer to the map
  L.tileLayer('http://localhost:8080/styles/basic-preview/512/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18,
    tileSize: 256
  }).addTo(map);


  // Function to convert Decimal Degrees to DMS
  // Convert Decimal Degrees to DMS
  function convertToDMS(decimalDegree) {
    const degrees = Math.floor(decimalDegree);
    const minutesDecimal = Math.abs((decimalDegree - degrees) * 60);
    const minutes = Math.floor(minutesDecimal);
    const seconds = ((minutesDecimal - minutes) * 60).toFixed(5);
    return { degrees, minutes, seconds };
  }

  // Convert DMS to Decimal Degrees
  function convertToDecimalDegrees(degrees, minutes, seconds) {
    const sign = degrees < 0 ? -1 : 1;
    return sign * (Math.abs(degrees) + minutes / 60 + seconds / 3600);
  }

  // Function to update DMS fields from Decimal Degrees input
  function updateDMS() {
    let lat = parseFloat(document.getElementById("current-lat").value);
    let lon = parseFloat(document.getElementById("current-lon").value);

    if (!isNaN(lat)) {
        const latDMS = convertToDMS(lat);
        document.getElementById("lat-degrees").value = latDMS.degrees;
        document.getElementById("lat-minutes").value = latDMS.minutes;
        document.getElementById("lat-seconds").value = latDMS.seconds;
    }
    if (!isNaN(lon)) {
        const lonDMS = convertToDMS(lon);
        document.getElementById("lon-degrees").value = lonDMS.degrees;
        document.getElementById("lon-minutes").value = lonDMS.minutes;
        document.getElementById("lon-seconds").value = lonDMS.seconds;
    }
  }

  // Function to update Decimal Degrees from DMS input
  function updateDecimalDegrees() {
    let latDegrees = parseFloat(document.getElementById("lat-degrees").value) || 0;
    let latMinutes = parseFloat(document.getElementById("lat-minutes").value) || 0;
    let latSeconds = parseFloat(document.getElementById("lat-seconds").value) || 0;

    let lonDegrees = parseFloat(document.getElementById("lon-degrees").value) || 0;
    let lonMinutes = parseFloat(document.getElementById("lon-minutes").value) || 0;
    let lonSeconds = parseFloat(document.getElementById("lon-seconds").value) || 0;

    let lat = convertToDecimalDegrees(latDegrees, latMinutes, latSeconds);
    let lon = convertToDecimalDegrees(lonDegrees, lonMinutes, lonSeconds);

    document.getElementById("current-lat").value = lat.toFixed(6);
    document.getElementById("current-lon").value = lon.toFixed(6);
  }

  // Add event listeners for real-time syncing
  document.getElementById("current-lat").addEventListener("input", updateDMS);
  document.getElementById("current-lon").addEventListener("input", updateDMS);

  document.getElementById("lat-degrees").addEventListener("input", updateDecimalDegrees);
  document.getElementById("lat-minutes").addEventListener("input", updateDecimalDegrees);
  document.getElementById("lat-seconds").addEventListener("input", updateDecimalDegrees);

  document.getElementById("lon-degrees").addEventListener("input", updateDecimalDegrees);
  document.getElementById("lon-minutes").addEventListener("input", updateDecimalDegrees);
  document.getElementById("lon-seconds").addEventListener("input", updateDecimalDegrees);

  // Map click event
  map.on("click", function (e) {
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;

    // Update the latitude and longitude input fields
    document.getElementById("current-lat").value = lat;
    document.getElementById("current-lon").value = lon;

    updateDMS();

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
          map.setView([newLat, newLon], 17); // Zoom in to the new marker
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

  // Function to update the background height based on visibility and screen width
  function updateBackgroundHeight() {
    const isMaxWidth360 = window.matchMedia("(max-width: 360px)").matches;
    const isMaxWidth1023 = window.matchMedia("(max-width: 1023px)").matches;
    const isMinWidth1024 = window.matchMedia("(min-width: 1024px)").matches;

    if (siteInfoSection.classList.contains("visible")) {
      if (isMinWidth1024) {
        background.style.height = "1725px"; 
      } else if (isMaxWidth1023) {
        background.style.height = "2400px"; 
      } else if (isMaxWidth360) {
        background.style.height = "2750px"; 
      } else {
        background.style.height = "1725px"; 
      }
    } else { 
      if (isMinWidth1024) {
        background.style.height = "600px"; 
      } else if (isMaxWidth1023) {
        background.style.height = "1100px"; 
      } else if (isMaxWidth360) {
        background.style.height = "1050px"; 
      } else {
        background.style.height = "600px"; 
      }
    }
  }

  // Function to handle visibility and update background height when fully visible
  function showSiteInfoSection() {
    siteInfoSection.classList.add("visible");

    // Use requestAnimationFrame to wait for DOM update
    requestAnimationFrame(() => {
      // Use Intersection Observer to detect when it's actually visible
      const observer = new IntersectionObserver(
        (entries, observer) => {
          if (entries[0].isIntersecting) {
            updateBackgroundHeight(); // Resize background after section is visible
            observer.disconnect(); // Stop observing once done
          }
        },
        { threshold: 0.5 } // Trigger when 50% of the section is visible
      );

      observer.observe(siteInfoSection);
      siteInfoSection.scrollIntoView({ behavior: "smooth" });
    });
  }

  // Observer to detect when loading popup is hidden
  const observer = new MutationObserver(() => {
    if (loadingPopup.style.display === "none") {
      showSiteInfoSection();
      observer.disconnect();
    }
  });

  // Add click event listener to "Check Data" button
  checkDataButton.addEventListener("click", () => {
    loadingPopup.style.display = "none";

    // Delay execution to ensure the section renders before resizing the background
    setTimeout(() => {
      showSiteInfoSection();
    }, 200); // Adjust if needed

    observer.observe(loadingPopup, {
      attributes: true,
      attributeFilter: ["style"],
    });
  });

  // Update height on window resize
  window.addEventListener("resize", updateBackgroundHeight);

  // Initial background height update on page load
  updateBackgroundHeight();
});


const sendEmailToUser = (imageFile) => {
  const formData = new FormData();
  const loadingPopup = document.getElementById("loading-popup");
  formData.append("registrationData", JSON.stringify(registrationData));
  formData.append("calculationData", JSON.stringify(rawData));
  formData.append("imageFile", imageFile, "map_snapshot.png"); // Attach the image file

  $.ajax({
      url: userEmailUrl,
      type: "POST",
      data: formData,
      processData: false, // Prevent jQuery from processing the data
      contentType: false, // Prevent jQuery from setting content type
      headers: {
          "X-CSRFToken": csrfToken, // Add CSRF token to the request headers
      },
      success: function (response) {
          if (response.status === "error") {
              alert(response.message);
          }
          alert(`Results have been emailed to ${response.email}`);
          loadingPopup.style.display = "none";
      },
      error: function (xhr, status, error) {
          console.error("Error sending email:", error);
          if (xhr.responseJSON) {
              console.error("Server Error:", xhr.responseJSON.message);
              console.error("Traceback:", xhr.responseJSON.trace);
              alert("Error: " + xhr.responseJSON.message);  // Show Django error in alert
          } else {
              alert("Unknown server error occurred.");
          }
      },
  });
};





// document.addEventListener("DOMContentLoaded", function () {
//   const emailButton = document.getElementById("email-results");
//   const warningModal = document.getElementById("email-warning-modal");
//   const confirmButton = document.getElementById("confirm-email-send");
//   const cancelButton = document.getElementById("cancel-email-send");
//   const loadingPopup = document.getElementById("loading-popup");

//   if (emailButton) {
//       emailButton.addEventListener("click", function () {
//           warningModal.style.display = "flex"; // Show warning popup
//       });

//       cancelButton.addEventListener("click", function () {
//           warningModal.style.display = "none"; // Hide warning popup
//       });

//       confirmButton.addEventListener("click", function () {
//           warningModal.style.display = "none"; // Hide warning popup
//           loadingPopup.style.display = "flex"; // Show loading popup

//           sendEmailToUser(); // Send email after confirmation

//           // Hide loading popup after 5 seconds (adjust as needed)
//           setTimeout(function () {
//               loadingPopup.style.display = "none";
//           }, 5000);
//       });
//   }
// });



document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("terms-popup");
    const acceptBtn = document.getElementById("accept-btn");
    const declineBtn = document.getElementById("decline-btn");

    // Ensure popup is always visible when the page loads
    popup.style.display = "flex";

    // Handle Accept Button Click
    acceptBtn.addEventListener("click", function () {
        popup.classList.add("hide"); // Add fade-out effect

        // Wait for animation to finish before hiding completely
        setTimeout(() => {
            popup.style.display = "none";
        }, 500);
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    const hamburger = document.querySelector('.hamburger');

    menuToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      hamburger.classList.toggle('open');
    });
  });

document.addEventListener("DOMContentLoaded", function () {
  const emailButton = document.getElementById("email-results");
  const warningModal = document.getElementById("email-warning-modal");
  const confirmButton = document.getElementById("confirm-email-send");
  const cancelButton = document.getElementById("cancel-email-send");
  const loadingPopup = document.getElementById("loading-popup");
  const mapPreviewContainer = document.getElementById("map-preview-container");
  const downloadMapButton = document.getElementById("download-map-button");

  if (emailButton) {
      emailButton.addEventListener("click", function () {
          warningModal.style.display = "flex";
      });

      cancelButton.addEventListener("click", function () {
          warningModal.style.display = "none"; // Hide warning popup
      });

      confirmButton.addEventListener("click", function () {
          warningModal.style.display = "none"; // Hide warning popup
          loadingPopup.style.display = "flex"; // Show loading popup
      
          captureLeafletMap((imageFile) => {  // Capture map as a file (Blob)
            if (!imageFile) {
                console.error("Map image capture failed!");
                return;
            }
            console.log("Captured Image File:", imageFile);

            sendEmailToUser(imageFile); // Send image as a file
          });
      });
    
  }

  function captureLeafletMap(callback) {
    if (window.map) {
        leafletImage(window.map, function (err, canvas) {
            if (err) {
                console.error("Error capturing Leaflet map:", err);
                return;
            }

            canvas.toBlob(function (blob) {
                if (!blob) {
                    console.error("Failed to convert canvas to Blob.");
                    return;
                }

                const file = new File([blob], "map_capture.png", { type: "image/png" });

                if (typeof callback === "function") {
                    callback(file); // Pass the image file to the callback
                }
            }, "image/png");
        });
    } else {
        console.warn("Leaflet map is not initialized.");
    }
  }
});
