# Url Shortener

Brief description of the project.

### Requirements
- Docker (version 26.1.3)

- Docker Compose (version 1.29.2)

### Getting Started
#### 1. Clone the repository:
```
git clone https://github.com/IshaqNiloy/url-shortener.git
```

#### 2. Navigate to the project directory:
```
cd url_shortener
```

#### 3. Environment Variables:
Copy the .sample.env file and rename it to .env. Update the variables as needed.

#### 4. Build the Docker images:
```
docker-compose build
```

#### 5. Run the Docker containers:
```
docker-compose up
```

#### 6. Initialize the Database:
```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

#### 7. Access the API documentation:
Open your web browser and navigate to http://localhost:8000/minify/doc/ for comprehensive API documentation.

### API Endpoints
POST /minify/: Returns the short url.  
GET /`<short_code>`: Redirects the user to the original url.
