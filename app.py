from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage
tasks = []
messages = []

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        task_title = request.form.get("task_title")
        assigned_to = request.form.get("assigned_to")
        priority = request.form.get("priority")
        deadline = request.form.get("deadline")
        
        if task_title:
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "assigned_to": assigned_to,
                "priority": priority,
                "deadline": deadline, # Format: YYYY-MM-DD
                "status": "Pending",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            tasks.append(new_task)
            return redirect(url_for('dashboard'))

    # --- NOTIFICATION SYSTEM LOGIC ---
    alerts = []
    today = datetime.now().date()
    
    for task in tasks:
        if task['status'] != "Completed" and task['deadline']:
            try:
                # Convert string deadline to date object
                task_deadline = datetime.strptime(task['deadline'], '%Y-%m-%d').date()
                
                # Check for Overdue
                if task_deadline < today:
                    alerts.append({
                        "type": "error",
                        "msg": f"OVERDUE: '{task['title']}' was due on {task['deadline']}!"
                    })
                
                # Check for Due Today
                elif task_deadline == today:
                    alerts.append({
                        "type": "urgent",
                        "msg": f"URGENT: '{task['title']}' is due TODAY!"
                    })
                
                # Check for Due Soon (e.g., within 2 days)
                elif task_deadline <= today + timedelta(days=2):
                    days_left = (task_deadline - today).days
                    alerts.append({
                        "type": "warning",
                        "msg": f"REMINDER: '{task['title']}' is due in {days_left} days."
                    })
            except ValueError:
                pass # Handle potential date format errors gracefully

    return render_template("dashboard.html", tasks=tasks, alerts=alerts)


@app.route('/talk', methods=["GET", "POST"])
def talk():
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

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = "Completed"
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
