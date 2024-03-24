/*document.addEventListener('DOMContentLoaded', function() {*/
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

    function changeTitleColor() {

        // Iterate over every single Post to change heading colors
        for (let i = 0; i < postDetailTitles.length; i++) {
            postDetailTitles[i].style.color = 'white';
        }
    }

    window.addEventListener('load', changeTitleColor);


    // Create New Post
    if (newPostBtn && formContainer && newPostContainer) {
        newPostBtn.addEventListener('click', function() {
            formContainer.style.display = 'block';
            newPostContainer.style.display = 'none';
            changeLabelColor('white', 'bold');
        });
    }

    // Change the color of label titles
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

    // Handle Slug Field in CreateNewPostForm
    if (titleInput && slugInput) {
        titleInput.addEventListener('input', function() {
            const title = titleInput.value;
            const slug = title.toLowerCase().replace(/\s+/g, '-').slice(0, 50);
            slugInput.value = slug;
        });
    }


    // Update Blog Post

    /*if (editButton) {
        editButton.addEventListener('click', function() {
            // Get the post slug
            const postSlug = '{{ post.slug }}';
            // Redirect to the update_post page with the post slug
            window.location.href = `/update_post/`;
        });
    }*/

    if (editButton && editFormContainer && cancelButton) {
        editButton.addEventListener('click', function() {
            editFormContainer.style.display = 'block';
            editButton.style.display = 'none';
        });

        cancelButton.addEventListener('click', function() {
            editFormContainer.style.display = 'none';
            editButton.style.display = 'block';
        });
    }
/*});*/