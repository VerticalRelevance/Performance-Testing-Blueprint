from locust import TaskSet, task, HttpUser, constant_throughput, LoadTestShape, events

from website.user_journey import UserJourney


# TODO: fix these parameters. They don't work!
@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--steady-state",
        type=int,
        env_var="LOCUST_STEADY_STATE",
        default=1,
        help="Pick a 'high' number that will not cause failures.")

    parser.add_argument(
        "--user-increment",
        type=int,
        env_var="LOCUST_USER_INCREMENT",
        default=1,
        help="Number of users to increment up or down to inject or remove a spike. "
             "Pick a number of to add that will cause failures.")

    parser.add_argument(
        "--dwell",
        type=int,
        env_var="LOCUST_DWELL",
        default=1,
        help="Amount of time in seconds to wait before adding or removing users.")


class UserTasks(TaskSet):
    @task(1)
    def purchase(self):
        UserJourney(self.client).purchase_workflow()

    @task(5)
    def browse(self):
        UserJourney(self.client).browse_workflow()

    @task(2)
    def abandon(self):
        UserJourney(self.client).abandon_cart()


class DataCaptor:
    steady_state = 10
    user_increment = 10
    dwell = 10


class SpikeUser(HttpUser):
    wait_time = constant_throughput(1)
    host = "https://demostore.gatling.io"
    tasks = [UserTasks]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DataCaptor.steady_state = self.environment.parsed_options.steady_state
        DataCaptor.user_increment = self.environment.parsed_options.user_increment
        DataCaptor.dwell = self.environment.parsed_options.dwell


class SpikeTestShaper(LoadTestShape):
    def __init__(self):
        super().__init__()
        self._steady_state = DataCaptor.steady_state
        self._user_increment = DataCaptor.user_increment
        self._dwell = DataCaptor.dwell
        self._tick_counter = 0
        self._number_of_users = DataCaptor.steady_state

    def tick(self):
        self._tick_counter += 1
        if self._tick_counter >= self._dwell:
            self._tick_counter = 0
            if self._number_of_users == self._steady_state:
                self._number_of_users += self._user_increment
            else:
                self._number_of_users -= self._user_increment
        return self._number_of_users, self._user_increment

