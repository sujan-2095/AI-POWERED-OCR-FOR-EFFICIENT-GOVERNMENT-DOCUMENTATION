import os
from io import BytesIO
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ocr_tamil.ocr import OCR

# ---------------------- Flask App Setup ----------------------
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key!

# SQLite database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocr_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# ---------------------- Models ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    records = db.relationship('OCRResult', backref='user', lazy=True)

class OCRResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ---------------------- Initialize OCR Models ----------------------
model_path = r"D:\Project\Niral 2.0\code\main\ocr\ocr_tamil\model_weights\parseq_tamil_v3.pt"
text_detect_model = r"D:\Project\Niral 2.0\code\main\ocr\ocr_tamil\model_weights\craft_mlt_25k.pth"

ocr_detect = OCR(detect=True, tamil_model_path=model_path, detect_model_path=text_detect_model, enable_cuda=True)
ocr_recognize = OCR(detect=False, tamil_model_path=model_path, detect_model_path=text_detect_model, enable_cuda=True)

# ---------------------- Create DB Tables Manually ----------------------
with app.app_context():
    db.create_all()

# ---------------------- Helper ----------------------
def read_image_as_np(image_file_storage):
    image_stream = image_file_storage.stream
    image = Image.open(image_stream).convert('RGB')
    image_np = np.array(image)
    return image_np

# ---------------------- Routes ----------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match.")
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return render_template('register.html')

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    username = session['username']
    records = OCRResult.query.filter_by(user_id=user_id).order_by(OCRResult.timestamp.desc()).all()
    return render_template('dashboard.html', username=username, records=records)

@app.route('/ocr', methods=['GET', 'POST'])
def ocr_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    result = None
    mode = "recognize"

    if request.method == 'POST':
        mode = request.form.get('mode')
        image_file = request.files.get('image')
        if image_file:
            try:
                image_np = read_image_as_np(image_file)
                filename = image_file.filename

                if mode == 'recognize':
                    texts = ocr_recognize.predict(image_np)
                else:
                    texts = ocr_detect.predict(image_np)

                if isinstance(texts, list):
                    flat_texts = []
                    for item in texts:
                        if isinstance(item, list):
                            flat_texts.extend(str(subitem) for subitem in item)
                        else:
                            flat_texts.append(str(item))
                    result = "\n".join(flat_texts)
                else:
                    result = str(texts)

                new_result = OCRResult(
                    filename=filename,
                    text=result,
                    user_id=session['user_id']
                )
                db.session.add(new_result)
                db.session.commit()

            except Exception as e:
                result = f"Error during OCR: {e}"

    return render_template('ocr.html', result=result, mode=mode)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------------- Run App ----------------------
if __name__ == '__main__':
    app.run(debug=True)
