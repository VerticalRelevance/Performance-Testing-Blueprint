from locust import HttpUser, task
from bs4 import BeautifulSoup


def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(attrs={"name": "_csrf"})["content"]


class GatlingDemoStore(HttpUser):
    host = "https://demostore.gatling.io"

    @task
    def login(self):
        csrf = None
        login_data = {"username": "john", "password": "pass"}
        with self.client.get("/login", stream=True) as response:
            if not csrf:
                html = response.raw
                csrf = get_csrf_token(html)
                login_data["_csrf"] = csrf
        self.client.post("/login", data=login_data)
