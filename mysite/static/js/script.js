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
        preview.style.display = 'block'; // Ensure the default image is displayed
    }
}


document.addEventListener("DOMContentLoaded", function () {
    // check elements exist
    const profileImageInput = document.getElementById('profileImage');
    if (profileImageInput) {
        profileImageInput.addEventListener('change', previewProfileImage);
    } else {
        console.error("ELement with ID 'profileImage' not found")
    }
    // Add event listener for the file input to preview the image
    // document.getElementById('profileImage').addEventListener('change', previewProfileImage);






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


document.addEventListener('DOMContentLoaded', function () {
    // Function to show only the first news item in each category on mobile
    function adjustNewsDisplay() {
        const newsCategories = document.querySelectorAll('.news-category');

        newsCategories.forEach(category => {
            const newsCards = category.querySelectorAll('.news-card');
            if (newsCards.length > 1) {
                newsCards.forEach((card, index) => {
                    if (index > 0) {
                        card.style.display = 'none'; // Hide all but the first news card
                    }
                });
            }
        });
    }

    // Check screen width and adjust news display
    function handleResize() {
        if (window.innerWidth <= 600) {
            adjustNewsDisplay();
        } else {
            // Show all news cards on larger screens
            const newsCards = document.querySelectorAll('.news-card');
            newsCards.forEach(card => {
                card.style.display = 'block';
            });
        }
    }

    // Initial check
    handleResize();

    // Recheck on window resize
    window.addEventListener('resize', handleResize);
});
