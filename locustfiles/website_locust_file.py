from locust import HttpUser, task, between

from website.user_journey import UserJourney


class WebsiteRunner(HttpUser):
    host = "https://demostore.gatling.io"
    wait_time = between(0.5, 2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_journey = UserJourney(self.client)

    @task
    def purchase_workflow(self):
        self._user_journey.purchase_workflow()

    @task
    def browse_workflow(self):
        self._user_journey.browse_workflow()

    @task
    def abandon_cart(self):
        self._user_journey.abandon_cart()
