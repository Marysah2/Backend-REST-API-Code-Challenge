# Flask REST API Code Challenge

A simple REST API built with Flask featuring Users and Posts with proper relationships, validations, and RESTful routes.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Users

- `GET /users` - Get all users
- `GET /users/<id>` - Get user by ID (includes posts)
- `POST /users` - Create new user
- `PATCH /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user

### Posts

- `GET /posts` - Get all posts (includes author info)
- `GET /posts/<id>` - Get post by ID (includes author info)
- `POST /posts` - Create new post
- `PATCH /posts/<id>` - Update post
- `DELETE /posts/<id>` - Delete post

## Example Usage

### Create User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Create Post
```bash
curl -X POST http://localhost:5000/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!", "user_id": 1}'
```

## Features

- **Models**: User and Post models with proper relationships
- **Validations**: Input validation with informative error messages
- **REST**: RESTful routing conventions
- **JSON Responses**: Proper JSON structure with nested data
- **HTTP Status Codes**: Appropriate status codes for all scenarios
- **Serializers**: Custom to_dict methods for structured data