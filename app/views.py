 
from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Review, User
from . import db

views = Blueprint('views', __name__)

def current_user():
    uid = session.get('user_id')
    return User.query.get(uid) if uid else None

def getReviews(user):
    return Review.query.filter_by(user_id=user.id).all()

def getOtherReviews(user):
    return Review.query.filter(Review.user_id != user.id).all()

@views.route('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('views.profile'))
    # otherwise send them to log in
    return redirect(url_for('auth.login'))

@views.route('/profile', methods=['GET', 'POST'])
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
        review = Review(
            Resturaunt=request.form['Resturaunt'],
            Spiciness=int(request.form['Spiciness']),
            Deliciousness=int(request.form['Deliciousness']),
            Value=int(request.form['Value']),
            Plating=int(request.form['Plating']),
            Review=request.form['Review'],
            image=request.form['image'],
            user_id=user.id
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('views.profile'))

    return render_template('newPost.html')


@views.route('/my_stats')
def my_stats():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))
    
    reviews = getReviews(user)

    stats = [{
        "Resturaunt" : r.Resturaunt, 
        "Spiciness" : r.Spiciness,
        "Deliciousness" : r.Deliciousness, 
        "Value" : r.Value, 
        "Plating" : r.Plating, 
        "Review" : r.Review, 
        "user_id" : user.id, 
    } for r in reviews]
    return render_template('my_stats.html', user=user, stats=stats)

@views.route('/global_stats')
def global_stats():
    return render_template('others_stats.html')

@views.route('/friends')
def friends():
    user = current_user()
    if not user:
        return redirect(url_for('auth.login'))
    reviews = getOtherReviews(user)

    review_data = [{
        "Resturaunt" : r.Resturaunt, 
        "Spiciness" : r.Spiciness,
        "Deliciousness" : r.Deliciousness, 
        "Value" : r.Value, 
        "Plating" : r.Plating, 
        "Review" : r.Review, 
        "image" : r.image, 
        "user_id": r.user.username,
    } for r in reviews]
    
    return render_template('my_friends.html', reviews=reviews)
