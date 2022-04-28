from dataclasses import dataclass


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

    def __init__(self, configuration, initial_state):
        self.configuration = configuration
        self.state = initial_state

    def is_time_limit_exceeded(self, run_time):
        return run_time > self.configuration.time_limit


@dataclass
class Configuration:
    time_limit: int  # seconds


@dataclass
class State:
    unused: str
