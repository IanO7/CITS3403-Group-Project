from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, abort
from .models import Note, User
from . import db

views = Blueprint('views', __name__)

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

    reviews = getReviews(user)
    review_data = [{
        "Resturaunt" : r.Resturaunt, 
        "Spiciness" : r.Spiciness,
        "Deliciousness" : r.Deliciousness, 
        "Value" : r.Value, 
        "Plating" : r.Plating, 
        "Review" : r.Review, 
        "image" : r.image, 
        "user_id" : user.id, 
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

    notes = getReviews(user)
    stats = {
        'spiciness': sum(n.rating for n in notes) / len(notes) if notes else 0,
        'deliciousness': sum(n.rating for n in notes) / len(notes) if notes else 0,
        'value': sum(n.price for n in notes) / len(notes) if notes else 0,
        'plating': sum(n.rating for n in notes) / len(notes) if notes else 0
    }
    return render_template('my_stats.html', user=user, stats=stats)

@views.route('/global_stats')
def global_stats():
    return render_template('others_stats.html')

@views.route('/friends')
def friends():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))
    notes = Note.query.filter(Note.user_id != user.id).all()
    return render_template('my_friends.html', notes=notes)

@views.route('/like/<int:note_id>', methods=['POST'])
def like(note_id):
    user = current_user()
    if not user:
        return jsonify(success=False, error='User not authenticated'), 401

    liked = session.get('liked_notes', [])
    if note_id in liked:
        return jsonify(success=False, error='Already liked'), 400

    note = Note.query.get(note_id)
    if not note:
        return jsonify(success=False, error='Note not found'), 404

    note.likes = (note.likes or 0) + 1
    db.session.commit()
    liked.append(note_id)
    session['liked_notes'] = liked
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
