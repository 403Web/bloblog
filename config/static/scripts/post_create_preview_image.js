const imageInput = document.getElementById('ImageUpload');
const previewImage = document.getElementById('previewImage');

imageInput.addEventListener('change', function () {
    const file = this.files[0];

    if (file) {
        previewImage.src = URL.createObjectURL(file);
    }
});
