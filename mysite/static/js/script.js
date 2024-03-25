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













