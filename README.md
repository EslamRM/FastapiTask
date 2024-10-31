
# FastAPI Project

A FastAPI application that provides user authentication and organization management. This project demonstrates the use of FastAPI with MongoDB, Redis, and Docker for building a comprehensive API with token management, CRUD operations, and efficient data handling.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

## Features

- User authentication with JWT tokens
- CRUD operations for organizations
- Asynchronous API handling with FastAPI
- Integration with MongoDB and Redis
- Containerization with Docker

## Technologies

- **FastAPI**: A modern web framework for building APIs with Python 3.7+.
- **MongoDB**: NoSQL database for storing user and organization data.
- **Redis**: In-memory data structure store, used as a cache.
- **Docker**: Containerization tool to streamline the development and deployment process.
- **pytest**: Testing framework for running unit and integration tests.

## Getting Started

To get a local copy up and running, follow these steps:

### Prerequisites

- Python 3.9 or later
- Docker and Docker Compose

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/EslamRM/FastapiTask.git
   cd FastapiTask
   ```

2. Create a `.env` file based on the `.env.example` template, and configure your environment variables.

3. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application at `http://localhost:8080`.

## API Endpoints

### Authentication
- **Sign Up**
  - `POST /auth/signup`
  - Request Body: `{"name" : "test" ,"email": "user@example.com", "password": "yourpassword" }`
  - Response: `{ "message","str"}`
  
- **Sign In**
  - `POST /auth/signin`
  - Request Body: `{ "email": "user@example.com", "password": "yourpassword" }`
  - Response: `{ "access_token": "token", "refresh_token": "token" ,"message","str"}`

### Organizations

- **Create Organization**
  - `POST /organization`
  - Request Body: `{ "name": "Organization Name", "description": "Description of the organization." }`
  - Response: `{ "organization_id": "org_id" }`

- **Read Organization**
  - `GET /organization/{organization_id}`
  - Response: `{ "name": "Organization Name", "description": "Description of the organization." }`

## Testing

To run the tests, use the following command:

```bash
docker-compose run --rm tests
```

Make sure your FastAPI application is running while executing the tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
