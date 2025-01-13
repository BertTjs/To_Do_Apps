from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import markdown

app = Flask(__name__)

# Daftar tugas
tasks = [
    {'name': 'Learn Flask', 'completed': False, 'created_at': datetime(2023, 1, 1), 'notes': '**Understand routes and templates**'},
    {'name': 'Build To-Do App', 'completed': False, 'created_at': datetime(2023, 1, 2), 'notes': '*Use Flask templates*'}
]

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    sort_order = request.args.get('sort', 'asc')
    
    filtered_tasks = [task for task in tasks if search_query in task['name'].lower()]
    
    if sort_order == 'asc':
        filtered_tasks.sort(key=lambda x: x['created_at'])
    elif sort_order == 'desc':
        filtered_tasks.sort(key=lambda x: x['created_at'], reverse=True)

    return render_template('index.html', tasks=filtered_tasks, search_query=search_query, sort_order=sort_order)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        notes = request.form.get('notes', '')
        if name:
            tasks.append({'name': name, 'completed': False, 'created_at': datetime.now(), 'notes': notes})
            return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def view_task(task_id):
    if 0 <= task_id < len(tasks):
        task = tasks[task_id]
        if request.method == 'POST':
            task['notes'] = request.form['notes']
            return redirect(url_for('index'))
        rendered_notes = markdown.markdown(task['notes'])  # Render Markdown ke HTML
        return render_template('view_task.html', task=task, task_id=task_id, rendered_notes=rendered_notes)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
    return redirect(url_for('index'))

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)