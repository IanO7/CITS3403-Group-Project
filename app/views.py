from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, abort
from .models import Note, User, Follow
from . import db

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
        "likes": r.likes  # Include the latest likes count
    } for r in reviews]

    return render_template('profile.html', user=user, reviews=review_data)

@views.route('/new_post', methods=['GET','POST'])
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
    total = len(notes) or 1  # avoid division by zero

    stats = {
        'spiciness':     sum(n.Spiciness     for n in notes) / total,
        'deliciousness': sum(n.Deliciousness for n in notes) / total,
        'value':         sum(n.Value         for n in notes) / total,
        'plating':       sum(n.Plating       for n in notes) / total
    }

    return render_template('my_stats.html', user=user, stats=stats)
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

    return render_template('my_friends.html', all_users=all_users, followed_users=followed_users, notes=notes)

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