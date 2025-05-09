from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'  # replace with a real secret key

DB_PATH = 'users.db'

# ------------------- User Login Helper -------------------
def check_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

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
        return redirect(url_for('login'))
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
def profile():
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
