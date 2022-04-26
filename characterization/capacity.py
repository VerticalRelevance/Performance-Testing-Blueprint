import math

from locust import TaskSet, task, HttpUser, constant_throughput, LoadTestShape
from components.category import Category


class UserTasks(TaskSet):
    """
    Build out the tasks that Locust will execute using the components or user journeys methods.
    """
    @task
    def get_category(self):
        Category(self.client).get_category()  # TODO: inject other components and user journeys


class WebsiteUser(HttpUser):
    """
    Define the load characteristics and specify tasks.
    """
    wait_time = constant_throughput(1)
    host = "https://demostore.gatling.io"
    tasks = [UserTasks]


class Capacity(LoadTestShape):
    """
    Define the load shape.
    """
    _time_limit = 120  # in seconds
    _number_of_users = 1

    def tick(self):  # TODO: need some insight into test results here to help dynamically calculate shape
        """
        Method that defines the shape at an instance of time, i.e. a "tick".
        :return: Tuple of number of users and spawn rate.
        """
        spawn_rate = 0.05  # dwell time baked in to < 1 spawn rate

        run_time = self.get_run_time()

        if run_time > self._time_limit:
            return None
        self._number_of_users += spawn_rate
        step_number_of_users = math.floor(self._number_of_users)
        return step_number_of_users, spawn_rate
