 
from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Note, User
from . import db

views = Blueprint('views', __name__)

def current_user():
    uid = session.get('user_id')
    return User.query.get(uid) if uid else None

@views.route('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('views.profile'))
    # otherwise send them to log in
    return redirect(url_for('auth.login'))

@views.route('/profile')
def profile():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=user, notes=user.notes)

@views.route('/new_post', methods=['GET','POST'])
def new_post():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        note = Note(
          restaurant=request.form['restaurant'],
          price=int(request.form['price']),
          rating=int(request.form['rating']),
          review=request.form['review'],
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

    notes = user.notes
    # dummy example – replace with real logic
    stats = {
      'spiciness'    : sum(n.rating for n in notes)//len(notes) if notes else 0,
      'deliciousness': 70,
      'value'        : 60,
      'plating'      : 80
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
    # all notes except the current user's
    notes = Note.query.filter(Note.user_id != user.id).all()
    return render_template('my_friends.html', notes=notes)
