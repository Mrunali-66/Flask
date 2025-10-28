from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)
tasks = []
task_id_counter = 1

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kanban Task Manager</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .board-container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .stats {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }

        .columns {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .column {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            min-height: 400px;
        }

        .column-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
        }

        .column-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #333;
        }

        .task-count {
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .tasks {
            min-height: 300px;
        }

        .task {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            cursor: move;
            transition: all 0.3s ease;
            border-left: 4px solid #667eea;
        }

        .task:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }

        .task-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            font-size: 1.05em;
        }

        .task-description {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
            line-height: 1.4;
        }

        .task-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #f0f0f0;
        }

        .task-priority {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }

        .priority-high { background: #fee; color: #c33; }
        .priority-medium { background: #ffeaa7; color: #d63031; }
        .priority-low { background: #e3f2fd; color: #1976d2; }

        .task-actions {
            display: flex;
            gap: 8px;
        }

        .task-btn {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.1em;
            padding: 4px;
            opacity: 0.6;
            transition: all 0.2s;
        }

        .task-btn:hover {
            opacity: 1;
            transform: scale(1.2);
        }

        .add-task-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s;
            margin-top: 10px;
        }

        .add-task-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal.active { display: flex; }

        .modal-content {
            background: white;
            border-radius: 16px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .modal-header {
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #333;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }

        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            font-family: inherit;
        }

        .form-group textarea {
            resize: vertical;
            min-height: 80px;
        }

        .modal-actions {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-top: 25px;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-secondary {
            background: #e0e0e0;
            color: #666;
        }

        .drag-over {
            background: rgba(102, 126, 234, 0.1);
            border: 2px dashed #667eea;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Kanban Task Manager</h1>
        <p>Python Flask Edition</p>
    </div>

    <div class="board-container">
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value" id="totalTasks">0</div>
                <div class="stat-label">Total Tasks</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="completedTasks">0</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="completionRate">0%</div>
                <div class="stat-label">Completion Rate</div>
            </div>
        </div>

        <div class="columns">
            <div class="column" data-status="todo" ondrop="drop(event)" ondragover="allowDrop(event)" ondragleave="dragLeave(event)">
                <div class="column-header">
                    <span class="column-title">📋 To Do</span>
                    <span class="task-count" id="count-todo">0</span>
                </div>
                <div class="tasks" id="tasks-todo"></div>
                <button class="add-task-btn" onclick="openModal('todo')">+ Add Task</button>
            </div>

            <div class="column" data-status="in-progress" ondrop="drop(event)" ondragover="allowDrop(event)" ondragleave="dragLeave(event)">
                <div class="column-header">
                    <span class="column-title">⚡ In Progress</span>
                    <span class="task-count" id="count-in-progress">0</span>
                </div>
                <div class="tasks" id="tasks-in-progress"></div>
                <button class="add-task-btn" onclick="openModal('in-progress')">+ Add Task</button>
            </div>

            <div class="column" data-status="done" ondrop="drop(event)" ondragover="allowDrop(event)" ondragleave="dragLeave(event)">
                <div class="column-header">
                    <span class="column-title">✅ Done</span>
                    <span class="task-count" id="count-done">0</span>
                </div>
                <div class="tasks" id="tasks-done"></div>
                <button class="add-task-btn" onclick="openModal('done')">+ Add Task</button>
            </div>
        </div>
    </div>

    <div class="modal" id="taskModal">
        <div class="modal-content">
            <div class="modal-header">Create New Task</div>
            <form id="taskForm">
                <div class="form-group">
                    <label>Task Title *</label>
                    <input type="text" id="taskTitle" required>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="taskDescription"></textarea>
                </div>
                <div class="form-group">
                    <label>Priority</label>
                    <select id="taskPriority">
                        <option value="low">Low</option>
                        <option value="medium" selected>Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
                <input type="hidden" id="taskStatus" value="todo">
                <div class="modal-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">Create Task</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        let draggedTask = null;

        async function loadTasks() {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            renderTasks(tasks);
        }

        function renderTasks(tasks) {
            document.getElementById('tasks-todo').innerHTML = '';
            document.getElementById('tasks-in-progress').innerHTML = '';
            document.getElementById('tasks-done').innerHTML = '';

            let counts = {todo: 0, 'in-progress': 0, done: 0};
            
            tasks.forEach(task => {
                const taskEl = createTaskElement(task);
                document.getElementById(`tasks-${task.status}`).appendChild(taskEl);
                counts[task.status]++;
            });

            document.getElementById('count-todo').textContent = counts.todo;
            document.getElementById('count-in-progress').textContent = counts['in-progress'];
            document.getElementById('count-done').textContent = counts.done;

            updateStats(tasks);
        }

        function createTaskElement(task) {
            const div = document.createElement('div');
            div.className = 'task';
            div.draggable = true;
            div.dataset.id = task.id;
            div.ondragstart = drag;
            
            div.innerHTML = `
                <div class="task-title">${escapeHtml(task.title)}</div>
                <div class="task-description">${escapeHtml(task.description)}</div>
                <div class="task-meta">
                    <span class="task-priority priority-${task.priority}">${task.priority.toUpperCase()}</span>
                    <div class="task-actions">
                        <button class="task-btn" onclick="deleteTask(${task.id})" title="Delete">🗑️</button>
                    </div>
                </div>
            `;
            return div;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function updateStats(tasks) {
            const total = tasks.length;
            const completed = tasks.filter(t => t.status === 'done').length;
            const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

            document.getElementById('totalTasks').textContent = total;
            document.getElementById('completedTasks').textContent = completed;
            document.getElementById('completionRate').textContent = rate + '%';
        }

        function openModal(status) {
            document.getElementById('taskStatus').value = status;
            document.getElementById('taskModal').classList.add('active');
        }

        function closeModal() {
            document.getElementById('taskModal').classList.remove('active');
            document.getElementById('taskForm').reset();
        }

        document.getElementById('taskForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const task = {
                title: document.getElementById('taskTitle').value,
                description: document.getElementById('taskDescription').value,
                priority: document.getElementById('taskPriority').value,
                status: document.getElementById('taskStatus').value
            };

            await fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(task)
            });

            closeModal();
            loadTasks();
        });

        async function deleteTask(id) {
            if (confirm('Delete this task?')) {
                await fetch(`/api/tasks/${id}`, {method: 'DELETE'});
                loadTasks();
            }
        }

        function drag(e) {
            draggedTask = e.target;
            e.target.style.opacity = '0.5';
        }

        function allowDrop(e) {
            e.preventDefault();
            e.currentTarget.classList.add('drag-over');
        }

        function dragLeave(e) {
            e.currentTarget.classList.remove('drag-over');
        }

        async function drop(e) {
            e.preventDefault();
            e.currentTarget.classList.remove('drag-over');
            
            if (draggedTask) {
                const newStatus = e.currentTarget.dataset.status;
                const taskId = draggedTask.dataset.id;
                
                await fetch(`/api/tasks/${taskId}/status`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({status: newStatus})
                });
                
                draggedTask.style.opacity = '1';
                draggedTask = null;
                loadTasks();
            }
        }

        window.onclick = (e) => {
            if (e.target.id === 'taskModal') closeModal();
        };

        loadTasks();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.json
    
    task = {
        'id': task_id_counter,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'priority': data.get('priority', 'medium'),
        'status': data.get('status', 'todo'),
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(task)
    task_id_counter += 1
    
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return '', 204

@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    data = request.json
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = data.get('status', task['status'])
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    print("🎯 Kanban Task Manager Starting...")
    print("📍 Open: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)