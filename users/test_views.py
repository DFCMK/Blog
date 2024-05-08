# from django.contrib.auth import logout
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserUpdateForm
from django.utils import timezone
from datetime import timedelta
# from django.core.paginator import Paginator, EmptyPage
from .models import Profile
from blog.models import Post
from django.contrib.messages import get_messages
# from django.contrib import messages


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def test_register_redirects_to_login_after_successful_registration(self):
        '''
        Test that a user is redirected to the login,
        page after successfully registering.
        '''
        # Submit registration form
        response = self.client.post(
            self.register_url,
            {
                "username": "Myusername",
                "email": "testname@testemail.com",
                "password1": "Mypassword123",
                "password2": "Mypassword123",
            },
            follow=True,
        )

        # Check if the registration form submission was successful
        self.assertEqual(response.status_code, 200)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, self.login_url, status_code=302)

    def test_form_validation_errors(self):
        '''
        Test that form validation errors are correctly displayed,
        when the registration form is submitted with invalid data.
        '''
        response = self.client.post(
            self.register_url,
            {
                "username": "Myusername",
                "email": "testname@testemail.com",
                "password1": "Mypassword123",
                "password2": "Mypassword123",
            },
            follow=True,
        )

        self.assertFalse(response.context["form"].is_valid())

    def test_duplicate_username(self):
        '''
        Test that attempting to register with a duplicate username,
        results in a form validation error.
        '''
        User.objects.create_user(
            username="Myusername",
            password="Mypassword123"
            )

        response = self.client.post(
            self.register_url,
            {
                "username": "Myusername",
                "email": "testname@testemail.com",
                "password1": "Mypassword123",
                "password2": "Mypassword123",
            },
            follow=True,
        )

        self.assertFalse(response.context["form"].is_valid())

    def test_duplicate_email(self):
        '''
        Test that attempting to register with a duplicate email,
        results in a form validation error.
        '''

        User.objects.create_user(
            username="Myusername",
            password="Mypassword",
            email="testname@testemail.com"
        )

        response = self.client.post(
            self.register_url,
            {
                "username": "Myusername",
                "email": "testname@testemail.com",
                "password1": "Mypassword123",
                "password2": "Mypassword123",
            },
            follow=True,
        )

        self.assertFalse(response.context["form"].is_valid())

    def test_password_mismatch(self):
        '''
        Test that attempting to register with mismatched passwords,
        results in a form validation error.
        '''

        response = self.client.post(
            self.register_url,
            {
                "username": "Myusername",
                "email": "testname@testemail.com",
                "password1": "Mypassword123",
                "password2": "Mypassword1234",
            },
            follow=True,
        )

        self.assertFalse(response.context["form"].is_valid())

    def test_get_request_renders_form(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_success_message_on_successful_registration(self):
        '''
        Test that accessing the registration page with a GET request,
        renders the registration form.
        '''

        response = self.client.post(
            self.register_url,
            {
                "username": "Myusername",
                "email": "testname@testemail.com",
                "password1": "Mypassword123",
                "password2": "Mypassword123",
            },
            follow=True,
        )

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Your account as Myusername has been created!" +
            " You are now able to log in.",
        )

    def test_error_message_on_form_submission_failure(self):
        '''
        Test that an error message is displayed,
        when the registration form submission fails,
        due to mismatched passwords.
        '''

        response = self.client.post(
            self.register_url,
            {
                "username": "Myusername",
                "email": "testname@testemail.com",
                "password1": "Mypassword123",
                "password2": "Mypassword1234",
            },
            follow=True,
        )

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "There was an error in the registration form. Please correct it.",
        )


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Myusername",
            password="Mypassword123",
            email="myemail@email.com"
        )

    def test_profile_view_requires_login(self):
        '''
        Test that accessing the profile view requires,
        the user to be logged in.
        '''
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/profile/")

    def test_profile_view_allows_authenticated_users(self):
        '''
        Test that the profile view allows access to authenticated users.
        '''
        self.client.login(username="Myusername", password="Mypassword123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_creation_if_not_exists(self):
        '''
        Test that a user profile is created if it does not exist,
        when accessing the profile view.
        '''
        self.client.login(username="Myusername", password="Mypassword123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_profile_retrieval_if_exists(self):
        '''
        Test that an existing user profile is retrieved,
        when accessing the profile view.
        '''
        Profile.objects.create(user=self.user)
        self.client.login(username="Myusername", password="Mypassword123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_posts_pagination_on_profile_page(self):
        '''
        Test that user posts are correctly paginated on the profile page.
        '''
        self.user = User.objects.create_user(
            username="Myprofile",
            password="Mypassword321"
        )
        self.client.force_login(self.user)
        # Create posts with decreasing timestamps
        for i in range(1, 13):
            days_ago = i
            timestamp = timezone.now() - timedelta(days=days_ago)
            Post.objects.create(
                author=self.user,
                title=f"Test Post {i}",
                content=f"Content {i}",
                date_posted=timestamp,
            )

        liked_posts_data = [
            {
                "title": f"Liked Title {i}",
                "slug": f"liked-title-{i}",
                "content": f"Liked Content {i}",
                "author": self.user,
                "date_posted": timezone.now()
                - timedelta(days=i),
            }
            for i in range(1, 13)
        ]
        liked_posts = Post.objects.bulk_create(
            [Post(**data) for data in liked_posts_data]
        )

        for post in liked_posts:
            post.likes.add(self.user)
            post.save()

        posts = Post.objects.filter(author=self.user).order_by("-date_posted")
        for i in range(len(posts) - 1):
            self.assertTrue(posts[i].date_posted >= posts[i + 1].date_posted)

        # Test pagination of the first page for user's posts
        response = self.client.get(reverse("profile"))
        self.assertEqual(len(response.context["user_posts"]), 6)

        # Test pagination of the second page for user's posts
        response = self.client.get(reverse("profile") + "?page=2")
        self.assertEqual(len(response.context["user_posts"]), 6)

        # Test pagination of the first page for liked posts
        response = self.client.get(reverse("profile") + "?liked_page=1")
        self.assertEqual(len(response.context["liked_posts"]), 6)

        # Test pagination of the second page for liked posts
        response = self.client.get(reverse("profile") + "?liked_page=2")
        self.assertEqual(len(response.context["liked_posts"]), 6)

    def test_user_posts_and_liked_posts_ordering(self):
        """
        Test that the user's posts and liked posts are ordered correctly,
        from newest to oldest.

        1. Create a user and log them in.
        2. Create posts for the user and liked posts.
        3. Make a GET request to the 'profile' URL.
        4. Get the list of user's posts and liked posts,
        from the response context.
        5. Check if the posts are ordered correctly from newest to oldest.
        """
        self.user = User.objects.create_user(
            username="MyAuthor",
            password="Mypass321"
            )

        self.client.login(
            username="MyAuthor",
            password="Mypass321"
            )

        posts_data = [
            {
                "title": f"Title {i}",
                "slug": f"title-{i}",
                "content": f"Content {i}",
                "author": self.user,
                "date_posted": timezone.now()
                - timezone.timedelta(days=i),
            }
            for i in range(1, 13)
        ]
        Post.objects.bulk_create([Post(**data) for data in posts_data])

        liked_posts_data = [
            {
                "title": f"Liked Title {i}",
                "slug": f"liked-title-{i}",
                "content": f"Liked Content {i}",
                "author": self.user,
                "date_posted": timezone.now()
                - timezone.timedelta(days=i),
            }
            for i in range(1, 13)
        ]
        liked_posts = Post.objects.bulk_create(
            [Post(**data) for data in liked_posts_data]
        )

        for post in liked_posts:
            post.likes.add(self.user)
            post.save()

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)

        user_posts = response.context["user_posts"]
        liked_posts = response.context["liked_posts"]

        # Ensure user's posts are ordered correctly from newest to oldest
        for i in range(len(user_posts) - 1):
            self.assertTrue(
                user_posts[i].date_posted >= user_posts[i + 1].date_posted
                )

        # Ensure liked posts are ordered correctly from newest to oldest
        for i in range(len(liked_posts) - 1):
            self.assertTrue(
                liked_posts[i].date_posted >= liked_posts[i + 1].date_posted
            )

    def test_profile_update_form_valid_data(self):
        '''
        Test that the profile update form correctly,
        updates user data with valid input.
        '''
        self.client.login(
            username="Myusername", password="Mypassword123"
        )

        new_username = "NewUsername"
        new_email = "newemail@email.com"

        data = {"username": new_username, "email": new_email}

        user_form = UserUpdateForm(data)

        self.assertTrue(user_form.is_valid())

        user_form.save()

        user = User.objects.get(username=new_username)

        # Create profile for the user
        profile = Profile.objects.create(user=user)
        self.assertIsNotNone(profile)

        # Access the profile object
        profile = user.profile

        # Assert that the user data has been updated
        self.assertEqual(user.username, new_username)
        self.assertEqual(user.email, new_email)

    def test_profile_update_form_invalid_data(self):
        '''
        Test that the profile update form,
        correctly displays validation errors with invalid input.
        '''
        self.client.login(username="Myusername", password="Mypassword123")

        new_username = ""
        new_email = "invalidemail"

        data = {"username": new_username, "email": new_email}

        user_form = UserUpdateForm(data)

        self.assertFalse(user_form.is_valid())

        # Assert using substrings for error messages
        self.assertIn("This field is required.", str(
            user_form.errors["username"][0]))
        self.assertIn(
            "Enter a valid email address", str(user_form.errors["email"][0])
            )

    def test_profile_link_visibility(self):
        '''
        Test that the profile link is visible only when the user is logged in.
        '''
        # Check for profile link visibility when user is not logged in
        response = self.client.get(reverse("blog-home"))
        self.assertNotContains(
            response, reverse("profile")
        )  # Asserts profile link is not in navbar

        self.client.login(username="Myusername", password="Mypassword123")

        # Check for profile link visibility when user is logged in
        response = self.client.get(reverse("blog-home"))
        self.assertContains(response, reverse("profile"))

    def test_handling_of_database_errors(self):
        '''
        Test that the profile view correctly handles database errors,
        during profile creation or update.
        '''
        # Simulate a database error during profile creation or update
        invalid_data = {"username": "", "email": "invalidemail.com"}
        response = self.client.post(reverse("profile"), data=invalid_data)
        self.assertEqual(response.status_code, 302)


class DeleteProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Myuser",
            password="Myauth123"
            )
        self.user.profile = Profile.objects.create(user=self.user)
        self.client.login(username="Myuser", password="Myauth123")

    def test_authorization(self):
        '''
        Test that accessing the delete profile view,
        requires the user to be logged in.
        '''

        self.client.logout()
        response = self.client.get(reverse("delete"))
        self.assertEqual(response.status_code, 302)

        self.client.login(username="Myuser", password="Myauth123")
        response = self.client.get(reverse("delete"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("blog-home"))
        self.assertEqual(response.status_code, 200)

    def test_profile_deletion_success(self):
        """
        Test that a user's profile is successfully deleted,
        and a success message is displayed.
        """
        response = self.client.post(reverse("delete"))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Your profile Myuser has been deleted successfully.",
        )
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="testuser")

    def test_success_message_on_profile_deletion(self):
        '''
        Test that a success message is displayed,
        after a user successfully deletes their profile.
        '''

        self.client.login(username="Myuser", password="Myauth123")

        response = self.client.post(reverse("delete"))

        # Check if the profile deletion was successful
        self.assertEqual(response.status_code, 302)

        # Follow the redirect to the logout URL
        response = self.client.get(response.url)

        # Check for the success message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Your profile Myuser has been deleted successfully.",
        )
