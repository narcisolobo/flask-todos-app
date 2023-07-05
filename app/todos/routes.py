from app.todos import bp as todos
from app.middleware import login_required
from .todo import Todo
from flask import (
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for
)


@todos.get("/")
@login_required
def all_todos():
    todos = Todo.find_all_todos_by_user(session.get("user_id"))
    return render_template("/todos/all_todos.html", todos=todos)


@todos.get("/<int:todo_id>")
@login_required
def one_todo(todo_id):
    todo = Todo.find_one_todo(todo_id)
    if todo is None:
        abort(404)
    return render_template("/todos/one_todo.html", todo=todo)


@todos.route("/new", methods=["GET", "POST"])
@login_required
def new_todo():
    if request.method == "POST":
        if not Todo.todo_is_valid(request.form):
            return redirect(url_for("todos.new_todo"))
        Todo.create_todo(request.form)
        return redirect(url_for("todos.all_todos"))
    return render_template("/todos/new_todo.html")


@todos.route("/<int:todo_id>/edit", methods=["GET", "POST"])
@login_required
def edit_todo(todo_id):
    if request.method == "POST":
        if not Todo.todo_is_valid(request.form):
            return redirect(url_for("todos.edit_todo", todo_id=todo_id))
        Todo.update_one_todo(request.form)
        return redirect(url_for("todos.one_todo", todo_id=todo_id))
    todo = Todo.find_one_todo(todo_id)
    if todo is None:
        abort(404)
    return render_template("/todos/edit_todo.html", todo=todo)


@todos.post("/delete")
@login_required
def delete_todo():
    Todo.delete_one_todo(request.form.get("todo_id"))
    return redirect(url_for("todos.all_todos"))
