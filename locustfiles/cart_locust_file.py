from locust import HttpUser, constant_throughput, task
from components.cart import Cart


class CartTest(HttpUser):
    host = "http://demostore.gatling.io"
    wait_time = constant_throughput(1)  # number of @tasks per second per user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cart = Cart(self.client)

    @task
    def add_to_cart(self):
        self._cart.add_to_cart()

    @task
    def view_cart(self):
        self._cart.view_cart()

    @task
    def checkout(self):
        self._cart.checkout()
