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
        self._tick_counter = 0
        self.hasInitialized = False
        self._current_users = 0
        self._state = "Not Initialized"
        self.state_dictionary = {
            "Not Initialized": self.not_initialized,
            "Ramping To Steady State": self.ramping_to_steady_state,
            "Idling At Steady State": self.idling_at_steady_state,
            "Ramping To Spike State": self._ramping_to_spike_state,
            "Idling At Spike State": self._idling_at_spike_state
        }

    def calculate(self, args: CustomArgs):
        self.state_dictionary[self._state](args)
        return self._current_users, args.spawn_rate

    def not_initialized(self, args):
        self._state = "Ramping To Steady State"

    def ramping_to_steady_state(self, args: CustomArgs):
        self._current_users += args.spawn_rate
        if self._current_users > args.steady_state_users:
            self._current_users = args.steady_state_users
        if self._current_users == args.steady_state_users:
            self._state = "Idling At Steady State"

    def idling_at_steady_state(self, args:CustomArgs):
        self._tick_counter += 1
        if args.steady_state_dwell - 1 == self._tick_counter:
            self._state = "Ramping To Spike State"

    def _ramping_to_spike_state(self, args:CustomArgs):
        if self._current_users == args.spike_state_users:
            self._state = "Idling At Spike State"
        else:
            self._current_users += 1

    def _idling_at_spike_state(self, args: CustomArgs):
        pass
