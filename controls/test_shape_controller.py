from controls.load_shape_controller import LoadShapeController, Configuration, ControllerState, LocustState


def build_default_configuration():
    return Configuration(1)


class TestLoadShapeController:

    def test_user_throughput_equals_1(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)

        assert 1 == shaper.configuration.user_throughput

    def test_calculate_returns_message_none_when_time_limit_not_exceeded(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(1)

        shaper.calculate(locust_state)

        assert None is shaper.message

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

        assert None is number_users_spawn_rate_tuple

    def test_calculate_returns_number_of_users_and_spawn_rate(self):
        config = build_default_configuration()
        initial_state = ControllerState()
        shaper = LoadShapeController(config, initial_state)
        locust_state = LocustState(0)

        number_users_spawn_rate_tuple = shaper.calculate(locust_state)

        assert (1, 1) == number_users_spawn_rate_tuple
