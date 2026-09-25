const {
    ClassicEditor,
    Essentials,
    Bold,
    Italic,
    Font,
    Paragraph,
    Image,
    ImageUpload,
    Base64UploadAdapter
} = CKEDITOR;

ClassicEditor
    .create({
        attachTo: document.querySelector('#editor'),

        licenseKey: 'eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3OTExNTgzOTksImp0aSI6ImY2OWQ2YTk2LTZlZGMtNDAwNC1hNDE5LWRlNTEyYTk4ZWY1MCIsInVzYWdlRW5kcG9pbnQiOiJodHRwczovL3Byb3h5LWV2ZW50LmNrZWRpdG9yLmNvbSIsImRpc3RyaWJ1dGlvbkNoYW5uZWwiOlsiY2xvdWQiLCJkcnVwYWwiLCJzaCJdLCJ3aGl0ZUxhYmVsIjp0cnVlLCJsaWNlbnNlVHlwZSI6InRyaWFsIiwiZmVhdHVyZXMiOlsiKiJdLCJyZW1vdmVGZWF0dXJlcyI6WyJBSSJdLCJ2YyI6ImFhNjZkNWZhIn0.0D0U7Icd3QzOFTJTgSeBWVyN902GNd5zZS8GdKHbNYH1oV0LDEgXVLVtG7CBZF1_We3lZGvcWSee8Ix-FWH9-A',

        plugins: [
            Essentials,
            Bold,
            Italic,
            Font,
            Paragraph,
            Image,
            ImageUpload,
            Base64UploadAdapter
        ],

        toolbar: [
            'undo', 'redo', '|',
            'bold', 'italic', '|',
            'fontSize',
            'fontFamily',
            'fontColor',
            'fontBackgroundColor',
            '|',
            'uploadImage'
        ],

        root: {
            placeholder: 'Type here...'
        }
    })
    .then(editor => {

        document.querySelector('#postForm').addEventListener('submit', function () {
            document.querySelector('#content').value = editor.getData();
        });

    })
    .catch(error => {
        console.error(error);
    });
