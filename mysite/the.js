
function toggleNavbar() {
    var navbar = document.getElementById("myNavbar");
    if (navbar.className === "navbar") {
        navbar.className += " responsive";
    } else {
        navbar.className = "navbar";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Function to preview the profile image
    function previewProfileImage(fileInputId, previewImageId) {
        var preview = document.getElementById(previewImageId);
        var fileInput = document.getElementById(fileInputId);

        // Check if the file input exists
        if (!fileInput) {
            console.error('File input element not found:', fileInputId);
            return; // Exit if the file input is not found
        }

        var file = fileInput.files[0];

        if (file) {
            var reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result; // Set the preview image source
            };
            reader.readAsDataURL(file);
        }
    }

    // Add event listeners for the signup form
    var signupFileInput = document.getElementById('profileImage'); // ID for signup file input
    if (signupFileInput) {
        signupFileInput.addEventListener('change', function () {
            previewProfileImage('profileImage', 'previewImage'); // IDs for preview
        });
    } else {
        console.error('Signup file input element not found');
    }

    // Add event listeners for the edit profile form
    var editFileInput = document.getElementById('editProfileImage'); // ID for edit profile file input
    if (editFileInput) {
        editFileInput.addEventListener('change', function () {
            previewProfileImage('editProfileImage', 'editPreviewImage'); // IDs for preview
        });
    } else {
        console.error('Edit file input element not found');
    }

    // Fetch country data from the API

    fetch('https://restcountries.com/v3.1/all')
        .then(res => res.json())
        .then(data => {
            console.log('Fetched countries data:', data); // Log the fetched data
            const countrySelect = document.querySelector('#country'); // Matches the ID in your HTML
            const locationSelect = document.querySelector('#location'); // Matches the ID in your HTML

            if (countrySelect && locationSelect) {
                // Sort the countries alphabetically by their common name
                const sortedCountries = data.sort((a, b) =>
                    a.name.common.localeCompare(b.name.common)
                );

                sortedCountries.forEach(country => {
                    const option = document.createElement('option');
                    option.value = country.cca2; // Use ISO code as the value
                    option.textContent = country.name.common; // Display country name

                    countrySelect.appendChild(option);
                    locationSelect.appendChild(option.cloneNode(true)); // Clone for the other dropdown
                });
            } else {
                console.error('Country select elements not found');
            }
        })
        .catch(error => {
            console.error('Error fetching country data:', error);
        });

    // Example universities array (replace with your actual data)
    const universities = [
        'Harvard University',
        'Stanford University',
        'Massachusetts Institute of Technology (MIT)',
        'University of Oxford',
        // Add more universities here...
    ];

    const institutionInput = document.querySelector('#institution');
    if (institutionInput) {
        institutionInput.addEventListener('input', () => {
            const inputValue = institutionInput.value.toLowerCase();
            const filteredUniversities = universities.filter(univ => univ.toLowerCase().startsWith(inputValue));

            const datalist = document.querySelector('#institution-datalist');
            if (datalist) {
                datalist.innerHTML = ''; // Clear previous options
                filteredUniversities.forEach(univ => {
                    const option = document.createElement('option');
                    option.value = univ;
                    datalist.appendChild(option);
                });
            } else {
                console.error('Datalist element not found');
            }
        });
    } else {
        console.error('Institution input element not found');
    }
});





