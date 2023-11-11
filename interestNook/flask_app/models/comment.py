from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import post, user
from flask import flash

db = "interestnook"

class Comments:
    def __init__(self, data):
        self.id = data['id']

        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    
    @classmethod
    def add_comment(cls, data):
        query = 'INSERT INTO comments (content, user_id, post_id) VALUE (%(content)s, %(user_id)s, %(post_id)s);'
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def delete_comment(cls, data):
        query = 'DELETE FROM comments where id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_comment(cls, data):
        query = 'SELECT * FROM comments WHERE id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_post_and_comments_by_user_id(cls,data):
        query = 'SELECT * FROM users LEFT JOIN posts ON posts.user_id = users.id LEFT JOIN comments ON comments.user_id = users.id WHERE users.id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_comments_by_post_id(cls,data):
        query = 'SELECT * FROM comments JOIN posts ON comments.post_id = posts.id'
        results = connectToMySQL(db).query_db(query, data)
        return results

    @staticmethod
    def validate_comment(form_data):
        is_valid = True

        if len(form_data['content']) < 1:
            flash("Comment must be more than 1 character long")
            is_valid = False
        return is_valid
