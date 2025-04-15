from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

volunteer_bp = Blueprint('volunteer', __name__)  # Define a Blueprint

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('volunteer.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT CHECK(status IN ('injured', 'dead', 'missing')) NOT NULL,
            details TEXT,
            contact_details TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Route for home/volunteer registration
@volunteer_bp.route('/')
def home():
    print("Rendering home page")
    return render_template('volin.html')


@volunteer_bp.route('/vol', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Save volunteer details to database
        conn = sqlite3.connect('volunteer.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO volunteers (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        conn.commit()
        conn.close()

        return redirect(url_for('volunteer.home'))
    return render_template('volunteer.html')





@volunteer_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@volunteer_bp.route('/update_person', methods=['GET', 'POST'])
def update_person():
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        details = request.form['details']
        contact_details = request.form['contact_details']
        image_file = request.files['image']

        image_path = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = filename  # Only store the filename
            image_file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Save person details including image path
        conn = sqlite3.connect('volunteer.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO persons (name, status, details, contact_details, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, status, details, contact_details, image_path))
        conn.commit()
        conn.close()

        return redirect(url_for('volunteer.home'))
    return render_template('update_person.html')


@volunteer_bp.route('/view_records')
def view_records():
    conn = sqlite3.connect('volunteer.db')
    cursor = conn.cursor()

    # Fetch all person records
    cursor.execute('SELECT * FROM persons')
    records = cursor.fetchall()
    conn.close()

    print("Fetched Records:", records)  # Debugging output
    return render_template('view_records.html', records=records)



init_db()












