function toggleNavbar() {
    var navbar = document.getElementById("myNavbar");
    if (navbar.className === "navbar") {
        navbar.className += " responsive";
    } else {
        navbar.className = "navbar";
    }
}
function previewProfileImage() {
    var preview = document.getElementById('previewImage');
    var fileINput = document.getElementById('profileImage');
    var file = fileINput.files[0];

    if (file) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(file)
    }
}

function populateCountries() {
    var countryListDiv = document.getElementById("countryList");
    countryListDiv.innerHTML = ""; // Clear previous list

    // Create the select element for the dropdown list
    var select = document.createElement("select");
    select.setAttribute("id", "countrySelect");
    select.setAttribute("name", "country");

    // Loop through all countries and add them to the dropdown list
    for (var countryCode in countryListDiv) {
        if (countryListDiv.hasOwnProperty(countryCode)) {
            var countryName = countryListDiv[countryCode];
            var option = document.createElement("option");
            option.text = countryName;
            option.value = countryCode;
            select.appendChild(option);
        }
    }

    // Append the select element to the countryListDiv
    countryListDiv.appendChild(select);
}

// Function to show the dropdown list of countries when the country input field is clicked
function showCountries() {
    var countryListDiv = document.getElementById("countryList");
    if (countryListDiv.style.display === "none") {
        populateCountries(); // Populate the dropdown list if it's not already populated
        countryListDiv.style.display = "block";
    } else {
        countryListDiv.style.display = "none";
    }
}

// Call the function to populate countries when the page is loaded
window.onload = populateCountries;











