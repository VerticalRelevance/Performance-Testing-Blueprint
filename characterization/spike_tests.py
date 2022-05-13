from locust import TaskSet, task, HttpUser, constant_throughput, LoadTestShape, events

from website.user_journey import UserJourney


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--steady-state",
        type=int,
        env_var="LOCUST_STEADY_STATE",
        default=10,
        help="Pick a 'high' number that will not cause failures.")

    parser.add_argument(
        "--user-increment",
        type=int,
        env_var="LOCUST_USER_INCREMENT",
        default=10,
        help="Number of users to increment up or down to inject or remove a spike. "
             "Pick a number of to add that will cause failures.")

    parser.add_argument(
        "--dwell",
        type=int,
        env_var="LOCUST_DWELL",
        default=10,
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


class CustomArgs:
    steady_state = 0
    user_increment = 1
    dwell = 5


class SpikeUser(HttpUser):
    wait_time = constant_throughput(1)
    host = "https://demostore.gatling.io"
    tasks = [UserTasks]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CustomArgs.steady_state = self.environment.parsed_options.steady_state
        CustomArgs.user_increment = self.environment.parsed_options.user_increment
        CustomArgs.dwell = self.environment.parsed_options.dwell


class SpikeTestShaper(LoadTestShape):
    def __init__(self):
        super().__init__()
        self._tick_counter = 0
        self._number_of_users = 0

    def tick(self):
        self._tick_counter += 1
        if self._number_of_users < CustomArgs.steady_state:
            self._number_of_users = CustomArgs.steady_state
        elif self._tick_counter >= CustomArgs.dwell:
            self._tick_counter = 0
            if self._number_of_users == CustomArgs.steady_state:
                self._number_of_users += CustomArgs.user_increment
            else:
                self._number_of_users -= CustomArgs.user_increment
        return self._number_of_users, CustomArgs.user_increment

