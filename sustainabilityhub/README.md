# Sustainability Hub

A comprehensive Django-based platform for connecting people passionate about sustainability. Collaborate on projects, participate in events, share resources, and engage in meaningful discussions.

## Features

- **User Accounts & Profiles**: Custom user model with profiles, avatars, and user information
- **Forums**: Discussion topics with categories, posts, likes, and replies
- **Projects**: Collaborative sustainability projects with updates and member management
- **Events**: Create and register for sustainability events (workshops, conferences, meetups)
- **Resources**: Share and discover sustainability resources with ratings
- **Messaging**: Private conversations between users
- **Notifications**: User notifications for important activities
- **Moderation**: Content reporting and moderation tools

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   cd sustainabilityhub
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## Apps

- **accounts**: User authentication and registration
- **profiles**: User profiles with location, skills, and interests
- **forums**: Discussion forums with topics and posts
- **projects**: Sustainability project management
- **events**: Event creation and registration
- **resources**: Resource sharing and rating
- **messaging**: Private messaging between users
- **notifications**: User notifications system
- **moderation**: Content moderation and reporting

## Admin Access

Access the admin panel at `/admin/` using your superuser credentials.

## Development

This project uses Django 4.2 with SQLite database for development. For production, configure PostgreSQL or another database in `settings.py`.

