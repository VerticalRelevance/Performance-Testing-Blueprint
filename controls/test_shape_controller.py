from controls.load_shape_controller import LoadShapeController, Configuration, ControllerState, LocustState


def build_default_configuration():
    return Configuration(1, 1, 1, 1)


class TestLoadShapeController:

    def test_user_throughput_equals_1(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)  # TODO: should not take initial state object

        assert shaper.configuration.user_throughput == 1

    def test_calculate_returns_message_none_when_time_limit_not_exceeded(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(1)

        shaper.calculate(locust_state)

        assert shaper.message is None

    def test_calculate_returns_message_time_exceeded_when_time_limit_has_exceeded(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(2)

        shaper.calculate(locust_state)

        assert "Time limit of 1 seconds exceeded. Stopping run." == shaper.message

    def test_calculate_stops_load_generation_when_time_limit_has_exceeded(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(2)

        number_users_spawn_rate_tuple = shaper.calculate(locust_state)

        assert number_users_spawn_rate_tuple is None

    def test_calculate_returns_number_of_users_and_spawn_rate(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(0)

        number_users_spawn_rate_tuple = shaper.calculate(locust_state)

        assert number_users_spawn_rate_tuple == (1, 1)

    def test_calculate_returns_message_when_number_max_users_exceeded(self):
        config = build_default_configuration()
        config.max_number_if_users = 0
        config.initial_number_of_users = 1
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(0)

        shaper.calculate(locust_state)

        assert shaper.message == "Max users exceeded. Stopping run at 1 of 0 users generated."

    def test_calculate_returns_stops_load_generation_when_number_max_users_exceeded(self):
        config = build_default_configuration()
        config.max_number_if_users = 0
        config.initial_number_of_users = 1
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(0)

        number_users_spawn_rate_tuple = shaper.calculate(locust_state)

        assert number_users_spawn_rate_tuple is None
