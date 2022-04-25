import random
import time

from locust import HttpUser, task, between
from demo_store_constants import ProductCategories
from website.website_user import WebsiteUser


class WebsiteRunner(HttpUser):
    host = "https://demostore.gatling.io"
    wait_time = between(0.5, 2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = WebsiteUser(self.client)

    @task
    def login_task(self):
        self.user.login_store()

    @task
    def get_all_products_task(self):
        self.user.get_products_in_category(ProductCategories.all)

    @task
    def purchase_workflow(self):
        self.user.get_products_in_category(ProductCategories.all)
        time.sleep(1)
        item = random.randint(19, 25)
        self.user.add_to_cart(item)
        time.sleep(0.5)
        self.user.view_cart()
        time.sleep(0.5)
        self.user.checkout()
        time.sleep(0.5)

    @task
    def browse_workflow(self):
        self.user.get_products_in_category(ProductCategories.for_him)
        time.sleep(2)
        available_products = ["casual-black-blue", "black-and-red-glasses"]
        item_key = random.choice(available_products)
        self.user.get_product(item_key)
        time.sleep(0.5)
        available_products = ["casual-black-blue", "black-and-red-glasses"]
        item_key = random.choice(available_products)
        self.user.get_product(item_key)
        time.sleep(0.5)
