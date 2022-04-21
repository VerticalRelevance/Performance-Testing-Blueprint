import random

from locust import HttpUser, task
from bs4 import BeautifulSoup


def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    csrf_tag = soup.find(attrs={"name": "_csrf"})
    if csrf_tag:
        return csrf_tag["content"]
    return ""


class GatlingDemoStore(HttpUser):
    host = "https://demostore.gatling.io"

    def login_store(self):
        login_data = {"username": "john", "password": "pass"}
        with self.client.get("/login", stream=True) as response:
            html = response.raw
            csrf = get_csrf_token(html)
            login_data["_csrf"] = csrf
        self.client.post("/login", data=login_data)

    def get_category(self):
        self.client.get("/category/all")

    def add_to_cart(self, item_number):
        self.client.get("/cart/add/{}".format(item_number), name="/cart/add/{item}")

    @task
    def login_task(self):
        self.login_store()

    @task
    def get_category_task(self):
        self.get_category()

    @task
    def add_to_cart_task(self):
        item = random.randint(19, 25)
        self.add_to_cart(item)
