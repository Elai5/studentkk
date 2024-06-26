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

// Fetch country data from the API
fetch('https://restcountries.com/v3.1/all')
    .then(res => res.json())
    .then(data => {
        const countrySelect = document.querySelector('#country');
        const locationSelect = document.querySelector('#location');

        data.forEach(country => {
            const option = document.createElement('option');
            option.value = country.alpha3Code; // Use ISO code as the value
            option.textContent = country.name; // Display country name

            countrySelect.appendChild(option);
            locationSelect.appendChild(option.cloneNode(true)); // Clone for the other dropdown
        });
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
institutionInput.addEventListener('input', () => {
    const inputValue = institutionInput.value.toLowerCase();
    const filteredUniversities = universities.filter(univ => univ.toLowerCase().startsWith(inputValue));

    const datalist = document.querySelector('#institution-datalist');
    datalist.innerHTML = '';
    filteredUniversities.forEach(univ => {
        const option = document.createElement('option');
        option.value = univ;
        datalist.appendChild(option);
    });
});










