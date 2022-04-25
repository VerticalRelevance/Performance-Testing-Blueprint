from locust import HttpUser, task, constant_throughput
from components.category import Category


class CategoryTester(HttpUser):
    host = "http://demostore.gatling.io"
    wait_time = constant_throughput(1)  # number of @tasks per second per user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = Category(self.client)

    @task
    def get_all(self):
        self.categories.get_category()
