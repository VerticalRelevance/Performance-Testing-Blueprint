from locust import HttpUser, task


class SimplePerformanceTest(HttpUser):
    host = "http://demostore.gatling.io"

    @task
    def get_all_categories(self):
        self.client.get("/api/category", headers={"accept": "application/json"})
