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
    max_number_of_users: int  # number of users to not exceed
    time_limit: int  # seconds
    failure_rate_threshold: int  # failures per second
    is_enabled_back_off: bool


@dataclass
class ControllerState:
    previous_number_of_failures = 0
    #  TODO: consider change from tick counts to seconds for time calculations
    #  Locust tick is a little more than 1s. Will affect long runs.
    #  Might only affect dwells of around 1000s being off 10s of seconds
    tick_counter = 0  # 1 tick = 1 second
    isStopping = False
    isFirstBackOff = True
    failure_rate = 0
    number_of_users: int
    spawn_rate: int
    dwell: int


class LoadShapeController:
    """
    State variables:
    is_backing_off: True -> ramp down. False -> ramp up

    Configuration variables:
    action_on_failure: 'back_off' -> ramp down when failure_rate_threshold is exceeded. any other value -> stop
    """

    def __init__(self, configuration: Configuration):
        self.message = None
        self.configuration = configuration
        self.state = ControllerState(
            configuration.initial_number_of_users,
            configuration.initial_spawn_rate,
            configuration.initial_dwell)

    def calculate(self, locust_state: LocustState):
        """
        Uses locust_state, controller_state, and configuration to calculate the number of users and spawn rate.
        Intended to be used inside Locust's LoadTestShape class tick method.
        :param locust_state: state managed by locust
        :return: A tuple of: (number_of_users, spawn_rate). The tick method inside Locust's LoadTestShape returns this.
        """
        self.state.tick_counter += 1
        self.check_stop_conditions(locust_state)
        if self.state.isStopping:
            return None
        self.calculate_number_of_users()
        return self.state.number_of_users, self.state.spawn_rate

    def check_stop_conditions(self, locust_state):
        self.check_time_limit_exceeded(locust_state)
        self.check_max_users_exceeded()
        self.check_failure_rate_exceeded(locust_state)

    def check_failure_rate_exceeded(self, locust_state):
        self.state.failure_rate = locust_state.number_of_failures - self.state.previous_number_of_failures
        self.state.previous_number_of_failures = locust_state.number_of_failures
        if self.state.failure_rate > self.configuration.failure_rate_threshold:
            if self.configuration.is_enabled_back_off:
                return
            self.message = "Failure rate of {} per second exceeds threshold of {} per second. Stopping.".format(
                self.state.failure_rate, self.configuration.failure_rate_threshold)
            self.state.isStopping = True

    def check_max_users_exceeded(self):
        if self.state.number_of_users > self.configuration.max_number_of_users:
            self.message = "Max users exceeded. Stopping run at {} of {} users generated.".format(
                self.state.number_of_users, self.configuration.max_number_of_users)
            self.state.isStopping = True

    def check_time_limit_exceeded(self, locust_state):
        if locust_state.run_time > self.configuration.time_limit:
            self.message = "Time limit of {} seconds exceeded. Stopping run.".format(self.configuration.time_limit)
            self.state.isStopping = True

    def calculate_number_of_users(self):
        if self.state.tick_counter > self.state.dwell:
            self.state.tick_counter = 1
            if self.configuration.is_enabled_back_off and self.state.failure_rate > 0:
                if self.state.isFirstBackOff:
                    self.state.isFirstBackOff = False
                    self.state.spawn_rate /= 2
                self.state.spawn_rate /= 2
                self.state.number_of_users -= self.state.spawn_rate
                return
            self.state.number_of_users += self.state.spawn_rate
            self.state.spawn_rate *= 2
