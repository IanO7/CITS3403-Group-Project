import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app import db, create_app
from app.models import User, Note

 
app = create_app()
app.app_context().push()

# List of demo usernames to delete
demo_usernames = [
    "alice", "bob", "carol", "dan", "eve", "frank", "grace", "heidi"
]

# Delete notes for each demo user
for username in demo_usernames:
    user = User.query.filter_by(username=username).first()
    if user:
        Note.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
db.session.commit()

print("Demo users and their posts deleted.")