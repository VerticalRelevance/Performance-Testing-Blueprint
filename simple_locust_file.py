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

    def get_all_products(self):
        self.client.get("/category/all")

    def add_to_cart(self, item_number):
        self.client.get("/cart/add/{}".format(item_number), name="/cart/add/{item}")

    def view_cart(self):
        self.client.get("/cart/view")

    def checkout(self):
        self.client.get("/cart/checkout")

    def clear_cart(self):
        self.client.get("/cart/clear")

    @task
    def login_task(self):
        self.login_store()

    @task
    def get_all_products_task(self):
        self.get_all_products()

    @task
    def purchase_workflow(self):  # flow enforced by website
        self.get_all_products()
        item = random.randint(19, 25)
        self.add_to_cart(item)
        self.view_cart()
        self.checkout()
