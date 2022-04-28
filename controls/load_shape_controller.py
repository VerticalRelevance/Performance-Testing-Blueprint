from dataclasses import dataclass


@dataclass
class LocustState:
    run_time: int


@dataclass
class Configuration:
    """
    Stores configuration for load shap controller
    """
    user_throughput = 1
    time_limit: int  # seconds


@dataclass
class ControllerState:
    unused: str


class LoadShapeController:
    """
    State variables:
    tick_counter: Used to calculate dwell. 1 tick = 1 second from locust docs
    is_backing_off: True -> ramp down. False -> ramp up
    failure_rate
    number_of_users: number of users present in system generating load (concurrency)
    spawn_rate:
    initial_dwell:

    Configuration variables:
    user_throughput: number of tasks every second per user
    time_limit: Run finishes when exceeded
    initial_number_of_users
    initial_spawn_rate: number of users to add or remove at a time
    initial_dwell: number of seconds to wait for a possible change in number of users
    max_users: Run finishes when exceeded
    failure_rate_threshold: Stop run or ramp down when exceeded. See action_on_failure.
    action_on_failure: 'back_off' -> ramp down when failure_rate_threshold is exceeded. any other value -> stop
    """

    def __init__(self, configuration: Configuration, initial_state: ControllerState):
        self.message = None
        self.configuration = configuration
        self.state = initial_state

    def calculate(self, locust_state: LocustState):
        """
        Uses locust_state, controller_state, and configuration to calculate the number of users and spawn rate.
        Intended to be used inside Locust's LoadTestShape class tick method.
        :param locust_state: state managed by locust
        :return: A tuple of: (number_of_users, spawn_rate). The tick method inside Locust's LoadTestShape returns this.
        """
        if locust_state.run_time > self.configuration.time_limit:
            self.message = "Time limit of {} seconds exceeded. Stopping run.".format(self.configuration.time_limit)
        return None
