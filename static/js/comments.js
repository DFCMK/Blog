// Based on CI Walk threw
const editButtons = document.getElementsByClassName("btn-primary");
const commentText = document.getElementById("id_body");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

const deleteCommentModal = document.getElementById("deleteCommentModal");
const deleteCommentForm = document.getElementById("deleteCommentForm");
const commentIdToDelete = document.getElementById("commentIdToDelete");
const deleteButtons = document.getElementsByClassName("delete-comment-button");
const cancelButton = document.querySelector('#deleteCommentModal .btn-secondary');
const closeButton = document.querySelector('#deleteCommentModal .close');


/*
 * Initializes edit functionality for the provided edit buttons.
 * 
 * For each button in the `editButtons` collection:
 * - Retrieves the associated comment's ID upon click.
 * - Fetches the content of the corresponding comment.
 * - Populates the `commentText` input/textarea with the comment's content for editing.
 * - Updates the submit button's text to "Update".
 * - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
 */

for (let button of editButtons) {
    button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("comment_id");
        let commentContent = document.getElementById(`comment${commentId}`).innerText;
        commentText.value = commentContent;
        submitButton.innerText = "Update";
        commentForm.setAttribute("action", `edit_comment/${commentId}`);
    });
}


/*
 * Initializes deletion functionality for the provided delete buttons.
 * 
 * For each button in the `deleteButtons` collection: 
 * - Retrieves the associated comment's ID upon click
 * - Generates url with appending the commentId at the end in form of an Integer
 * - Display Modal
*/


    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            let commentId = e.target.getAttribute("comment_id");
            deleteCommentForm.action = `/${postSlug}/delete_comment/${commentId}`; 
            deleteCommentModal.classList.add('show');
            deleteCommentModal.style.display = 'block';
        });
    }

    // Show Modal 
    cancelButton.addEventListener('click', () => {
        deleteCommentModal.classList.remove('show');
        deleteCommentModal.style.display = 'none';
    });
    
    // Close Modal
    closeButton.addEventListener('click', () => {
        deleteCommentModal.classList.remove('show');
        deleteCommentModal.style.display = 'none';
    });