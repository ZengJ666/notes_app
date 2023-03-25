from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = "note_app"


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls, form_data):
        user_data = {
            "first_name": form_data['first_name'],
            "last_name": form_data['last_name'],
            "email": form_data['email'],
            "password": bcrypt.generate_password_hash(form_data['password'])
        }

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        result = connectToMySQL(db).query_db(query, user_data)

        return result

    @staticmethod
    def validate_user_registration(form_data):
        is_valid = True

        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid Email Address", "register")
            is_valid = False
        elif len(form_data) < 1:
            flash("Email cannot be blank", "register")
            is_valid = False
        elif User.get_by_email(form_data):
            flash("A User already exist with this email", "register")
            is_valid = False
        if len(form_data['first_name']) < 1:
            flash("First Name can not be blank", "register")
            is_valid = False
        if len(form_data['last_name']) < 1:
            flash("Last Name can not be blank", "register")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if form_data['confirm_password'] != form_data['password']:
            flash("Password must match", "register")
            is_valid = False

        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL(db).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        result = connectToMySQL(db).query_db(query, data)

        return cls(result[0])
