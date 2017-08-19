from app import app
import unittest

class FlaskTestCase1(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="text/html")
        self.assertEqual(response.status_code, 200)

    def test_login_page_load(self):
        tester = app.test_client(self)
        response = tester.get("/login")
        self.assertIn("Please login", response.data)

    def test_login_page_incorret(self):
        tester = app.test_client(self)
        res = tester.post("/login", data=dict(username="wrong", password="wrong"), follow_redirects=True)
        self.assertIn("Invalid Credentials", res.data)

    def test_login_page_corret(self):
        tester = app.test_client(self)
        res = tester.post("/login", data=dict(username="admin", password="admin"), follow_redirects=True)
        self.assertIn("You were logged in", res.data)
     
    def test_logout(self):
        tester = app.test_client(self)
        tester.post("/login", data=dict(username="admin", password="admin"), follow_redirects=True)
        res = tester.get("/logout", follow_redirects=True)
        self.assertIn("You were logged out", res.data)

    def test_requires_login(self):
        tester = app.test_client(self)
        res = tester.get("/", follow_redirects=True)
        self.assertIn("You need to login first", res.data)

    def test_logout_requires_login(self):
        tester = app.test_client(self)
        res = tester.get("/logout", follow_redirects=True)
        self.assertIn("You need to login first", res.data)

    def test_posts_show_up_on_main_page(self):
        tester = app.test_client(self)
        res = tester.post("/login", data=dict(username="admin", password="admin"), follow_redirects=True)
        self.assertIn("Posts", res.data)

if __name__ == "__main__":
    unittest.main()
