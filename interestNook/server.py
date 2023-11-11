from flask_app import app
import flask_app
from flask_app.controllers import users, posts, likes, comments

app.register_blueprint(likes.likes_bp)



# app = flask_app(__name__)
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)