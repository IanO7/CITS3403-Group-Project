from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, session, jsonify, abort, flash, current_app, 
    send_from_directory )

from .models import Note, User, Follow, Comments, SharedPost
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
import re
from collections import Counter, defaultdict
import math
from difflib import get_close_matches


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



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

def get_user_level(badges):
    earned = sum(1 for b in badges if b['earned'])
    if earned >= 6:
        return 5
    elif earned >= 4:
        return 4
    elif earned >= 2:
        return 3
    elif earned >= 1:
        return 2
    else:
        return 1

@views.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@views.route('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('views.profile'))
    return redirect(url_for('views.landing'))

@views.route('/landing')
def landing():
    notes = Note.query.order_by(Note.id.desc()).limit(10).all()
    total_posts = Note.query.count()
    total_users = User.query.count()
    trending_dishes = Note.query.order_by(Note.likes.desc()).limit(5).all()
    return render_template('landing.html', notes=notes, total_posts=total_posts, total_users=total_users, trending_dishes=trending_dishes)


@views.route('/profile', methods=['GET', 'POST'])
def profile():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login')) 

    if request.method == 'POST':
        comment = Comments(
                Comment = request.form['Comment'], 
                user_id = request.form['user_id'],
                note_id = request.form['note_id'], 
                parentID = request.form['parentID']
            )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('views.profile', user_id=user.id))
    
    reviews = Note.query.filter_by(user_id=user.id).all()
    
    comments_by_review = {
        review.id: [comment.to_dict() for comment in review.comments]
        for review in reviews 
    }

    # Calculate badges and level
    total = len(reviews) or 1
    stats = {
        'spiciness':     sum(n.Spiciness     for n in reviews) / total,
        'deliciousness': sum(n.Deliciousness for n in reviews) / total,
        'value':         sum(n.Value         for n in reviews) / total,
        'service':       sum(n.Service       for n in reviews) / total
    }

    # Use the same badge logic as my_stats
    min_reviews_spice = 5
    min_reviews_service = 5
    min_reviews_value = 5
    min_reviews_critic = 20
    min_reviews_allrounder = 10

    badges = [
        {
            'name': 'First Post',
            'earned': len(reviews) > 0,
        },
        {
            'name': 'Spice Master',
            'earned': len(reviews) >= min_reviews_spice and stats['spiciness'] > 80,
        },
        {
            'name': 'Service Perfectionist',
            'earned': len(reviews) >= min_reviews_service and stats['service'] > 90,
        },
        {
            'name': 'Value Hunter',
            'earned': len(reviews) >= min_reviews_value and stats['value'] > 85,
        },
        {
            'name': 'Food Critic',
            'earned': len(reviews) >= min_reviews_critic,
        },
        {
            'name': 'All-Rounder',
            'earned': (
                len(reviews) >= min_reviews_allrounder and
                all(stat > 75 for stat in stats.values())
            ),
        },
    ]
    level = get_user_level(badges)

    return render_template('profile.html', user=user, reviews=reviews, level=level, comments_by_review=comments_by_review)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/new_post', methods=['GET', 'POST'])
def new_post():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        image_file = request.files.get('image')
        image_path = None

        if image_file:
            filename = secure_filename(os.path.basename(image_file.filename))
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            image_filename = filename

       
        note = Note(
            Resturaunt=request.form['Resturaunt'],
            Cuisine=request.form['Cuisine'],
            Spiciness=int(request.form['Spiciness']),
            Deliciousness=int(request.form['Deliciousness']),
            Value=int(request.form['Value']),
            Stars=int(request.form['Stars']),
            Service=int(request.form['Service']),
            Review=request.form['Review'],

            image=image_filename, 

            location=request.form.get('location'),
            latitude  = float(request.form.get('latitude') or 0),
            longitude = float(request.form.get('longitude') or 0),
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
        'service':       sum(n.Service       for n in notes) / total
    }

    # Calculate the average rating for each review and then across all reviews
    average_ratings = [
        (n.Spiciness + n.Deliciousness + n.Value + n.Service) / 4 for n in notes
    ]
    overall_average_rating = sum(average_ratings) / total

    # Favorite cuisine calculation
    cuisine_list = [n.Cuisine for n in notes if n.Cuisine]
    favorite_cuisine = None
    if cuisine_list:
        favorite_cuisine = Counter(cuisine_list).most_common(1)[0][0]

    # Determine earned badges (progressive, robust)
    min_reviews_spice = 5
    min_reviews_service = 5
    min_reviews_value = 5
    min_reviews_critic = 20
    min_reviews_allrounder = 10

    badges = [
        {
            'name': '👨‍🍳 First Post',
            'earned': len(notes) > 0,
            'description': 'Write your first post!'
        },
        {
            'name': '🌶️ Spice Master',
            'earned': len(notes) >= min_reviews_spice and stats['spiciness'] > 80,
            'description': f'Average spiciness above 80% (at least {min_reviews_spice} reviews)'
        },
        {
            'name': '🍽️ Service Perfectionist',
            'earned': len(notes) >= min_reviews_service and stats['service'] > 90,
            'description': f'Average service above 90% (at least {min_reviews_service} reviews)'
        },
        {
            'name': '💰 Value Hunter',
            'earned': len(notes) >= min_reviews_value and stats['value'] > 85,
            'description': f'Average value above 85% (at least {min_reviews_value} reviews)'
        },
        {
            'name': '🧑‍🎨 Food Critic',
            'earned': len(notes) >= min_reviews_critic,
            'description': f'Write at least {min_reviews_critic} reviews'
        },
        {
            'name': '👨‍🍳 All-Rounder',
            'earned': (
                len(notes) >= min_reviews_allrounder and
                all(stat > 75 for stat in stats.values())
            ),
            'description': f'All stats above 75% (at least {min_reviews_allrounder} reviews)'
        },
    ]

    user_level = get_user_level(badges)

    return render_template(
        'my_stats.html',
        user=user,
        stats=stats,
        overall_average_rating=overall_average_rating,
        badges=badges,
        favorite_cuisine=favorite_cuisine,  # Pass to template
        user_level=user_level
    )

@views.route('/global_stats')
def global_stats():
    return render_template('others_stats.html')

@views.route('/friends', methods=['GET', 'POST'])
def friends():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    # Only approved friends
    approved_friends = [f.followed_id for f in user.following if f.status == 'approved']
    notes = Note.query.filter(Note.user_id.in_(approved_friends)).all()

    # Calculate stats for the current user
    user_notes = get_user_notes(user)
    user_stats = {
        'spiciness': sum(n.Spiciness for n in user_notes) / (len(user_notes) or 1),
        'deliciousness': sum(n.Deliciousness for n in user_notes) / (len(user_notes) or 1),
        'value': sum(n.Value for n in user_notes) / (len(user_notes) or 1),
        'service': sum(n.Service for n in user_notes) / (len(user_notes) or 1),
    }

    # Prepare data for KNN
    user_data = []
    user_ids = []

    for u in User.query.filter(User.id != user.id).all():
        u_notes = get_user_notes(u)
        if u_notes:
            stats = [
                sum(n.Spiciness for n in u_notes) / len(u_notes),
                sum(n.Deliciousness for n in u_notes) / len(u_notes),
                sum(n.Value for n in u_notes) / len(u_notes),
                sum(n.Service for n in u_notes) / len(u_notes),
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
            user_stats['service'],
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
    for u in User.query.filter(User.id != user.id).all():
        u_notes = get_user_notes(u)
        total = len(u_notes) or 1
        stats = {
            'spiciness': sum(n.Spiciness for n in u_notes) / total,
            'deliciousness': sum(n.Deliciousness for n in u_notes) / total,
            'value': sum(n.Value for n in u_notes) / total,
            'service': sum(n.Service for n in u_notes) / total
        }
        badges = [
            {'name': 'First Post', 'earned': len(u_notes) > 0},
            {'name': 'Spice Master', 'earned': stats['spiciness'] > 80},
            {'name': 'Service Perfectionist', 'earned': stats['service'] > 90},
            {'name': 'Value Hunter', 'earned': stats['value'] > 85},
            {'name': 'Food Critic', 'earned': len(u_notes) > 20},
            {'name': 'All-Rounder', 'earned': all(stat > 75 for stat in stats.values())}
        ]
        user_levels[u.id] = sum(1 for badge in badges if badge['earned'])
    
    if request.method == 'POST':
        comment = Comments(
                Comment = request.form['Comment'], 
                user_id = request.form['user_id'],
                note_id = request.form['note_id'], 
                parentID = request.form['parentID'], 
            )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('views.friends', user_id=user.id))

    comments_by_review = {
        review.id: [comment.to_dict() for comment in review.comments]
        for review in notes 
    }

    return render_template(
        'my_friends.html',
        user=user,
        all_users=User.query.filter(User.id != user.id).all(),
        followed_users=approved_friends,
        notes=notes,
        similar_user=similar_user,
        user_levels=user_levels,
        user_stats=user_stats,      # <-- add this
        user_notes=user_notes,      # <-- add this
        comments_by_review=comments_by_review
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
    if not user or user.id == user_id:
        return jsonify(success=False, error="Invalid request"), 400

    followed_user = User.query.get(user_id)
    if not followed_user:
        return jsonify(success=False, error='User not found'), 404

    existing = Follow.query.filter_by(follower_id=user.id, followed_id=user_id).first()
    if existing:
        return jsonify(success=False, error='Request already sent'), 400

    follow = Follow(follower_id=user.id, followed_id=user_id, status='pending')
    db.session.add(follow)
    db.session.commit()
    return jsonify(success=True, message="Follow request sent."), 200

@views.route('/approve_follow/<int:follow_id>', methods=['POST'])
def approve_follow(follow_id):
    user = current_user()
    follow = Follow.query.get_or_404(follow_id)
    if follow.followed_id != user.id:
        return jsonify(success=False, error="Not authorized"), 403
    follow.status = 'approved'
    db.session.commit()
    return jsonify(success=True, message="Follow request approved.")

@views.route('/reject_follow/<int:follow_id>', methods=['POST'])
def reject_follow(follow_id):
    user = current_user()
    follow = Follow.query.get_or_404(follow_id)
    if follow.followed_id != user.id:
        return jsonify(success=False, error="Not authorized"), 403
    db.session.delete(follow)
    db.session.commit()
    return jsonify(success=True, message="Follow request rejected.")

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
@views.route("/settings", methods=["GET", "POST"])
def settings():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        action = request.form.get("action", "").strip()

        # Handle profile image upload for relevant actions
        image_file = request.files.get('profileImage')
        image_filename = None
        if image_file:
            filename = secure_filename(os.path.basename(image_file.filename))
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            image_filename = filename

        # ──────────────── INDIVIDUAL FIELD UPDATES ────────────────
        if action == "update_username":
            new_username = request.form.get("username", "").strip()
            username_ok = 3 <= len(new_username) <= 30 and re.match(r"^[A-Za-z0-9_.-]+$", new_username)
            if not username_ok:
                return jsonify(success=False, error="Username must be 3-30 chars and contain only letters, digits, underscores, dots or dashes."), 400
            if new_username != user.username and User.query.filter_by(username=new_username).first():
                return jsonify(success=False, error="That username is already taken."), 409
            user.username = new_username
            db.session.commit()
            return jsonify(success=True, message="Username updated successfully."), 200

        elif action == "update_email":
            new_email = request.form.get("email", "").strip().lower()
            email_ok = re.match(r"^[^@]+@[^@]+\.[^@]+$", new_email)
            if not email_ok:
                return jsonify(success=False, error="Please enter a valid e-mail address."), 400
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify(success=False, error="That e-mail is already registered."), 409
            user.email = new_email
            db.session.commit()
            return jsonify(success=True, message="Email updated successfully."), 200

        elif action == "update_profile":
            if not image_filename:
                return jsonify(success=False, error="No image uploaded."), 400
            user.profileImage = image_filename
            db.session.commit()
            return jsonify(success=True, message="Profile picture updated."), 200

        # ──────────────── EXISTING ACTIONS ────────────────
        elif action == "update_password":
            current_pw = request.form.get("current_password", "")
            new_pw     = request.form.get("new_password", "")
            if not check_password_hash(user.password, current_pw):
                return jsonify(success=False, error="Current password is incorrect."), 401
            if len(new_pw) < 8 or len(new_pw) > 128:
                return jsonify(success=False, error="Password must be between 8 and 128 characters long."), 400
            if new_pw.isalpha() or new_pw.isdigit():
                return jsonify(success=False, error="Password must include at least one letter and one number/symbol."), 400
            user.password = generate_password_hash(new_pw)
            db.session.commit()
            return jsonify(success=True, message="Password changed."), 200

        elif action == "delete_account":
            db.session.delete(user)
            db.session.commit()
            session.clear()
            return jsonify(success=True, message="Account deleted. Goodbye!"), 200

        # ──────────────── UNKNOWN ACTION ────────────────
        return jsonify(success=False, error="Unknown action."), 400

    # GET → render page
    return render_template("settings.html", user=user)



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


@views.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    selected_user = User.query.get_or_404(user_id)
    posts = Note.query.filter_by(user_id=selected_user.id).all()
    total_posts = len(posts) or 1
    stats = {
        'spiciness': sum(n.Spiciness for n in posts) / total_posts,
        'deliciousness': sum(n.Deliciousness for n in posts) / total_posts,
        'value': sum(n.Value for n in posts) / total_posts,
        'service': sum(n.Service for n in posts) / total_posts,
    }
    average_ratings = [
        (n.Spiciness + n.Deliciousness + n.Value + n.Service) / 4 for n in posts
    ]
    overall_average_rating = sum(average_ratings) / total_posts

    # Add follow status objects
    follow = Follow.query.filter_by(follower_id=user.id, followed_id=selected_user.id).first()
    incoming = Follow.query.filter_by(follower_id=selected_user.id, followed_id=user.id, status='pending').first()

    # Calculate user level
    badges = [
        {'name': 'First Post', 'earned': len(posts) > 0},
        {'name': 'Spice Master', 'earned': stats['spiciness'] > 80},
        {'name': 'Service Perfectionist', 'earned': stats['service'] > 90},
        {'name': 'Value Hunter', 'earned': stats['value'] > 85},
        {'name': 'Food Critic', 'earned': len(posts) > 20},
        {'name': 'All-Rounder', 'earned': all(stat > 75 for stat in stats.values())}
    ]
    user_level = sum(1 for badge in badges if badge['earned'])

    if request.method == 'POST':
        comment = Comments(
                Comment = request.form['Comment'], 
                user_id = request.form['user_id'],
                note_id = request.form['note_id'], 
                parentID = request.form['parentID']
            )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('views.user_profile', user_id=user_id))

    comments_by_review = {
        review.id: [comment.to_dict() for comment in review.comments]
        for review in posts  # or whatever your review list is called
    }

    return render_template(
        'user_profile.html',
        user=user,
        selected_user=selected_user,
        stats=stats,
        overall_average_rating=overall_average_rating,
        posts=posts,
        follow=follow,
        incoming=incoming,
        user_level=user_level,
        comments_by_review=comments_by_review
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

    # Fetch all food items; ENSURE THAT OWN USER'S POSTS ARE NOT RECOMMENDED TO THEMSELVES!
    food_items = Note.query.all().filter(Note.user_id != user.id).all()

    # Gather all unique cuisines and locations for one-hot encoding
    all_cuisines = sorted({food.Cuisine for food in food_items if food.Cuisine})
    all_locations = sorted({food.location for food in food_items if food.location})

    def one_hot(value, all_values):
        return [1 if value == v else 0 for v in all_values]

    # Prepare the data for KNN
    food_data = []
    food_ids = []
    for food in food_items:
        vector = [
            food.Spiciness,
            food.Deliciousness,
            food.Value,
            food.Service,
            (food.Spiciness + food.Deliciousness + food.Value + food.Service) / 4,
            getattr(food, 'Stars', 5)  # Default to 5 if missing
        ]
        vector += one_hot(food.Cuisine, all_cuisines)
        vector += one_hot(food.location, all_locations)
        food_data.append(vector)
        food_ids.append(food.id)

    food_data = np.array(food_data)

    # User's preference vector (from query params)
    user_cuisine = request.args.get('cuisine', '')
    user_location = request.args.get('location', '')

    user_preference = [
        request.args.get('spiciness', 50, type=int),
        request.args.get('deliciousness', 50, type=int),
        request.args.get('value', 50, type=int),
        request.args.get('service', 50, type=int),
        request.args.get('overall', 50, type=int),
        request.args.get('stars', 5, type=int)
    ]
    user_preference += one_hot(user_cuisine, all_cuisines)
    user_preference += one_hot(user_location, all_locations)
    user_preference = np.array(user_preference).reshape(1, -1)

    # Fit the KNN model
    n_neighbors = min(5, len(food_data)) if len(food_data) > 0 else 1
    if n_neighbors == 0:
        return jsonify(success=False, recommendations=[])

    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
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
            'cuisine': food.Cuisine,
            'location': food.location,
            'spiciness': food.Spiciness,
            'deliciousness': food.Deliciousness,
            'value': food.Value,
            'service': food.Service,
            'stars': getattr(food, 'Stars', 5),
            'overall': (food.Spiciness + food.Deliciousness + food.Value + food.Service) / 4,
            'image': food.image  # <-- Add this line
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
            'service': sum(n.Service for n in notes) / total
        }
        badges = [
            {'name': 'First Post', 'earned': len(notes) > 0},
            {'name': 'Spice Master', 'earned': stats['spiciness'] > 80},
            {'name': 'Service Perfectionist', 'earned': stats['service'] > 90},
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
        'service': dish.Service
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
        'service': post.Service,
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
            'service': non_followed_post.Service,
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
        'service': post.Service
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
    user = current_user()
    query = request.args.get('q', '').strip().lower()
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)

    ATTR_SYNONYMS = {
        'spiciness': ['spicy', 'heat', 'hot', 'smpicy', 'spiciness'],
        'deliciousness': ['delicious', 'tasty', 'yummy', 'delish', 'deliciousness'],
        'value': ['cheap', 'affordable', 'value for money', 'cheep', 'value'],
        'service': ['service', 'staff', 'waiter'],
        'stars': ['rating', 'stars', 'starred', 'star'],
        'location': ['near me', 'around here', 'nearby', 'close by', 'close to me'],
    }
    COMMON_CUISINES = [
        'indian', 'korean', 'japanese', 'ramen', 'pizza', 'italian', 'thai', 'chinese', 'mexican', 'burger', 'curry', 'sushi', 'noodle', 'bbq', 'seafood', 'french', 'greek'
    ]
    MODIFIERS = {
        'high': ['high', 'very', 'super', 'extreme', 'max', 'maximum', 'most'],
        'low': ['low', 'little', 'not', 'no', 'none', 'minimal', 'least', 'zero'],
    }

    import re
    tokens = re.findall(r'\w+', query)
    matched_attrs = set()
    attr_thresholds = {}
    attr_ranges = {}
    cuisine_match = None
    location_trigger = False

    def fuzzy_match(token, group):
        matches = get_close_matches(token, group, n=1, cutoff=0.7)
        return matches[0] if matches else None

    def extract_number(text):
        nums = re.findall(r'\d+', text)
        return int(nums[0]) if nums else None

    # Detect modifiers for each attribute
    for attr, synonyms in ATTR_SYNONYMS.items():
        for mod_type, mod_words in MODIFIERS.items():
            for mod in mod_words:
                for syn in synonyms:
                    # e.g. "high spicy", "very spicy", "no stars"
                    if f"{mod} {syn}" in query or f"{syn} {mod}" in query:
                        matched_attrs.add(attr)
                        if attr == 'stars':
                            if mod_type == 'low':
                                attr_ranges[attr] = ('<=', 1)
                            elif mod_type == 'high':
                                attr_ranges[attr] = ('>=', 4)
                        else:
                            if mod_type == 'low':
                                attr_ranges[attr] = ('<=', 40)
                            elif mod_type == 'high':
                                attr_ranges[attr] = ('>=', 80)
    # Detect "not" or "no" as negative for attributes
    for attr, synonyms in ATTR_SYNONYMS.items():
        for syn in synonyms:
            if f"not {syn}" in query or f"no {syn}" in query:
                matched_attrs.add(attr)
                if attr == 'stars':
                    attr_ranges[attr] = ('<=', 1)
                else:
                    attr_ranges[attr] = ('<=', 20)

    # Fuzzy match tokens to attributes and cuisines, and extract numbers
    for token in tokens:
        for attr, synonyms in ATTR_SYNONYMS.items():
            match = fuzzy_match(token, synonyms)
            if match:
                matched_attrs.add(attr)
                num = extract_number(query)
                if num is not None:
                    attr_thresholds[attr] = num
        cuisine = fuzzy_match(token, COMMON_CUISINES)
        if cuisine:
            cuisine_match = cuisine

    # Fuzzy match for location trigger (multi-word)
    for loc_kw in ATTR_SYNONYMS['location']:
        if get_close_matches(loc_kw, [query], n=1, cutoff=0.7):
            location_trigger = True
            break

    # Proximity search
    if location_trigger and lat is not None and lng is not None:
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371
            phi1, phi2 = math.radians(lat1), math.radians(lat2)
            dphi = math.radians(lat2 - lat1)
            dlambda = math.radians(lon2 - lon1)
            a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
            return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        notes = Note.query.filter(
            Note.latitude.isnot(None),
            Note.longitude.isnot(None),
            Note.latitude != 0,
            Note.longitude != 0
        ).all()
        results = []
        for n in notes:
            distance = haversine(lat, lng, n.latitude, n.longitude)
            if distance <= 5:
                results.append(n)
    else:
        notes_query = Note.query
        # Apply attribute filters with modifiers and thresholds
        if 'spiciness' in matched_attrs:
            if 'spiciness' in attr_ranges:
                op, val = attr_ranges['spiciness']
                if op == '>=':
                    notes_query = notes_query.filter(Note.Spiciness >= val)
                else:
                    notes_query = notes_query.filter(Note.Spiciness <= val)
            else:
                val = attr_thresholds.get('spiciness', 80)
                notes_query = notes_query.filter(Note.Spiciness >= val)
        if 'deliciousness' in matched_attrs:
            if 'deliciousness' in attr_ranges:
                op, val = attr_ranges['deliciousness']
                if op == '>=':
                    notes_query = notes_query.filter(Note.Deliciousness >= val)
                else:
                    notes_query = notes_query.filter(Note.Deliciousness <= val)
            else:
                val = attr_thresholds.get('deliciousness', 80)
                notes_query = notes_query.filter(Note.Deliciousness >= val)
        if 'value' in matched_attrs:
            if 'value' in attr_ranges:
                op, val = attr_ranges['value']
                if op == '>=':
                    notes_query = notes_query.filter(Note.Value >= val)
                else:
                    notes_query = notes_query.filter(Note.Value <= val)
            else:
                val = attr_thresholds.get('value', 80)
                notes_query = notes_query.filter(Note.Value >= val)
        if 'service' in matched_attrs:
            if 'service' in attr_ranges:
                op, val = attr_ranges['service']
                if op == '>=':
                    notes_query = notes_query.filter(Note.Service >= val)
                else:
                    notes_query = notes_query.filter(Note.Service <= val)
            else:
                val = attr_thresholds.get('service', 80)
                notes_query = notes_query.filter(Note.Service >= val)
        if 'stars' in matched_attrs:
            if 'stars' in attr_ranges:
                op, val = attr_ranges['stars']
                if op == '>=':
                    notes_query = notes_query.filter(Note.Stars >= val)
                else:
                    notes_query = notes_query.filter(Note.Stars <= val)
            else:
                val = attr_thresholds.get('stars', 4)
                notes_query = notes_query.filter(Note.Stars >= val)
        if cuisine_match:
            notes_query = notes_query.filter(Note.Cuisine.ilike(f"%{cuisine_match}%"))
        if not matched_attrs and not cuisine_match:
            notes_query = notes_query.filter(
                (Note.Resturaunt.ilike(f"%{query}%")) | (Note.Review.ilike(f"%{query}%"))
            )
        results = notes_query.all()

    if user:
        results = [n for n in results if n.user_id != user.id]

    results_data = [{
        'id': n.id,
        'restaurant': n.Resturaunt,
        'review': n.Review,
        'image': n.image,
        'spiciness': n.Spiciness,
        'deliciousness': n.Deliciousness,
        'value': n.Value,
        'service': n.Service,
        'cuisine': n.Cuisine,
        'location': n.location,
        'stars': getattr(n, 'Stars', 5)
    } for n in results]
    return jsonify(success=True, results=results_data)


@views.route('/share_post', methods=['POST'])
def share_post():
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    data = request.json
    note_id = data.get('note_id')
    recipient_id = data.get('recipient_id')

    if not note_id or not recipient_id:
        return jsonify(success=False, error='Missing data'), 400

    # Prevent sharing to self
    if user.id == int(recipient_id):
        return jsonify(success=False, error="Can't share to yourself"), 400

    # Check if recipient exists
    recipient = User.query.get(recipient_id)
    if not recipient:
        return jsonify(success=False, error='Recipient not found'), 404

    # Check if note exists
    note = Note.query.get(note_id)
    if not note:
        return jsonify(success=False, error='Post not found'), 404

    # Prevent duplicate shares (optional)
    from .models import SharedPost
    already_shared = SharedPost.query.filter_by(sender_id=user.id, recipient_id=recipient_id, note_id=note_id).first()
    if already_shared:
        return jsonify(success=False, error='Already shared with this user'), 400

    # Create shared post
    shared = SharedPost(sender_id=user.id, recipient_id=recipient_id, note_id=note_id)
    db.session.add(shared)
    db.session.commit()
    return jsonify(success=True, message="Post shared successfully!"), 200

@views.route('/share_multiple_posts', methods=['POST'])
def share_multiple_posts():
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    data = request.json
    note_ids = data.get('note_ids', [])
    recipient_id = data.get('recipient_id')

    if not note_ids or not recipient_id:
        return jsonify(success=False, error='Missing data'), 400

    if user.id == int(recipient_id):
        return jsonify(success=False, error="Can't share to yourself"), 400

    recipient = User.query.get(recipient_id)
    if not recipient:
        return jsonify(success=False, error='Recipient not found'), 404

    from .models import SharedPost
    shared_count = 0
    ignored_count = 0
    for note_id in map(int, note_ids):
        note = Note.query.get(note_id)
        if not note:
            continue
        already_shared = SharedPost.query.filter_by(sender_id=user.id, recipient_id=recipient_id, note_id=note_id).first()
        if already_shared:
            ignored_count += 1
            continue
        shared = SharedPost(sender_id=user.id, recipient_id=recipient_id, note_id=note_id)
        db.session.add(shared)
        shared_count += 1
    db.session.commit()
    return jsonify(
        success=True,
        shared=shared_count,
        ignored=ignored_count,
        message=f"{shared_count} post(s) shared! {ignored_count} already shared."
    )

@views.route('/inbox')
def inbox():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    # Mark all unseen shared posts as seen
    unseen_posts = SharedPost.query.filter_by(recipient_id=user.id, seen=False).all()
    for sp in unseen_posts:
        sp.seen = True
    if unseen_posts:
        db.session.commit()

    # Fetch all shared posts sent to this user, newest first
    shared_posts = SharedPost.query.filter_by(recipient_id=user.id).order_by(SharedPost.timestamp.desc()).all()

    posts = []
    for sp in shared_posts:
        sender = User.query.get(sp.sender_id)
        note = Note.query.get(sp.note_id)
        if sender and note:
            posts.append({
                'sender': sender,
                'note': note,
                'timestamp': sp.timestamp,
                'seen': sp.seen,
            })

    # Get incoming follow requests
    incoming_requests = Follow.query.filter_by(followed_id=user.id, status='pending').all()

    # Count unseen posts (should now be zero)
    unseen_count = SharedPost.query.filter_by(recipient_id=user.id, seen=False).count()

    if request.method == 'POST':
        comment = Comments(
                Comment = request.form['Comment'], 
                user_id = request.form['user_id'],
                note_id = request.form['note_id'], 
                parentID = request.form['parentID'], 
            )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('views.friends', user_id=user.id))

    review_ids = [post.note_id for post in shared_posts]
    comments = Comments.query.filter(Comments.note_id.in_(review_ids)).all()

    comments_by_review = defaultdict(list)
    for comment in comments:
        comments_by_review[comment.note_id].append(comment.to_dict())

    return render_template(
        'inbox.html',
        user=user, 
        posts=posts,
        unseen_count=unseen_count,
        incoming_requests=incoming_requests, 
        comments_by_review=comments_by_review
    )


@views.route('/api/users')
def api_users():
    user = current_user()
    if not user:
        return jsonify(users=[])
    q = request.args.get('q', '').strip()
    query = User.query.filter(User.id != user.id)
    if q:
        query = query.filter(User.username.ilike(f"%{q}%"))
    users = query.all()
    return jsonify(users=[{'id': u.id, 'username': u.username} for u in users])

@views.route('/api/user_stats/<int:user_id>')
def api_user_stats(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(success=False), 404
    notes = Note.query.filter_by(user_id=user.id).all()
    total = len(notes) or 1
    stats = {
        'spiciness': sum(n.Spiciness for n in notes) / total,
        'deliciousness': sum(n.Deliciousness for n in notes) / total,
        'value': sum(n.Value for n in notes) / total,
        'service': sum(n.Service for n in notes) / total,
    }
    return jsonify(
        success=True,
        stats=stats,
        posts=len(notes),
        username=user.username
    )

@views.route('/api/globe_reviews')
def api_globe_reviews():
    notes = Note.query.filter(Note.latitude.isnot(None), Note.longitude.isnot(None)).all()
    return jsonify([
        {
          'lat':  n.latitude,
          'lng':  n.longitude,
          'title': n.Resturaunt,
          'imageUrl': url_for('views.uploaded_file', filename=n.image),
          'tooltip': n.Review
        }
        for n in notes
    ])