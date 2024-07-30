function toggleNavbar() {
    var navbar = document.getElementById("myNavbar");
    if (navbar.className === "navbar") {
        navbar.className += " responsive";
    } else {
        navbar.className = "navbar";
    }
}

// Function to preview the profile image
function previewProfileImage() {
    const file = document.getElementById('profileImage').files[0];
    const preview = document.getElementById('previewImage');

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result; // Set the image source to the uploaded file
            preview.style.display = 'block'; // Ensure the image is displayed
        }
        reader.readAsDataURL(file); // Read the file as a data URL
    } else {
        preview.src = '{% static "images/woman.jpg" %}'; // Reset to default image if no file is selected
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Add event listener for the file input to preview the image
    document.getElementById('profileImage').addEventListener('change', previewProfileImage);

    // Fetch country data from the API
    fetch('https://restcountries.com/v3.1/all')
        .then(res => res.json())
        .then(data => {
            const countrySelect = document.querySelector('#country');
            const locationSelect = document.querySelector('#location');

            if (countrySelect && locationSelect) {
                data.forEach(country => {
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

    // Handle form submission
    document.querySelector('form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        const selectedCountryCode = countrySelect.value;
        const selectedLocationCode = locationSelect.value;

        // Create a data object to send to the server
        const data = {
            country: selectedCountryCode,
            location: selectedLocationCode
        };

        // Send the data to the Django backend
        fetch('/your-django-endpoint/', { // Replace with your actual endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(result => {
                console.log('Success:', result);
                // Handle the result here (e.g., display the full country names)
                alert(`Country of Origin: ${result.country_name}, Country of Study: ${result.location_name}`);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Check if this cookie string begins with the name we want
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});