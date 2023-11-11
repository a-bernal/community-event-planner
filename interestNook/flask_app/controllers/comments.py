from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import comment, post

@app.route("/comment/<int:post_id>/submit", methods = ['POST'])
def submit_comment(post_id):
    if 'user_id' not in session:
        return redirect('/')
    if not comment.Comments.validate_comment(request.form):
        return redirect(f'/comment/{post_id}')
    data = {
        'user_id': session['user_id'],
        'post_id': post_id,
        'content' : request.form['content'],
    }
    comment.Comments.add_comment(data)
    print('MADE IT HERE####################################')
    return redirect('/dash')

@app.route("/comment/delete/<int:comment_id>")
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect('/clear')
    data = {
        'id' : comment_id
    }
    Comments.delete_comment(data)
    return redirect('/dash', comment = Comments.get_comment({'id':comment_id}))
@app.route('/comments/<int:post_id>')
def show_comments(post_id):
    if 'user_id' not in session:
        return redirect('/clear')
    data = {'id': post_id}
    return render_template('comments2.html', post = post.Post.get_one_post_with_comments_and_user(data))
@app.route("/comment/<int:post_id>/delete/<int:comment_id>")
def delete_a_comment(comment_id, post_id):
    comment.Comments.delete_comment({'id': comment_id})
    return redirect(f'/comments/{post_id}')

