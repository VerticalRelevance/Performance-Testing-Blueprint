import random


class Category:

    def __init__(self, client):
        self._client = client
        self._headers = {"accept": "application/json"}
        self._endpoint = "/category/{}?page={}"
        self._category_ids = ["all", "for-him", "for-her", "unisex"]

    def get_category(self):
        category_id = random.choice(self._category_ids)
        pages_list = range(4) if category_id == "all" else range(2)
        page = random.choice(pages_list)
        path = self._endpoint.format(category_id, page, name=self._endpoint)
        self._client.get(path, headers=self._headers)
