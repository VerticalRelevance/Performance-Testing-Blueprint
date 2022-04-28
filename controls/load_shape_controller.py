from dataclasses import dataclass


@dataclass
class LocustState:
    run_time: int
    number_of_failures: int


@dataclass
class Configuration:
    """
    Stores configuration for load shap controller
    """
    user_throughput = 1
    initial_number_of_users: int
    initial_spawn_rate: int  # number of users to increase at a time
    initial_dwell: int  # number of seconds to hold before changing number of users
    max_number_if_users: int  # number of users to not exceed
    time_limit: int  # seconds
    failure_rate_threshold: int  # failures per second


@dataclass
class ControllerState:
    previous_number_of_failures = 0
    #  TODO: consider change from tick counts to seconds for time calculations
    #  Locust tick is a little more than 1s. Will affect long runs.
    #  Might only affect dwells of around 1000s being off 10s of seconds
    tick_counter = 0 # 1 tick = 1 second
    number_of_users: int
    spawn_rate: int
    dwell: int


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
    initial_dwell: number of seconds to wait for a possible change in number of users
    action_on_failure: 'back_off' -> ramp down when failure_rate_threshold is exceeded. any other value -> stop
    """

    def __init__(self, configuration: Configuration):
        self.message = None
        self.configuration = configuration
        self.state = ControllerState\
            (configuration.initial_number_of_users,
             configuration.initial_spawn_rate,
             configuration.initial_dwell)

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

        if self.state.number_of_users > self.configuration.max_number_if_users:
            self.message = "Max users exceeded. Stopping run at {} of {} users generated.".format(
                self.state.number_of_users, self.configuration.max_number_if_users)
            return None

        failure_rate = locust_state.number_of_failures - self.state.previous_number_of_failures
        self.state.previous_number_of_failures = locust_state.number_of_failures
        if failure_rate > self.configuration.failure_rate_threshold:
            self.message = "Failure rate of {} per second exceeds threshold of {} per second. Stopping.".format(
                failure_rate, self.configuration.failure_rate_threshold)
            return None

        if self.state.tick_counter >= self.state.dwell:
            self.state.number_of_users += self.state.spawn_rate
        self.state.tick_counter += 1
        return self.state.number_of_users, self.state.spawn_rate
