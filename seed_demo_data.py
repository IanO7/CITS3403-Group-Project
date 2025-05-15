import os
from app import db, create_app
from app.models import User, Note
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Remove all data (optional, for a clean slate)
db.drop_all()
db.create_all()

# Demo users
users = [
    {
        "username": "alice",
        "email": "alice@example.com",
        "password": "alicepass",
        "profileImage": None
    },
    {
        "username": "bob",
        "email": "bob@example.com",
        "password": "bobpass",
        "profileImage": None
    }
]

user_objs = []
for u in users:
    user = User(
        username=u["username"],
        email=u["email"],
        profileImage=u["profileImage"],
        password=generate_password_hash(u["password"])
    )
    db.session.add(user)
    user_objs.append(user)
db.session.commit()

# Write demo user credentials to a text file
with open("seed_demo_users.txt", "w") as f:
    for u in users:
        f.write(f"Username: {u['username']}\nEmail: {u['email']}\nPassword: {u['password']}\n\n")

# Demo posts for each user (add as many as you like)
demo_posts = [
    # Alice's posts
    {
        "Resturaunt": "Spicy Palace",
        "Spiciness": 90,
        "Deliciousness": 85,
        "Value": 70,
        "Stars": 5,
        "Service": 80,
        "Cuisine": "indian",
        "Review": "Amazing spicy curry!",
        "image": "spicy_palace.jpg",
        "user_id": user_objs[0].id,
        "location": "Perth",
        "latitude": -31.9505,
        "longitude": 115.8605
    },
    {
        "Resturaunt": "Noodle House",
        "Spiciness": 60,
        "Deliciousness": 80,
        "Value": 75,
        "Stars": 4,
        "Service": 70,
        "Cuisine": "chinese",
        "Review": "Great noodles, decent spice.",
        "image": "noodle_house.jpg",
        "user_id": user_objs[0].id,
        "location": "Perth",
        "latitude": -31.9505,
        "longitude": 115.8605
    },
    {
        "Resturaunt": "Curry Express",
        "Spiciness": 95,
        "Deliciousness": 90,
        "Value": 60,
        "Stars": 5,
        "Service": 85,
        "Cuisine": "indian",
        "Review": "Super spicy and delicious curry!",
        "image": "curry_express.jpg",
        "user_id": user_objs[0].id,
        "location": "Perth",
        "latitude": -31.9505,
        "longitude": 115.8605
    },
    # Bob's posts
    {
        "Resturaunt": "Bob's Burgers",
        "Spiciness": 20,
        "Deliciousness": 95,
        "Value": 90,
        "Stars": 4,
        "Service": 85,
        "Cuisine": "burger",
        "Review": "Juicy burgers and great value.",
        "image": "bobs_burgers.jpg",
        "user_id": user_objs[1].id,
        "location": "Fremantle",
        "latitude": -32.0569,
        "longitude": 115.7439
    },
    {
        "Resturaunt": "Pizza Planet",
        "Spiciness": 10,
        "Deliciousness": 88,
        "Value": 80,
        "Stars": 5,
        "Service": 90,
        "Cuisine": "pizza",
        "Review": "Best pizza in town!",
        "image": "pizza_planet.jpg",
        "user_id": user_objs[1].id,
        "location": "Fremantle",
        "latitude": -32.0569,
        "longitude": 115.7439
    },
    {
        "Resturaunt": "Sushi Central",
        "Spiciness": 5,
        "Deliciousness": 92,
        "Value": 85,
        "Stars": 5,
        "Service": 95,
        "Cuisine": "japanese",
        "Review": "Fresh sushi and friendly staff.",
        "image": "sushi_central.jpg",
        "user_id": user_objs[1].id,
        "location": "Fremantle",
        "latitude": -32.0569,
        "longitude": 115.7439
    }
]

for post in demo_posts:
    note = Note(**post)
    db.session.add(note)
db.session.commit()

print("Demo users and posts loaded!")
print("See 'seed_demo_users.txt' for login details.")