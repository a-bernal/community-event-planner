from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post, comment
from flask_app.controllers import users
from datetime import datetime

@app.route('/posts/new')
def new_post():
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    return render_template('create_event.html', current_date = datetime.now())

@app.route('/create/post', methods = ['POST'])
def create_new_post():
    if not post.Post.validate_post(request.form):
        return redirect('/posts/new')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date_time'],
        'user_id': session['user_id']
    }
    post.Post.save(data)
    return redirect('/dash')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {'id': post_id}
    return render_template('view_event.html', post = post.Post.get_one(data))

@app.route('/like/<int:post_id>')
def add_like(post_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {'user_id': session['user_id'], 'post_id': post_id}
    post.Post.add_like(data)
    return redirect('/dash')

@app.route('/rsvps/<int:user_id>')
def show_rsvps(user_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    # if 'user_id' != user_id:
    #     flash("Do not have access.")
    #     return redirect('/dash')
    data = {'id': user_id}
    return render_template('your_events.html', user = user.User.get_user_with_rsvps(data))

@app.route('/join/<int:post_id>')
def add_rsvp(post_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {'user_id': session['user_id'], 'post_id': post_id}
    id = session['user_id']
    post.Post.add_rsvp(data)
    return redirect(f'/rsvps/{id}')

@app.route('/leave/<int:post_id>/<dash>')
def leave_rsvp(post_id, dash):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {'user_id': session['user_id'], 'post_id': post_id}
    id = session['user_id']
    post.Post.remove_rsvp(data)
    if dash:
        return redirect(f'/rsvps/{id}')
    else:
        return redirect('/dash')
    
@app.route('/post/edit/<int:posts_id>')
def edit_post(posts_id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':posts_id
    }
    one_post=post.Post.get_one(data)
    user_id={'id':session['user_id']}
    return render_template('edit_event.html', post=one_post, user=user.User.get_one(user_id))

@app.route('/posts/edit/process/<int:post_id>', methods=['POST'])
def process_edit_post(post_id):
    if "user_id" not in session:
        return redirect("/clear")
    if not post.Post.validate_post(request.form):
        return redirect(f'/post/edit/{post_id}')
    
    data = {
        'id': post_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date_time'],
        'created_at': None,  # Replace with actual created_at value
        'updated_at': None   # Replace with actual updated_at value
    }

    # Create an instance of the Post class and pass the data argument
    #post_instance = post.Post(data)

    post.Post.update(data)
    
    return redirect('/dash')


@app.route('/post/delete/<int:post_id>')
def delete_post(post_id):
    if "user_id" not in session:
        return redirect('/clear')
    
    post.Post.destroy({'id': post_id})
    return redirect('/dash')

@app.route('/update/<int:posts_id>',methods=['POST'])
def update(posts_id):
    if not post.Post.validations(request.form):
        return redirect(f"/events/edit/{posts_id}")
    data={
        'event_name': request.form['event_name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date'],
        'id':request.form['id']
        }
    post.Post.update(data)
    return redirect('/dash')
    





