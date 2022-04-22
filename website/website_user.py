import time

from utils.html_parser import get_csrf_token


class WebsiteUser:

    def __init__(self, client):
        self.client = client

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
