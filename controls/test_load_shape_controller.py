from controls.load_shape_controller import LoadShapeController, Configuration, LocustState


def build_default_configuration():
    return Configuration(
        initial_number_of_users=1,
        initial_spawn_rate=1,
        initial_dwell=10,
        max_number_of_users=10,
        time_limit=10,
        failure_rate_threshold=0,
        is_enabled_back_off=False)


class TestLoadShapeController:

    def test_user_throughput_equals_1(self):
        config = build_default_configuration()
        shaper = LoadShapeController(config)

        assert shaper.configuration.user_throughput == 1

    def test_calculate_returns_message_none_when_time_limit_not_exceeded(self):
        config = build_default_configuration()
        shaper = LoadShapeController(config)
        locust_state = LocustState(1, 0)

        shaper.calculate(locust_state)

        assert shaper.message is None

    def test_calculate_returns_message_time_exceeded_when_time_limit_has_exceeded(self):
        config = build_default_configuration()
        config.time_limit = 1
        shaper = LoadShapeController(config)
        locust_state = LocustState(2, 0)

        shaper.calculate(locust_state)

        assert "Time limit of 1 seconds exceeded. Stopping run." == shaper.message

    def test_calculate_stops_load_generation_when_time_limit_has_exceeded(self):
        config = build_default_configuration()
        config.time_limit = 1
        shaper = LoadShapeController(config)
        locust_state = LocustState(2, 0)

        number_users_spawn_rate_tuple = shaper.calculate(locust_state)

        assert number_users_spawn_rate_tuple is None

    def test_calculate_returns_number_of_users_and_spawn_rate(self):
        config = build_default_configuration()
        shaper = LoadShapeController(config)
        locust_state = LocustState(0, 0)

        number_users_spawn_rate_tuple = shaper.calculate(locust_state)

        assert number_users_spawn_rate_tuple == (1, 1)

    def test_calculate_returns_message_when_number_max_users_exceeded(self):
        config = build_default_configuration()
        config.max_number_of_users = 0
        config.initial_number_of_users = 1
        shaper = LoadShapeController(config)
        locust_state = LocustState(0, 0)

        shaper.calculate(locust_state)

        assert shaper.message == "Max users exceeded. Stopping run at 1 of 0 users generated."

    def test_calculate_returns_stops_load_generation_when_number_max_users_exceeded(self):
        config = build_default_configuration()
        config.max_number_of_users = 0
        config.initial_number_of_users = 1
        shaper = LoadShapeController(config)
        locust_state = LocustState(0, 0)

        number_users_spawn_rate_tuple = shaper.calculate(locust_state)

        assert number_users_spawn_rate_tuple is None

    def test_calculate_returns_message_when_failure_rate_exceeded(self):
        config = build_default_configuration()
        config.failure_rate_threshold = 1
        shaper = LoadShapeController(config)
        locust_state_t0 = LocustState(0, 0)
        locust_state_t1 = LocustState(0, 1)
        locust_state_t2 = LocustState(0, 3)

        shaper.calculate(locust_state_t0)
        message_t0 = shaper.message
        shaper.calculate(locust_state_t1)
        message_t1 = shaper.message
        shaper.calculate(locust_state_t2)
        message_t2 = shaper.message

        assert message_t0 is None
        assert message_t1 is None
        assert message_t2 == "Failure rate of 2 per second exceeds threshold of 1 per second. Stopping."

    def test_calculate_stops_load_generation_when_failure_rate_exceeded(self):
        config = build_default_configuration()
        config.failure_rate_threshold = 1
        shaper = LoadShapeController(config)
        locust_state_t0 = LocustState(0, 0)
        locust_state_t1 = LocustState(0, 1)
        locust_state_t2 = LocustState(0, 3)

        number_users_spawn_rate_tuple_t0 = shaper.calculate(locust_state_t0)
        number_users_spawn_rate_tuple_t1 = shaper.calculate(locust_state_t1)
        number_users_spawn_rate_tuple_t2 = shaper.calculate(locust_state_t2)

        assert number_users_spawn_rate_tuple_t0 == (1, 1)
        assert number_users_spawn_rate_tuple_t1 == (1, 1)
        assert number_users_spawn_rate_tuple_t2 is None

    def test_calculate_increases_number_of_users_when_dwell_reached(self):
        config = build_default_configuration()
        config.initial_dwell = 1
        shaper = LoadShapeController(config)
        locust_state_t0 = LocustState(0, 0)
        locust_state_t1 = LocustState(1, 0)
        locust_state_t2 = LocustState(2, 0)
        locust_state_t3 = LocustState(3, 0)

        number_users_spawn_rate_tuple_t0 = shaper.calculate(locust_state_t0)
        number_users_spawn_rate_tuple_t1 = shaper.calculate(locust_state_t1)
        number_users_spawn_rate_tuple_t2 = shaper.calculate(locust_state_t2)
        number_users_spawn_rate_tuple_t3 = shaper.calculate(locust_state_t3)

        assert number_users_spawn_rate_tuple_t0 == (1, 1)
        assert number_users_spawn_rate_tuple_t1 == (2, 2)
        assert number_users_spawn_rate_tuple_t2 == (4, 4)
        assert number_users_spawn_rate_tuple_t3 == (8, 8)

    def test_can_back_off_when_failure_threshold_exceeded(self):
        config = build_default_configuration()
        config.is_enabled_back_off = True
        config.initial_number_of_users = 5
        config.initial_spawn_rate = 4
        config.initial_dwell = 1
        shaper = LoadShapeController(config)
        locust_state_t0 = LocustState(0, 0)
        locust_state_t1 = LocustState(1, 1)

        number_users_spawn_rate_tuple_t0 = shaper.calculate(locust_state_t0)
        number_users_spawn_rate_tuple_t1 = shaper.calculate(locust_state_t1)

        assert number_users_spawn_rate_tuple_t0 == (5, 4)
        assert number_users_spawn_rate_tuple_t1 == (4, 1)
