import random


class Category:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/category/{}"
        self.category_ids = ["all", "for-him", "for-her", "unisex"]

    def get_category(self):
        category_id = random.choice(self.category_ids)
        path = self.endpoint.format(category_id)
        self.client.get(path, headers=self.headers)
