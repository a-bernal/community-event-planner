from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import post
import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = "interestnook"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []
        self.comments = []
        self.likes = []
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    @classmethod
    def get_user_with_posts(cls,data):
        query = "SELECT * FROM users LEFT JOIN posts on posts.user_id = users.id WHERE users.id = %(id)s ORDER BY date_time DESC;"
        results = connectToMySQL(db).query_db(query, data)
        user = cls(results[0])
        for row in results:
            post_data = {
                "id": row['posts.id'],
                "event_name": row['event_name'],
                "description": row['description'],
                "location": row['location'],
                "date_time": row['date_time'],
                "created_at": row['posts.created_at'],
                "updated_at": row['posts.updated_at']
            }
            new_post = post.Post(post_data)
            new_post.creator = user
            if(row['posts.id'] != None):
                query2 = f"SELECT COUNT(id) AS likes, post_id FROM likes WHERE post_id = {new_post.id};"
                results2 = connectToMySQL(db).query_db(query2)
                new_post.likes = results2[0]['likes']
            user.posts.append(new_post)
        return user
    @classmethod
    def get_user_with_rsvps(cls,data):
        query = "SELECT * FROM users LEFT JOIN rsvps ON rsvps.user_id = users.id LEFT JOIN posts ON rsvps.post_id = posts.id WHERE users.id = %(id)s ORDER BY date_time DESC;"
        results = connectToMySQL(db).query_db(query,data)
        user = cls(results[0])
        for row in results:
            post_data = {
                "id": row['posts.id'],
                "event_name": row['event_name'],
                "description": row['description'],
                "location": row['location'],
                "date_time": row['date_time'],
                "created_at": row['posts.created_at'],
                "updated_at": row['posts.updated_at']
            }
            new_post = post.Post(post_data)
            if(row['posts.user_id'] != None):
                creator_data = {'id': row['posts.user_id']}
                new_post.creator = cls.get_one(creator_data)
            user.posts.append(new_post)
        return user
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_user(user, users):
        is_valid = True
        for u in users:
            if u.first_name == user['first_name'] and u.last_name == user['last_name']:
                flash("You are already registered", "registration")
                is_valid = False
                break
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", "registration")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "registration")
            is_valid = False
        '''password = user['password']
        password_list = [*password]
        print(password_list)
        has_upper = False
        has_number = False
        for character in password_list:
            if character.isupper() == True:
                has_upper = True
                continue
            if character.isnumeric() == True:
                has_number = True
                continue
        if not has_upper or not has_number:
            flash("Password must have at least one capital letter and one number")
            is_valid = False'''
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long", "registration")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Invalid password", "registration")
            is_valid = False
        for u in users:
            if user['email'] == u.email:
                flash("Email is already taken.  Please use another one", "registration")
                is_valid = False
                break
        return is_valid