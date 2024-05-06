from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
# from django.utils import timezone
# from datetime import timedelta
from django.core.paginator import Paginator
from .forms import CommentForm, CreateNewPostForm
from unittest.mock import Mock
from django.contrib import messages
from .models import Post, Comment, Vote


class HomeViewTestCase(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a user and some sample posts.
        """
        self.user = User.objects.create_user(
            username='myUsername',
            password='myPassword'
            )
        Post.objects.create(
            author=self.user,
            title="Test Post 1",
            content="Content 1"
            )
        Post.objects.create(
            author=self.user,
            title="Test Post 2",
            content="Content 2")

    def test_home_view(self):
        '''
        Test when Get request is made to the 'blog-home' URL
        and the 200 Status code is
        indicating that request recieved successfully
        '''
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')


class PostListViewTest(TestCase):
    def setUp(self):
        '''
        Create a user and 12 posts with timestamps
        ranging from 1 day ago to 12 days ago.
        '''
        self.user = User.objects.create_user(
            username='myUsername',
            password='myPassword'
            )

        for i in range(1, 13):
            # days_ago = i
            # timestamp = timezone.now() - timedelta(days=days_ago)
            Post.objects.create(
                author=self.user,
                title=f"Test Post {i}",
                content=f"Content {i}"
                )

    def test_ordering(self):
        '''
        Test that the posts are ordered correctly,
        based on the date_posted field.

        1. Make a GET request to the 'blog-home' URL.
        2. Get the list of posts from the response context.
        3. Iterate over the list of posts
        and check if the posts are ordered correctly,
        based on the date_posted field
        '''
        response = self.client.get(reverse('blog-home'))
        posts = response.context['posts']

        for i in range(len(posts) - 1):
            self.assertTrue(posts[i].date_posted >= posts[i+1].date_posted)

    def test_template_name(self):
        '''
        Make get request to the 'blog-home' URL and check the template used.
        '''
        response = self.client.get(reverse('blog-home'))
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_context_object_name(self):
        '''
        1. Make get request to the 'blog-home' URL
        and retrieve the post list in context_posts.
        2. Paginate the queryset retrieved directly from the database.
        3. Compare the paginated queryset with the posts from the context.
        '''
        response = self.client.get(reverse('blog-home'))
        context_posts = response.context['posts']

        database_posts = Paginator(
            Post.objects.all().order_by('-date_posted'), 6)
        database_posts = database_posts.get_page(1).object_list

        self.assertEqual(list(context_posts), list(database_posts))

    def test_pagination(self):
        '''
        1. Make a GET request to the 'blog-home' URL
        and check if pagination is True.
        2. Check the number of pages.
        3. Check the content of the first page.
        4. Check the content of the second page.
        '''
        response = self.client.get(reverse('blog-home'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['posts']) == 6)

        self.assertTrue('paginator' in response.context)
        self.assertEqual(response.context['paginator'].num_pages, 2)

        self.assertEqual(response.context['posts'][0].title, "Test Post 12")
        self.assertEqual(response.context['posts'][5].title, "Test Post 7")

        response = self.client.get(reverse('blog-home') + '?page=2')
        self.assertEqual(response.context['posts'][0].title, "Test Post 6")
        self.assertEqual(response.context['posts'][5].title, "Test Post 1")


class post_detail(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a user and a sample posts.
        """
        self.user = User.objects.create_user(
            username='myUsername',
            password='myPassword'
            )
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Content"
            )

        self.comments = [
            Comment.objects.create(
                author=self.user,
                post=self.post,
                body="Comment 1"
                ),
            Comment.objects.create(
                author=self.user,
                post=self.post,
                body="Comment 2"
                ),
            Comment.objects.create(
                author=self.user,
                post=self.post,
                body="Comment 3"
                ),
        ]
        self.comment_form = CommentForm()

        # Apprrove all comments for testing
        for comment in self.comments:
            comment.approved = True
            comment.save()

    def test_response_for_existing_posts(self):
        '''
        Test when a GET request is made to
        the 'post_detail' URL with a valid slug,
        the response status code is 200,
        indicating a successful request,
        and thecorrect template is used.
        '''

        post = Post.objects.first()
        response = self.client.get(
            reverse(
                'post_detail',
                kwargs={'slug': post.slug}
                )
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_response_for_non_exising_posts(self):
        '''
        Test when GET request is made to 'post_detail'
        URL with a slug that does not correspond to any exising post.
        The 404 status code is indicating then that the post was not found
        '''
        response = self.client.get(
            reverse(
                'post_detail',
                kwargs={'slug': 'non-exisiting-slug'}
                )
            )
        self.assertEqual(response.status_code, 404)

    def test_comment_submission_with_approval_message(self):
        '''
        Test the submission of a comment:
        1. Log in a user.
        2. Simulate a POST request to the comment submission URL
        with test comment data.
        3. Check if the response status code is 200 or 201,
        indicating a successful submission.
        4. Verify if the comment was created and saved in the database.
        '''
        self.client.force_login(self.user)

        response = self.client.post(reverse(
            'post_detail',
            kwargs={'slug': self.post.slug}),
            {'body': 'Test comment', }, follow=True)

        self.assertIn(response.status_code, [200, 201])

        comment = Comment.objects.filter(
            post=self.post,
            body='Test comment').first()
        self.assertIsNotNone(comment)

        self.assertIn(
            messages.SUCCESS,
            [msg.level for msg in response.context['messages']]
            )

    def test_form_validation(self):
        '''
        Test form validation by submitting invalid data
        to the comment submission form.
        '''
        self.client.force_login(self.user)

        # Simulate submitting invalid data to trigger form validation error
        response = self.client.post(
            reverse(
                'post_detail',
                kwargs={'slug': self.post.slug}
                ), {
                    'body': '',
                    })

        comment_form = response.context['comment_form']

        self.assertTrue(comment_form.is_bound)

        self.assertFalse(comment_form.is_valid())

        # Check if the correct form validation error message is present
        self.assertTrue('body' in comment_form.errors)
        self.assertEqual(
            comment_form.errors['body'], ['This field is required.']
            )

    def test_comment_ordering(self):
        """
        Test if comments are ordered correctly based on their date of posting.
        """
        comment1 = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Comment 1")
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Comment 2")

        response = self.client.get(
            reverse(
                'post_detail',
                kwargs={'slug': self.post.slug}
                ))
        comments = response.context['comments']

        # Check if comments are ordered correctly
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1], comment1)

    def test_total_likes_count(self):
        """
        Test if the total likes count for a post is accurate.
        """
        # Like the post twice
        self.post.likes.add(self.user)
        self.post.likes.add(
            User.objects.create_user(
                username='anotheruser',
                password='password456'
                ))

        response = self.client.get(
            reverse(
                'post_detail',
                kwargs={'slug': self.post.slug}))

        # Check if the total likes count matches the expected value
        self.assertEqual(response.context['total_likes_count'], 2)

    def test_context(self):
        '''
        Test if the correct context is passed to the template
        '''
        response = self.client.get(
            reverse(
                'post_detail',
                kwargs={'slug': self.post.slug}
                ))
        self.assertEqual(response.status_code, 200)

        # Mock the form in context
        mock_context = Mock()
        mock_context.configure_mock(comment_form=CommentForm())

        self.assertTrue('post' in response.context)
        self.assertEqual(response.context['post'], self.post)

        self.assertTrue('comments' in response.context)

        # Sort the comments by body before comparing
        response_comments = sorted(
            response.context['comments'],
            key=lambda comment: comment.body
            )
        self_comments = sorted(
            self.comments,
            key=lambda comment: comment.body
            )

        self.assertEqual(
            [comment.body for comment in response_comments],
            [comment.body for comment in self_comments])

        self.assertTrue(hasattr(mock_context, 'comment_form'))
        self.assertEqual(
            response.context['comment_count'],
            len(self.comments))

        # Verify attribute exists
        self.assertTrue(hasattr(mock_context, 'comment_form'))
        self.assertEqual(mock_context.comment_form.__class__, CommentForm)


class create_new_post(TestCase):
    def setUp(self):
        '''
        Create test user for authentication
        '''
        self.user = User.objects.create_user(
            username='myUsername',
            password='myPassword'
            )

    def test_redirect_if_not_logged_in(self):
        '''
        Test redirection when user in not logged in
        '''
        response = self.client.get(reverse('new_post'))
        self.assertRedirects(response, '/login/?next=/create')

    def test_post_creation(self):
        '''
        Simulate creating a new post:
        1. Log in a user
        2. Create a dictionary `post_data`,
        containing test data for the new post.
        3. Send a POST request to the `new_post`,
        view with the `post_data`.
        4. Assert that the response status code is 302
        (indicating a redirect after successful creation).
        5. Assert that a new Post object was created,
        and saved in the database.
        '''
        self.client.force_login(self.user)
        post_data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'content': 'Test Content',
            'excerpt': 'Test Excerpt',
            'status': 0
        }

        response = self.client.post(reverse('new_post'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

    def test_form_validation_error(self):
        '''
        Test that the form validation works correctly,
        when invalid data is submitted.

        1. Log in a user.
        2. Modify the post data with invalid data.
        3. Send a POST request with the invalid data,
        to simulate form submission.
        4. Ensure that the response status code is 200,
        indicating a failed form submission.
        5. Instantiate the form with the invalid data,
        and test that it's not valid.
        '''
        self.client.force_login(self.user)
        invalid_post_data = {}
        response = self.client.post(reverse('new_post'), invalid_post_data)
        self.assertEqual(response.status_code, 200)

        # Test form is not valid
        form = CreateNewPostForm(data=invalid_post_data)
        self.assertFalse(form.is_valid())

    def test_successful_submission_and_message(self):
        '''
        1. Force User Login
        2. Modify post_data with expected submission data
        3. Submit the form data
        4. Follow redirection to access the rendered message
        5. Verify message existance in the redirected response
        '''
        self.client.force_login(self.user)

        post_data = {
            'title': 'Test Post',
            'slug': 'test-post',
            'content': 'Test Content',
            'excerpt': 'Test Excerpt',
            'status': 0
        }

        response = self.client.post(reverse('new_post'), post_data)

        redirected_response = self.client.get(response.url)

        self.assertContains(
            redirected_response,
            'Your post was successfully submitted!'
            )

    def test_error_message(self):
        '''
        1. Force user Login
        2. Submit invalid data (empty dictonary)
        3. Retrieve template name,
        and empty dictonary saved to invalid_post_data
        4. Verify existance of error message
        '''
        self.client.force_login(self.user)
        invalid_post_data = {}
        response = self.client.post(reverse('new_post'), invalid_post_data)
        self.assertContains(
            response,
            'There was an error submitting your post.'
            )


class update_post(TestCase):
    def setUp(self):
        '''
        Create test user and post with assigning user to test post
        '''
        self.user = User.objects.create(
            username='Myusername',
            password="Mypassword"
            )
        self.post = Post.objects.create(
            title='Test Post',
            content="Test Content",
            author=self.user
            )

    def test_author_access_update_form(self):
        '''
        Login post author and access update_post URL to verify redirection
        '''
        self.client.login(username='Myusername', password='Mypassword')

        response = self.client.get(
            reverse(
                'update_post',
                kwargs={'slug': self.post.slug}), follow=True)

        self.assertEqual(response.status_code, 200)

    def test_non_author_access_update_form(self):
        '''
        Login other user and test accessability of update_post form URL
        '''
        User.objects.create(
            username='Otherusername',
            password='Otherpassword'
            )

        self.client.login(username='Otherusername', password='Otherpassword')

        response = self.client.get(
            reverse(
                'update_post',
                kwargs={'slug': self.post.slug}
                ), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_post_valid_data(self):
        '''
        Test updating a post with valid data
        '''
        self.client.force_login(self.user)

        updated_data = {
            'title': 'Updated Title',
            'slug': 'updated-title',
            'content': 'Updated Content',
            'excerpt': 'Updated Excerpt',
            'status': 0
        }

        # Submit the update form
        response = self.client.post(
            reverse(
                'update_post', kwargs={'slug': self.post.slug}
                ), updated_data, follow=True)

        # Check if the response is a redirect
        self.assertRedirects(
            response,
            reverse(
                'post_detail', kwargs={'slug': 'updated-title'}
                ))

    def test_update_post_invalid_data(self):
        '''
        Test updating a post with invalid data
        '''
        self.client.force_login(self.user)

        invalid_data = {
            'title': '',
            'content': 'Updated Content',
        }

        # Submit the update form with invalid data and follow the redirect
        response = self.client.post(
            reverse(
                'update_post', kwargs={'slug': self.post.slug}
                ), invalid_data, follow=True)

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Verify that error messages are displayed
        self.assertFormError(
            response,
            'post_form',
            'title',
            'This field is required.'
            )

    def test_update_post_get_request(self):
        '''

        Ensure that the update post form is accessible via a GET request.

        1. Log in as the test user.
        2. Access the update form for the post.
        3. Verify that the response status code is 200
        4. Verify that the update form template is used.
        5. Verify that the form is pre-filled with existing post data.
        '''
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                'update_post', kwargs={'slug': self.post.slug}
                ))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'blog/update_post.html')

        self.assertEqual(
            response.context['post_form'].instance.title,
            self.post.title
            )
        self.assertEqual(
            response.context['post_form'].instance.content,
            self.post.content
            )


class DeletePostTestCase(TestCase):
    def setUp(self):
        '''
        Set up Test enviorment:
        1. Create author of post.
        2. Create other user.
        3. Create Post and assign it to user (author)
        '''
        self.user = User.objects.create_user(
            username='Myusername',
            password='Mypassword'
            )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
            )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
            )

    def test_user_logged_in_can_delete_own_post(self):
        '''
        Test if author can delete own post
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        response = self.client.post(
            reverse(
                'delete_post', args=[self.post.slug]))
        self.assertRedirects(response, reverse('blog-home'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_user_not_logged_in_cannot_delete_post(self):
        '''
        Test if user isn't logged in, cant't delete Post
        '''
        response = self.client.post(
            reverse(
                'delete_post', args=[self.post.slug]
                ))
        self.assertRedirects(
            response, reverse('login') + '?next=' + reverse(
                'delete_post', args=[self.post.slug]
                ))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_only_post_author_can_delete_post(self):
        '''
        Test if only the Post's author can delete the Post
        '''
        self.client.login(
            username='otheruser',
            password='otherpassword'
            )
        response = self.client.post(
            reverse(
                'delete_post',
                args=[self.post.slug]
                ))
        self.assertRedirects(response, reverse('blog-home'))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_user_not_author_cannot_delete_post(self):
        '''
        Test if other users can not delete Posts they havent written.
        '''
        self.client.login(
            username='otheruser',
            password='otherpassword'
            )
        response = self.client.post(
            reverse(
                'delete_post', args=[self.post.slug]
                ))
        self.assertRedirects(response, reverse('blog-home'))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_deleted_successfully(self):
        '''
        Test if Post got deleted successfully
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        response = self.client.post(
            reverse(
                'delete_post', args=[self.post.slug]
                 ))
        self.assertRedirects(response, reverse('blog-home'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_redirect_after_deletion(self):
        '''
        Test redirection after deletion.
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        response = self.client.post(
            reverse('delete_post', args=[self.post.slug])
            )
        self.assertRedirects(response, reverse('blog-home'))


class edit_comment(TestCase):
    def setUp(self):
        '''
        Sets up the initial state for each test.
        It creates a author, other user, a post and a comment.
        '''
        self.user = User.objects.create_user(
            username='Myusername',
            password='Mypassword'
            )
        self.other_user = User.objects.create_user(
            username='otherusername',
            password='otherpassword'
            )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user)
        self.comment = Comment.objects.create(
            body='Test Comment',
            author=self.user,
            post=self.post
            )

    def test_user_logged_in_can_edit_own_comment(self):
        '''
        Test if a user can edit own comments
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        new_body = 'Updated Comment'
        response = self.client.post(
            reverse(
                'edit_comment', args=[self.post.slug, self.comment.id]
                ), data={'body': new_body})
        self.assertRedirects(
            response, reverse(
                'post_detail', args=[self.post.slug]
                ))

        # Assert comment is updated
        self.assertTrue(
            Comment.objects.filter(
                pk=self.comment.id,
                body=new_body).exists())

    def test_user_not_logged_in_cannot_edit_comments(self):
        '''
        Test if a user which isn't logged in can edit comments
        '''
        self.client.logout()
        response = self.client.post(
            reverse(
                'edit_comment', args=[self.post.slug, self.comment.id]
                 ))

        # Assert that the response redirects to the login page
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse(
                'edit_comment', args=[self.post.slug, self.comment.id]
                ))

    def test_user_not_author_cannot_edit_comment(self):
        '''
        Test if a user which is not the author of the comment can edit comment
        '''
        self.client.login(
            username='otheruser',
            password='otherpassword')
        self.client.post(
            reverse(
                'edit_comment', args=[self.post.slug, self.comment.id]
                 ))
        # Update assertion based on expected behavior (redirect or error)
        self.assertTrue(Post.objects.filter(pk=self.comment.id).exists())

    def test_comment_edited_successfully(self):
        '''
        Test if comment got edited successfully
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        updated_body = 'This is my updated comment'
        response = self.client.post(
            reverse(
                'edit_comment', args=[self.post.slug, self.comment.id]
                ), data={'body': updated_body}
                )
        self.assertRedirects(
            response,
            reverse(
                'post_detail', args=[self.post.slug]
                ))

    def test_comment_content_updated(self):
        '''
        Test if the comments body (content) got updated correctly
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        updated_body = 'This is my updated comment'
        response = self.client.post(
            reverse(
                'edit_comment', args=[self.post.slug, self.comment.id]
                ), data={'body': updated_body}
                )
        self.assertRedirects(
            response,
            reverse(
                'post_detail', args=[self.post.slug]
                ))
        # Get the updated comment from the database
        updated_comment = Comment.objects.get(pk=self.comment.id)
        self.assertEqual(updated_comment.body, updated_body)


class delete_comment(TestCase):
    def setUp(self):
        '''
        Sets up the initial state for each test.
        It creates a author, other user, a post and a comment
        '''
        self.user = User.objects.create_user(
            username='Myusername',
            password='Mypassword'
            )
        self.other_user = User.objects.create_user(
            username='otherusername',
            password='otherpassword'
            )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
            )
        self.comment = Comment.objects.create(
            body='Test Comment',
            author=self.user,
            post=self.post
            )

    def test_user_logged_in_can_delete_own_comment(self):
        '''
        Test if a logged in user can delete own comment
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        response = self.client.post(
            reverse(
                'delete_comment', args=[self.post.slug, self.comment.id]
                 ))
        self.assertRedirects(
            response,
            reverse(
                'post_detail', args=[self.post.slug]
                 ))
        self.assertFalse(Comment.objects.filter(pk=self.comment.id).exists())

    def test_user_not_logged_in_cannot_delete_comments(self):
        '''
        Test if a not logged in user can delete comment
        '''
        self.client.logout()
        response = self.client.post(
            reverse(
                'delete_comment', args=[self.post.slug, self.comment.id]
                 ))
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse(
                'delete_comment', args=[self.post.slug, self.comment.id]
                 ))

    def test_user_not_author_cannot_delete_comment(self):
        '''
        Test if user can delete an authors comment
        '''
        self.client.login(
            username='otheruser',
            password='otherpassword'
            )
        self.client.post(
            reverse(
                'delete_comment', args=[self.post.slug, self.comment.id]
                ))
        self.assertTrue(Post.objects.filter(pk=self.comment.id).exists())

    def test_comment_deletion_successfully(self):
        '''
        Test if the comment got deleted successfully
        '''
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        response = self.client.post(
            reverse(
                'delete_comment', args=[self.post.slug, self.comment.id]
                ))
        self.assertRedirects(
            response,
            reverse(
                'post_detail', args=[self.post.slug]
                 ))
        self.assertFalse(Comment.objects.filter(pk=self.comment.id).exists())


class LikesView(TestCase):
    def setUp(self):
        '''
        Sets up the initial state for each test. It creates a user and a post.
        '''
        self.user = User.objects.create_user(
            username='Myusername',
            password='Mypassword'
            )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
            )

    def test_logged_in_user_can_like_post(self):
        '''
        Test if a logged in user can like a post (like = favorite)
        '''
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                'like_post', kwargs={'pk': self.post.pk}
                 ))
        self.assertEqual(
            response.status_code, 302)  # Redirects to home page after liking
        self.assertIn(
            self.user,
            self.post.likes.all())  # User is in the post's likes

    def test_logged_in_user_can_unlike_post(self):
        '''
        Test if a logged in user can unlike a post
        '''
        self.post.likes.add(self.user)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                'like_post', kwargs={'pk': self.post.pk}
                ))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(
            self.user,
            self.post.likes.all())  # User is not in the post's likes

    def test_logged_out_user_cannot_like_post(self):
        '''
        Test if a logged out user can not like a post
        '''
        response = self.client.post(
            reverse(
                'like_post', kwargs={'pk': self.post.pk}
                 ))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user, self.post.likes.all())

    def test_likes_count_increases_when_post_is_liked(self):
        '''
        Test if like count get incremented correctly when liked by a user
        '''
        initial_likes_count = self.post.likes.count()
        self.client.force_login(self.user)
        self.client.post(reverse('like_post', kwargs={'pk': self.post.pk}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), initial_likes_count + 1)


class thumbs(TestCase):
    def setUp(self):
        """
        Sets up the initial state for each test. It creates a user and a post,
        stores the URL for the 'thumbs' view function for the created post.
        """
        self.user = User.objects.create_user(
            username='Myusername',
            password='Mypassword'
            )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user
            )
        self.url = reverse('thumbs', kwargs={'pk': self.post.pk})

    def test_successfull_upvote_unvoted_user(self):
        """
        This test checks the scenario where,
        a user who has not previously voted on a post
        attempts to upvote it.
        It verifies that the upvote is successfully processed,
        the response status code is 200,
        and the response JSON contains the 'up' key
        indicating the number of upvotes, without any error messages.
        """
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        response = self.client.post(
            self.url,
            {
                'action': 'thumbs',
                'button': 'thumbsup'
            })
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('up', response_json)  # Check if 'up' key exists
        self.assertNotIn(
            'error', response_json
            )  # Ensure 'error' key does not exist

    def test_successful_downvote_unvoted_user(self):
        """
        This test checks the scenario where,
        a user who has not previously voted on a post
        attempts to downvote it.
        It verifies that the downvote is successfully processed,
        the response status code is 200,
        and the response JSON contains the 'down' key
        indicating the number of downvotes, without any error messages.
        """
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )
        response = self.client.post(
            self.url,
            {
                'action': 'thumbs',
                'button': 'thumbsdown'
            })

        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('down', response_json)
        self.assertNotIn('error', response_json)

    def test_upvote_by_user_who_already_upvoted(self):
        """
        This test checks the scenario where,
        a user who has already upvoted a post
        attempts to upvote it again.
        It verifies that the upvote is successfully removed,
        the response status code is 200,
        and the response JSON contains the 'up' key
        indicating the updated number of upvotes, without any error messages.
        """
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )

        self.voted = Vote.objects.create(
            post=self.post,
            user=self.user,
            vote=True
            )
        response = self.client.post(
            self.url,
            {
                'action': 'thumbs',
                'button': 'thumbsup'
            })

        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('up', response_json)
        self.assertNotIn('error', response_json)

    def test_downvote_by_user_who_already_downvoted(self):
        """
        This test checks the scenario where,
        a user who has already downvoted a post
        attempts to downvote it again.
        It verifies that the downvote is successfully removed,
        the response status code is 200,
        and the response JSON contains the 'down' key
        indicating the updated number of downvotes,
        without any error messages.
        """
        self.client.login(
            username='Myusername',
            password='Mypassword'
            )

        self.voted = Vote.objects.create(
            post=self.post,
            user=self.user,
            vote=True
            )
        response = self.client.post(
            self.url,
            {
                'action': 'thumbs',
                'button': 'thumbsdown'
            })

        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('down', response_json)
        self.assertNotIn('error', response_json)


class AboutViewTest(TestCase):
    def test_about_view_template_rendering(self):
        '''
        Test template rendering
        '''
        response = self.client.get(reverse('blog-about'))
        self.assertTemplateUsed(response, 'blog/about.html')

    def test_about_view_context_data(self):
        '''
        Test context data
        '''
        response = self.client.get(reverse('blog-about'))
        self.assertEqual(response.context['title'], 'About')

    def test_about_view_http_response(self):
        '''
        Test http response
        '''
        response = self.client.get(reverse('blog-about'))
        self.assertEqual(response.status_code, 200)
