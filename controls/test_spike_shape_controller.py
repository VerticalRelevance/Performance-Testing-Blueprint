from controls.spike_shape_controller import SpikeShapeController, CustomArgs


def build_custom_args():
    return CustomArgs(
        spawn_rate=1,
        steady_state_users=2,
        steady_state_dwell=2,
        spike_state_users=3,
        spike_state_dwell=1)


class TestSpikeShapeController:
    def test_calculate_returns_0_users_and_args_spawn_rate_on_first_tick(self):
        args = build_custom_args()
        controller = SpikeShapeController()
        expected_users_rate_tuple = (0, 1)

        result = controller.calculate(args)

        assert result == expected_users_rate_tuple

    def test_calculate_ramps_up_when_below_steady_state(self):
        args = build_custom_args()
        controller = SpikeShapeController()
        expected_users_rate_tuple_t0 = (0, 1)
        expected_users_rate_tuple_t1 = (1, 1)

        result_t0 = controller.calculate(args)
        result_t1 = controller.calculate(args)

        assert result_t0 == expected_users_rate_tuple_t0
        assert result_t1 == expected_users_rate_tuple_t1

    def test_calculate_ramps_up_at_spawn_rate_when_below_steady_state(self):
        default_args = build_custom_args()
        args = default_args._replace(spawn_rate=2)
        controller = SpikeShapeController()
        expected_users_rate_tuple_t0 = (0, 2)
        expected_users_rate_tuple_t1 = (2, 2)

        result_t0 = controller.calculate(args)
        result_t1 = controller.calculate(args)

        assert result_t0 == expected_users_rate_tuple_t0
        assert result_t1 == expected_users_rate_tuple_t1

    def test_calculate_stops_ramp_up_to_steady_state_when_users_reached(self):
        args = build_custom_args()
        controller = SpikeShapeController()
        expected_users_rate_tuple_t0 = (0, 1)
        expected_users_rate_tuple_t1 = (1, 1)
        expected_users_rate_tuple_t2 = (2, 1)
        expected_users_rate_tuple_t3 = (2, 1)

        result_t0 = controller.calculate(args)
        result_t1 = controller.calculate(args)
        result_t2 = controller.calculate(args)
        result_t3 = controller.calculate(args)

        assert result_t0 == expected_users_rate_tuple_t0
        assert result_t1 == expected_users_rate_tuple_t1
        assert result_t2 == expected_users_rate_tuple_t2
        assert result_t3 == expected_users_rate_tuple_t3

    def test_calculate_corrects_to_steady_state_if_overshot(self):
        default_args = build_custom_args()
        args = default_args._replace(spawn_rate=5)
        controller = SpikeShapeController()
        expected_users_rate_tuple_t0 = (0, 5)
        expected_users_rate_tuple_t1 = (2, 5)

        result_t0 = controller.calculate(args)
        result_t1 = controller.calculate(args)

        assert result_t0 == expected_users_rate_tuple_t0
        assert result_t1 == expected_users_rate_tuple_t1

    def test_calculate_ramps_up_to_spike_state_when_dwell_reached(self):
        args = build_custom_args()
        controller = SpikeShapeController()
        expected_users_rate_tuple_t4 = (3, 1)

        controller.calculate(args)
        controller.calculate(args)
        controller.calculate(args)
        controller.calculate(args)
        result_t4 = controller.calculate(args)

        assert result_t4 == expected_users_rate_tuple_t4

    def test_calculate_stops_adding_users_when_spiking_when_spike_users_reached(self):
        args = build_custom_args()
        controller = SpikeShapeController()
        expected_users_rate_tuple_t5 = (3, 1)

        controller.calculate(args)
        controller.calculate(args)
        controller.calculate(args)
        controller.calculate(args)
        controller.calculate(args)
        result_t5 = controller.calculate(args)

        assert result_t5 == expected_users_rate_tuple_t5
