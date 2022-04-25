import random


class Product:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/product/{}"
        self.products_for_him = ["casual-black-blue", "black-and-red-glasses", "bright-yellow-glasses",
                                 "casual-brown-glasses", "deepest-blue", "light-blue-glasses",
                                 "sky-blue-case", "white-casual-case"]
        self.products_for_her = ["perfect-pink", "curved-black", "black-grey-curved", "black-light-blue", "curved-pink",
                                 "velvet-red", "deep-blue-ocean"]
        self.products_for_unisex = ["curved-brown", "leopard-skin", "gold-design", "pink-panther", "curve-ocean-sky",
                                    "plain-white", "white-leopard-pattern"]

    def _get_product(self, path):
        self.client.get(path, headers=self.headers)

    def get_product_for_him(self):
        product = random.choice(self.products_for_him)
        path = self.endpoint.format(product)
        self._get_product(path)

    def get_product_for_her(self):
        product = random.choice(self.products_for_her)
        path = self.endpoint.format(product)
        self._get_product(path)

    def get_product_for_unisex(self):
        product = random.choice(self.products_for_unisex)
        path = self.endpoint.format(product)
        self._get_product(path)
