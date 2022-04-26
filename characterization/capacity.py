from datetime import datetime
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


class Configuration:
    user_throughput = 1  # number of tasks every second per user
    time_limit = 300  # in seconds
    initial_number_of_users = 1
    spawn_rate = 9001  # no-op? Used only for printing to console?
    user_step = 1
    dwell = 10  # seconds to wait for an increase in number of users
    max_users = 20


class WebsiteUser(HttpUser):
    """
    Define the load characteristics and specify tasks.
    """
    wait_time = constant_throughput(Configuration.user_throughput)
    host = "https://demostore.gatling.io"
    tasks = [UserTasks]


class Capacity(LoadTestShape):
    """
    Define the load shape.
    """
    _number_of_users = Configuration.initial_number_of_users
    _tick_counter = 0

    # TODO: need some insight into test results here to help dynamically calculate shape
    def tick(self):  # 1 tick = 1s
        """
        Method that defines the shape at an instance of time, i.e. a "tick".
        :return: Tuple of number of users and spawn rate.
        """
        run_time = self.get_run_time()

        if run_time > Configuration.time_limit:  # stop at end of time limit
            return None
        if self._number_of_users == Configuration.max_users:
            return None
        if self._tick_counter == Configuration.dwell:  # add users if dwell reached
            self._number_of_users += Configuration.user_step
            self._tick_counter = 0
        self._tick_counter += 1
        return self._number_of_users, Configuration.spawn_rate
