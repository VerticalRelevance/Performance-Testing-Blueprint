from controls.spike_shape_controller import SpikeShapeController, CustomArgs


class TestSpikeShapeController:
    def test_calculate_returns_0_users_and_args_spawn_rate_on_first_tick(self):
        args = CustomArgs
        controller = SpikeShapeController()
        expected_users_rate_tuple = (0, 1)

        result = controller.calculate(args)

        assert result == expected_users_rate_tuple

    def test_calculate_ramps_up_when_below_steady_state(self):
        args = CustomArgs
        controller = SpikeShapeController()
        expected_users_rate_tuple_t0 = (0, 1)
        expected_users_rate_tuple_t1 = (1, 1)

        result_t0 = controller.calculate(args)
        result_t1 = controller.calculate(args)

        assert result_t0 == expected_users_rate_tuple_t0
        assert result_t1 == expected_users_rate_tuple_t1

    def test_calculate_ramps_up_at_spawn_rate_when_below_steady_state(self):
        args = CustomArgs
        args.spawn_rate = 2
        controller = SpikeShapeController()
        expected_users_rate_tuple_t0 = (0, 2)
        expected_users_rate_tuple_t1 = (2, 2)

        result_t0 = controller.calculate(args)
        result_t1 = controller.calculate(args)

        assert result_t0 == expected_users_rate_tuple_t0
        assert result_t1 == expected_users_rate_tuple_t1

    # def test_calculate_ramps_up_when_dwell_reached(self):
    #     args = CustomArgs
    #     controller = SpikeShapeController()
    #     expected_users_rate_tuple_t0 = (1, 1)
    #     expected_users_rate_tuple_t1 = (1, 1)
    #     expected_users_rate_tuple_t2 = (2, 1)
    #     expected_users_rate_tuple_t3 = (3, 1)
    #
    #     result_t0 = controller.calculate(args)
    #     result_t1 = controller.calculate(args)
    #     result_t2 = controller.calculate(args)
    #     result_t3 = controller.calculate(args)
    #
    #     assert result_t0 == expected_users_rate_tuple_t0
    #     assert result_t1 == expected_users_rate_tuple_t1
    #     assert result_t2 == expected_users_rate_tuple_t2
    #     assert result_t3 == expected_users_rate_tuple_t3