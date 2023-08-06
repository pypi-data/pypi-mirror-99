import unittest
import pandas as pd
from psense_common import kfilter
from datetime import datetime, timedelta


class TestKFilter(unittest.TestCase):
    def test_invalid_input(self):
        print("\ntest_invalid_input:")
        print("initialize class using fully populated buffer")
        kf = kfilter.kfilter()

        print("> should not allow inputting string")
        # kf.input_latest_measurement('teststring')
        self.assertRaises(
            AssertionError, kf.input_latest_measurement, ["StringInsteadOfNumber"]
        )
        self.assertEqual(kf.posteri_estimate, 5)
        self.assertEqual(kf.posteri_error_estimate, 0.01)
        self.assertEqual(kf.measurements, [])
        self.assertEqual(kf.consecutive_replacements, 0)

        print("> should not allow inputting list")
        self.assertRaises(AssertionError, kf.input_latest_measurement, [[10, 10]])

        print("> should allow inputting numeric string")
        kf.input_latest_measurement("10.10")
        self.assertEqual(kf.posteri_estimate, 10.1)
        self.assertEqual(kf.measurements, [10.10])

    def test_initial_state(self):
        print("\ntest_initial_state:")
        print("> test initalization with default values")
        kf = kfilter.kfilter()
        self.assertEqual(kf.filter_length, 10)
        self.assertEqual(kf.process_variance, 0.01)
        self.assertEqual(kf.posteri_estimate, 5)
        self.assertEqual(kf.posteri_error_estimate, 0.01)
        self.assertEqual(kf.measurements, [])
        self.assertEqual(kf.consecutive_replacements, 0)

        print("> test initalization with custom values")
        kf = kfilter.kfilter(1, 0, 1, 1, [1], 1, 1)
        self.assertEqual(kf.filter_length, 1)
        self.assertEqual(kf.filter_init, 0)
        self.assertEqual(kf.process_variance, 1)
        self.assertEqual(kf.posteri_estimate, 1)
        self.assertEqual(kf.posteri_error_estimate, 1)
        self.assertEqual(kf.measurements, [1])
        self.assertEqual(kf.consecutive_replacements, 1)

    def test_add_meas_full_buffer(self):
        print("\ntest_add_meas_full_buffer:")
        print("initialize class using fully populated buffer")
        kf = kfilter.kfilter(
            filter_length=3, filter_init=0, initial_guess=10, measurements=[10, 10, 10]
        )

        # print('{:06.3f}\t{:07.5f}\t{}\t{}'.format(kf.posteri_estimate, kf.posteri_error_estimate, kf.consecutive_replacements, kf.measurements))
        print("> test adding higher measurement, in range")
        kf.input_latest_measurement(10.5)
        self.assertEqual(kf.measurements, [10, 10, 10.5])
        self.assertEqual(kf.get_latest_estimated_measurement(), (10.039, 10.5))
        self.assertEqual(round(kf.posteri_error_estimate, 3), 0.018)

        print("> test adding higher measurement, clipping filter")
        kf.input_latest_measurement(10)
        self.assertEqual(kf.get_latest_estimated_measurement(), (10.035, 10))
        kf.input_latest_measurement(10)
        self.assertEqual(kf.get_latest_estimated_measurement(), (10.03, 10))
        kf.input_latest_measurement(10)
        self.assertEqual(kf.get_latest_estimated_measurement(), (10, 10))
        kf.input_latest_measurement(12)
        self.assertEqual(kf.measurements, [10, 10, 10.5])

        print("> test adding higher measurement, not clipped but out of range")
        self.assertEqual(kf.get_latest_estimated_measurement(), (10.02, 10.5))
        self.assertEqual(round(kf.posteri_error_estimate, 3), 0.010)

        print("> test adding higher measurement, edge of range")
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(10.5)
        self.assertEqual(kf.measurements, [10, 10, 10.5])

        print("> test adding lower measurement, out of range")
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(5.0)
        self.assertEqual(kf.measurements, [10, 10, 9.5])
        self.assertEqual(kf.get_latest_estimated_measurement(), (09.98, 9.5))

        print("> test adding lower measurement, edge of range")
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(10)
        kf.input_latest_measurement(9.5)
        self.assertEqual(kf.measurements, [10, 10, 9.5])
        self.assertEqual(kf.get_latest_estimated_measurement(), (09.956, 9.5))

        print("initialize class using fully populated buffer, negative current")
        kf = kfilter.kfilter(
            filter_length=3, filter_init=0, initial_guess=-9, measurements=[-9, -9, -9]
        )

        print("> test adding more negative measurement, in range")
        kf.input_latest_measurement(-9.1)
        self.assertEqual(kf.measurements, [-9, -9, -9.1])
        self.assertEqual(kf.get_latest_estimated_measurement(), (-9.03, -9.1))
        self.assertEqual(round(kf.posteri_error_estimate, 3), 0.014)

        print("> test adding more negative measurement, clipped")
        kf.input_latest_measurement(-9)
        kf.input_latest_measurement(-9)
        kf.input_latest_measurement(-9)
        kf.input_latest_measurement(-10)
        self.assertEqual(kf.measurements, [-9, -9, -9.45])
        self.assertEqual(kf.get_latest_estimated_measurement(), (-9.02, -9.45))
        self.assertEqual(round(kf.posteri_error_estimate, 3), 0.010)

    def test_buffer_replacements(self):
        print("\ntest_buffer_replacements:")
        print("initialize class using fully populated buffer")
        kf = kfilter.kfilter(
            filter_length=3, filter_init=0, initial_guess=10, measurements=[10, 10, 10]
        )

        print("> should update OOR count when out of 0.5/2x range")
        kf.input_latest_measurement(20)
        self.assertEqual(kf.consecutive_replacements, 1)

        print("> should not truncate when (OOR count < filter_length)")
        kf.input_latest_measurement(21)
        self.assertEqual(kf.consecutive_replacements, 2)

        print("> should not truncate when (OOR count == filter_length)")
        kf.input_latest_measurement(22)
        self.assertEqual(kf.consecutive_replacements, 3)

        print(
            "> should truncate with too many consecutive replacement (OOR count > filter_length)"
        )
        kf.input_latest_measurement(25)
        self.assertEqual(len(kf.measurements), 2)
        self.assertEqual(kf.measurements[-1], 25)
        self.assertEqual(kf.consecutive_replacements, 0)

    def test_add_meas_part_buffer(self):
        print("\ntest_add_meas_part_buffer")
        print("initialize class with empty buffer")
        kf = kfilter.kfilter(
            filter_length=3, filter_init=0, initial_guess=10, measurements=[]
        )

        # print('{:06.3f}\t{:07.5f}\t{}\t{}'.format(kf.posteri_estimate, kf.posteri_error_estimate, kf.consecutive_replacements, kf.measurements))
        print("> test adding measurement, buffer 0/3")
        kf.input_latest_measurement(5)
        self.assertEqual(kf.measurements, [5])
        self.assertEqual(kf.get_latest_estimated_measurement(), (5, 5))

        print("> test adding measurement, buffer 1/3")
        kf.input_latest_measurement(5.1)
        self.assertEqual(kf.measurements, [5, 5.1])
        self.assertEqual(kf.get_latest_estimated_measurement(), (5.1, 5.1))

        print("> test adding measurement, buffer 2/3")
        kf.input_latest_measurement(5.2)
        self.assertEqual(kf.measurements, [5, 5.1, 5.2])
        self.assertEqual(kf.get_latest_estimated_measurement(), (5.2, 5.2))

        print("> test adding measurement, buffer 3/3")
        kf.input_latest_measurement(5.3)
        self.assertEqual(kf.measurements, [5.1, 5.2, 5.3])
        self.assertNotEqual(kf.get_latest_estimated_measurement(), (5.3, 5.3))

    def test_init_filter(self):
        print("\ntest_init_filter:")
        print("initialize filter with empty buffer")
        kf = kfilter.kfilter(filter_length=10, initial_guess=10, measurements=[])
        # disable init mode

        # print('{:06.3f}\t{:07.5f}\t{}\t{}'.format(kf.posteri_estimate, kf.posteri_error_estimate, kf.consecutive_replacements, kf.measurements))
        print("> filter is disabled during init period")
        for i in range(kf.filter_init):
            kf.input_latest_measurement(i)
            self.assertEqual(kf.measurements[-1], i)

        print("> filter should start after init period ends")
        kf.input_latest_measurement(i * 0.95)
        self.assertEqual(i * 0.95, kf.measurements[-1])
        self.assertNotEqual(kf.get_latest_estimated_measurement(), kf.measurements[-1])

    def test_blend(self):
        print("\ntest_run_blend:")
        # check blending is working as intended with default blending factor
        print("> filter should average signals 1 and 2 when noise = blend factor")
        self.assertEqual(kfilter.blend(1, 0, 0.05), 0.5)  # noise level = bf
        print("> filter should double-weight signal 2 when noise = 2 * blend factor")
        self.assertEqual(kfilter.blend(1, 0, 0.10), 1 / 3)  # noise level = 2x bf
        print("> filter should half-weight signal 2 when noise = 1/2 * blend factor")
        self.assertEqual(kfilter.blend(1, 0, 0.025), 2 / 3)  # noise level = 0.5x bf

        # adjust the blending factor
        print("> filter should adjust output based on the blend factor")
        self.assertEqual(kfilter.blend(1, 0, 0.05, blending_factor=0.10), 2 / 3)

    def test_run_psensefilter(self):
        print("\ntest_run_psensefilter:")

        # ts = (datetime.utcnow() - timedelta(minutes=10)).isoformat("T")
        data = pd.DataFrame(dict(signal1=[10] * 10, vout1=[0.4] * 10))

        print(
            "> filter executes kalman + mavg filters, and blends them based on SG accel"
        )
        res = kfilter.run_psensefilter(
            data, blending_factor=0.05, samples_mavg=100, samples_stdev=40
        )
        expected_keys = [
            "signal1",
            "vout1",
            "c_signal1",
            "fk_signal1",
            "f100_signal1",
            "d_signal1",
            "dd_signal1",
            "noise40_signal1",
            "fblend_signal1",
        ]
        self.assertTrue(res.keys().tolist() == expected_keys)

        res = kfilter.run_psensefilter(data, blending_factor=0.05)
        expected_keys = [
            "signal1",
            "vout1",
            "c_signal1",
            "fk_signal1",
            "f40_signal1",
            "d_signal1",
            "dd_signal1",
            "noise10_signal1",
            "fblend_signal1",
        ]
        self.assertTrue(res.keys().tolist() == expected_keys)

        self.assertEqual(res["signal1"][0], 10)
        self.assertEqual(res["signal1"][9], 10)
        self.assertEqual(res["vout1"][0], 0.4)
        self.assertEqual(res["c_signal1"][0], 10)
        self.assertEqual(res["d_signal1"][0], 0)
        self.assertEqual(res["d_signal1"].iloc[-1], 0)
        self.assertEqual(res["noise10_signal1"][0], 0)
        self.assertEqual(res["noise10_signal1"].iloc[-1], 0)
        self.assertEqual(res["fblend_signal1"][0], 10)
        self.assertEqual(res["fblend_signal1"].iloc[-1], 10)

        def frange(x, y, jump):
            while x <= y:
                yield x
                x += jump

        print("> filter response to a 0.01nA ramp")
        data = list(frange(5, 10, 0.01))
        data = pd.DataFrame(dict(signal1=data, vout1=[0.4] * len(data)))
        res = kfilter.run_psensefilter(
            data,
            blending_factor=1,
            samples_mavg=40,
            samples_stdev=7,
            kalman_coeff={
                "filter-window": 10,
                "filter-smoothing": 0.01,
                "filter-init": 40,
            },
        )
        self.assertEqual(res["signal1"].iloc[250], 7.5)
        self.assertEqual(res["fk_signal1"].iloc[250], 7.48)
        self.assertEqual(res["f40_signal1"].iloc[250], 7.31)
        self.assertEqual(res["d_signal1"].iloc[250], 0.01)
        self.assertEqual(res["fblend_signal1"].iloc[250], 7.49)
        self.assertEqual(res["fk_signal1"].iloc[-1], 9.98)
        self.assertEqual(res["f40_signal1"].iloc[-1], 9.81)
        self.assertEqual(res["d_signal1"].iloc[-1], 0.01)
        self.assertEqual(res["fblend_signal1"].iloc[-1], 9.99)

        print("> filter response to a 0.10nA ramp")
        data = list(frange(5, 10, 0.1))
        data = pd.DataFrame(dict(signal1=data, vout1=[0.4] * len(data)))
        res = kfilter.run_psensefilter(
            data,
            blending_factor=0.10,
            samples_mavg=40,
            samples_stdev=7,
            kalman_coeff={
                "filter-window": 10,
                "filter-smoothing": 0.05,
                "filter-init": 40,
            },
        )
        self.assertEqual(res["d_signal1"].iloc[-1], 0.09)
        self.assertEqual(res["fk_signal1"].iloc[-1], 9.7)
        self.assertEqual(res["fblend_signal1"].iloc[-1], 9.79)

        print("> filter response to a 0.10nA ramp, with blending factor modified")
        res = kfilter.run_psensefilter(
            data,
            blending_factor=0.10,
            samples_mavg=40,
            samples_stdev=7,
            kalman_coeff={
                "filter-window": 10,
                "filter-smoothing": 0.01,
                "filter-init": 40,
            },
        )
        self.assertEqual(res["fk_signal1"].iloc[-1], 9.35)
        self.assertEqual(res["fblend_signal1"].iloc[-1], 9.44)

        print("> filter response to a 1nA step change")

        def fstep(x, y, val1, val2):
            while x <= y:
                yield val1
                x += 1

            while x <= y + 30:
                yield val2
                x += 1

        data = list(fstep(1, 100, 5, 6))
        data = pd.DataFrame(dict(signal1=data, vout1=[0.4] * len(data)))
        res = kfilter.run_psensefilter(
            data,
            blending_factor=0.10,
            samples_mavg=40,
            samples_stdev=7,
            kalman_coeff={
                "filter-window": 10,
                "filter-smoothing": 0.01,
                "filter-init": 40,
            },
        )
        print("\t.. check kalman output")
        self.assertEqual(res["fk_signal1"].iloc[-31], 5)
        self.assertEqual(res["fk_signal1"].iloc[-30], 5.04)
        self.assertEqual(res["fk_signal1"].iloc[-21], 5.64)
        self.assertEqual(res["fk_signal1"].iloc[-11], 5.92)
        self.assertEqual(res["fk_signal1"].iloc[-1], 6)
        print("\t.. check blend output")
        self.assertEqual(res["fblend_signal1"].iloc[-31], 5)
        self.assertEqual(res["fblend_signal1"].iloc[-30], 5.05)
        self.assertEqual(res["fblend_signal1"].iloc[-10], 5.94)
        self.assertEqual(res["fblend_signal1"].iloc[-1], 6)


if __name__ == "__main__":
    unittest.main()
