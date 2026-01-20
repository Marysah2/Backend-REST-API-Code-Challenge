from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    # Validations
    def __init__(self, name, email):
        if not name or len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        self.name = name.strip()
        self.email = email.lower().strip()
    
    def to_dict(self, include_posts=False):
        result = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
        if include_posts:
            result['posts'] = [post.to_dict() for post in self.posts]
        return result

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Validations
    def __init__(self, title, content, user_id):
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if not content or len(content.strip()) == 0:
            raise ValueError("Content cannot be empty")
        if not user_id:
            raise ValueError("User ID is required")
        self.title = title.strip()
        self.content = content.strip()
        self.user_id = user_id
    
    def to_dict(self, include_author=False):
        result = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }
        if include_author:
            result['author'] = self.author.to_dict()
        return result

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Flask REST API is running!',
        'endpoints': {
            'users': '/users',
            'posts': '/posts'
        }
    })

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict(include_posts=True)), 200

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user = User(data.get('name'), data.get('email'))
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create user'}), 500

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'name' in data:
            if not data['name'] or len(data['name'].strip()) == 0:
                return jsonify({'error': 'Name cannot be empty'}), 400
            user.name = data['name'].strip()
        
        if 'email' in data:
            if not data['email'] or '@' not in data['email']:
                return jsonify({'error': 'Invalid email format'}), 400
            user.email = data['email'].lower().strip()
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Failed to update user'}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict(include_author=True) for post in posts]), 200

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post.to_dict(include_author=True)), 200

@app.route('/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Verify user exists
        user = User.query.get(data.get('user_id'))
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        post = Post(data.get('title'), data.get('content'), data.get('user_id'))
        db.session.add(post)
        db.session.commit()
        return jsonify(post.to_dict(include_author=True)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create post'}), 500

@app.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'title' in data:
            if not data['title'] or len(data['title'].strip()) == 0:
                return jsonify({'error': 'Title cannot be empty'}), 400
            post.title = data['title'].strip()
        
        if 'content' in data:
            if not data['content'] or len(data['content'].strip()) == 0:
                return jsonify({'error': 'Content cannot be empty'}), 400
            post.content = data['content'].strip()
        
        db.session.commit()
        return jsonify(post.to_dict(include_author=True)), 200
    except Exception as e:
        return jsonify({'error': 'Failed to update post'}), 500

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    db.session.delete(post)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)