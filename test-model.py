from unittest import TestCase
from app import app
from models import User, Pet, db

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt-a-pet-test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

db.drop_all()
db.create_all()


class AdoptTests(TestCase):
    """Unit tests"""

    def setUp(self):
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

    def tearDown(self):
        Pet.query.delete()
        db.session.commit()
        User.query.delete()
        db.session.commit()

    def test_user(self):
        try:
            user = User.query.filter(User.username == "username1").one()
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        self.assertEqual("username1", user.username)

    def test_pet(self):
        pet1 = Pet(
            api_id="51234567",
            peteval="This is a pet eval",
            username="username1",
        )
        db.session.add(pet1)
        db.session.commit()
        try:
            pet = Pet.query.filter(Pet.api_id == "51234567").one()
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        self.assertEqual("username1", pet.username)
