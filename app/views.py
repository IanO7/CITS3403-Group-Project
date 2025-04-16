from flask import Blueprint, render_template, request
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("base.html")

@views.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template("profile.html")

@views.route('/new_post', methods=['GET', 'POST'])
def newPost():
    if request.method == 'POST':
        restaurant = request.form.get("restaurant")
        price = request.form.get("price")
        rating = request.form.get("rating")
        review = request.form.get("review")
        image = request.form.get("image")

        new_post = Note(Restuarant=restaurant,Price=price, Rating=rating, Review=review, Image=image)
        db.session.add(new_post)
        db.session.commit()

    data = request.form 
    print (data)
     

    return render_template("newPost.html")