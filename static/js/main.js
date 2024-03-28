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

    // Edit Comment Button
    /*const editButtons = document.getElementsByClassName("edit-comment");
    const commentText = document.getElementById("id_body");
    const commentForm = document.getElementById("commentForm");
    const submitButton = document.getElementById("submitButton");*/

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

    // Trigger Deletion button of Post Modal
    // Show modal when delete button is clicked
    document.getElementById('delete-post-button').addEventListener('click', function() {
        document.getElementById('deletePostModal').style.display = 'block';
    });

    // Hide modal when cancel button is clicked
    document.querySelector('#deletePostModal .modal-footer .btn-secondary').addEventListener('click', function() {
        document.getElementById('deletePostModal').style.display = 'none';
    });

    // Edit Comment
    document.querySelectorAll('.btn-edit-comment').forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const commentBody = document.querySelector(`#comment${commentId} p`).textContent;
            document.querySelector('#id_body').value = commentBody.trim();
            document.querySelector('#comment-id').value = commentId;
            document.querySelector('#edit-comment-form').style.display = 'block';
        });
    });
    
    document.querySelectorAll('.btn-delete-comment').forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            document.querySelector('#comment-id').value = commentId;
            document.querySelector('#delete-comment-form').style.display = 'block';
        });
    });

    // Edit Comment / Toggle Edit button
   /* for (let button of editButtons) {
        button.addEventListener("click", (e) => {
            // Get the comment ID and content
            let commentId = e.target.getAttribute("comment_id");
            let commentContent = document.getElementById(`comment${commentId}`).innerText;
            
            // Update the form fields and button text
            commentText.value = commentContent;
            submitButton.innerText = "Update";
            
            // Update the form action to include comment ID
            commentForm.setAttribute("action", `edit_comment/${commentId}`);
        });
    }*/
});