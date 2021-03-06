import random


class Cart:
    def __init__(self, client):
        self._client = client

    def add_to_cart(self):
        item = random.choice([17] + [x for x in range(19, 39)])
        path = "/cart/add/{}"
        self._client.get(path.format(item), name=path)

    def view_cart(self):
        self._client.get("/cart/view")

    def checkout(self):
        self._client.get("/cart/checkout")

    def clear_cart(self):
        self._client.get("/cart/clear")
