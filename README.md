# django-blog-app

A **comprehensive and user-friendly blog application** built with Django, demonstrating the core capabilities of the Django framework. This application provides a full-stack blogging platform with key functionalities for managing blog content, handling user authentication, and implementing role-based access controls. Designed to offer seamless management for both authors and editors, it enables smooth content creation and editorial workflows. Readers, on the other hand, can easily browse and explore various blog posts organized by categories.

## Features

- **User Authentication:** Register, login, logout, and password reset via email, ensuring secure user management.
- **User Groups & Permissions:** Role-based access control for Readers, Authors, and Editors, with each user having appropriate privileges.
- **Blog Posts:** Authors can create, edit, delete, and publish/unpublish posts; editors have control over all posts.
- **Categories:** Organize posts into categories to enhance content discoverability.
- **Dashboard:** A personalized dashboard for managing and tracking posts.
- **Responsive UI:** A fully responsive design using **Bootstrap 5** and custom CSS for a modern user experience.
- **Error & Success Messages:** Clear feedback for users on successful actions or errors.
- **Pagination:** Paginated post lists on both the homepage and user dashboards for improved user experience.
- **Email Integration:** Password reset functionality integrated with Django's email system.
- **Middleware:** Custom middleware for handling user access control and redirection.

## Tech Stack

- Django 5.x
- Bootstrap 5
- SQLite (default, can be easily switched to other databases like PostgreSQL or MySQL)
- Python 3.13+

## How to Run

1. Clone the repo:
    ```
    git clone https://github.com/DineshR-dev/django-blog-app.git
    cd django-blog-project
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run migrations to set up the database:
    ```
    python manage.py migrate
    ```
4. Start the server:
    ```
    python manage.py runserver
    ```

Visit **http://127.0.0.1:8000/** to access the app.

## Folder Structure

- `blog/` - Main app (models, views, forms, templates, static files)
- `templates/blog/` - All HTML templates
- `static/css/` - Custom styles

## Customization

- **Email Settings:** Update the email configuration in `settings.py` to enable email functionality (for password resets and notifications).
- **Categories:** Add or modify categories via the Django admin interface for better content management.

## Screenshot

Below is a screenshot of the main page and the personalized user dashboard for authors:

![Main Page]<img width="1263" height="748" alt="mMy Blog" src="https://github.com/user-attachments/assets/6a56316c-5f32-4269-a5db-442893ce31e0" />
*Example of the blog's homepage with posts listed by category.*

![Dashboard]<img width="1263" height="1025" alt="Dashboard - My Blog" src="https://github.com/user-attachments/assets/0a598944-c620-4eb1-a350-e26d7b3b6512" />  
*Example of the author’s personalized dashboard for managing posts.*

![Blog Reading Page]
 <img width="1263" height="706" alt="My Blog" src="https://github.com/user-attachments/assets/b6e9339b-86d1-4528-a33e-007a08f16f07" />
 
*Example of a single blog post being read by a user with full content.*



## Acknowledgments

- This project was built as a practical exercise to apply concepts learned through Django tutorials, particularly inspired by **JVL code(Youtube Channel)**. The project’s design and style were directly influenced by the tutorials and examples provided by the channel, offering a structured way to implement the full functionality of a blogging platform.

---
