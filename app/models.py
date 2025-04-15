from . import db 

class Note(db.Model):
    Id = db.Column(db.Integer, primary_key = True)
    Restuarant = db.Column(db.String(100)) 
    Price = db.Column(db.Integer)
    Rating = db.Column(db.Integer)
    Review = db.Column(db.String(100))
    Image = db.Column(db.String(100))
    User = db.Column(db.String(100))

