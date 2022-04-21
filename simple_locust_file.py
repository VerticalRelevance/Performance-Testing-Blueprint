from locust import HttpUser, task
from bs4 import BeautifulSoup


def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(attrs={"name": "_csrf"})["content"]


class GatlingDemoStore(HttpUser):
    host = "https://demostore.gatling.io"

    def login_store(self):
        login_data = {"username": "john", "password": "pass"}
        with self.client.get("/login", stream=True) as response:
            html = response.raw
            csrf = get_csrf_token(html)
            login_data["_csrf"] = csrf
        self.client.post("/login", data=login_data)

    @task
    def login_task(self):
        self.login_store()