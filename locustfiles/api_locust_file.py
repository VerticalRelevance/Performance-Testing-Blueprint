from locust import HttpUser, task, between
from apis.categories import Categories


class AuthApi(HttpUser):
    host = "http://demostore.gatling.io"
    wait_time = between(0.5, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = Categories(self.client)

    @task
    def get_all(self):
        self.api.get_all()
