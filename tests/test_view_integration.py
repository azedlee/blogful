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
    entry_data = {
        'title' : 'New Title',
        'content' : 'New Content'
    }
    
    def setUp(self):
        self.client = User(name="Alice", email="alice@example.com",
                     password=generate_password_hash("test"))
        peter = User(name="Peter", email="peter@example.com",
                     password=generate_password_hash("test"))
        test_entry = Entry(title="Test Title", content="Test Content", author=self.client)
        session.add(self.client)
        session.add(peter)
        session.add(test_entry)
        try:
            session.commit()
        except:
            session.rollback()
            raise
    
    def simulate_login(self):
        # Method to get access to a variable representing the HTTP session
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.client.id)
            # _fresh means active
            http_session["_fresh"] = True
    
    def test_wrong_author_edit(self, test_users):
        self.simulate_login()
        
        response = self.client.post("entry/0/edit", data=self.entry_data)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertNotEqual(entry.author, test_users.peter)
    
    def test_right_author_edit(self):
        self.simulate_login()
        
        response = self.client.post("entry/0/edit", data=self.entry_data)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.author, self.client)
    
    def tearDown(self):
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

class TestDeleteEntry(unittest.TestCase):
    entry_data = {
        'title' : 'New Title',
        'content' : 'New Content'
    }
    
    def setUp(self):
        self.client = User(name="Alice1", email="alice1@example.com",
                     password=generate_password_hash("test"))
        peter = User(name="Peter1", email="peter1@example.com",
                     password=generate_password_hash("test1"))
        test_entry = Entry(title="Test Title 2", content="Test Content 2", author=self.client)
        session.add(self.client)
        session.add(peter)
        session.add(test_entry)
        try:
            session.commit()
        except:
            session.rollback()
            raise
    
    def simulate_login(self):
        # Method to get access to a variable representing the HTTP session
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.client.id)
            # _fresh means active
            http_session["_fresh"] = True
    
    def test_wrong_author_edit(self, test_users):
        self.simulate_login()
        
        response = self.client.post("entry/0/delete", data=self.entry_data)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertNotEqual(entry.author, test_users.peter)
    
    def test_right_author_edit(self):
        self.simulate_login()
        
        response = self.client.post("entry/0/delete", data=self.entry_data)
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.author, self.client)
    
    def tearDown(self):
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()