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
/*document.addEventListener('DOMContentLoaded', function() {
    // Show form when "New Post" button is clicked
    document.getElementById('new-post-btn').addEventListener('click', function() {
        document.getElementById('form-container').style.display = 'block';
        document.getElementById('new-post-container').style.display = 'none'; // hide New Post container when form is opened
        document.getElementById('page-title').style.color = 'white'; // THIS HAVE TO BE ADJUSTED TO CHANGE ALL HEADING COLORS WHEN FORM TRIGGERED!!!
    });

    // Change the color of the page title to white when the window is loaded
    window.addEventListener('load', changePageTitleColor);

    // Change the color of the page title to white
    function changePageTitleColor() {
        document.getElementById('page-title').style.color = 'white';// THIS ISN'T OPTIMAL NETHER, ADJUST IT TO CHANGE ALL HEADING COLORS WITHIN THE FORM!!!!
        document.getElementById('id_title').style.color = 'white';
        document.getElementById('id_content').style.color = 'white';
        document.getElementById('id_excerpt').style.color = 'white';
    }
});*/

// Create New Post
document.addEventListener('DOMContentLoaded', function() {
    // Show form
    document.getElementById('new-post-btn').addEventListener('click', function() {
        document.getElementById('form-container').style.display = 'block';
        document.getElementById('new-post-container').style.display = 'none'; 
        changeLabelColor('white', 'bold'); 
    });

    // Change the color of label titles
    function changeLabelColor(color, fontWeight) {
        const labels = document.querySelectorAll('label[for]');
        labels.forEach(label => {
            const inputId = label.getAttribute('for');
            const input = document.getElementById(inputId);
            if (input) {
                label.style.color = color;
                label.style.fontWeight = fontWeight;
            }
        });
    }
});



// Handel Slug Field in CreateNewPostForm
document.addEventListener('DOMContentLoaded', function() {
    const titleInput = document.getElementById('id_title');
    const slugInput = document.getElementById('id_slug');

    titleInput.addEventListener('input', function() {
        const title = titleInput.value;
        const slug = title.toLowerCase().replace(/\s+/g, '-').slice(0, 50);
        slugInput.value = slug;
    });
});


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