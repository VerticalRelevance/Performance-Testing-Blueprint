import random


class Cart:
    def __init__(self, client):
        self._client = client

    def add_to_cart(self):
        item = random.choice([17] + [x for x in range(19, 39)])
        self._client.get("/cart/add/{}".format(item))

    def view_cart(self):
        self._client.get("/cart/view")

    def checkout(self):
        self._client.get("/cart/checkout")

    def clear_cart(self):
        self._client.get("/cart/clear")
