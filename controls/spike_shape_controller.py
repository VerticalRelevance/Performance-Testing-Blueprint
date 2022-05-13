from collections import namedtuple

CustomArgs = namedtuple('CustomArgs', [
    "spawn_rate",
    "steady_state_users",
    "steady_state_dwell",
    "spike_state_users",
    "spike_state_dwell"
])


class SpikeShapeController:

    def __init__(self):
        self.hasInitialized = False
        self._current_users = 0

    def calculate(self, args: CustomArgs):
        if not self.hasInitialized:
            self.hasInitialized = True
            return 0, args.spawn_rate
        if self._current_users < args.steady_state_users:
            self._current_users += args.spawn_rate
        return self._current_users, args.spawn_rate

