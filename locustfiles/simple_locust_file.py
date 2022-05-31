from locust import HttpUser, task, constant_throughput


class SimplePerformanceTest(HttpUser):
    """
    Extend HttpUser class. This class has the httpclient on it that is used to send http requests.
    """

    # Specify the host to attack here
    host = "http://demostore.gatling.io"
    wait_time = constant_throughput(1)  # number of @tasks per second per user

    # The @task annotation is used to tell Locust what the test methods are. Note the use of self.client inside the
    # test method to send http requests.
    @task
    def get_all_categories(self):
        self.client.get("/api/category", headers={"accept": "application/json"})
