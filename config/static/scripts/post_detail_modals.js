document.addEventListener('DOMContentLoaded', () => {
    const deleteCommentForm = document.getElementById('delete-comment-form');
    const deletePostForm = document.getElementById('delete-post-form');

    document.querySelectorAll('.delete-comment-btn').forEach(button => {
        button.addEventListener('click', () => {
            const deleteUrl = button.dataset.deleteUrl;
            deleteCommentForm.action = deleteUrl;
        });
    });

    document.querySelectorAll('.delete-post-btn').forEach(button => {
        button.addEventListener('click', () => {
            const deleteUrl = button.dataset.deleteUrl;
            deletePostForm.action = deleteUrl;
        });
    });
});
