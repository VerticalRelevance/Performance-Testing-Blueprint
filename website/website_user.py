import random
import time

from utils.html_parser import get_csrf_token
from components.product import Product


class WebsiteUser:

    def __init__(self, client):
        self.client = client
        self.product = Product(client)
        self.get_product_by_category = [
            self.product.get_product_for_him,
            self.product.get_product_for_her,
            self.product.get_product_for_unisex]

    def login_store(self):
        login_data = {"username": "john", "password": "pass"}
        with self.client.get("/login", stream=True) as response:
            html = response.raw
            csrf = get_csrf_token(html)
            login_data["_csrf"] = csrf
        time.sleep(0.1)
        self.client.post("/login", data=login_data)

    def get_products_in_category(self):
        random.choice(self.get_product_by_category)()

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
