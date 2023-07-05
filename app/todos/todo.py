from __future__ import annotations
from flask import flash
from datetime import datetime
from app.config.mysql_connection import connectToMySQL


class Todo:
    _db = "flaskTodosDb"

    def __init__(self, data: dict[str, str | datetime]) -> None:
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.title = data["title"]
        self.description = data["description"]
        self.is_complete = data["is_complete"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    def __repr__(self) -> str:
        f"<Todo {self.title}>"

    @staticmethod
    def todo_is_valid(form_data: dict[str, str]) -> bool:
        is_valid = True
        if len(form_data["title"].strip()) < 2:
            flash("Todo must be at least two characters.", "title")
            is_valid = False
        if len(form_data["description"].strip()) < 3:
            flash("Description must be at least three characters.", "description")
            is_valid = False
        return is_valid

    @classmethod
    def create_todo(cls, form_data: dict[str, str]) -> int:
        query = "INSERT INTO todos (user_id, title, description) VALUES (%(user_id)s, %(title)s, %(description)s);"
        return connectToMySQL(Todo._db).query_db(query, form_data)

    @classmethod
    def find_all_todos_by_user(cls, user_id: int) -> list[Todo]:
        query = "SELECT * from todos WHERE user_id = %(user_id)s;"
        data = {
            "user_id": user_id
        }
        results = connectToMySQL(Todo._db).query_db(query, data)
        todos = []
        for result in results:
            todos.append(Todo(result))
        return todos

    @classmethod
    def find_one_todo(cls, todo_id: int) -> list[Todo]:
        query = "SELECT * from todos WHERE id = %(todo_id)s;"
        data = {
            "todo_id": todo_id
        }
        results = connectToMySQL(Todo._db).query_db(query, data)
        if len(results) > 0:
            return Todo(results[0])
        return None

    @classmethod
    def update_one_todo(cls, form_data: dict[str, str]) -> None:
        query = "UPDATE todos SET title = %(title)s, description = %(description)s, is_complete = %(is_complete)s WHERE id = %(todo_id)s;"
        return connectToMySQL(Todo._db).query_db(query, form_data)

    @classmethod
    def delete_one_todo(cls, todo_id: int) -> None:
        query = "DELETE from todos WHERE id = %(todo_id)s;"
        data = {
            "todo_id": todo_id
        }
        return connectToMySQL(Todo._db).query_db(query, data)
