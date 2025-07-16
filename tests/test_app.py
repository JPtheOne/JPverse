

from app import app, TimelinePost
import unittest
import os
os.environ['TESTING'] = 'true'


from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            TimelinePost.delete().execute()



    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Juan Pablo Morales</title>" in html

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "pp.jpg" in html


    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
        
        
    def test_new_post(self):
        response = self.client.post("/api/timeline_post", data={
            "name": "Juan",
            "email": "juan@example.com",
            "content": "Test post content"
        })
        assert response.status_code == 200
        json = response.get_json()
        assert "id" in json
        assert json["name"] == "Juan"
        assert json["email"] == "juan@example.com"
        assert json["content"] == "Test post content"
        
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Juan"
        
    def test_new_post(self):
        resp = self.client.post(
            "/api/timeline_post",
            data={"name": "Juan", "email": "juan@example.com", "content": "Test post content"},
            content_type="application/x-www-form-urlencoded",
        )


        assert resp.status_code == 200
        created = resp.get_json()
        assert "id" in created
        assert created["name"] == "Juan"
        assert created["email"] == "juan@example.com"
        assert created["content"] == "Test post content"

       
        resp = self.client.get("/api/timeline_post")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["timeline_posts"]) == 1
        assert data["timeline_posts"][0]["name"] == "Juan"

    def test_timeline_page(self):
        resp = self.client.get("/timeline")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "Timeline" in html      
        

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data=
                                    {"name": "", "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html


        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email":"john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html


        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

