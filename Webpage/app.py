from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
        user = check_user(username, password);
        if user:
            session['username'] = username
            session['user_id'] = user[0]
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

@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.json
    user_id = session.get('user_id')
    subject = data.get('subject')
    correct = data.get('correct')
    incorrect = data.get('incorrect')
    lessons_completed = data.get('lessons_completed')
    streak = data.get('streak')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Upsert logic: update if exists, else insert
    c.execute("SELECT id FROM user_progress WHERE user_id=? AND subject=?", (user_id, subject))
    row = c.fetchone()
    if row:
        c.execute('''
            UPDATE user_progress
            SET lessons_completed=?, correct_answers=?, incorrect_answers=?, longest_streak=?
            WHERE id=?
        ''', (lessons_completed, correct, incorrect, streak, row[0]))
    else:
        c.execute('''
            INSERT INTO user_progress (user_id, subject, lessons_completed, correct_answers, incorrect_answers, longest_streak)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, subject, lessons_completed, correct, incorrect, streak))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# ------------------- App Runner -------------------
if __name__ == '__main__':
    app.run(debug=True)
