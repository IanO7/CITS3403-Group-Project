from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Note(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    Resturaunt      = db.Column(db.String(100), nullable = False)
    Spiciness       = db.Column(db.Integer, nullable=False)
    Deliciousness   = db.Column(db.Integer, nullable = False)
    Value           = db.Column(db.Integer, nullable=False)
    Stars           = db.Column(db.Integer, nullable=False)
    Service         = db.Column(db.Integer, nullable=False)
    Cuisine         = db.Column(db.String(100), nullable = False)
    Review          = db.Column(db.String(1000), nullable=False)
    image           = db.Column(db.String(200))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes           = db.Column(db.Integer, default=0)  # New column for likes
    location        = db.Column(db.String(255), nullable=True, index=True)  # Add index for faster querying
    latitude   = db.Column(db.Float, nullable=True, index=True)
    longitude  = db.Column(db.Float, nullable=True, index=True)
class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150),  unique=True, nullable=False)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    profileImage = db.Column(db.String(200))
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
    status = db.Column(db.String(20), default='pending')  # 'pending' or 'approved'

    follower = db.relationship('User', foreign_keys=[follower_id], backref='following')
    followed = db.relationship('User', foreign_keys=[followed_id], backref='followers')

class SharedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    seen = db.Column(db.Boolean, default=False)  # <-- Add this line