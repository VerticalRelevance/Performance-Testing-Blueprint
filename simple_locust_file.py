import random

from bs4 import BeautifulSoup
from locust import HttpUser, task
from demo_store_constants import ProductCategories


def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    csrf_tag = soup.find(attrs={"name": "_csrf"})
    if csrf_tag:
        return csrf_tag["content"]
    return ""


class GatlingDemoStoreUser(HttpUser):
    host = "https://demostore.gatling.io"

    def login_store(self):
        login_data = {"username": "john", "password": "pass"}
        with self.client.get("/login", stream=True) as response:
            html = response.raw
            csrf = get_csrf_token(html)
            login_data["_csrf"] = csrf
        self.client.post("/login", data=login_data)

    def get_products_in_category(self, category):
        self.client.get("/category/{}".format(category))

    def get_product(self, item):
        self.client.get("/product/{}".format(item), name="/product/{}")

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
        self.get_products_in_category(ProductCategories.all)

    # should probably add some waits to these workflows
    @task
    def purchase_workflow(self):  # flow enforced by website
        self.get_products_in_category(ProductCategories.all)
        item = random.randint(19, 25)
        self.add_to_cart(item)
        self.view_cart()
        self.checkout()

    @task
    def browse_workflow(self):
        self.get_products_in_category(ProductCategories.for_him)
        available_products = ["casual-black-blue", "black-and-red-glasses"]
        item_key = random.choice(available_products)
        self.get_product(item_key)
