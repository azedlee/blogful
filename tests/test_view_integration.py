import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestAddEntry(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()
        
        # Set up the tables in the database
        Base.metadata.create_all(engine)
        
        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
                        password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()
    
    # simulate_login method essentially mimics what Flask-Login looks for when determining whether a user is logged in.
    def simulate_login(self):
        # Method to get access to a variable representing the HTTP session
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            # _fresh means active
            http_session["_fresh"] = True
    
    def test_add_entry(self):
        # Call simulate_login method so you can act as a logged in user
        self.simulate_login()
        
        response = self.client.post("/entry/add", data={
            "title": "Test Entry",
            "content": "Test Content"
        })
        
        # The HTTP response status code 302 Found is a common way of performing URL redirection.
        # Make sure that your user is being redirected to the / route by checking the status code and the location header of the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test Content")
        self.assertEqual(entry.author, self.user)
    
    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

class TestEditEntry(unittest.TestCase):
    def setUp(self):
        alice = User(name="Alice", email="alice@example.com",
                     password=generate_password_hash("test"))
        peter = User(name="Peter", email="peter@example.com",
                     password=generate_password_hash("test"))
        test_entry = Entry(title="Test Title", content="Test Content", author="Alice")
        session.add(alice, peter, test_entry)
        session.commit()
    
    def test_wrong_author_edit(self):
        self.simulate_login(peter)
        
        response = self.client.post("entry/0/edit", data=self.test_entry)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertNotEqual(entry.author, peter)
    
    def test_right_author_edit(self):
        self.simulate_login(alice)
        
        response = self.client.post("entry/0/edit", data=self.test_entry)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.author, alice)
    
    def tearDown(self):
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

class TestDeleteEntry(unittest.TestCase):
    def setUp(self):
        alice = User(name="Alice", email="alice@example.com",
                     password=generate_password_hash("test"))
        peter = User(name="Peter", email="peter@example.com",
                     password=generate_password_hash("test"))
        test_entry = Entry(title="Test Title", content="Test Content", author="Alice")
        session.add(alice, peter, test_entry)
        session.commit()
    
    def test_wrong_author_edit(self):
        self.simulate_login(peter)
        
        response = self.client.post("entry/0/delete", data=self.test_entry)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertNotEqual(entry.author, peter)
    
    def test_right_author_edit(self):
        self.simulate_login(alice)
        
        response = self.client.post("entry/0/delete", data=self.test_entry)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.author, alice)
    
    def tearDown(self):
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()