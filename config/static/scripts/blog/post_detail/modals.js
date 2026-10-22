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
const editButtons = document.querySelectorAll(
    '[data-comment-id]'
);

const form = document.getElementById('edit-comment-form');
const input = document.getElementById('edit-comment-input');

editButtons.forEach(button => {
    button.addEventListener('click', () => {
        const post_id = button.dataset.postId;
        const comment_id = button.dataset.commentId;

        input.value = button.dataset.commentText;

        form.action = `/comment/posts/${post_id}/comment/${comment_id}/edit/`;
    });
});
