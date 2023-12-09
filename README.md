# Image Upload Service API



### Prerequisites

- Docker Desktop

### Setup

1. **Start the Service**:

   Navigate to the project directory and start the service using Docker Compose.

   ```shell
   docker-compose build
   docker-compose up
   ```
   
2. **Database Migrations**:
   
   Apply the database migrations to ensure the database schema is updated.

   ```shell
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

3. **Create Admin User**:
   
   Create a superuser account to access the Django Admin panel.

   ```shell
   docker-compose exec web python manage.py createsuperuser
   ```

### Security (.env file)

Place .env in .gitignore, then change the values of .env variables for private.
Without Docker, use a package like python-dotenv to read the values of .env variables.


## Admin UI

Administrators can manage users, images, account tiers, and expiring links via Django-admin UI at [http://localhost:8000/admin/](http://localhost:8000/admin/).

## Testing

To run tests, type the command:

   ```shell
   docker-compose exec web python manage.py test
   ```