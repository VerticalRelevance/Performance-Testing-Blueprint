class Categories:

    def __init__(self, client):
        self.client = client
        self.headers = {"accept": "application/json"}
        self.endpoint = "/api/category"

    def get_all(self):
        self.client.get(self.endpoint, headers=self.headers)
