function changeTitleColor() {
    const postDetailTitles = document.getElementsByClassName('post-title');

    // Iterate over every single Post to change heading colors
    for (let i = 0; i < postDetailTitles.length; i++) {
        postDetailTitles[i].style.color = 'white';
    }
}

window.addEventListener('load', changeTitleColor);



/* Update Blog Post
document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('edit-button');
    const editForm = document.getElementById('edit-form');

    editButton.addEventListener('click', function() {
        editForm.style.display = 'block';
        editButton.style.display = 'none';
    });

    const cancelButton = document.getElementById('cancel-button');
    cancelButton.addEventListener('click', function() {
        editForm.style.display = 'none';
        editButton.style.display = 'block';
    });
});*/


// Update Blog Post
document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('edit-button');
    const editForm = document.getElementById('edit-form');
    const cancelButton = document.getElementById('cancel-button');

    if (editButton && editForm && cancelButton) {
        editButton.addEventListener('click', function() {
            editForm.style.display = 'block';
            editButton.style.display = 'none';
        });

        cancelButton.addEventListener('click', function() {
            editForm.style.display = 'none';
            editButton.style.display = 'block';
        });
    }
});

// Create New Post
document.addEventListener('DOMContentLoaded', function() {
    // Show form when "New Post" button is clicked
    document.getElementById('new-post-btn').addEventListener('click', function() {
        document.getElementById('form-container').style.display = 'block';
        document.getElementById('new-post-container').style.display = 'none'; // hide New Post container when form is opened
        document.getElementById('page-title').style.color = 'white'; // THIS HAVE TO BE ADJUSTED TO CHANGE ALL HEADING COLORS WHEN FORM TRIGGERED!!!
    });

    // Change the color of the page title to white when the window is loaded
    changeTitleColor();

    // Change the color of the page title to white
    function changeTitleColor() {
        document.getElementById('page-title').style.color = 'white';// THIS ISN'T OPTIMAL NETHER, ADJUST IT TO CHANGE ALL HEADING COLORS WITHIN THE FORM!!!!
    }
});
