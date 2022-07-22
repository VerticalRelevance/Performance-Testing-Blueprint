from locust import TaskSet, task, HttpUser, constant_throughput, LoadTestShape

from components.category import Category
from controls.capacity_finder_shape_controller import Configuration, LocustState, LoadShapeController

config = Configuration(
    initial_number_of_users=1,
    initial_spawn_rate=1,
    initial_dwell=10,
    max_number_of_users=50,
    time_limit=300,
    failure_rate_threshold=0,
    is_enabled_tuning=True,
    user_dead_band=1
)


class DataCaptor:
    """
    I pass data between various concerns
    """
    number_of_failures = 0


class UserTasks(TaskSet):
    """
    Build out the tasks that Locust will execute using the components or user journeys method.
    """

    @task
    def get_category(self):
        Category(self.client).get_category()
        DataCaptor.number_of_failures = self.user.environment.stats.num_failures


class WebSiteUser(HttpUser):
    """
    Define the load characteristics and specify tasks.
    """
    wait_time = constant_throughput(config.user_throughput)
    host = "https://demostore.gatling.io"
    tasks = [UserTasks]


class LoadShaper(LoadTestShape):
    def __init__(self):
        super().__init__()
        self.shaper = LoadShapeController(config)

    def tick(self):
        locust_state = LocustState(self.get_run_time(), DataCaptor.number_of_failures)
        number_of_users_and_spawn_rate_tuple = self.shaper.calculate(locust_state)
        if self.shaper.message:
            print(self.shaper.message)
        return number_of_users_and_spawn_rate_tuple
