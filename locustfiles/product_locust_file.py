from locust import HttpUser, task, constant_throughput
from components.product import Product


class ProductsTester(HttpUser):
    host = "http://demostore.gatling.io"
    wait_time = constant_throughput(1)  # number of @tasks per second per user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._product = Product(self.client)

    @task
    def get_product_for_him(self):
        self._product.get_product_for_him()

    @task
    def get_product_for_her(self):
        self._product.get_product_for_her()

    @task
    def get_product_for_unisex(self):
        self._product.get_product_for_unisex()
