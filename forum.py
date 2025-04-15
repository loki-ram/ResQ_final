from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import random
from flask import Blueprint, request, jsonify, render_template, send_from_directory

forum_bp=Blueprint('forum',__name__)

# Configurations
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for posts
posts = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@forum_bp.route('/')
def index():
    return render_template('forum.html', posts=posts)

@forum_bp.route('/add_post', methods=['POST'])
def add_post():
    global posts
    try:
        data = request.form
        print("Form Data:", data)  # Debugging
        text = data.get('text', '')

        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                image_url = f"/{file_path}"  # URL for the uploaded image

        post = {
            "id": len(posts) + 1,
            "text": text,
            "image_url": image_url,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        posts.append(post)
        print("Post Added:", post)  # Debugging

        return jsonify({"message": "Post added successfully", "post": post}), 201
    except Exception as e:
        print("Error:", e)  # Debugging
        return jsonify({"message": "Failed to add post", "error": str(e)}), 500

# Route to serve uploaded files
@forum_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@forum_bp.route('/get_posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

