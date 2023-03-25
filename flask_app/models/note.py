from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = "note_app"


class Note:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.note_content = db_data['note_content']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.modify_at = db_data['modify_at']

    @classmethod
    def save_note(cls, form_data):
        query = "INSERT INTO notes (title, note_content, user_id) VALUES (%(title)s, %(note_content)s, %(user_id)s);"

        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def delete_note(cls, data):
        query = "DELETE FROM notes WHERE id = %(id)s;"

        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_note(cls, data):
        query = "UPDATE notes SET title = %(title)s, note_content = %(note_content)s WHERE id = %(id)s;"

        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM notes JOIN users ON notes.user_id = users.id WHERE notes.id = %(id)s;"

        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False

        result = result[0]
        this_note = cls(result)
        return this_note

    @classmethod
    def notes_by_user(cls, data):
        query = "SELECT * FROM notes LEFT JOIN users ON users.id = notes.user_id WHERE users.id = %(id)s;"

        results = connectToMySQL(db).query_db(query, data)

        my_notes = []
        for i in results:
            this_note = cls(i)

            my_notes.append(this_note)

        return my_notes

    @staticmethod
    def validate_note(form_data):
        is_valid = True

        if len(form_data['note_content']) < 1:
            flash("Note content cannot be empty", "create_note")
            is_valid = False

        return is_valid
