import sqlite3
import datetime

def connectToDB(reset=False):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()

    if reset:
    
        cursor.execute("DROP TABLE IF EXISTS Todo")
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Todo (
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                date TEXT NOT NULL,
                project TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER
            )
''')
                 
    
    conn.commit()
    print("Connected to database")
    conn.close()
    print("Disconnected from database")

def addTodo(title, priority, status,date, project,completed, user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
                  INSERT INTO Todo (title, priority, status,date,project, completed, user_id) 
                  VALUES (?, ?, ?, ?, ?,?,?)
                  ''', (title, priority, status,date, project,completed, user_id))
    
    conn.commit()
    print("Todo added")
    conn.close()
    print("Disconnected from database")

def getTodos(user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Todo
        WHERE user_id = ?
        ORDER BY date(date) ASC, priority DESC
    ''', (user_id,))
    todos = cursor.fetchall()
    conn.close()
    print("Disconnected from database")
    return todos


    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
                   UPDATE Todo 
                   SET completed = 1
                   WHERE id = ?
                   ''', (id,))
    
    conn.commit()
    print("Todo completed")
    conn.close()
    print("Disconnected from database")

def deleteTodo(id, user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM Todo 
        WHERE user_id = ?
        AND id = ?
    ''', (user_id, id))
    conn.commit()
    print("Todo deleted")
    conn.close()
    print("Disconnected from database")

def getCompletedTodos(user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Todo 
        WHERE user_id = ?
        AND status = 'completed'
    ''', (user_id,))
    completedTodos = cursor.fetchall()
    conn.close()
    print("Disconnected from database")
    return completedTodos


def getIncompleteTodos(user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Todo 
        WHERE user_id = ?
        AND (status = 'pending' OR status = 'in Progress')
    ''', (user_id,))
    incompleteTodos = cursor.fetchall()
    conn.close()
    print("Disconnected from database")
    return incompleteTodos


def getInboxTodos(user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Todo
        WHERE user_id = ?
        AND (project IS NULL OR project = '')
        ORDER BY date(date) ASC, priority DESC
    ''', (user_id,))
    todos = cursor.fetchall()
    conn.close()
    return todos


def getTodayTodos(user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()
    cursor.execute('''
        SELECT * FROM Todo
        WHERE user_id = ?
        AND date(date) = ?
    ''', (user_id, today))
    todos = cursor.fetchall()
    conn.close()
    return todos


def getUpcomingTodos(user_id):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()
    cursor.execute('''
        SELECT * FROM Todo
        WHERE user_id = ?
        AND date(date) > ?
        ORDER BY date(date) ASC
    ''', (user_id, today))
    todos = cursor.fetchall()
    conn.close()
    return todos


def getProjectTodos(user_id, project_name):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Todo
        WHERE user_id = ?
        AND project = ?
    ''', (user_id, project_name))
    todos = cursor.fetchall()
    conn.close()
    return todos

def searchTodos(keyword):
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    query = '''
        SELECT * FROM Todo
        WHERE title LIKE ? OR priority LIKE ? OR status LIKE ?
    '''
    wildcard = f"%{keyword}%"
    cursor.execute(query, (wildcard, wildcard, wildcard))
    results = cursor.fetchall()
    conn.close()
    return results

def getAllProjects():
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT project FROM Todo WHERE project IS NOT NULL AND project != ""')
    projects = [row[0] for row in cursor.fetchall()]
    conn.close()
    return projects

def create_user_table():
    conn = sqlite3.connect('TaskiGoals.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Use reset=True ONLY if you want to wipe all data and start fresh!
    connectToDB(reset=False)
