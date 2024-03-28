console.log("comments.js loaded")


const editCommentButtons = document.querySelectorAll('.edit-comment-button');
editCommentButtons.forEach(button => {
    const editCommentButtons = document.querySelectorAll('.edit-comment-button');
    button.addEventListener('click', function() {
        const commentId = this.getAttribute('comment_id'); // Get comment ID from button attribute
        editComment(commentId); // Call your editComment function
    });
});