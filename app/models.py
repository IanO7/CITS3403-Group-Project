from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Note(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    Resturaunt      = db.Column(db.String(100), nullable = False)
    Spiciness       = db.Column(db.Integer, nullable=False)
    Deliciousness   = db.Column(db.Integer, nullable = False)
    Value           = db.Column(db.Integer, nullable=False)
    Plating         = db.Column(db.Integer, nullable=False)
    Review          = db.Column(db.String(1000), nullable=False)
    image           = db.Column(db.String(200))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    likes      = db.Column(db.Integer, default=0)  # New column for likes

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150),  unique=True, nullable=False)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    Note       = db.relationship(Note, backref='user', lazy=True)

    # ALways use generate_password_hash() & check_password_hash() for security => AUTOMATIC SALTING, NOT JUST HASHING ONLY!!
    def set_password(self, raw):
        self.password = generate_password_hash(raw)
    def check_password(self, raw):
        return check_password_hash(self.password, raw)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    follower = db.relationship('User', foreign_keys=[follower_id], backref='following')
    followed = db.relationship('User', foreign_keys=[followed_id], backref='followers')