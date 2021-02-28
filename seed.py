"""Seed file to make sample data .
   Database adopt-a-pet must exist before running this file.
   defined in app.py():
   app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt-a-pet"
"""

from models import db, User, Pet
from app import app

# create all tables
db.drop_all()
db.create_all()

# create user
user1 = User(
    username="username1",
    # hashed password for "password = 'password'"
    password="$2b$12$h9kN440NdtdbCimRcpu.Z.JSRGMWv42TJFlxeeBLPn6JqelMCQCPe",
    email="user@user.com",
    first_name="userfirstname",
    last_name="userlastname",
)

db.session.add(user1)
db.session.commit()

# create pet(s) for user1
pet1 = Pet(
    username="username1",
    api_id=123,
    petname="Spot",
    petphoto="https://msn.com",
    peteval="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean quis orci eget neque tempor euismod non ut dui. Donec velit felis, auctor nec sapien ut, scelerisque congue dui.",
)

db.session.add(pet1)
db.session.commit()
