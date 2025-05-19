from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'  # replace with a real secret key

DB_PATH = 'users.db'

# ------------------- User Login Helper -------------------
def check_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Retrieve the hashed password for the given username
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    # If a user is found, verify the hashed password
    if user and check_password_hash(user[0], password):
        return True
    return False

# ------------------- Routes -------------------

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('subjects_page'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate input
        if not username or not email or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Check if username or email already exists
        cursor.execute('SELECT * FROM users WHERE username=? OR email=?', (username, email))
        if cursor.fetchone():
            flash('Username or email already exists!', 'error')
            return render_template('register.html')
        # Save user to the database
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, hashed_password))
            conn.commit()
            flash('Registration successful!', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        # Here you would implement the logic to reset the password
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/subjects')
def subjects_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('subjects.html', username=session['username'])

@app.route('/math')
def math_page():
    if 'username' not in session:
        return redirect(url_for('/login'))
    return render_template('math.html', username=session['username'])

@app.route('/reading')
def reading_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('reading.html', username=session['username'])

@app.route('/spelling')
def spelling_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('spelling.html', username=session['username'])

@app.route('/profile')
def profile_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'])

@app.route('/evaluations')
def evaluations():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('evaluations.html', username=session['username'])

# ------------------- App Runner -------------------
if __name__ == '__main__':
    app.run(debug=True)
