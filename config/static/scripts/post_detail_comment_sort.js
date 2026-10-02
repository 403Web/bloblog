const commentSort = document.getElementById('comment-sort');

commentSort.addEventListener('change', function () {
    const url = new URL(window.location.href);

    if (this.value) {
        url.searchParams.set('sort', this.value);
    } else {
        url.searchParams.delete('sort');
    }

    window.location.href = url.toString();
});
