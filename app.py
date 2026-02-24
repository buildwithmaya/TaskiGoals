from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import connectToDB, addTodo, getTodos, deleteTodo, getAllProjects, getCompletedTodos, getTodayTodos, getUpcomingTodos, getProjectTodos, searchTodos, getInboxTodos, create_user_table, completeTodo, updateTodo
from functools import wraps
import sqlite3
import bcrypt
import os

create_user_table()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('TaskiGoals.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User WHERE username=?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = sqlite3.connect('TaskiGoals.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO User (username, password) VALUES (?, ?)', (username, hashed_password.decode('utf-8')))
            conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    view = getTodos(user_id)
    return render_template('index.html', view=view)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    priority = request.form.get('priority')
    status = request.form.get('status')
    date = request.form.get('date')  # Optional
    project = request.form.get('project')
    
    if title and priority and status and date:
        user_id = session['user_id']
        addTodo(title, priority, status, date, project, 0, user_id)
    return redirect(url_for('index'))   

@app.route('/completed')
@login_required
def completed():
    user_id = session['user_id']
    view = getCompletedTodos(user_id)
    return render_template('completed.html', view=view)



@app.route('/delete/<int:id>')
@login_required
def delete(id):
    user_id = session['user_id']
    deleteTodo(id, user_id)
    return redirect(url_for('index'))

@app.route('/today') 
@login_required
def today():
    user_id = session['user_id']
    view = getTodayTodos(user_id)
    return render_template('today.html', view=view)

@app.route('/upcoming') 
@login_required
def upcoming():
    user_id = session['user_id']
    view = getUpcomingTodos(user_id)
    return render_template('upcoming.html', view=view)
   

@app.route('/myProjects') 
@login_required
def myProjects():
    user_id = session['user_id']
    projects = getAllProjects(user_id)
    return render_template('myProjects.html', projects=projects)
   
@app.route('/myProjects/<project_name>')
@login_required
def project(project_name):
    user_id = session['user_id']
    view = getProjectTodos(user_id, project_name)
    return render_template('project.html', view=view, project_name=project_name)

@app.route('/inbox') 
@login_required
def inbox():
    user_id = session['user_id']
    view = getInboxTodos(user_id)
    return render_template('inbox.html', view=view)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    results = []
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        if keyword:
            user_id = session['user_id']
            results = searchTodos(keyword, user_id)
    return render_template('search.html', results=results)

@app.route('/complete/<int:id>')
@login_required
def complete(id):
    user_id = session['user_id']
    completeTodo(id, user_id)
    return redirect(request.referrer or url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user_id = session['user_id']
    if request.method == 'POST':
        title = request.form.get('title')
        priority = request.form.get('priority')
        status = request.form.get('status')
        date = request.form.get('date')
        project = request.form.get('project')
        
        if title and priority and status and date:
            updateTodo(id, user_id, title, priority, status, date, project)
            flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
