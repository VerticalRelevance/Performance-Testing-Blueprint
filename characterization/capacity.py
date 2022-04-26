import queue

from locust import TaskSet, task, HttpUser, constant_throughput, LoadTestShape

from components.category import Category


class UserTasks(TaskSet):
    """
    Build out the tasks that Locust will execute using the components or user journeys methods.
    """
    @task
    def get_category(self):
        Category(self.client).get_category()  # TODO: inject other components and user journeys
        DataCaptor.set_number_of_failures(self.user.environment.stats.num_failures)


class Configuration:
    """
    Config values in a single place that control the shape of the load
    """
    user_throughput = 1  # number of tasks every second per user
    time_limit = 300  # in seconds
    initial_number_of_users = 1
    spawn_rate = 1
    dwell = 10  # seconds to wait for an increase in number of users
    max_users = 50
    failure_rate_threshold = 2  # in failures per second
    action_on_failure = "back_off"


class DataCaptor:
    """
    I pass data between various concerns
    """
    _number_of_failures = 0
    _previous_number_of_failures = 0

    @classmethod
    def set_number_of_failures(cls, number_of_failures):
        cls._number_of_failures = number_of_failures

    @classmethod
    def calculate_failures_per_second(cls):
        failures_per_second = cls._number_of_failures - cls._previous_number_of_failures
        cls._previous_number_of_failures = cls._number_of_failures
        return failures_per_second


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
        failure_rate = DataCaptor.calculate_failures_per_second()

        if run_time > Configuration.time_limit:  # stop at end of time limit
            print("Time limit of {} seconds reached. Stopping run.".format(Configuration.time_limit))
            return None

        if self._number_of_users > Configuration.max_users: # stop when max users exceeded
            print("Max users exceeded. Stopping run at {} of {} users generated."
                  .format(self._number_of_users, Configuration.max_users))
            return None

        if failure_rate > Configuration.failure_rate_threshold:
            if Configuration.action_on_failure != "back_off":
                print("Failure rate exceeded threshold. Stopping run.")
                return None
            if self._tick_counter == Configuration.dwell:  # remove users if dwell reached
                if Configuration.spawn_rate == 1:
                    self._number_of_users -= 1
                    Configuration.spawn_rate = 0
                    self._tick_counter = 0
                    return self._number_of_users, Configuration.spawn_rate
                Configuration.spawn_rate /= 2
                self._number_of_users -= Configuration.spawn_rate
                self._tick_counter = 0
                return self._number_of_users, Configuration.spawn_rate

        if self._tick_counter == Configuration.dwell:  # add users if dwell reached
            Configuration.spawn_rate *= 2
            self._number_of_users += Configuration.spawn_rate
            self._tick_counter = 0
        self._tick_counter += 1

        return self._number_of_users, Configuration.spawn_rate
