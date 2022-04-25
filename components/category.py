import random


class Category:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/category/{}?page={}"
        self.category_ids = ["all", "for-him", "for-her", "unisex"]

    def get_category(self):
        category_id = random.choice(self.category_ids)
        pages_list = range(4) if category_id == "all" else range(2)
        page = random.choice(pages_list)
        path = self.endpoint.format(category_id, page)
        self.client.get(path, headers=self.headers)
