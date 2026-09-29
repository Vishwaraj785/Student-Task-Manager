import os

from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

tasks = []

VALID_PRIORITIES = {"Low", "Medium", "High"}


@app.route("/")
def home():
    return render_template(
        "index.html",
        tasks=tasks,
        commit=os.getenv("RENDER_GIT_COMMIT", "local")
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    subject = request.form.get("subject", "").strip()
    priority = request.form.get("priority", "").strip()
    due_date = request.form.get("due_date", "").strip()

    if not title or not subject or not due_date:
        return "Title, subject and due date are required.", 400

    if priority not in VALID_PRIORITIES:
        return "Invalid priority value.", 400

    task = {
        "title": title,
        "description": description,
        "subject": subject,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)

    return redirect(url_for("home"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        return redirect(url_for("home"))

    return "Task not found.", 404

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        return redirect(url_for("home"))

    return "Task not found.", 404


@app.route("/api/tasks")
def api_tasks():
    return jsonify(tasks)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )