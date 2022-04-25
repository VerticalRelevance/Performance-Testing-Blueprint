import random


class Category:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/category/{}?page={}"
        self.category_ids = ["all", "for-him", "for-her", "unisex"]
        self.pages = range(2)

    def get_category(self):
        category_id = random.choice(self.category_ids)
        page = random.choice(self.pages)
        path = self.endpoint.format(category_id, page)
        self.client.get(path, headers=self.headers)
