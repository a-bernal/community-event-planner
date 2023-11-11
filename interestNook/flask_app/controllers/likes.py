from flask import Blueprint, jsonify

likes_bp = Blueprint('likes', __name__)

# Store initial like counts in the data storage solution
like_data = {
    1: 0,  # Example: Post ID 1 with 5 initial likes
    2: 0,
    3: 0,
    4: 0,
    5: 0,  # Example: Post ID 2 with 3 initial likes
    # Add more initial like counts as needed
}

@likes_bp.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if post_id in like_data:
        like_data[post_id] += 1
    else:
        like_data[post_id] = 1

    # Return the updated like count as JSON response
    return jsonify({'like_count': like_data[post_id]})