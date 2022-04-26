import random
import time

from utils.html_parser import get_csrf_token
from components.product import Product
from components.cart import Cart


class WebsiteUser:

    def __init__(self, client):
        self._client = client
        self._cart = Cart()
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

    def add_to_cart(self):
        self._cart.add_to_cart()

    def view_cart(self):
        self._cart.view_cart()

    def checkout(self):
        self._cart.checkout()

    def clear_cart(self):
        self._cart.clear_cart()
