import random


class Categories:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/api/category"

    def get_all(self):
        self.client.get(self.endpoint, headers=self.headers)

    def get_by_id(self):
        category_id = random.choice([5, 6, 7])
        self.client.get(self.endpoint + "/{}".format(category_id), headers=self.headers)
