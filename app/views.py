from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, abort, flash
from .models import Note, User, Follow
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
from sklearn.neighbors import NearestNeighbors

views = Blueprint('views', __name__)

def get_user_notes(user):
    """Fetch all notes for a given user."""
    return Note.query.filter_by(user_id=user.id).all()
    
def current_user():
    uid = session.get('user_id')
    return User.query.get(uid) if uid else None

# Helper to fetch reviews for a user
def getReviews(user):
    return Note.query.filter_by(user_id=user.id).all()

@views.route('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('views.profile'))
    return redirect(url_for('auth.login'))

@views.route('/landing')
def landing():
    notes = Note.query.order_by(Note.id.desc()).limit(10).all()
    return render_template('landing.html', notes=notes)

@views.route('/profile')
def profile():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    reviews = Note.query.filter_by(user_id=user.id).all()  # Fetch all notes for the user
    review_data = [{
        "id": r.id,
        "Resturaunt": r.Resturaunt,
        "Spiciness": r.Spiciness,
        "Deliciousness": r.Deliciousness,
        "Value": r.Value,
        "Plating": r.Plating,
        "Review": r.Review,
        "image": r.image,
        "likes": r.likes,  # Include the latest likes count
        "location": r.location  # Include the location field
    } for r in reviews]

    return render_template('profile.html', user=user, reviews=review_data)

@views.route('/new_post', methods=['GET', 'POST'])
def new_post():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        note = Note(
            Resturaunt=request.form['Resturaunt'],
            Spiciness=int(request.form['Spiciness']),
            Deliciousness=int(request.form['Deliciousness']),
            Value=int(request.form['Value']),
            Plating=int(request.form['Plating']),
            Review=request.form['Review'],
            image=request.form['image'],
            location=request.form.get('location'),  # Add location
            user_id=user.id
        )

        db.session.add(note)
        db.session.commit()
        return redirect(url_for('views.profile'))

    return render_template('newPost.html')

@views.route('/my_stats')
def my_stats():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    notes = get_user_notes(user)
    total = len(notes) or 1  # Avoid division by zero

    # Calculate individual stats
    stats = {
        'spiciness':     sum(n.Spiciness     for n in notes) / total,
        'deliciousness': sum(n.Deliciousness for n in notes) / total,
        'value':         sum(n.Value         for n in notes) / total,
        'plating':       sum(n.Plating       for n in notes) / total
    }

    # Calculate the average rating for each review and then across all reviews
    average_ratings = [
        (n.Spiciness + n.Deliciousness + n.Value + n.Plating) / 4 for n in notes
    ]
    overall_average_rating = sum(average_ratings) / total

    # Determine earned badges
    badges = [
        {'name': 'First Post', 'earned': len(notes) > 0, 'description': 'Write your first post!'},
        {'name': 'Spice Master', 'earned': stats['spiciness'] > 80, 'description': 'Average spiciness above 80%'},
        {'name': 'Plating Perfectionist', 'earned': stats['plating'] > 90, 'description': 'Average plating above 90%'},
        {'name': 'Value Hunter', 'earned': stats['value'] > 85, 'description': 'Average value above 85%'},
        {'name': 'Food Critic', 'earned': len(notes) > 20, 'description': 'Write more than 20 reviews'},
        {'name': 'All-Rounder', 'earned': all(stat > 75 for stat in stats.values()), 'description': 'All stats above 75%'},
    ]

    return render_template(
        'my_stats.html',
        user=user,
        stats=stats,
        overall_average_rating=overall_average_rating,
        badges=badges
    )

@views.route('/global_stats')
def global_stats():
    return render_template('others_stats.html')

@views.route('/friends', methods=['GET', 'POST'])
def friends():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    # Fetch all users except the current user
    all_users = User.query.filter(User.id != user.id).all()

    # Fetch followed users
    followed_users = [f.followed_id for f in user.following]

    # Fetch posts from followed users
    notes = Note.query.filter(Note.user_id.in_(followed_users)).all()

    # Calculate stats for the current user
    user_notes = get_user_notes(user)
    user_stats = {
        'spiciness': sum(n.Spiciness for n in user_notes) / (len(user_notes) or 1),
        'deliciousness': sum(n.Deliciousness for n in user_notes) / (len(user_notes) or 1),
        'value': sum(n.Value for n in user_notes) / (len(user_notes) or 1),
        'plating': sum(n.Plating for n in user_notes) / (len(user_notes) or 1),
    }

    # Prepare data for KNN
    user_data = []
    user_ids = []
    for u in all_users:
        u_notes = get_user_notes(u)
        if u_notes:
            stats = [
                sum(n.Spiciness for n in u_notes) / len(u_notes),
                sum(n.Deliciousness for n in u_notes) / len(u_notes),
                sum(n.Value for n in u_notes) / len(u_notes),
                sum(n.Plating for n in u_notes) / len(u_notes),
            ]
            user_data.append(stats)
            user_ids.append(u.id)

    # Use KNN to find the most similar user
    if user_data:
        user_data = np.array(user_data)
        current_user_vector = np.array([
            user_stats['spiciness'],
            user_stats['deliciousness'],
            user_stats['value'],
            user_stats['plating'],
        ]).reshape(1, -1)

        knn = NearestNeighbors(n_neighbors=1, metric='euclidean')
        knn.fit(user_data)
        distances, indices = knn.kneighbors(current_user_vector)

        # Get the most similar user
        similar_user_id = user_ids[indices[0][0]]
        similar_user = User.query.get(similar_user_id)
    else:
        similar_user = None

    # Calculate levels for all users
    user_levels = {}
    for u in all_users:
        u_notes = get_user_notes(u)
        total = len(u_notes) or 1
        stats = {
            'spiciness': sum(n.Spiciness for n in u_notes) / total,
            'deliciousness': sum(n.Deliciousness for n in u_notes) / total,
            'value': sum(n.Value for n in u_notes) / total,
            'plating': sum(n.Plating for n in u_notes) / total
        }
        badges = [
            {'name': 'First Post', 'earned': len(u_notes) > 0},
            {'name': 'Spice Master', 'earned': stats['spiciness'] > 80},
            {'name': 'Plating Perfectionist', 'earned': stats['plating'] > 90},
            {'name': 'Value Hunter', 'earned': stats['value'] > 85},
            {'name': 'Food Critic', 'earned': len(u_notes) > 20},
            {'name': 'All-Rounder', 'earned': all(stat > 75 for stat in stats.values())}
        ]
        user_levels[u.id] = sum(1 for badge in badges if badge['earned'])

    return render_template(
        'my_friends.html',
        user=user,
        all_users=all_users,
        followed_users=followed_users,
        notes=notes,
        similar_user=similar_user,
        user_levels=user_levels
    )

@views.route('/like/<int:note_id>', methods=['POST'])
def like(note_id):
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    note = Note.query.get(note_id)
    if not note:
        return jsonify(success=False, error='Note not found'), 404

    # Check if the user has already liked the post
    liked_notes = session.get('liked_notes', [])
    if note_id in liked_notes:
        # Unlike the post
        note.likes = max((note.likes or 0) - 1, 0)  # Ensure likes don't go below 0
        liked_notes.remove(note_id)
    else:
        # Like the post
        note.likes = (note.likes or 0) + 1
        liked_notes.append(note_id)

    # Save the updated likes and session
    session['liked_notes'] = liked_notes
    db.session.commit()

    return jsonify(success=True, likes=note.likes), 200

@views.route('/edit_post/<int:note_id>', methods=['GET','POST'])
def edit_post(note_id):
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    note = Note.query.get_or_404(note_id)
    if note.user_id != user.id:
        abort(403)

    if request.method == 'POST':
        note.restaurant = request.form.get('restaurant')
        note.price      = int(request.form.get('price'))
        note.rating     = int(request.form.get('rating'))
        note.review     = request.form.get('review')
        note.image      = request.form.get('image')
        db.session.commit()
        return redirect(url_for('views.profile'))

    return render_template('editPost.html', note=note)

@views.route('/delete_post/<int:note_id>', methods=['POST'])
def delete_post(note_id):
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    note = Note.query.get_or_404(note_id)
    if note.user_id != user.id:
        abort(403)

    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('views.profile'))

@views.route('/api/reviews')
def api_reviews():
    offset = int(request.args.get('offset', 0))
    notes = Note.query.order_by(Note.id.desc()).offset(offset).limit(10).all()
    return jsonify([
        {'restaurant': n.restaurant, 'review': n.review, 'user': n.user.username}
        for n in notes
    ])

@views.route('/follow/<int:user_id>', methods=['POST'])
def follow(user_id):
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    if user.id == user_id:
        return jsonify(success=False, error="You can't follow yourself"), 400

    followed_user = User.query.get(user_id)
    if not followed_user:
        return jsonify(success=False, error='User not found'), 404

    if Follow.query.filter_by(follower_id=user.id, followed_id=user_id).first():
        return jsonify(success=False, error='Already following'), 400

    follow = Follow(follower_id=user.id, followed_id=user_id)
    db.session.add(follow)
    db.session.commit()
    return jsonify(success=True), 200


@views.route('/unfollow/<int:user_id>', methods=['POST'])
def unfollow(user_id):
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    follow = Follow.query.filter_by(follower_id=user.id, followed_id=user_id).first()
    if not follow:
        return jsonify(success=False, error='Not following'), 400

    db.session.delete(follow)
    db.session.commit()
    return jsonify(success=True), 200

@views.route('/settings', methods=['GET', 'POST'])
def settings():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_info':
            # Update user information
            user.username = request.form.get('username')
            user.email = request.form.get('email')
            db.session.commit()
            return jsonify(success=True, message="User information updated successfully"), 200

        elif action == 'update_password':
            # Update password
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            if not check_password_hash(user.password, current_password):
                return jsonify(success=False, error="Current password is incorrect"), 400
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return jsonify(success=True, message="Password updated successfully"), 200

        elif action == 'delete_account':
            # Delete user account
            db.session.delete(user)
            db.session.commit()
            session.clear()
            return jsonify(success=True, message="Account deleted successfully"), 200

    return render_template('settings.html', user=user)

@views.route('/search', methods=['GET'])
def search():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('views.friends'))

    # Search for users whose username contains the query (case-insensitive)
    search_results = User.query.filter(User.username.ilike(f"%{query}%")).all()

    return render_template('search_results.html', user=user, query=query, search_results=search_results)


@views.route('/user/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    # Fetch the selected user
    selected_user = User.query.get_or_404(user_id)

    # Fetch the selected user's posts
    posts = Note.query.filter_by(user_id=selected_user.id).all()

    # Calculate stats for the selected user
    total_posts = len(posts) or 1  # Avoid division by zero
    stats = {
        'spiciness': sum(n.Spiciness for n in posts) / total_posts,
        'deliciousness': sum(n.Deliciousness for n in posts) / total_posts,
        'value': sum(n.Value for n in posts) / total_posts,
        'plating': sum(n.Plating for n in posts) / total_posts,
    }

    # Calculate the overall average rating
    average_ratings = [
        (n.Spiciness + n.Deliciousness + n.Value + n.Plating) / 4 for n in posts
    ]
    overall_average_rating = sum(average_ratings) / total_posts

    return render_template(
        'user_profile.html',
        user=user,
        selected_user=selected_user,
        stats=stats,
        overall_average_rating=overall_average_rating,
        posts=posts
    )

@views.route('/api/search_suggestions', methods=['GET'])
def search_suggestions():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify(success=False, suggestions=[])

    # Search for users whose usernames contain the query (case-insensitive)
    suggestions = User.query.filter(User.username.ilike(f"%{query}%")).limit(10).all()

    # Return a list of usernames
    return jsonify(success=True, suggestions=[user.username for user in suggestions])

@views.route('/recommend_food', methods=['GET'])
def recommend_food():
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    # Fetch all food items
    food_items = Note.query.all()

    # Prepare the data for KNN
    food_data = []
    food_ids = []
    for food in food_items:
        food_data.append([
            food.Spiciness,
            food.Deliciousness,
            food.Value,
            food.Plating,
            (food.Spiciness + food.Deliciousness + food.Value + food.Plating) / 4  # Overall rating
        ])
        food_ids.append(food.id)

    food_data = np.array(food_data)

    # User's preference vector (example: adjust weights based on user preferences)
    user_preference = np.array([
        request.args.get('spiciness', 50, type=int),
        request.args.get('deliciousness', 50, type=int),
        request.args.get('value', 50, type=int),
        request.args.get('plating', 50, type=int),
        request.args.get('overall', 50, type=int)
    ]).reshape(1, -1)

    # Fit the KNN model
    knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
    knn.fit(food_data)

    # Find the nearest neighbors
    distances, indices = knn.kneighbors(user_preference)

    # Get the recommended food items
    recommendations = []
    for idx in indices[0]:
        food = Note.query.get(food_ids[idx])
        recommendations.append({
            'id': food.id,
            'restaurant': food.Resturaunt,
            'spiciness': food.Spiciness,
            'deliciousness': food.Deliciousness,
            'value': food.Value,
            'plating': food.Plating,
            'overall': (food.Spiciness + food.Deliciousness + food.Value + food.Plating) / 4
        })

    return jsonify(success=True, recommendations=recommendations)

@views.route('/search_users', methods=['GET'])
def search_users():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '').strip()
    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('views.friends'))

    # Search for users by username
    results = User.query.filter(User.username.ilike(f"%{query}%")).all()

    # Calculate levels for search results
    user_levels = {}
    for result in results:
        notes = get_user_notes(result)
        total = len(notes) or 1
        stats = {
            'spiciness': sum(n.Spiciness for n in notes) / total,
            'deliciousness': sum(n.Deliciousness for n in notes) / total,
            'value': sum(n.Value for n in notes) / total,
            'plating': sum(n.Plating for n in notes) / total
        }
        badges = [
            {'name': 'First Post', 'earned': len(notes) > 0},
            {'name': 'Spice Master', 'earned': stats['spiciness'] > 80},
            {'name': 'Plating Perfectionist', 'earned': stats['plating'] > 90},
            {'name': 'Value Hunter', 'earned': stats['value'] > 85},
            {'name': 'Food Critic', 'earned': len(notes) > 20},
            {'name': 'All-Rounder', 'earned': all(stat > 75 for stat in stats.values())}
        ]
        user_levels[result.id] = sum(1 for badge in badges if badge['earned'])

    return render_template(
        'search_results.html',
        user=user,
        query=query,
        results=results,
        user_levels=user_levels
    )

@views.route('/trending_dishes', methods=['GET'])
def trending_dishes():
    # Fetch all dishes sorted by likes in descending order
    dishes = Note.query.order_by(Note.likes.desc()).all()

    # Prepare data for the frontend
    trending_data = [{
        'id': dish.id,
        'restaurant': dish.Resturaunt,
        'review': dish.Review,
        'image': dish.image,
        'likes': dish.likes,
        'spiciness': dish.Spiciness,
        'deliciousness': dish.Deliciousness,
        'value': dish.Value,
        'plating': dish.Plating
    } for dish in dishes]

    return jsonify(success=True, dishes=trending_data)

@views.route('/merged_posts', methods=['GET'])
def merged_posts():
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    # Fetch posts from followed users
    followed_users = [f.followed_id for f in user.following]
    followed_posts = Note.query.filter(Note.user_id.in_(followed_users)).order_by(Note.likes.desc()).all()

    # Fetch the highest liked post from non-followed users
    non_followed_post = Note.query.filter(~Note.user_id.in_(followed_users)).order_by(Note.likes.desc()).all()

    # Prepare data for the frontend
    posts_data = [{
        'id': post.id,
        'restaurant': post.Resturaunt,
        'review': post.Review,
        'image': post.image,
        'likes': post.likes,
        'spiciness': post.Spiciness,
        'deliciousness': post.Deliciousness,
        'value': post.Value,
        'plating': post.Plating,
        'is_special': False  # Default to not special
    } for post in followed_posts]

    # Add the featured post if it exists
    if non_followed_post:
        posts_data.append({
            'id': non_followed_post.id,
            'restaurant': non_followed_post.Resturaunt,
            'review': non_followed_post.Review,
            'image': non_followed_post.image,
            'likes': non_followed_post.likes,
            'spiciness': non_followed_post.Spiciness,
            'deliciousness': non_followed_post.Deliciousness,
            'value': non_followed_post.Value,
            'plating': non_followed_post.Plating,
            'is_special': True  # Mark as special
        })

    return jsonify(success=True, posts=posts_data)

@views.route('/friend_posts', methods=['GET'])
def friend_posts():
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    # Fetch posts from followed friends
    followed_users = [f.followed_id for f in user.following]
    friend_posts = Note.query.filter(Note.user_id.in_(followed_users)).order_by(Note.likes.desc()).all()

    # Prepare data for the frontend
    posts_data = [{
        'id': post.id,
        'restaurant': post.Resturaunt,
        'review': post.Review,
        'image': post.image,
        'likes': post.likes,
        'spiciness': post.Spiciness,
        'deliciousness': post.Deliciousness,
        'value': post.Value,
        'plating': post.Plating
    } for post in friend_posts]

    return jsonify(success=True, posts=posts_data)

@views.route('/api/location_suggestions', methods=['GET'])
def location_suggestions():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify(success=False, suggestions=[])

    # Fetch similar restaurant names and their locations
    suggestions = Note.query.filter(Note.Resturaunt.ilike(f"%{query}%")).with_entities(Note.Resturaunt, Note.location).distinct().all()

    # Return unique restaurant name suggestions with locations
    return jsonify(success=True, suggestions=[{'name': s[0], 'location': s[1]} for s in suggestions if s[0]])

@views.route('/api/search_reviews', methods=['GET'])
def search_reviews():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify(success=False, results=[])

    # Search for posts matching the query in restaurant name, review, or location
    results = Note.query.filter(
        (Note.Resturaunt.ilike(f"%{query}%")) |
        (Note.Review.ilike(f"%{query}%")) |
        (Note.location.ilike(f"%{query}%"))
    ).all()

    # Prepare data for the frontend
    results_data = [{
        'id': post.id,
        'restaurant': post.Resturaunt,
        'review': post.Review,
        'image': post.image,
        'spiciness': post.Spiciness,
        'deliciousness': post.Deliciousness,
        'value': post.Value,
        'plating': post.Plating
    } for post in results]

    return jsonify(success=True, results=results_data)