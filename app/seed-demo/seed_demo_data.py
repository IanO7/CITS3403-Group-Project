import os
import shutil
import sys

from app import db, create_app
from app.models import User, Note
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Remove all data (optional, for a clean slate)
db.drop_all()
db.create_all()

# Demo users (8 users, various names)
users = [
    {"username": "alice", "email": "alice@example.com", "password": "alicepass", "profileImage": None},
    {"username": "bob", "email": "bob@example.com", "password": "bobpass", "profileImage": None},
    {"username": "carol", "email": "carol@example.com", "password": "carolpass", "profileImage": None},
    {"username": "dan", "email": "dan@example.com", "password": "danpass", "profileImage": None},
    {"username": "eve", "email": "eve@example.com", "password": "evepass", "profileImage": None},
    {"username": "frank", "email": "frank@example.com", "password": "frankpass", "profileImage": None},
    {"username": "grace", "email": "grace@example.com", "password": "gracepass", "profileImage": None},
    {"username": "heidi", "email": "heidi@example.com", "password": "heidipass", "profileImage": None},
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

# Demo posts for each user (varied cuisines, locations, and review levels)
demo_posts = [
    # Alice
    {"Restaurant": "Spicy Palace", "Spiciness": 90, "Deliciousness": 85, "Value": 70, "Stars": 5, "Service": 80, "Cuisine": "indian", "Review": "Amazing spicy curry!", "image": "spicy_palace.jpeg", "user_id": user_objs[0].id, "location": "Perth", "latitude": -31.9505, "longitude": 115.8605},
    {"Restaurant": "Noodle House", "Spiciness": 60, "Deliciousness": 80, "Value": 75, "Stars": 4, "Service": 70, "Cuisine": "chinese", "Review": "Great noodles, decent spice.", "image": "noodle_house.jpeg", "user_id": user_objs[0].id, "location": "Perth", "latitude": -31.9505, "longitude": 115.8605},
    # Bob
    {"Restaurant": "Bob's Burgers", "Spiciness": 20, "Deliciousness": 95, "Value": 90, "Stars": 4, "Service": 85, "Cuisine": "burger", "Review": "Juicy burgers and great value.", "image": "bobs_burgers.jpeg", "user_id": user_objs[1].id, "location": "Fremantle", "latitude": -32.0569, "longitude": 115.7439},
    {"Restaurant": "Pizza Planet", "Spiciness": 10, "Deliciousness": 88, "Value": 80, "Stars": 5, "Service": 90, "Cuisine": "pizza", "Review": "Best pizza in town!", "image": "pizza_planet.jpeg", "user_id": user_objs[1].id, "location": "Fremantle", "latitude": -32.0569, "longitude": 115.7439},
    # Carol
    {"Restaurant": "Sushi Central", "Spiciness": 5, "Deliciousness": 92, "Value": 85, "Stars": 5, "Service": 95, "Cuisine": "japanese", "Review": "Fresh sushi and friendly staff.", "image": "sushi_central.jpeg", "user_id": user_objs[2].id, "location": "Subiaco", "latitude": -31.9500, "longitude": 115.8000},
    {"Restaurant": "Ramen Den", "Spiciness": 40, "Deliciousness": 90, "Value": 70, "Stars": 4, "Service": 80, "Cuisine": "japanese", "Review": "Tasty ramen, good value.", "image": "ramen_den.jpeg", "user_id": user_objs[2].id, "location": "Subiaco", "latitude": -31.9500, "longitude": 115.8000},
    # Dan
    {"Restaurant": "Taco Fiesta", "Spiciness": 70, "Deliciousness": 75, "Value": 60, "Stars": 3, "Service": 70, "Cuisine": "mexican", "Review": "Spicy tacos, fun vibe.", "image": "taco_fiesta.jpeg", "user_id": user_objs[3].id, "location": "Northbridge", "latitude": -31.9430, "longitude": 115.8570},
    {"Restaurant": "BBQ Bros", "Spiciness": 80, "Deliciousness": 85, "Value": 65, "Stars": 4, "Service": 75, "Cuisine": "bbq", "Review": "Great BBQ meats!", "image": "bbq_bros.jpeg", "user_id": user_objs[3].id, "location": "Northbridge", "latitude": -31.9430, "longitude": 115.8570},
    # Eve
    {"Restaurant": "Thai Orchid", "Spiciness": 85, "Deliciousness": 80, "Value": 70, "Stars": 5, "Service": 90, "Cuisine": "thai", "Review": "Authentic Thai flavors.", "image": "thai_orchid.jpeg", "user_id": user_objs[4].id, "location": "Cannington", "latitude": -32.0150, "longitude": 115.9380},
    {"Restaurant": "Green Curry House", "Spiciness": 75, "Deliciousness": 85, "Value": 80, "Stars": 4, "Service": 85, "Cuisine": "thai", "Review": "Best green curry!", "image": "green_curry_house.jpeg", "user_id": user_objs[4].id, "location": "Cannington", "latitude": -32.0150, "longitude": 115.9380},
    # Frank
    {"Restaurant": "Seafood Shack", "Spiciness": 15, "Deliciousness": 90, "Value": 75, "Stars": 4, "Service": 80, "Cuisine": "seafood", "Review": "Fresh seafood, nice view.", "image": "seafood_shack.jpeg", "user_id": user_objs[5].id, "location": "Hillarys", "latitude": -31.8230, "longitude": 115.7380},
    {"Restaurant": "Fish & Chips Co", "Spiciness": 5, "Deliciousness": 80, "Value": 85, "Stars": 3, "Service": 70, "Cuisine": "seafood", "Review": "Classic fish and chips.", "image": "fish_chips_co.jpeg", "user_id": user_objs[5].id, "location": "Hillarys", "latitude": -31.8230, "longitude": 115.7380},
    # Grace
    {"Restaurant": "French Delights", "Spiciness": 10, "Deliciousness": 95, "Value": 60, "Stars": 5, "Service": 95, "Cuisine": "french", "Review": "Delicious pastries!", "image": "french_delights.jpeg", "user_id": user_objs[6].id, "location": "Leederville", "latitude": -31.9360, "longitude": 115.8410},
    {"Restaurant": "Crepe Corner", "Spiciness": 0, "Deliciousness": 90, "Value": 70, "Stars": 4, "Service": 90, "Cuisine": "french", "Review": "Sweet and savoury crepes.", "image": "crepe_corner.jpeg", "user_id": user_objs[6].id, "location": "Leederville", "latitude": -31.9360, "longitude": 115.8410},
    # Heidi
    {"Restaurant": "Greek Taverna", "Spiciness": 30, "Deliciousness": 85, "Value": 80, "Stars": 4, "Service": 85, "Cuisine": "greek", "Review": "Great moussaka and souvlaki.", "image": "greek_taverna.jpeg", "user_id": user_objs[7].id, "location": "Mount Lawley", "latitude": -31.9365, "longitude": 115.8710},
    {"Restaurant": "Olive Grove", "Spiciness": 20, "Deliciousness": 80, "Value": 85, "Stars": 5, "Service": 90, "Cuisine": "greek", "Review": "Lovely salads and olives.", "image": "olive_grove.jpeg", "user_id": user_objs[7].id, "location": "Mount Lawley", "latitude": -31.9365, "longitude": 115.8710},
]

for post in demo_posts:
    if "image" not in post or not post["image"]:
        post["image"] = "food.jpeg"  # fallback image if none provided
    note = Note(**post)
    db.session.add(note)
db.session.commit()

# Path to the uploads folder in your app configuration
upload_folder = os.path.join(os.getcwd(), 'app', 'uploads')
# Path to your seed images folder (adjust the folder name if needed)
seed_images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

# Copy image files from the seed images folder to the app uploads folder
for post in demo_posts:
    image_filename = post.get('image', 'food.jpeg')
    source_path = os.path.join(seed_images_folder, image_filename)
    dest_path = os.path.join(upload_folder, image_filename)
    if os.path.exists(source_path):
        shutil.copy(source_path, dest_path)
    else:
        print(f"Image file not found: {source_path}")

print("Demo users and posts loaded!")
print("See 'seed_demo_users.txt' for login details.")