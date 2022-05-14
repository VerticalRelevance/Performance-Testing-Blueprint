from locust import TaskSet, task, HttpUser, constant_throughput, LoadTestShape, events

from controls.spike_shape_controller import CustomArgs, SpikeShapeController
from website.user_journey import UserJourney


custom_args = None


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--spike-spawn-rate",
        type=int,
        env_var="LOCUST_SPIKE_SPAWN_RATE",
        default=10,
        help="Number of users to add or remove per second.")

    parser.add_argument(
        "--steady-state-users",
        type=int,
        env_var="LOCUST_STEADY_STATE",
        default=12,
        help="Pick a 'high' number that will not cause failures.")

    parser.add_argument(
        "--steady-state-dwell",
        type=int,
        env_var="LOCUST_STEADY_STATE_DWELL",
        default=10,
        help="Number of seconds to idle at steady state users.")

    parser.add_argument(
        "--spike-state-users",
        type=int,
        env_var="LOCUST_SPIKE_USERS",
        default=22,
        help="Pick a number that will cause failures.")

    parser.add_argument(
        "--spike-state-dwell",
        type=int,
        env_var="LOCUST_SPIKE_STATE_DWELL",
        default=5,
        help="Number of seconds to idle at spike state users.")


@events.test_start.add_listener
def _(environment, **kwargs):
    global custom_args
    custom_args = CustomArgs(
        environment.parsed_options.spike_spawn_rate,
        environment.parsed_options.steady_state_users,
        environment.parsed_options.steady_state_dwell,
        environment.parsed_options.spike_state_users,
        environment.parsed_options.spike_state_dwell
    )


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


class ArgCaptor:
    spawn_rate = 1
    steady_state_users = 0
    steady_state_dwell = 1
    spike_state_users = 5
    spike_state_dwell = 1


class SpikeUser(HttpUser):
    wait_time = constant_throughput(1)
    host = "https://demostore.gatling.io"
    tasks = [UserTasks]


class SpikeTestShaper(LoadTestShape):
    def __init__(self):
        super().__init__()
        self._tick_counter = 0
        self._number_of_users = 0
        self.shaper = SpikeShapeController()

    def tick(self):
        global custom_args
        if custom_args is None:
            return 0,1
        return self.shaper.calculate(custom_args)
