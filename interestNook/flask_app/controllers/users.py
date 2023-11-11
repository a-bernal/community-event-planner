from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post
from flask_app.controllers import likes
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def show_login_reg():
    if 'user_id' in session:
        session.clear()
    return render_template("login_page.html")
@app.route('/register/user', methods = ['POST'])
def create_user():
    print(request.form)
    users = user.User.get_all()
    if not user.User.validate_user(request.form, users):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "fname": request.form['first_name'],
        "lname": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = user.User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect("/dash")

@app.route("/dash")
def show_dash():
    if 'user_id' not in session:
        flash("Must login or register.")
        return redirect('/')
    
    data = {
        "id": session['user_id']
    }
    
    # Include the like_data dictionary in the context
    # context = {
    #     'user': user.User.get_user_with_posts(data),
    #     'posts': post.Post.get_all_posts_with_creator(),
    #     'like_data': likes.like_data  # Include the like_data in the context
    # }

    return render_template("dashboard.html", user = user.User.get_user_with_posts(data),  posts = post.Post.get_all_posts_with_creator()  )

@app.route("/login/user", methods = ["POST"])
def check_login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = user.User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    # never render on a post!!!
    return redirect("/dash")
@app.route('/clear')
def clear_session():
    session.clear()
    return redirect('/')
