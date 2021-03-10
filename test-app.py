from unittest import TestCase
from app import app
from models import User, Pet, db

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt-a-pet-test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True
# Bypass WTForms CSRF enforcement which causes failed form vailidations
app.config["WTF_CSRF_ENABLED"] = False

db.drop_all()
db.create_all()


class AdoptTests(TestCase):
    """Unit tests"""

    # -----------------------------------------
    def setUp(self):
        """ Runs before each test"""
        # Create a user in database
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
        # Create a entry in the pets table tied to username in users table
        pet1 = Pet(
            api_id="51234567",
            peteval="This is a pet eval",
            username="username1",
        )

        db.session.add(pet1)
        db.session.commit()

    # -----------------------------------------
    def tearDown(self):
        """Runs after each test
        Deletes all records in users and pets tables"""
        Pet.query.delete()
        db.session.commit()
        User.query.delete()
        db.session.commit()

    # -----------------------------------------
    def test_home_route(self):
        """Tests home (index) route"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Adopt A Pet</h1>", html)

    # -----------------------------------------
    def test_login_route(self):
        """Tests login route passing in username and password"""
        with app.test_client() as client:
            data = {"username": "username1", "password": "password"}
            resp = client.post("/login", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('<form class="mt-3" id="search-form" method="POST">', html)
            self.assertEqual(resp.status_code, 200)

    # -----------------------------------------
    def test_register_route(self):
        """Tests registration creates new user"""
        with app.test_client() as client:

            data = {
                "username": "username2",
                "password": "password",
                "email": "user@user.com",
                "first_name": "userfirstname",
                "last_name": "userlastname",
            }

            resp = client.post("/register", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn('<form class="mt-3" id="search-form" method="POST">', html)
            self.assertEqual(resp.status_code, 200)

    # -----------------------------------------
    def test_logout_route(self):
        """Tests logout route"""
        with app.test_client() as client:
            resp = client.get("/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("li>You must Register / Login to display pets.</li>", html)
            self.assertEqual(resp.status_code, 200)

    # -----------------------------------------
    def test_search_route(self):
        """Tests search route"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "username1"

            data = {
                "type": "dog",
                "gender": "male",
                "distance": 50,
                "location": 32162,
            }

            resp = client.post("/search", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("<h3>Search for a pet</h3>", html)
            self.assertEqual(resp.status_code, 200)

    # -----------------------------------------
    def test_postnote_route(self):
        """Tests postnote route"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "username1"

            data = {
                "note": "This is a pet note",
                "apiid": "51234567",
            }

            resp = client.post("/postnote", json=data)

            # pets.apiid value should change from "This is a pet eval" to
            # "This is a pet note" for route to be successful
            noteField = Pet.query.first()

            self.assertEqual(noteField.peteval, "This is a pet note")
            # show return 204 No Content due to only a table update
            self.assertEqual(resp.status_code, 204)

    # -----------------------------------------
    def test_shownotes_route(self):
        """Tests shownotes route"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["username"] = "username1"
            resp = client.get("/shownotes")
            html = resp.get_data(as_text=True)
            self.assertIn("<li>A pet is no longer available and has been removed</li>", html)
            self.assertEqual(resp.status_code, 200)

    # -----------------------------------------
    def test_deletenotes_route(self):
        """Tests delete-notes route:
        deletes only record from pets table, checks if record deleted,
        checks if redirection worked
        """
        with app.test_client() as client:
            # creates client instance of session object
            # note following indention
            with client.session_transaction() as sess:
                sess["username"] = "username1"
            resp = client.get("/delete-note/51234567", follow_redirects=True)
            # get pet record, returns None if delete
            record_exists = Pet.query.first()
            # record deleted
            self.assertIsNone(record_exists)
            self.assertEqual(resp.status_code, 200)
