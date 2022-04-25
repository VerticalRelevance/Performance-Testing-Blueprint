import random


class Categories:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/api/category"
        self.category_ids = [5, 6, 7]

    def get_all(self):
        self.client.get(self.endpoint, headers=self.headers)

    def get_by_id(self):
        category_id = random.choice(self.category_ids)
        self.client.get(self.endpoint + "/{}".format(category_id), headers=self.headers)
