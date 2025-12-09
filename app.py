from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage for prototype purposes
# In a real production app, you would use a database like SQLite or PostgreSQL
tasks = []
messages = []

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        # Feature: Create, assign, and track tasks [cite: 16]
        task_title = request.form.get("task_title")
        assigned_to = request.form.get("assigned_to")
        priority = request.form.get("priority") # Feature: Priority tasks (low, medium, high) [cite: 41]
        deadline = request.form.get("deadline") # Feature: Deadlines [cite: 17]
        
        # Simple validation
        if task_title:
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "assigned_to": assigned_to,
                "priority": priority,
                "deadline": deadline,
                "status": "Pending",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            tasks.append(new_task)
            return redirect(url_for('dashboard'))

    # Feature: Visual dashboards [cite: 27]
    return render_template("dashboard.html", tasks=tasks)


@app.route('/talk', methods=["GET", "POST"])
def talk():
    # Feature: Communicate within members / Real-time chat [cite: 18, 21]
    if request.method == "POST":
        user = request.form.get("username")
        content = request.form.get("message")
        
        if user and content:
            new_message = {
                "user": user,
                "content": content,
                "timestamp": datetime.now().strftime("%H:%M")
            }
            messages.append(new_message)
            return redirect(url_for('talk'))

    return render_template('talk.html', messages=messages)

# Feature: Update task status (Simulated logic for "Done")
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = "Completed"
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
