# **Review | Alliance**
Review | Restaurant-Review-Blog is designed with a singular purpose: to enable users to share their unique dining adventures and insights with a global audience. Here, users can meticulously document their restaurant visits, capturing the essence of every dining experience, from the exquisite flavors to the ambiance that makes each visit memorable.

Users can leave comments, share their reviews, and express their opinions through simple thumbs-up or thumbs-down gestures. This interactive environment encourages a rich exchange of ideas and perspectives, making every visit to Restaurant-Review-Blog a unique culinary adventure.

But the journey doesn't end there! Users have the option to mark their favorite posts, ensuring that unforgettable dining experiences are always within easy reach. This feature is a testament to our commitment to enhancing the user experience and making the most cherished dining memories easily accessible.

This fictional site was created for Portfolio Project #4 (Full-Stack Toolkit) - Diploma in Full Stack Software Development Diploma at the [Code Institute](https://www.codeinstitute.net).

[View live website here](https://django-restaurant-blog-d6ddec41b70e.herokuapp.com/)


# Table of Content

* [**Project**](<#project>)
    * [Objective](<#objective>)
    * [Site Users Goal](<#site-users-goal>)
    * [Site Owners Goal](<#site-owners-goal>)
    * [Project Management](<#project-management>)

* [**User Experience (UX)**](<#user-experience-ux>)
    * [User Stories](<#user-stories>)
    * [Site Structure](<#site-structure>)
    * [Design Choices](<#design-choices>)

* [**Existing Features**](<#existing-features>)
    * [Navigation](<#navigation>)
    * [about](<#about>)
    * [Home](<#home>)
    * [Profile](<#profile>)
    * [Create Post](<#create-post>)
    * [Post](<#post>)
    * [Update Post / Delete Post](<#update-post-and-delete-post>)
    * [Thumbs / Favorites](<#thumbs-and-favorites>)
    * [Create / Update / Delete Comment](<#create-update-and-delete-comment>)
    * [Admin Area](<#admin-area>)
    * [Sign Up](<#sign-up>)
    * [Sign In](<#sign-in>)
    * [Sign Out](<#sign-out>)
    * [Footer](<#footer>)
    * [Flash Messages](<#flash-messages-and-confirmation-pages-to-the-user>)

* [**Features Left To Implement**](<#features-left-to-implement>)

* [**Technologies Used**](<#technologies-used>)
    * [Languages](<#languages>)
    * [Frameworks & Software](<#frameworks--software>)
    * [Libraries](<#libraries>)

* [**Testing**](<#testing>)
    * [Testing User Stories](<#testing-user-stories>)
    * [Code Validation](<#code-validation>)
    * [Additional Testing](<#additional-testing>)
    * [Known Bugs](<#known-bugs>)
* [Deployment](<#deployment>)
* [Credits](<#credits>)
* [Acknowledgements](<#acknowledgements>)

# **Project**

## Objective
I decided to build a Restaurant Review Page because there are many examples of it, such as Yelp and others, which are very useful for making informed decisions and avoiding unpleasant surprises. A review platform comes in handy when you are visiting from somewhere and need a reliable source to filter out the restaurants worth dining in.

## Site Users Goal
The user want to be able to write and Publish Posts to Share experiences about Restaurants and leave a comment below other users Posts.

## Site Owners Goal
The goal of the site owner is to deliver a site where the users in an intuitive part of the Website and be able to interact with the community.

## Project Management


### Github Board
I've been using Github Projects to plan and organize the user stories for this Project

<details><summary><b>Github Board</b></summary>

![User Stories](user-stories/screenshot)<!--Screenshots about user stories on Github HERE!!-->
</details><br/>

[Back to top](<#table-of-content>)

# **User Experience (UX)**

## User Stories
Below the user stories for the project are listed to clarify why particular feature matters. These will then be tested and confirmed in the [Testing](<#testing>) section.

### Site User
|  | | | 
|:-------:|:--------|:--------|
| As a Site User | I can view a list of **Restaurant** reviews so that I can select one to read | &check; |
| As a Site User | I can click on a specific review to read it in detail | &check; |
| As a Site User | I can like and unlike a review to interact with it | &check; |
| As a Site User | I can view the number of likes on each review to see its popularity | &check; |
| As a Site User | I can contact The Restaurant Review easily | &check; |
| As a Site User | I can navigate easily through paginated lists of posts | &check; |
| As a Site User | I can view comments on a specific review to read conversations | &check; |
| As a Site User | I can sign up for an account to like and comment on reviews, create a profile page, create my own reviews, and edit/remove my reviews | &check; |
| As a Site User | I can create a profile page for other reviewers to read about me | &check; |
| As a Site User | I can comment on a review to join the conversation | &check; |
| As a Site User | I can edit my comment to change its content if needed | &check; |
| As a Site User | I can remove my review to have full control over my reviews | &check; |
| As a Site User | I can choose to see my own reviews for easy access | &check; |
| As a Site User | I can create a new review to contribute new content | &check; |
| As a Site User | I can log out from the site to ensure the security of my information | &check; |
| As a Site User | I can create draft reviews to finish writing them later | &check; |
| As a Site User | I can receive visual feedback when interacting with the content | &check; |here

### Site Admin

|  | | | 
|:-------:|:--------|:--------|
| As a Site Admin | I can log out from the site so that I can feel safe that nobody can access my information | &check; |
| As a Site Admin | I can create, read, update and delete reviews so that I can manage my review content | &check; |
| As a Site Admin | I can approve reviews so that I can secure high quality of the content | &check; |
| As a Site Admin | I can approve and disapprove comments so that I can secure a safe environment for the Site Users | &check; |
| As a Site Admin | I can create draft reviews so that I can finish writing the content later | &check; |
| As a Site Admin | I can access an admin area so that I can get a general understanding of logged in users, number of likes and number of posts | &check; |
| As a Site Admin | I can get visual feedback when interacting with the content so that I can be sure how I have interacted with the page | &check; |

[Back to top](<#table-of-content>)

## Site Structure

The Restaurant Review Blog is organized into two distinct sections based on the user's **login** status: **Logged Out** and **Logged In**. The availability of pages varies depending on whether the user is logged in or not. For users who are **not logged in**, the navigation bar at the top of the site displays the following pages: **Home, About, Login**, and **Register**. Conversely, when a user is **logged in**, the navigation bar includes **Home, About, Profile, Logout**, and **New Post**. Additionally, if the user is logged in as an **administrator**, an **Admin** page is also accessible, along with the other pages mentioned. The design of the site is minimalistic, clean, and intuitive, ensuring ease of navigation for users.

Read more about the different choices in the [Features](<#features>) section.

[Back to top](<#table-of-content>)

## Design Choices

* ### Color Scheme
The color scheme for the Restaurant Review site is designed with a focus on a dark background, inspired by Bootstrap's dark theme.
The Navbar and Footer are styled with a light grey background color, specifically using the hexadecimal color code #555. This choice ensures a subtle contrast that maintains readability and aesthetic appeal.

The main body of the site utilizes Bootstrap's dark-bg class, which is designed to provide a dark background suitable for text and other elements. This class is essential for creating a visually appealing and readable layout, especially in environments with bright lighting conditions.

For the Published Posts, a white card container is employed to encapsulate the content. This container is styled with a black text color, which contrasts well with the white background, enhancing readability and ensuring that the content stands out against the darker background of the site. This combination of colors ensures that the text is easily readable, making it simple for users to navigate through the site and find the information they're looking for.

The Colors choosen for this project are based on the <a href="https://www.colorhexa.com/5f788a">Monochromatic Colorsheme:</a> 

![Color Palette image](readme/assets/images/Monochromatic.png)

* ### Typography
The typography for the Restaurant Review site is designed with a focus on readability and aesthetic appeal. The primary font chosen is 'Roboto', which is used throughout the site to ensure a consistent and modern look. For the headings, 'Roboto' is utilized in its regular weight to create a strong visual hierarchy and draw attention to the main points of each section.

For the body text, including excerpts and post content, the 'Roboto' font is used in its regular weight. This choice ensures that the text remains readable and maintains a cohesive look across the site. The fallback font for both 'Roboto' and the normal text is set to sans-serif, ensuring that the site's typography remains accessible and visually appealing even if the primary font fails to load for any reason.

![Google Fonts Impact](readme/assets/images/roboto.png)

[Back to top](<#table-of-content>)

# **Features**
The features of the site are listed below.

## **Existing Features**

### **Navigation**
The navigation bar of the Restaurant Review site is designed to be clean and straightforward, ensuring ease of use for all visitors. The availability of different pages to the user depends on their login status. Specifically, if a user is logged in, additional pages become accessible to them. Furthermore, an extra page is made visible to users who are logged in as administrators, providing them with additional functionalities and controls.

*Links that are visible to logged out users*

* Home - Displays posts as a list of 6 per page. On devices with a large screen, such as laptops or PCs, 3 posts are displayed per row within a white card container to maintain readability. If there are fewer than 7 posts, a "Next" button will not appear. However, if there are more than 7 posts, a "Next" button will appear, allowing users to visit the second page.
* About -  Describes the purpose and motivation behind the Restaurant Review Blog.
* Login - Contains a login form where users can enter their username and password to log into their account.
* Register - Contains a sign-up form where users can enter their username, email address, password, and password confirmation to create a new account.

<details><summary><b>Navigation Large - User Not Logged In</b></summary>

![Navigation Large - User Not Logged In](readme/assets/images/logged-out-navbar.png)
</details><br/>


*Links that are visible to logged in users*

All of the links that are visible to a not logged in user plus the ones below.

* Profile - User can visit his profile and edit or delete his Profile. He can edit his profile image, user details such as Name, emailadress etc. The Users Profile page displays also the users own posts in a similar way like on the homepage and the Posts he marked as Favorites below that in the same way like on the homepage within a scrollable container.
* Logout - Log user out of his profile and show a brief logged out message to user.
* New Post - User can Create a new Post and upload an Image to it.

<details><summary><b>Navigation Large - User Logged In</b></summary>

![Navigation Large - User Logged In](readme/assets/images/user-logged-in-large.png)
</details><br/>

<details><summary><b>Navigation Small - User Logged In</b></summary>

![Navigation Small - User Logged In](readme/assets/images/user-logged-in-small.png)
</details><br/>

*Link that is visible if user is administrator*

All of the links above plus the one below.
* Admin Area - Bring the Administrator to the Django Admin page, where they can view and modify all users, their permissions, posts, comments, approve comments and posts, add or remove permissions for certain users, etc. The default Django Admin page has been replaced with Jazzmin, as it provides a better overview and has been configured to include a "Back To Website" link in the top left corner of the page. This allows the user to return to the website at any time.

<details><summary><b>Additional Link in Navbar - Admin Logged In</b></summary>

![Navigation Small - User Logged In](readme/assets/images/admin-loggedin-marked.png)
</details><br/>

### **About**
The About Page describes the purpose and motivation behind the website to the user.

<details><summary><b>About page</b></summary>

![About](readme/assets/images/about-page.png)
</details><br/>

### **Home**
The Home Page contains a list of all published posts and displays 3 posts per row. The Posts are wrapped in a white card container with an Image and the Title and Excerpt below that. All Posts displayed on the Homepage are wrapped in a scrollable container to give some flexibility to it when the content given to it makes the post-container grow. In the bottom right corner of the post container, there are 3 icons: a thumbs up, a thumbs down, and a heart icon. The user can up and down vote the Post using the thumbs and save the post to their Favorites by clicking on the Heart icon. If the Heart Icon is pressed, the icon gets filled out with a red color, and the Favorites are saved to the user's Profile Page

<details><summary><b>Home Page</b></summary>

![Home Page](readme/assets/images/home-page.png)
</details><br/>

### **Profile**
The User's Profile Page has a Profile container with the username, profile image, and user details such as email address, etc. Below that container, there are two buttons located at the bottom right side. One is the **Edit** button, and the other one is the **Delete** button. When the user clicks on Edit, the profile form opens up, allowing the user to adjust user details and profile image and save the changes with the save button below the form. When the user clicks on the 'Delete' button, a Modal will open up to get a second confirmation from the user to ensure users really want to delete theire profile. Below the Profile Container, the user's own published posts are listed in the same way they are on the homepage. Below that, there is a second section where the user's favorite posts are listed, also in the same way the homepage does. This layout ensures that the user always has his own and his favorite posts close by.


<details><summary><b>Profile Container</b></summary>

![Profile Container](readme/assets/images/profile-container.png)
</details><br/>

<details><summary><b>Profile Form</b></summary>

![Profile Form](readme/assets/images/profile-form.png)
</details><br/>

<details><summary><b>Deletion Modal</b></summary>

![Review Detail View - User Logged In](readme/assets/images/delete-profile.png)
</details><br/>

<details><summary><b>Users Own Posts</b></summary>

![Profile Form](readme/assets/images/users-posts.png)
</details><br/>

<details><summary><b>Users Favorite Posts</b></summary>

![Profile Form](readme/assets/images/users-favorites.png)
</details><br/>

### **Create Post**
If the user is logged in, they can create a post by clicking on the navbar link "New Post". This link directs the user to the post form where they must click on the button *Create Post* to confirm their decision and open the post form. The post form contains four input fields: Title, Slug, Content, and Excerpt.
The Slug field will be automatically populated based on the title.
Additionally, there is an upload field that allows the user to upload an image to their post.

**Important Notice:**: The Slug field only accepts letters and spaces, which will be replaced by a hyphen. Unfortunately, I haven't yet figured out how to allow special characters in the slug, so users need to choose titles that only contain normal letters and spaces in order to successfully save and publish the post.

<details><summary><b>Closed Post Form</b></summary>

![Update Comment](readme/assets/images/closed-postform.png)
</details><br/>

<details><summary><b>Opened Post Form</b></summary>

![Update Comment](readme/assets/images/opned-postform.png)
</details><br/>

### **Post**
When a user clicks on the title of a post on the homepage, they are redirected to the post page. The post page contains the title on the top left and the image on the top right. Below the title and image, the post content is displayed. Beneath the content, there are icons for thumbs up, thumbs down, and a heart icon on the bottom left side. Below these icons, there is a comment section with two containers. On the left side, approved comments are displayed, while on the right side, there is a small text input form with a submit button where logged-in users can write and post comments about the post. If a user is logged out, the right create-comment section will display a message: "You have to be logged in to leave a comment".
Post and comment sections are wrapped in a scrollable container to enable scrolling down to the end when the content overflows the regular body section.

* *Post* - Title with an image at the top of the page, followed by content below.
* *Icons Thumbs (Up/Down), Heart* - Icons allow user to like/dislike and mark post as favorite
<!--IMPLEMENTATION OF DRAFT AND APPROVAL FOR POSTS WOULD BE NECESSERY!!!!!-->

<details><summary><b>Post</b></summary>

![Member Reviews](readme/assets/images/post.png)
</details><br/>

### **Update Post / Delete Post**
Below the user's own published posts, there are two buttons: Edit and Delete. When a user clicks on the Edit button, the post form will open up and repopulate the input fields with the existing post content and title. Additionally, there is an upload field below the post form that allows the user to upload a new image to the post. After making any necessary changes, the user can click the Update button below the form to submit the new data. If the user wishes to delete the post, they can click the Delete button.
<!--ADD APPROVE FUNCTIONALITY SO SUBMITED POSTS GET SAVED AS DRAFT AS DEFAULT!!!!!!-->

<details><summary><b>Post with Update option</b></summary>

![Member Reviews](readme/assets/images/post-with-update-btn.png)
</details><br/>

<details><summary><b>Post Update Form</b></summary>

![Create Review](readme/assets/images/post-updateform.png)
</details><br/>

### Thumbs / Favorites

Users can interact with the thumbs-up and thumbs-down icons to indicate whether they like or dislike a post. Clicking once on one of the thumb icons will increase the count by one. If the user clicks on the opposite thumb icon from the one clicked before, the old icon's count will reset to -1, and the recently clicked icon will increase by 1.

Additionally, users can click on the Heart icon to save the post to their favorites. The post will then be displayed within the user's profile page, and the Heart icon will be filled out in red to indicate that it has been saved to favorites.

<details><summary><b>Post Icons</b></summary>

![Member Reviews](readme/assets/images/post-icons.png)
</details><br/>

### **Create / Update / Delete Comment**
If the user is logged in, they can write and submit comments below the posts. Once submitted, comments will need to be approved by an administrator to ensure they comply with the site's policy and terms. If a user wishes to update their comment, they can simply click the Edit button below their own comment. Clicking the Edit button in the comment section on the left side will automatically repopulate the text field of the create-comment container on the right side with the comment's content. Additionally, with the dynamic help of the innerText function in JavaScript, the Submit button will become an Update button.
The second button that appears below the user's own comments is the Delete button. Clicking on the Delete button will open a modal to get a second confirmation from the user to ensure they are sure about deleting their comment.

<details><summary><b>Create Comment</b></summary>

![Update Review](readme/assets/images/create-container.png)
</details><br/>

<details><summary><b>Comment Buttons</b></summary>

![Update Review](readme/assets/images/comment-btn.png)
</details><br/>

<details><summary><b>Update Comment</b></summary>

![Update Review](readme/assets/images/update-comment.png)
</details><br/>

<details><summary><b>Delete Comment Modal</b></summary>

![Update Review](readme/assets/images/comment-delete-modal.png)
</details><br/>

<details><summary><b>Comment and Create Container</b></summary>

![Update Review](readme/assets/images/submit-comment.png)
</details><br/>


### **Admin Area**
On this page, the administrator (or another superuser designated by Restaurant Review) is responsible for content management, including approving comments, managing user rights, profiles, posts, etc. The Admin link in the Navbar of the Restaurant Review Blog directs superusers to the default Django Admin page, which has been replaced with Jazzmin to provide a better overview. Jazzmin is configured to use Dark mode instead of Light mode, and a Back To Website button has been added to the Top menu, which is only visible on larger devices like laptops, desktops, and tablets. 

**Important Notice** It is recommended to manage the site via the Admin page using devices with larger screens such as laptops, desktops, and tablets. This is because the "Back To Website" link in the Top Menu, which brings the superuser back to the website, is only displayed on these devices. If an administrator wants to manage the site's content via a smartphone, for instance, they will need to delete the /admin part of the URL to return to the website.

<details><summary><b>Navigation Large - Admin Logged In</b></summary>

![Navigation Large - Admin Logged In](readme/assets/images/admin-dark-large.png)
</details><br/>

<details><summary><b>Navigation Small - Admin Logged In</b></summary>

![Navigation Small - Admin Logged In](readme/assets/images/admin-dark-small.png)
</details><br/>

### **Register**
If a site visitor is not registered as a user at Restaurant Review, they can sign up. During the sign-up process, they can also upload a profile image. If they do not upload an image, the default image of Nobody will be set as their profile image. An unregistered user can only read and view the posts listed on the website but cannot leave comments or publish posts.

<details><summary><b>Register</b></summary>

![Sign Up](readme/assets/images/join-today.png)
</details><br/>

### **Login**
This is the sign-in form for users to access their accounts.

<details><summary><b>Sign In</b></summary>

![Sign In](readme/assets/images/login.png)
</details><br/>

### **Logout**
When the user clicks "Logout" in the navbar, a brief message will be shown to them to inform them that they have successfully logged out from their accounts. Below that, there is a small "Login Again" link to allow the user to access the login form again.

<details><summary><b>Logout</b></summary>

![Logout](readme/assets/images/logout.png)
</details><br/>

### **Footer**
The footer area includes the name of the person who made the website and social media links that users can use to follow *Restaurant Review*.

<details><summary><b>Footer</b></summary>

![Footer](readme/assets/images/footer.png)
</details><br/>

### **Flash Messages and confirmation pages to the user**
The sites incorporates flash messages and confirmation messages when an action has been performed (i.e. delete/update actions). Examples of this in the screenshots below.

<details><summary><b>Confirmation Messages</b></summary>

![Comment Created Success](readme/assets/images/comment-submited.png)
![Comment Updated Success](readme/assets/images/comment-updated.png)
![Comment Deleted Success](readme/assets/images/comment-deleted.png)
![Post Published Success](readme/assets/images/post-published.png)
![Post Updated Success](readme/assets/images/post-updated.png)
![Post Deleted Success](readme/assets/images/post-deleted.png)

### Features Left to Implement

<!--* Add more automated testing
* Add 'current page is active' in navbar
* Search reviews functionality from the navbar
* Information in the about section how many reviews each reviewer has made
* Add / remove genre and category in admin section
* Add image resize functionality
* Remove admin approval of comments

[Back to top](<#table-of-content>)-->

# Technologies Used

## Languages

* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - Provides the functionality for the site.
* [HTML5](https://en.wikipedia.org/wiki/HTML) - Provides the content and structure for the website.
* [CSS3](https://en.wikipedia.org/wiki/CSS) - Provides the styling for the website.
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript) - Provides interactive elements of the website

## Frameworks & Software
* [Bootstrap](https://getbootstrap.com/) - A CSS framework that helps building solid, responsive, mobile-first sites
* [Django](https://www.djangoproject.com/) - A model-view-template framework used to create the Review | Alliance site
* [Github](https://github.com/) - Used to host and edit the website.
* [Heroku](https://en.wikipedia.org/wiki/Heroku) - A cloud platform that the application is deployed to.
* [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/) - Used to test performance of site.
* [Responsive Design Checker](https://www.responsivedesignchecker.com/) - Used for responsiveness check.
* [Favicon](https://favicon.io/) - Used to create the favicon.
* [VSCode](https://code.visualstudio.com/) - Used to create and edit the site.
* [Google Chrome DevTools](https://developer.chrome.com/docs/devtools/) - Used to debug and test responsiveness.
* [Cloudinary](https://cloudinary.com/) - A service that hosts all static files in the project.
* [HTML Validation](https://validator.w3.org/) - Used to validate HTML code
* [CSS Validation](https://jigsaw.w3.org/css-validator/) - Used to validate CSS code
* [PEP8 Validation](http://pep8online.com/) - At the time for deploying this project the PEP8 Online Validaton service was offline, therefore not used.
* [JSHint Validation](https://jshint.com/) - Used to validate JavaScript code