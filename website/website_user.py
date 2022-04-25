import random
import time

from utils.html_parser import get_csrf_token
from components.product import Product


class WebsiteUser:

    def __init__(self, client):
        self._client = client
        self._product = Product(client)
        self._get_product = [
            self._product.get_product_for_him,
            self._product.get_product_for_her,
            self._product.get_product_for_unisex]

    def login_store(self):
        login_data = {"username": "john", "password": "pass"}
        with self._client.get("/login", stream=True) as response:
            html = response.raw
            csrf = get_csrf_token(html)
            login_data["_csrf"] = csrf
        time.sleep(0.1)
        self._client.post("/login", data=login_data)

    def get_random_product(self):
        random.choice(self._get_product)()

    def add_to_cart(self, item_number):
        self._client.get("/cart/add/{}".format(item_number), name="/cart/add/{item}")

    def view_cart(self):
        self._client.get("/cart/view")

    def checkout(self):
        self._client.get("/cart/checkout")

    def clear_cart(self):
        self._client.get("/cart/clear")
