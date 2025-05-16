import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, create_app
from app.models import User, Note
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Remove all data (optional, for a clean slate)
db.drop_all()
db.create_all()

# Use the burger demo image for all users and reviews
burger_demo_image = "Burgerdemo.png"  # Make sure this matches the actual filename in your demo folder

# Demo users (8 users, various names)
users = [
    {"username": "alice", "email": "alice@example.com", "password": "alicepass", "profileImage": burger_demo_image},
    {"username": "bob", "email": "bob@example.com", "password": "bobpass", "profileImage": burger_demo_image},
    {"username": "carol", "email": "carol@example.com", "password": "carolpass", "profileImage": burger_demo_image},
    {"username": "dan", "email": "dan@example.com", "password": "danpass", "profileImage": burger_demo_image},
    {"username": "eve", "email": "eve@example.com", "password": "evepass", "profileImage": burger_demo_image},
    {"username": "frank", "email": "frank@example.com", "password": "frankpass", "profileImage": burger_demo_image},
    {"username": "grace", "email": "grace@example.com", "password": "gracepass", "profileImage": burger_demo_image},
    {"username": "heidi", "email": "heidi@example.com", "password": "heidipass", "profileImage": burger_demo_image},
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

# Use the burger demo image for all reviews
default_review_image = burger_demo_image

# Demo posts for each user (varied cuisines, locations, and review levels)
demo_posts = [
    # Alice
    {"Restaurant": "Spicy Palace", "Spiciness": 90, "Deliciousness": 85, "Value": 70, "Stars": 5, "Service": 80, "Cuisine": "indian", "Review": "Amazing spicy curry!", "user_id": user_objs[0].id, "location": "Perth", "latitude": -31.9505, "longitude": 115.8605},
    {"Restaurant": "Noodle House", "Spiciness": 60, "Deliciousness": 80, "Value": 75, "Stars": 4, "Service": 70, "Cuisine": "chinese", "Review": "Great noodles, decent spice.", "user_id": user_objs[0].id, "location": "Perth", "latitude": -31.9505, "longitude": 115.8605},
    # Bob
    {"Restaurant": "Bob's Burgers", "Spiciness": 20, "Deliciousness": 95, "Value": 90, "Stars": 4, "Service": 85, "Cuisine": "burger", "Review": "Juicy burgers and great value.", "user_id": user_objs[1].id, "location": "Fremantle", "latitude": -32.0569, "longitude": 115.7439},
    {"Restaurant": "Pizza Planet", "Spiciness": 10, "Deliciousness": 88, "Value": 80, "Stars": 5, "Service": 90, "Cuisine": "pizza", "Review": "Best pizza in town!", "user_id": user_objs[1].id, "location": "Fremantle", "latitude": -32.0569, "longitude": 115.7439},
    # Carol
    {"Restaurant": "Sushi Central", "Spiciness": 5, "Deliciousness": 92, "Value": 85, "Stars": 5, "Service": 95, "Cuisine": "japanese", "Review": "Fresh sushi and friendly staff.", "user_id": user_objs[2].id, "location": "Subiaco", "latitude": -31.9500, "longitude": 115.8000},
    {"Restaurant": "Ramen Den", "Spiciness": 40, "Deliciousness": 90, "Value": 70, "Stars": 4, "Service": 80, "Cuisine": "japanese", "Review": "Tasty ramen, good value.", "user_id": user_objs[2].id, "location": "Subiaco", "latitude": -31.9500, "longitude": 115.8000},
    # Dan
    {"Restaurant": "Taco Fiesta", "Spiciness": 70, "Deliciousness": 75, "Value": 60, "Stars": 3, "Service": 70, "Cuisine": "mexican", "Review": "Spicy tacos, fun vibe.", "user_id": user_objs[3].id, "location": "Northbridge", "latitude": -31.9430, "longitude": 115.8570},
    {"Restaurant": "BBQ Bros", "Spiciness": 80, "Deliciousness": 85, "Value": 65, "Stars": 4, "Service": 75, "Cuisine": "bbq", "Review": "Great BBQ meats!", "user_id": user_objs[3].id, "location": "Northbridge", "latitude": -31.9430, "longitude": 115.8570},
    # Eve
    {"Restaurant": "Thai Orchid", "Spiciness": 85, "Deliciousness": 80, "Value": 70, "Stars": 5, "Service": 90, "Cuisine": "thai", "Review": "Authentic Thai flavors.", "user_id": user_objs[4].id, "location": "Cannington", "latitude": -32.0150, "longitude": 115.9380},
    {"Restaurant": "Green Curry House", "Spiciness": 75, "Deliciousness": 85, "Value": 80, "Stars": 4, "Service": 85, "Cuisine": "thai", "Review": "Best green curry!", "user_id": user_objs[4].id, "location": "Cannington", "latitude": -32.0150, "longitude": 115.9380},
    # Frank
    {"Restaurant": "Seafood Shack", "Spiciness": 15, "Deliciousness": 90, "Value": 75, "Stars": 4, "Service": 80, "Cuisine": "seafood", "Review": "Fresh seafood, nice view.", "user_id": user_objs[5].id, "location": "Hillarys", "latitude": -31.8230, "longitude": 115.7380},
    {"Restaurant": "Fish & Chips Co", "Spiciness": 5, "Deliciousness": 80, "Value": 85, "Stars": 3, "Service": 70, "Cuisine": "seafood", "Review": "Classic fish and chips.", "user_id": user_objs[5].id, "location": "Hillarys", "latitude": -31.8230, "longitude": 115.7380},
    # Grace
    {"Restaurant": "French Delights", "Spiciness": 10, "Deliciousness": 95, "Value": 60, "Stars": 5, "Service": 95, "Cuisine": "french", "Review": "Delicious pastries!", "user_id": user_objs[6].id, "location": "Leederville", "latitude": -31.9360, "longitude": 115.8410},
    {"Restaurant": "Crepe Corner", "Spiciness": 0, "Deliciousness": 90, "Value": 70, "Stars": 4, "Service": 90, "Cuisine": "french", "Review": "Sweet and savoury crepes.", "user_id": user_objs[6].id, "location": "Leederville", "latitude": -31.9360, "longitude": 115.8410},
    # Heidi
    {"Restaurant": "Greek Taverna", "Spiciness": 30, "Deliciousness": 85, "Value": 80, "Stars": 4, "Service": 85, "Cuisine": "greek", "Review": "Great moussaka and souvlaki.", "user_id": user_objs[7].id, "location": "Mount Lawley", "latitude": -31.9365, "longitude": 115.8710},
    {"Restaurant": "Olive Grove", "Spiciness": 20, "Deliciousness": 80, "Value": 85, "Stars": 5, "Service": 90, "Cuisine": "greek", "Review": "Lovely salads and olives.", "user_id": user_objs[7].id, "location": "Mount Lawley", "latitude": -31.9365, "longitude": 115.8710},
]

for post in demo_posts:
    post["image"] = default_review_image  # Set burger demo image for all reviews
    note = Note(**post)
    db.session.add(note)
db.session.commit()

print("Demo users and posts loaded!")
print("See 'seed_demo_users.txt' for login details.")