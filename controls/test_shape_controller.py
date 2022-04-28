from controls.load_shape_controller import LoadShapeController, Configuration, State


class TestLoadShapeController:
    def test_is_time_limit_exceeded_returns_false_when_not_exceeded(self):
        config = Configuration(1)
        initial_state = State("unused")
        shaper = LoadShapeController(config, initial_state)

        time_exceeded = shaper.is_time_limit_exceeded(1)

        assert not time_exceeded

    def test_is_time_limit_exceeded_returns_true_when_exceeded(self):
        config = Configuration(1)
        initial_state = State("unused")
        shaper = LoadShapeController(config, initial_state)

        time_exceeded = shaper.is_time_limit_exceeded(2)

        assert time_exceeded




