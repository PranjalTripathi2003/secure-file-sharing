from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bcrypt, mail
from app.models import User, File
from app.utils import generate_confirmation_token, confirm_token, send_email, token_required, generate_download_token
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Page Route that shows instructions
@app.route('/')
def home():
    instructions = {
        'POST /register': 'Register a new client user.',
        'GET /confirm/<token>': 'Confirm email address for a user.',
        'POST /login': 'Login as a user (client or ops).',
        'POST /upload': 'Upload a file (Ops users only).',
        'GET /files': 'List all uploaded files (Client users only).',
        'GET /download/<token>': 'Download a file (Client users only).'
    }
    return render_template('index.html', instructions=instructions)

# Register Route for Client Users
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(email=data['email'], password=hashed_password, role='client')
    db.session.add(user)
    db.session.commit()

    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    send_email('Confirm Your Account', user.email, html)

    return jsonify({'message': 'User created, please confirm your email!'})

# Email Confirmation Route
@app.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if email:
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Account already confirmed.', 'success')
        else:
            user.confirmed = True
            db.session.commit()
            flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('login'))
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# File Upload Route (Ops User)
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if current_user.role != 'ops':
        return jsonify({'message': 'Only Ops users can upload files!'}), 403

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        new_file = File(filename=filename, uploader_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully!'}), 200
    return jsonify({'message': 'Invalid file type!'}), 400

# List Files Route (Client User)
@app.route('/files', methods=['GET'])
@login_required
def list_files():
    if current_user.role != 'client':
        return jsonify({'message': 'Only clients can view files!'}), 403

    files = File.query.all()
    return jsonify({'files': [{'id': f.id, 'filename': f.filename} for f in files]})

# Download File Route (Client User)
@app.route('/download/<token>', methods=['GET'])
@login_required
def download_file(token):
    if current_user.role != 'client':
        return jsonify({'message': 'Only clients can download files!'}), 403

    file_id = generate_download_token(token)
    file = File.query.get_or_404(file_id)
    return jsonify({'file_url': url_for('static', filename='uploads/' + file.filename, _external=True)})
