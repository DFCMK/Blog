document.addEventListener('DOMContentLoaded', function() {
    
    // DOM Element References
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

    // Create Post Form Elements
    const quickStart = document.getElementById('quick-start');
    const formContainer = document.getElementById('post-form-container');
    const categorySelect = document.getElementById('id_category');
    const categoryPreview = document.getElementById('category-preview');
    const selectedCategorySpan = document.getElementById('selected-category');
    const categoryButtons = document.querySelectorAll('.category-btn');
    const backButton = document.getElementById('back-to-categories');
    const skipButton = document.getElementById('skip-category-btn');
    const featuredImageInput = document.getElementById('id_featured_image');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const removeImageBtn = document.getElementById('remove-image');
    const excerptField = document.getElementById('id_excerpt');

    initializeEventListeners();

    // =========================================================================
    // INITIALIZATION FUNCTIONS
    // =========================================================================

    /**
     * Initializes all event listeners for the application
     * This function sets up all interactive elements with their respective handlers
     */
    function initializeEventListeners() {
        window.addEventListener('load', changeTitleColor);
        
        if (newPostBtn && formContainer && newPostContainer) {
            newPostBtn.addEventListener('click', showNewPostForm);
        }

        if (titleInput && slugInput) {
            titleInput.addEventListener('input', handleSlugField);
        }

        if (editButton && editFormContainer && cancelButton) {
            editButton.addEventListener('click', showEditForm);
            cancelButton.addEventListener('click', cancelEdit);
            editButton.addEventListener('click', hideDeleteButton);
        }

        initializeNavbarScroll();
        initializeCategorySelection();
        initializeImagePreview();
        initializeFormValidation();
        initializeCommentManagement();
    }

    /**
     * Initializes navbar scroll effects and active page highlighting
     * Adds scroll-based styling and highlights current page in navigation
     */
    function initializeNavbarScroll() {
        $(document).ready(function() {
            
            // Navbar scroll effect - adds shadow when scrolled
            $(window).scroll(function() {
                if ($(window).scrollTop() > 50) {
                    $('.navbar').addClass('navbar-scrolled');
                } else {
                    $('.navbar').removeClass('navbar-scrolled');
                }
            });
            
            const currentLocation = location.href;
            const menuItems = document.querySelectorAll('.nav-link');
            
            menuItems.forEach(item => {
                if (item.href === currentLocation) {
                    item.parentElement.classList.add('active');
                }
            });
        });
    }

    /**
     * Initializes category selection system for post creation
     * Handles category buttons, preview display, and navigation
     */
    function initializeCategorySelection() {
        if (!categoryButtons.length) return;

        categoryButtons.forEach(button => {
            button.addEventListener('click', function() {
                const category = this.getAttribute('data-category');
                categorySelect.value = category;
                
                const categoryText = this.querySelector('h5').textContent;
                selectedCategorySpan.textContent = categoryText;
                categoryPreview.style.display = 'block';
                
                quickStart.style.display = 'none';
                formContainer.style.display = 'block';
            });
        });

        if (backButton) {
            backButton.addEventListener('click', function() {
                formContainer.style.display = 'none';
                quickStart.style.display = 'block';
                categoryPreview.style.display = 'none';
            });
        }

        if (skipButton) {
            skipButton.addEventListener('click', function() {
                quickStart.style.display = 'none';
                formContainer.style.display = 'block';
            });
        }
    }

    /**
     * Initializes image preview functionality for featured images
     * Provides visual feedback when users select images for posts
     */
    function initializeImagePreview() {
        if (!featuredImageInput) return;

        // Image preview on file selection
        featuredImageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    imagePreview.style.display = 'block';
                    document.querySelector('.custom-file-label').textContent = file.name;
                }
                reader.readAsDataURL(file);
            }
        });

        if (removeImageBtn) {
            removeImageBtn.addEventListener('click', function() {
                featuredImageInput.value = '';
                imagePreview.style.display = 'none';
                document.querySelector('.custom-file-label').textContent = 'Choose image...';
            });
        }
    }

    /**
     * Initializes form validation for post creation
     * Ensures required fields are filled before submission
     */
    function initializeFormValidation() {
        const postForm = document.getElementById('post-form');
        if (!postForm) return;

        postForm.addEventListener('submit', function(e) {
            const title = document.getElementById('id_title').value.trim();
            const content = document.getElementById('id_content').value.trim();
            
            if (!title) {
                e.preventDefault();
                alert('Please enter a title for your post.');
                return;
            }
            
            if (!content) {
                e.preventDefault();
                alert('Please add some content to your post.');
                return;
            }
        });
        initializeExcerptCounter();
    }

    /**
     * Initializes character counter for post excerpt field
     * Provides real-time feedback on excerpt length with visual indicators
     */
    function initializeExcerptCounter() {
        if (!excerptField) return;

        const counter = document.createElement('small');
        counter.className = 'form-text text-muted text-right';
        counter.textContent = '0/200 characters';
        excerptField.parentNode.appendChild(counter);

        excerptField.addEventListener('input', function() {
            const length = this.value.length;
            counter.textContent = `${length}/200 characters`;
            
            if (length > 200) {
                counter.classList.remove('text-muted');
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
                counter.classList.add('text-muted');
            }
        });
    }

    /**
     * Initializes comment management functionality
     * Handles edit and delete operations for comments
     */
    function initializeCommentManagement() {
        const deletePostButton = document.getElementById('delete-post-button');
        if (deletePostButton) {
            deletePostButton.addEventListener('click', showModal);
        }

        const modalCancelButton = document.querySelector('#deletePostModal .modal-footer .btn-secondary');
        if (modalCancelButton) {
            modalCancelButton.addEventListener('click', hideModal);
        }

        document.querySelectorAll('.btn-edit-comment').forEach(addEditCommentListener);
        document.querySelectorAll('.btn-delete-comment').forEach(addDeleteCommentListener);
    }

    // =========================================================================
    // UI MANIPULATION FUNCTIONS
    // =========================================================================

    /**
     * Changes the color of post titles to white for better visibility
     * This ensures titles are readable against potentially dark backgrounds
     */
    function changeTitleColor() {
        for (let i = 0; i < postDetailTitles.length; i++) {
            postDetailTitles[i].style.color = 'white';
        }
    }

    /**
     * Hides the delete button when edit mode is activated
     * Prevents accidental deletions while editing profile information
     */
    function hideDeleteButton() {
        const deleteButton = document.getElementById('delete-button');
        if (deleteButton) {
            deleteButton.style.display = 'none';
        }
    }

    /**
     * Displays the new post form and hides the initial button
     * Transitions from the "New Post" button to the full creation form
     */
    function showNewPostForm() {
        formContainer.style.display = 'block';
        newPostContainer.style.display = 'none';
        changeLabelColor('white', 'bold');
    }

    /**
     * Changes the color and weight of form labels
     * @param {string} color - CSS color value for labels
     * @param {string} fontWeight - CSS font-weight value for labels
     * Enhances label visibility in different form states
     */
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

    /**
     * Automatically generates a slug from the title input
     * Converts titles to URL-friendly slugs in real-time as user types
     */
    function handleSlugField() {
        const title = titleInput.value;
        const slug = title.toLowerCase().replace(/\s+/g, '-').slice(0, 50);
        slugInput.value = slug;
    }

    /**
     * Displays the profile edit form and hides the edit button
     * Transitions to edit mode for profile information
     */
    function showEditForm() {
        editFormContainer.style.display = 'block';
        editButton.style.display = 'none';
    }

    /**
     * Cancels profile editing and returns to view mode
     * Hides the edit form and shows the edit button again
     */
    function cancelEdit() {
        editFormContainer.style.display = 'none';
        editButton.style.display = 'block';
        window.location.href = "/post_detail/<post_id>";  
    }

    /**
     * Displays the delete confirmation modal
     * Shows the Bootstrap modal for post deletion confirmation
     */
    function showModal() {
        document.getElementById('deletePostModal').style.display = 'block';
    }

    /**
     * Hides the delete confirmation modal
     * Closes the Bootstrap modal when cancel is clicked
     */
    function hideModal() {
        document.getElementById('deletePostModal').style.display = 'none';
    }

    /**
     * Adds edit functionality to comment buttons
     * @param {Element} button - The edit button element
     * Populates the edit form with existing comment content when edit is clicked
     */
    function addEditCommentListener(button) {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const commentBody = document.querySelector(`#comment${commentId} p`).textContent;
            document.querySelector('#id_body').value = commentBody.trim();
            document.querySelector('#comment-id').value = commentId;
            document.querySelector('#edit-comment-form').style.display = 'block';
        });
    }

    /**
     * Adds delete functionality to comment buttons
     * @param {Element} button - The delete button element
     * Prepares the delete form with the target comment ID when delete is clicked
     */
    function addDeleteCommentListener(button) {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            document.querySelector('#comment-id').value = commentId;
            document.querySelector('#delete-comment-form').style.display = 'block';
        });
    }
});
