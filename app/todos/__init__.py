from .todo import Todo
from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)

bp = Blueprint("todos", __name__, url_prefix="/todos")


@bp.get("/")
def all_todos():
    if "user_id" not in session:
        flash("Please log in.", "auth")
        return redirect(url_for("auth.login"))
    todos = Todo.find_all_todos_by_user(session.get("user_id"))
    return render_template("/todos/all_todos.html", todos=todos)


@bp.get("/<int:todo_id>")
def one_todo(todo_id):
    if "user_id" not in session:
        flash("Please log in.", "auth")
        return redirect(url_for("auth.login"))
    todo = Todo.find_one_todo(todo_id)
    if todo is None:
        abort(404)
    return render_template("/todos/one_todo.html", todo=todo)


@bp.route("/new", methods=["GET", "POST"])
def new_todo():
    if "user_id" not in session:
        flash("Please log in.", "auth")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if not Todo.todo_is_valid(request.form):
            return redirect(url_for("todos.new_todo"))
        Todo.create_todo(request.form)
        return redirect(url_for("todos.all_todos"))
    return render_template("/todos/new_todo.html")


@bp.route("/<int:todo_id>/edit", methods=["GET", "POST"])
def edit_todo(todo_id):
    if "user_id" not in session:
        flash("Please log in.", "auth")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if not Todo.todo_is_valid(request.form):
            return redirect(url_for("todos.edit_todo", todo_id=todo_id))
        Todo.update_one_todo(request.form)
        return redirect(url_for("todos.one_todo", todo_id=todo_id))
    todo = Todo.find_one_todo(todo_id)
    if todo is None:
        abort(404)
    return render_template("/todos/edit_todo.html", todo=todo)


@bp.post("/delete")
def delete_todo():
    if "user_id" not in session:
        flash("Please log in.", "auth")
        return redirect(url_for("auth.login"))
    Todo.delete_one_todo(request.form.get("todo_id"))
    return redirect(url_for("todos.all_todos"))


@bp.errorhandler(404)
def not_found(e):
    print(e)
    return render_template("404.html", e=e), 404
