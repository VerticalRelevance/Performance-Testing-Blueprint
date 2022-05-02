import sys

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
    user_dead_band: int


@dataclass
class ControllerState:
    previous_number_of_failures = 0
    #  TODO: consider change from tick counts to seconds for time calculations
    #  Locust tick is a little more than 1s. Will affect long runs.
    #  Might only affect dwells of around 1000s being off 10s of seconds
    tick_counter = 0  # 1 tick = 1 second
    isStopping = False
    isFirstBackOff = True
    isBackingOff = False
    failure_rate = 0
    max_users_without_fails = 0
    min_users_with_fails = sys.maxsize
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
        self._configuration = configuration
        self._state = ControllerState(
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
        self._state.tick_counter += 1
        self._check_stop_conditions(locust_state)
        if self._state.isStopping:
            return None
        self._calculate_number_of_users()
        return self._state.number_of_users, self._state.spawn_rate

    def _check_stop_conditions(self, locust_state):
        self._check_time_limit_exceeded(locust_state)
        self._check_max_users_exceeded()
        self._check_failure_rate_exceeded(locust_state)

    def _check_failure_rate_exceeded(self, locust_state):
        self._calculate_failure_rate(locust_state)
        if self._state.failure_rate > self._configuration.failure_rate_threshold:
            if self._configuration.is_enabled_back_off:
                return
            self.message = "Failure rate of {} per second exceeds threshold of {} per second. Stopping.".format(
                self._state.failure_rate, self._configuration.failure_rate_threshold)
            self._state.isStopping = True

    def _calculate_failure_rate(self, locust_state):
        self._state.failure_rate = locust_state.number_of_failures - self._state.previous_number_of_failures
        self._state.previous_number_of_failures = locust_state.number_of_failures

    def _check_max_users_exceeded(self):
        if self._state.number_of_users > self._configuration.max_number_of_users:
            self.message = "Max users exceeded. Stopping run at {} of {} users generated.".format(
                self._state.number_of_users, self._configuration.max_number_of_users)
            self._state.isStopping = True

    def _check_time_limit_exceeded(self, locust_state):
        if locust_state.run_time > self._configuration.time_limit:
            self.message = "Time limit of {} seconds exceeded. Stopping run.".format(self._configuration.time_limit)
            self._state.isStopping = True

    def _calculate_number_of_users(self):
        if self._state.tick_counter > self._state.dwell:
            self._state.tick_counter = 1
            self._update_history()
            if self._configuration.is_enabled_back_off \
                    and self._state.failure_rate > self._configuration.failure_rate_threshold:
                self._state.isBackingOff = True
                if self._state.isFirstBackOff:
                    self._state.isFirstBackOff = False
                    self._state.spawn_rate /= 2
                self._state.spawn_rate /= 2
                self._state.number_of_users -= self._state.spawn_rate
            else:
                if self._state.min_users_with_fails - self._state.max_users_without_fails <= \
                        self._configuration.user_dead_band:
                    return self._state.number_of_users, self._state.spawn_rate
                self._state.number_of_users += self._state.spawn_rate
                self._state.spawn_rate *= 2
                if self._state.isBackingOff and self._state.number_of_users >= self._state.min_users_with_fails:
                    self._state.number_of_users -= self._state.spawn_rate / 2
                    self._state.spawn_rate /= 4
                    self._state.number_of_users += self._state.spawn_rate

    def _update_history(self):
        if self._state.failure_rate == self._configuration.failure_rate_threshold \
                and self._state.number_of_users > self._state.max_users_without_fails:
            self._state.max_users_without_fails = self._state.number_of_users

        if self._state.failure_rate > self._configuration.failure_rate_threshold \
                and self._state.number_of_users < self._state.min_users_with_fails:
            self._state.min_users_with_fails = self._state.number_of_users
