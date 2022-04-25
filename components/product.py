import random


class Product:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/product/{}"
        self.products_for_him = ["casual-black-blue", "black-and-red-glasses", "bright-yellow-glasses",
                                 "casual-brown-glasses", "deepest-blue", "light-blue-glasses",
                                 "sky-blue-case", "white-casual-case"]

    def get_product_for_him(self):
        product = random.choice(self.products_for_him)
        path = self.endpoint.format(product)
        self.client.get(path, headers=self.headers)
