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


    function changeTitleColor() {

        // Iterate over every single Post to change heading colors
        for (let i = 0; i < postDetailTitles.length; i++) {
            postDetailTitles[i].style.color = 'white';
        }
    }

    window.addEventListener('load', changeTitleColor);


    // PROFILE //
    //Profile Delete Button hide when Profile form is opened:
    document.getElementById('edit-button').addEventListener('click', function() {
        document.getElementById('delete-button').style.display = 'none';
    })


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
        
            window.location.href = "/post_detail/<post_id>";  
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

    // Up and Downvote for Posts with AJAX
    // Based on: https://www.youtube.com/watch?v=onZ69P9wS2o
    /*$(document).ready(function () {
      $(document).on('click', '.thumbaction', function (e) {
          e.preventDefault();
          console.log("Thumb button clicked");
          var postid = $(this).closest('.thumb-container').find('#thumbs').data('value'); 
          var button = $(this).attr("value");
          $.ajax({
              type: 'POST',
              url: thumbsUrl, 
              data: {
                  postid: postid,
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                  action: 'thumbs',
                  button: button,
              },
              success: function (json) {
                  if (json.length < 1 || json == undefined) {
                  }
                  $("#up").text(json['up']); 
                  $("#down").text(json['down']);
                  $("svg").removeClass("thumb-active");
                  if (json['remove'] == 'none') {
                      $("#" + button).removeClass("thumb-active");
                  } else {
                      $("#" + button).addClass("thumb-active");
                  }
              },
              error: function (xhr, errmsg, err) {
              }
          });
      });
  });*/
 });