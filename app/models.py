from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Review(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    Resturaunt      = db.Column(db.String(100), nullable = False)
    Spiciness       = db.Column(db.Integer, nullable=False)
    Deliciousness   = db.Column(db.Integer, nullable = False)
    Value           = db.Column(db.Integer, nullable=False)
    Plating         = db.Column(db.Integer, nullable=False)
    Review          = db.Column(db.String(1000), nullable=False)
    image           = db.Column(db.String(200))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),  unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    Reviews = db.relationship(Review,  backref='user', lazy=True)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)
    def check_password(self, raw):
        return check_password_hash(self.password, raw)

