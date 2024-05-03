document.addEventListener('DOMContentLoaded', function() {
    console.log("load static");
    const formContainer = document.getElementById('form-container');
    const postDetailTitles = document.getElementsByClassName('post-title');
    const newPostBtn = document.getElementById('new-post-btn');
    const newPostContainer = document.getElementById('new-post-container');
    const labels = document.querySelectorAll('label[for]');
    const titleInput = document.getElementById('id_title');
    const slugInput = document.getElementById('id_slug');
    const editButton = document.getElementById('edit-button');
    const editFormContainer = document.getElementById('edit-form-container');
    const cancelButton = document.getElementById('cancel-button');
    const deleteProfileButton = document.getElementById('delete-button');

    // Change Title Color
    function changeTitleColor() {
        for (let i = 0; i < postDetailTitles.length; i++) {
            postDetailTitles[i].style.color = 'white';
        }
    }

    // Profile Delete Button Hide
    function hideDeleteButton() {
        const deleteButton = document.getElementById('delete-button');
        if (deleteButton) {
            deleteButton.style.display = 'none';
        }
    }

    // Event Listeners
    window.addEventListener('load', changeTitleColor);
    if (editButton) {
        editButton.addEventListener('click', hideDeleteButton);
    }

    if (newPostBtn && formContainer && newPostContainer) {
        newPostBtn.addEventListener('click', showNewPostForm);
    }

    if (titleInput && slugInput) {
        titleInput.addEventListener('input', handleSlugField);
    }

    if (editButton && editFormContainer && cancelButton) {
        editButton.addEventListener('click', showEditForm);
        cancelButton.addEventListener('click', cancelEdit);
    }

    document.getElementById('delete-post-button').addEventListener('click', showModal);
    document.querySelector('#deletePostModal .modal-footer .btn-secondary').addEventListener('click', hideModal);
    document.querySelectorAll('.btn-edit-comment').forEach(addEditCommentListener);
    document.querySelectorAll('.btn-delete-comment').forEach(addDeleteCommentListener);

    // Functions
    function showNewPostForm() {
        formContainer.style.display = 'block';
        newPostContainer.style.display = 'none';
        changeLabelColor('white', 'bold');
    }

    function changeLabelColor(color, fontWeight) {
        labels.forEach(label => {
            const inputId = label.getAttribute('for');
            const input = document.getElementById(inputId);
            if (input) {
                label.style.color = color;
                label.style.fontWeight = fontWeight;
            }
        });
    }

    function handleSlugField() {
        const title = titleInput.value;
        const slug = title.toLowerCase().replace(/\s+/g, '-').slice(0, 50);
        slugInput.value = slug;
    }

    function showEditForm() {
        editFormContainer.style.display = 'block';
        editButton.style.display = 'none';
    }

    function cancelEdit() {
        editFormContainer.style.display = 'none';
        editButton.style.display = 'block';
        window.location.href = "/post_detail/<post_id>";  
    }

    function showModal() {
        document.getElementById('deletePostModal').style.display = 'block';
    }

    function hideModal() {
        document.getElementById('deletePostModal').style.display = 'none';
    }

    function addEditCommentListener(button) {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const commentBody = document.querySelector(`#comment${commentId} p`).textContent;
            document.querySelector('#id_body').value = commentBody.trim();
            document.querySelector('#comment-id').value = commentId;
            document.querySelector('#edit-comment-form').style.display = 'block';
        });
    }

    function addDeleteCommentListener(button) {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            document.querySelector('#comment-id').value = commentId;
            document.querySelector('#delete-comment-form').style.display = 'block';
        });
    }
});