import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test Setup """
        self.browser = Browser("phantomjs")
        
        # Set up the tables in the database
        Base.metadata.create_all(engine)
        
        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
                        password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        # multiprocessing module gives you the ability to start and run other code simultaneously with your own scripts
        # also allows you to communicate and control this code, by called methods such as start and terminate
        # also provides features for implements concurrency in your applications
        # in this test, you can't call app.run method as usual because this method is blocking and will stop the tests from running
        # instead, you target which function to run
        self.process = multiprocessing.Process(target=app.run, kwargs={"port": 8080})
        
        self.process.start()
        # time.sleep(1) in order to pause for a second to allow server to start
        time.sleep(1)
    
    def test_login_correct(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")

    def test_login_incorrect(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")
    
    def tearDown(self):
        """ Test Teardown """
        # Remove the tables and their data from the database
        
        # Kill the server
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        # Exit the browser
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()