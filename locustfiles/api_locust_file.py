from locust import HttpUser, task, constant_throughput
from apis.categories import Categories


class AuthApi(HttpUser):
    host = "http://demostore.gatling.io"
    wait_time = constant_throughput(1)  # number of requests per second per user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = Categories(self.client)

    @task
    def get_all(self):
        self.api.get_all()

    @task
    def get_by_id(self):
        self.api.get_by_id()
