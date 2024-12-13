from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('gallery'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Account already exists! Please log in.")
            return redirect(url_for('login'))
        
        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verify user credentials
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!")
            return redirect(url_for('gallery'))
        
        flash("Invalid credentials. Please try again.")
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/gallery', methods=['GET'])
def gallery():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))
    
    return render_template('gallery.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)