from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home - List all employees
@app.route('/')
def index():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employee')
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

# Add Employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']

        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employee (name, email, department, salary) VALUES (?, ?, ?, ?)',
                       (name, email, department, salary))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# Edit Employee
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']

        cursor.execute('UPDATE employee SET name=?, email=?, department=?, salary=? WHERE id=?',
                       (name, email, department, salary, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM employee WHERE id=?', (id,))
    employee = cursor.fetchone()
    conn.close()
    return render_template('edit.html', employee=employee)

# Delete Employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employee WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
