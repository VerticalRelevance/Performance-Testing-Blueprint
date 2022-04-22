import random
import time

from locust import HttpUser, task, between
from demo_store_constants import ProductCategories
from utils.html_parser import get_csrf_token


class StorefrontUser(HttpUser):
    host = "https://demostore.gatling.io"
    wait_time = between(0.5, 2)

    def login_store(self):
        login_data = {"username": "john", "password": "pass"}
        with self.client.get("/login", stream=True) as response:
            html = response.raw
            csrf = get_csrf_token(html)
            login_data["_csrf"] = csrf
        time.sleep(0.1)
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
        time.sleep(1)
        item = random.randint(19, 25)
        self.add_to_cart(item)
        time.sleep(0.5)
        self.view_cart()
        time.sleep(0.5)
        self.checkout()
        time.sleep(0.5)

    @task
    def browse_workflow(self):
        self.get_products_in_category(ProductCategories.for_him)
        time.sleep(2)
        available_products = ["casual-black-blue", "black-and-red-glasses"]
        item_key = random.choice(available_products)
        self.get_product(item_key)
        time.sleep(0.5)
        available_products = ["casual-black-blue", "black-and-red-glasses"]
        item_key = random.choice(available_products)
        self.get_product(item_key)
        time.sleep(0.5)
