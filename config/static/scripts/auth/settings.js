const imageInput = document.getElementById('ImageUpload');
const previewImage = document.getElementById('previewImage');
const deleteAvatar = document.getElementById('DeleteAvatar');

const defaultImage = '/media/avatars/default.jpg';

imageInput.addEventListener('change', function () {
    const file = this.files[0];

    if (file) {
        previewImage.src = URL.createObjectURL(file);
        deleteAvatar.value = 'false';
    }
});

document.getElementById('ImageDelete').addEventListener('click', function () {
    imageInput.value = '';
    previewImage.src = defaultImage;
    deleteAvatar.value = 'true';
});
