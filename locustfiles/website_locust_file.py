import random
import time

from locust import HttpUser, task, between
from website.website_user import WebsiteUser


class WebsiteRunner(HttpUser):
    host = "https://demostore.gatling.io"
    wait_time = between(0.5, 2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = WebsiteUser(self.client)

    @task
    def login_task(self):
        self._user.login_store()

    @task
    def get_some_product(self):
        self._user.get_random_product()

    @task
    def purchase_workflow(self):
        self._user.get_random_product()
        time.sleep(1)
        self._user.add_to_cart()
        time.sleep(0.5)
        self._user.view_cart()
        time.sleep(0.5)
        self._user.checkout()
        time.sleep(0.5)

    @task
    def browse_workflow(self):
        self._user.get_random_product()
        time.sleep(2)
        self._user.get_random_product()
        time.sleep(0.5)
        self._user.get_random_product()
        time.sleep(0.5)
