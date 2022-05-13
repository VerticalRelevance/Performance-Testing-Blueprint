class CustomArgs:
    spawn_rate = 1  # number of users to add or remove at a time
    steady_state_users = 2  # number of users to sit at that does not cause failures
    steady_state_dwell = 2  # amount of time in seconds to dwell at the steady state before spiking
    spike_state_users = 3  # number of users to increase to at a spike should cause failures
    spike_state_dwell = 1  # amount of time in seconds to dwell at the spike state before returning to steady


class SpikeShapeController:

    def __init__(self):
        self.hasInitialized = False
        self._current_users = 0

    def calculate(self, args):
        if not self.hasInitialized:
            self.hasInitialized = True
            return 0, args.spawn_rate
        if self._current_users < args.steady_state_users:
            self._current_users += args.spawn_rate
        return self._current_users, args.spawn_rate

