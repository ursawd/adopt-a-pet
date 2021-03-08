from unittest import TestCase
from app import app
from models import User, Pet, db

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt-a-pet-test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False

db.drop_all()
db.create_all()


class AdoptTests(TestCase):
    """Unit tests"""

    # -----------------------------------------
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

        pet1 = Pet(
            api_id="51234567",
            peteval="This is a pet eval",
            username="username1",
        )

        db.session.add(pet1)
        db.session.commit()

    # -----------------------------------------
    def tearDown(self):
        Pet.query.delete()
        db.session.commit()
        User.query.delete()
        db.session.commit()

    # -----------------------------------------
    def test_home_route(self):

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Adopt A Pet</h1>", html)

    # -----------------------------------------
    def test_login_route(self):

        with app.test_client() as client:
            data = {"username": "username1", "password": "password"}
            resp = client.post("/login", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

    # -----------------------------------------
    def test_register_route(self):

        with app.test_client() as client:

            data = {
                "username": "username2",
                "password": "password",
                "email": "user@user.com",
                "first_name": "userfirstname",
                "last_name": "userlastname",
            }

            resp = client.post("/register", data=data, follow_redirects=True)

            try:
                pet = Pet.query.filter(Pet.api_id == "51234567").one()
                self.assertTrue(True)
            except:
                self.assertTrue(False)
                self.assertEqual("username2", pet.username)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
