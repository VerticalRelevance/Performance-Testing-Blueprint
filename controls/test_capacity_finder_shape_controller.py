from controls.capacity_finder_shape_controller import LoadShapeController, Configuration, LocustState


def build_default_configuration():
    return Configuration(
        initial_number_of_users=1,
        initial_spawn_rate=1,
        initial_dwell=10,
        max_number_of_users=10,
        time_limit=10,
        failure_rate_threshold=0,
        is_enabled_tuning=False,
        user_dead_band=1)


class TestLoadShapeController:

    def test_user_throughput_equals_1(self):
        config = build_default_configuration()
        shaper = LoadShapeController(config)

        assert shaper._configuration.user_throughput == 1

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
        config.is_enabled_tuning = True
        config.initial_number_of_users = 5
        config.initial_spawn_rate = 4
        config.initial_dwell = 1
        config.user_dead_band = 0
        shaper = LoadShapeController(config)
        locust_state_t0 = LocustState(0, 0)
        locust_state_t1 = LocustState(1, 1)

        number_users_spawn_rate_tuple_t0 = shaper.calculate(locust_state_t0)
        number_users_spawn_rate_tuple_t1 = shaper.calculate(locust_state_t1)

        assert number_users_spawn_rate_tuple_t0 == (5, 4)
        assert number_users_spawn_rate_tuple_t1 == (4, 1)

    def test_does_not_return_number_of_users_or_greater_than_previously_failed(self):
        config = build_default_configuration()
        config.is_enabled_tuning = True
        config.initial_number_of_users = 5
        config.initial_spawn_rate = 4
        config.initial_dwell = 2
        shaper = LoadShapeController(config)
        locust_state_t0 = LocustState(0, 0)  # 5 users, 4 spawn rate
        locust_state_t1 = LocustState(1, 0)  # 5 users, 4 spawn rate
        locust_state_t2 = LocustState(2, 0)  # 9 users, 8 spawn rate
        locust_state_t3 = LocustState(3, 1)  # 9 users, 8 spawn rate
        locust_state_t4 = LocustState(4, 2)  # 7 users, 2 spawn rate
        locust_state_t5 = LocustState(5, 2)  # 7 users, 2 spawn rate
        locust_state_t6 = LocustState(6, 2)  # 8 users, 1 spawn rate

        number_users_spawn_rate_tuple_t0 = shaper.calculate(locust_state_t0)
        number_users_spawn_rate_tuple_t1 = shaper.calculate(locust_state_t1)
        number_users_spawn_rate_tuple_t2 = shaper.calculate(locust_state_t2)
        number_users_spawn_rate_tuple_t3 = shaper.calculate(locust_state_t3)
        number_users_spawn_rate_tuple_t4 = shaper.calculate(locust_state_t4)
        number_users_spawn_rate_tuple_t5 = shaper.calculate(locust_state_t5)
        number_users_spawn_rate_tuple_t6 = shaper.calculate(locust_state_t6)

        assert number_users_spawn_rate_tuple_t0 == (5, 4)
        assert number_users_spawn_rate_tuple_t1 == (5, 4)
        assert number_users_spawn_rate_tuple_t2 == (9, 8)
        assert number_users_spawn_rate_tuple_t3 == (9, 8)
        assert number_users_spawn_rate_tuple_t4 == (7, 2)
        assert number_users_spawn_rate_tuple_t5 == (7, 2)
        assert number_users_spawn_rate_tuple_t6 == (8, 1)

    def test_settles_to_max_number_users_within_error_threshold(self):
        config = build_default_configuration()
        config.is_enabled_tuning = True
        config.initial_number_of_users = 5
        config.initial_spawn_rate = 4
        config.initial_dwell = 2
        shaper = LoadShapeController(config)
        locust_state_t0 = LocustState(0, 0)  # 5 users, 4 spawn rate
        locust_state_t1 = LocustState(1, 0)  # 5 users, 4 spawn rate
        locust_state_t2 = LocustState(2, 0)  # 9 users, 8 spawn rate
        locust_state_t3 = LocustState(3, 1)  # 9 users, 8 spawn rate
        locust_state_t4 = LocustState(4, 2)  # 7 users, 2 spawn rate
        locust_state_t5 = LocustState(5, 2)  # 7 users, 2 spawn rate
        locust_state_t6 = LocustState(6, 2)  # 8 users, 1 spawn rate
        locust_state_t7 = LocustState(7, 2)  # 8 users, 1 spawn rate
        locust_state_t8 = LocustState(8, 2)  # 8 users, 1 spawn rate
        locust_state_t9 = LocustState(9, 2)  # 8 users, 1 spawn rate

        number_users_spawn_rate_tuple_t0 = shaper.calculate(locust_state_t0)
        number_users_spawn_rate_tuple_t1 = shaper.calculate(locust_state_t1)
        number_users_spawn_rate_tuple_t2 = shaper.calculate(locust_state_t2)
        number_users_spawn_rate_tuple_t3 = shaper.calculate(locust_state_t3)
        number_users_spawn_rate_tuple_t4 = shaper.calculate(locust_state_t4)
        number_users_spawn_rate_tuple_t5 = shaper.calculate(locust_state_t5)
        number_users_spawn_rate_tuple_t6 = shaper.calculate(locust_state_t6)
        number_users_spawn_rate_tuple_t7 = shaper.calculate(locust_state_t7)
        number_users_spawn_rate_tuple_t8 = shaper.calculate(locust_state_t8)
        number_users_spawn_rate_tuple_t9 = shaper.calculate(locust_state_t9)

        assert number_users_spawn_rate_tuple_t0 == (5, 4)
        assert number_users_spawn_rate_tuple_t1 == (5, 4)
        assert number_users_spawn_rate_tuple_t2 == (9, 8)
        assert number_users_spawn_rate_tuple_t3 == (9, 8)
        assert number_users_spawn_rate_tuple_t4 == (7, 2)
        assert number_users_spawn_rate_tuple_t5 == (7, 2)
        assert number_users_spawn_rate_tuple_t6 == (8, 1)
        assert number_users_spawn_rate_tuple_t7 == (8, 1)
        assert number_users_spawn_rate_tuple_t8 == (8, 1)
        assert number_users_spawn_rate_tuple_t9 == (8, 1)
