function toggleNavbar() {
    var navbar = document.getElementById("myNavbar");
    if (navbar.className === "navbar") {
        navbar.className += " responsive";
    } else {
        navbar.className = "navbar";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    function previewProfileImage() {
        var preview = document.getElementById('previewImage');
        var fileInput = document.getElementById('profileImage');
        var file = fileInput.files[0];

        if (file) {
            var reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    }

    // Fetch country data from the API
    fetch('https://restcountries.com/v3.1/all')
        .then(res => res.json())
        .then(data => {
            const countrySelect = document.querySelector('#country');
            const locationSelect = document.querySelector('#location');

            console.log('Country Select:', countrySelect); // Debugging line
            console.log('Location Select:', locationSelect); // Debugging line

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

    // Example universities array (replace with your actual data)
    const universities = [
        'Harvard University',
        'Stanford University',
        'Massachusetts Institute of Technology (MIT)',
        'University of Oxford',
        // Add more universities here...
    ];

    const institutionInput = document.querySelector('#institution');
    console.log('Institution Input:', institutionInput); // Debugging line

    if (institutionInput) {
        institutionInput.addEventListener('input', () => {
            const inputValue = institutionInput.value.toLowerCase();
            const filteredUniversities = universities.filter(univ => univ.toLowerCase().startsWith(inputValue));

            const datalist = document.querySelector('#institution-datalist');
            if (datalist) {
                datalist.innerHTML = '';
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
