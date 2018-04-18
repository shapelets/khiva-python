# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from tsa.features import *
from tsa.array import array
import logging


########################################################################################################################

class FeatureTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_cid_ce(self):
        cid_ce_result = cid_ce(array(data=[[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]),
                               False).to_numpy()
        self.assertAlmostEqual(cid_ce_result[0], 2.23606797749979, delta=self.DELTA)
        self.assertAlmostEqual(cid_ce_result[1], 2.23606797749979, delta=self.DELTA)

        cid_ce_result = cid_ce(array(data=[[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]),
                               True).to_numpy()
        self.assertAlmostEqual(cid_ce_result[0], 1.30930734141595, delta=self.DELTA)
        self.assertAlmostEqual(cid_ce_result[1], 1.30930734141595, delta=self.DELTA)

    def test_c3(self):
        c3_result = c3(array(data=[[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]), 2).to_numpy()
        self.assertEqual(c3_result[0], 7.5)
        self.assertEqual(c3_result[1], 586.5)

    def test_abs_sum_of_changes(self):
        abs_sum_of_changes_result = absolute_sum_of_changes(
            array(data=[[0, 1, 2, 3], [4, 6, 8, 10], [11, 14, 17, 20]])).to_numpy()
        self.assertEqual(abs_sum_of_changes_result[0], 3)
        self.assertEqual(abs_sum_of_changes_result[1], 6)
        self.assertEqual(abs_sum_of_changes_result[2], 9)

    def test_abs_energy(self):
        abs_energy_result = abs_energy(array(data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])).to_numpy()
        self.assertAlmostEqual(abs_energy_result[0], 385, delta=self.DELTA)

    def test_cross_correlation(self):
        cross_correlation_result = cross_correlation(xss=array(data=[1, 2, 3, 4]),
                                                     yss=array(data=[4, 6, 8, 10, 12]),
                                                     unbiased=False).to_numpy()
        self.assertAlmostEqual(cross_correlation_result[0][0], 0.790569415, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[0][1], 0.790569415, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[0][2], 0.079056941, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[0][3], -0.395284707, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[0][4], -0.474341649, delta=self.DELTA)

    def test_auto_covariance(self):
        auto_covariance_result = auto_covariance(
            array(data=[[0, 1, 2, 3], [10, 11, 12, 13]])).to_numpy()
        self.assertAlmostEquals(auto_covariance_result[0][0], 1.25, delta=self.DELTA)
        self.assertAlmostEquals(auto_covariance_result[0][1], 0.3125, delta=self.DELTA)
        self.assertAlmostEquals(auto_covariance_result[0][2], -0.375, delta=self.DELTA)
        self.assertAlmostEquals(auto_covariance_result[0][3], -0.5625, delta=self.DELTA)
        self.assertAlmostEquals(auto_covariance_result[1][0], 1.25, delta=self.DELTA)
        self.assertAlmostEquals(auto_covariance_result[1][1], 0.3125, delta=self.DELTA)
        self.assertAlmostEquals(auto_covariance_result[1][2], -0.375, delta=self.DELTA)
        self.assertAlmostEquals(auto_covariance_result[1][3], -0.5625, delta=self.DELTA)

    def test_cross_covariance(self):
        cross_covariance_result = cross_covariance(
            xss=array(data=[[0, 1, 2, 3], [10, 11, 12, 13]]),
            yss=array(data=[[4, 6, 8, 10, 12], [14, 16, 18, 20, 22]]),
            unbiased=False).to_numpy().flatten()
        for i in range(4):
            self.assertAlmostEqual(cross_covariance_result[(i * 5)], 2.5, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 1], 2.5, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 2], 0.25, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 3], -1.25, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 4], -1.5, delta=self.DELTA)

    def test_approximate_entropy(self):
        approximate_entropy_result = approximate_entropy(
            array(data=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]],
                  tsa_type=dtype.f32), 4, 0.5).to_numpy()

        self.assertAlmostEqual(approximate_entropy_result[0][0], 0.13484281753639338, delta=self.DELTA)
        self.assertAlmostEqual(approximate_entropy_result[0][1], 0.13484281753639338, delta=self.DELTA)

    def test_auto_correlation(self):
        auto_correlation_result = auto_correlation(
            array(data=[[0, 1, 2, 3], [10, 11, 12, 13]]), 4, False).to_numpy().flatten()
        self.assertAlmostEqual(auto_correlation_result[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[1], 0.25, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[2], -0.3, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[3], -0.45, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[4], 1.0, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[5], 0.25, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[6], -0.3, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[7], -0.45, delta=self.DELTA)

    def test_binned_entropy(self):
        binned_entropy_result = binned_entropy(array(data=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                                            14, 15, 16, 17, 18, 19, 20],
                                                           [1, 1, 3, 10, 5, 6, 1, 8, 9, 10, 11, 1, 13, 14, 10, 16,
                                                            17, 10, 19,
                                                            20]]), 5).to_numpy()
        self.assertAlmostEqual(binned_entropy_result[0], 1.6094379124341005, delta=self.DELTA)
        self.assertAlmostEqual(binned_entropy_result[1], 1.5614694247763998, delta=self.DELTA)

    def test_count_above_mean(self):
        count_above_mean_result = count_above_mean(array(data=[[0, 1, 2, 3, 4, 5],
                                                               [6, 7, 8, 9, 10, 11]])).to_numpy()
        self.assertAlmostEqual(count_above_mean_result[0], 3, delta=self.DELTA)
        self.assertAlmostEqual(count_above_mean_result[1], 3, delta=self.DELTA)

    def test_count_below_mean(self):
        count_below_mean_result = count_below_mean(array(data=[[0, 1, 2, 3, 4, 5],
                                                               [6, 7, 8, 9, 10, 11]])).to_numpy()
        self.assertAlmostEqual(count_below_mean_result[0], 3, delta=self.DELTA)
        self.assertAlmostEqual(count_below_mean_result[1], 3, delta=self.DELTA)

    def test_energy_ratio_by_chunks(self):
        energy_ratio_by_chunks_result = energy_ratio_by_chunks(array([[0, 1, 2, 3, 4, 5],
                                                                      [6, 7, 8, 9, 10, 11]]),
                                                               2, 0).to_numpy()
        self.assertAlmostEqual(energy_ratio_by_chunks_result[0], 0.090909091, delta=self.DELTA)
        self.assertAlmostEqual(energy_ratio_by_chunks_result[1], 0.330376940, delta=self.DELTA)
        energy_ratio_by_chunks_result = energy_ratio_by_chunks(array([[0, 1, 2, 3, 4, 5],
                                                                      [6, 7, 8, 9, 10, 11]]), 2,
                                                               1).to_numpy()
        self.assertAlmostEqual(energy_ratio_by_chunks_result[0], 0.909090909, delta=self.DELTA)
        self.assertAlmostEqual(energy_ratio_by_chunks_result[1], 0.669623060, delta=self.DELTA)

    def test_first_location_of_maximum(self):
        first_location_of_maximum_result = first_location_of_maximum(
            array([[5, 4, 3, 5, 0, 1, 5, 3, 2, 1], [2, 4, 3, 5, 2, 5, 4, 3, 5, 2]])).to_numpy()
        self.assertEqual(first_location_of_maximum_result[0], 0.0)
        self.assertEqual(first_location_of_maximum_result[1], 0.3)

    def test_first_location_of_minimum(self):
        first_location_of_minimum_result = first_location_of_minimum(
            array([[5, 4, 3, 0, 0, 1], [5, 4, 3, 0, 2, 1]])).to_numpy()
        self.assertAlmostEqual(first_location_of_minimum_result[0], 0.5, delta=self.DELTA)
        self.assertAlmostEqual(first_location_of_minimum_result[1], 0.5, delta=self.DELTA)

    def test_has_duplicates(self):
        has_duplicates_result = has_duplicates(
            array([[5, 4, 3, 0, 0, 1], [5, 4, 3, 0, 2, 1]])).to_numpy()
        self.assertEqual(has_duplicates_result[0], True)
        self.assertEqual(has_duplicates_result[1], False)

    def test_has_duplicate_max(self):
        has_duplicate_max_result = has_duplicate_max(
            array([[5, 4, 3, 0, 5, 1], [5, 4, 3, 0, 2, 1]])).to_numpy()
        self.assertEqual(has_duplicate_max_result[0], True)
        self.assertEqual(has_duplicate_max_result[1], False)

    def test_index_max_quantile(self):
        index_max_quantile_result = index_max_quantile(array([[5, 4, 3, 0, 0, 1], [5, 4, 0, 0, 2, 1]]),
                                                       0.5).to_numpy()

        self.assertAlmostEqual(index_max_quantile_result[0], 0.333333333, delta=self.DELTA)
        self.assertAlmostEqual(index_max_quantile_result[1], 0.333333333, delta=self.DELTA)

    def test_kurtosis(self):
        kurtosis_result = kurtosis(array([[0, 1, 2, 3, 4, 5], [2, 2, 2, 20, 30, 25]])).to_numpy()
        self.assertAlmostEqual(kurtosis_result[0], -1.2, delta=1e-4)
        self.assertAlmostEqual(kurtosis_result[1], -2.66226722, delta=1e-4)

    def test_large_standard_deviation(self):
        large_standard_deviation_result = large_standard_deviation(
            array([[-1, -1, -1, 1, 1, 1], [4, 6, 8, 4, 5, 4]]), 0.4).to_numpy()
        self.assertEqual(large_standard_deviation_result[0], True)
        self.assertEqual(large_standard_deviation_result[1], False)

    def test_last_location_of_maximum(self):
        last_location_of_maximum_result = last_location_of_maximum(
            array([[0, 4, 3, 5, 5, 1], [0, 4, 3, 2, 5, 1]])).to_numpy()
        self.assertAlmostEqual(last_location_of_maximum_result[0], 0.8333333333333334, delta=self.DELTA)
        self.assertAlmostEqual(last_location_of_maximum_result[1], 0.8333333333333334, delta=self.DELTA)

    def test_last_location_of_minimum(self):
        last_location_of_minimum_result = last_location_of_minimum(
            array([[0, 4, 3, 5, 5, 1, 0, 4], [3, 2, 5, 1, 4, 5, 1, 2]])).to_numpy()
        self.assertAlmostEqual(last_location_of_minimum_result[0], 0.875, delta=self.DELTA)
        self.assertAlmostEqual(last_location_of_minimum_result[1], 0.875, delta=self.DELTA)

    def test_length(self):
        length_result = length(array([[0, 4, 3, 5, 5, 1], [0, 4, 3, 2, 5, 1]])).to_numpy().flatten()
        self.assertEqual(length_result[0], 6)
        self.assertEqual(length_result[1], 6)

    def test_linear_trend(self):
        pvalue, rvalue, intercept, slope, stderr = linear_trend(array([[0, 4, 3, 5, 5, 1], [2, 4, 1, 2, 5, 3]]))

        pvalue = pvalue.to_numpy()
        self.assertAlmostEqual(pvalue[0], 0.6260380997892747, delta=self.DELTA)
        self.assertAlmostEqual(pvalue[1], 0.5272201945463578, delta=self.DELTA)
        rvalue = rvalue.to_numpy()
        self.assertAlmostEqual(rvalue[0], 0.2548235957188128, delta=self.DELTA)
        self.assertAlmostEqual(rvalue[1], 0.3268228676411533, delta=self.DELTA)
        intercept = intercept.to_numpy()
        self.assertAlmostEqual(intercept[0], 2.2857142857142856, delta=self.DELTA)
        self.assertAlmostEqual(intercept[1], 2.1904761904761907, delta=self.DELTA)
        slope = slope.to_numpy()
        self.assertAlmostEqual(slope[0], 0.2857142857142857, delta=self.DELTA)
        self.assertAlmostEqual(slope[1], 0.2571428571428572, delta=self.DELTA)
        stderr = stderr.to_numpy()
        self.assertAlmostEqual(stderr[0], 0.5421047417431507, delta=self.DELTA)
        self.assertAlmostEqual(stderr[1], 0.37179469135129783, delta=self.DELTA)

    def test_has_duplicate_min(self):
        has_duplicate_min_result = has_duplicate_min(
            array(data=[[5, 4, 3, 0, 0, 1], [5, 4, 3, 0, 2, 1]])).to_numpy()
        self.assertEqual(has_duplicate_min_result[0], True)
        self.assertEqual(has_duplicate_min_result[1], False)

    def test_longest_strike_above_mean(self):
        longest_strike_above_mean_result = longest_strike_above_mean(
            array(data=[[20, 20, 20, 1, 1, 1, 20, 20, 20, 20, 1, 1, 1, 1,
                         1, 1, 1, 1, 20, 20],
                        [20, 20, 20, 1, 1, 1, 20, 20,
                         20, 1, 1, 1, 1, 1, 1, 1, 1,
                         1, 20, 20]])).to_numpy()
        self.assertEqual(longest_strike_above_mean_result[0], 4)
        self.assertEqual(longest_strike_above_mean_result[1], 3)

    def test_longest_strike_below_mean(self):
        longest_strike_below_mean_result = longest_strike_below_mean(
            array([[20, 20, 20, 1, 1, 1, 20, 20, 20, 20, 1, 1, 1, 1,
                    1, 1, 1, 1, 20, 20],
                   [20, 20, 20, 1, 1, 1, 20, 20,
                    20, 1, 1, 1, 1, 1, 1, 1, 1,
                    1, 20, 20]], dtype.f32)).to_numpy()
        self.assertEqual(longest_strike_below_mean_result[0], 8)
        self.assertEqual(longest_strike_below_mean_result[1], 9)

    def test_maximum(self):
        maximum_result = maximum(array([[20, 20, 20, 18, 25, 19, 20, 20, 20, 20, 40, 30, 1, 50, 1, 1, 5, 1, 20, 20],
                                        [20, 20, 20, 2, 19, 1, 20, 20, 20, 1, 15, 1, 30, 1, 1, 18, 4, 1, 20,
                                         20]])).to_numpy()
        self.assertEqual(maximum_result[0], 50)
        self.assertEqual(maximum_result[1], 30)

    def test_mean_absolute_change(self):
        mean_absolute_change_result = mean_absolute_change(
            array([[0, 1, 2, 3, 4, 5], [8, 10, 12, 14, 16, 18]])).to_numpy()
        r = 5 / 6
        self.assertAlmostEqual(mean_absolute_change_result[0], r, delta=self.DELTA)
        self.assertAlmostEqual(mean_absolute_change_result[1], r * 2, delta=self.DELTA)

    def test_fft_coefficient(self):
        fftCoefficient_result = fftCoefficient(
            array([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]), 0)
        a = fftCoefficient_result[0].to_numpy()
        self.assertAlmostEqual(a[0], 15, delta=self.DELTA)
        self.assertAlmostEqual(a[1], 51, delta=self.DELTA)
        b = fftCoefficient_result[1].to_numpy()

        self.assertAlmostEqual(b[0], 0, delta=self.DELTA)
        self.assertAlmostEqual(b[1], 0, delta=self.DELTA)
        c = fftCoefficient_result[2].to_numpy()

        self.assertAlmostEqual(c[0], 15, delta=self.DELTA)
        self.assertAlmostEqual(c[1], 51, delta=self.DELTA)
        d = fftCoefficient_result[3].to_numpy()

        self.assertAlmostEqual(d[0], 0, delta=self.DELTA)
        self.assertAlmostEqual(d[1], 0, delta=self.DELTA)

    def test_aggregated_autocorrelation_mean(self):
        aggregated_autocorrelation_result = aggregated_autocorrelation(
            array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]), 0).to_numpy()
        self.assertAlmostEqual(aggregated_autocorrelation_result[0], -0.6571428571428571, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_autocorrelation_result[1], -0.6571428571428571, delta=self.DELTA)

    def test_aggregated_autocorrelation_median(self):
        aggregated_autocorrelation_result = aggregated_autocorrelation(
            array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]), 1).to_numpy()
        self.assertAlmostEqual(aggregated_autocorrelation_result[0], -0.54285717010498047, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_autocorrelation_result[1], -0.54285717010498047, delta=self.DELTA)

    def test_aggregated_autocorrelation_min(self):
        aggregated_autocorrelation_result = aggregated_autocorrelation(
            array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]), 2).to_numpy()
        self.assertAlmostEqual(aggregated_autocorrelation_result[0], -2.142857142857143, delta=1e-4)
        self.assertAlmostEqual(aggregated_autocorrelation_result[1], -2.142857142857143, delta=1e-4)

    def test_aggregated_autocorrelation_max(self):
        aggregated_autocorrelation_result = aggregated_autocorrelation(
            array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]), 3).to_numpy()
        self.assertAlmostEqual(aggregated_autocorrelation_result[0], 0.6, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_autocorrelation_result[1], 0.6, delta=self.DELTA)

    def test_aggregated_autocorrelation_stdev(self):
        aggregated_autocorrelation_result = aggregated_autocorrelation(
            array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]), 4).to_numpy()
        self.assertAlmostEqual(aggregated_autocorrelation_result[0], 0.9744490855905009, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_autocorrelation_result[1], 0.9744490855905009, delta=self.DELTA)

    def test_aggregated_autocorrelation_var(self):
        aggregated_autocorrelation_result = aggregated_autocorrelation(
            array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]), 5).to_numpy()
        self.assertAlmostEqual(aggregated_autocorrelation_result[0], 0.9495510204081633, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_autocorrelation_result[1], 0.9495510204081633, delta=self.DELTA)

    def test_aggregated_linear_trend_mean(self):
        aggregated_linear_trend_result = aggregated_linear_trend(
            array([[2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]]), 3, 0)
        self.assertAlmostEqual(aggregated_linear_trend_result[0].to_numpy()[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_linear_trend_result[1].to_numpy()[0], 2, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_linear_trend_result[2].to_numpy()[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_linear_trend_result[3].to_numpy()[0], 0, delta=self.DELTA)
        self.assertAlmostEqual(aggregated_linear_trend_result[4].to_numpy()[0], 0, delta=self.DELTA)

    def test_aggregated_linear_trend_min(self):
        aggregated_linear_trend_result = aggregated_linear_trend(
            array([2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]), 3, 2)
        self.assertAlmostEqual(aggregated_linear_trend_result[0].to_numpy()[0], 1, delta=1e-3)
        self.assertAlmostEqual(aggregated_linear_trend_result[1].to_numpy()[0], 2, delta=1e-3)
        self.assertAlmostEqual(aggregated_linear_trend_result[2].to_numpy()[0], 1, delta=1e-3)
        self.assertAlmostEqual(aggregated_linear_trend_result[3].to_numpy()[0], 0, delta=1e-3)
        self.assertAlmostEqual(aggregated_linear_trend_result[4].to_numpy()[0], 0, delta=1e-3)

    def test_cwt_coefficients(self):
        cwt_coefficients_result = cwt_coefficients(array([[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]),
                                                   array(data=[1, 2, 3], tsa_type=dtype.s32), 2, 2).to_numpy()
        self.assertAlmostEqual(cwt_coefficients_result[0], 0.26517161726951599, delta=self.DELTA)
        self.assertAlmostEqual(cwt_coefficients_result[1], 0.26517161726951599, delta=self.DELTA)

    def test_mean_second_derivative_central(self):
        mean_second_derivative_central_result = mean_second_derivative_central(
            array([[1, 3, 7, 4, 8], [2, 5, 1, 7, 4]])).to_numpy()
        self.assertAlmostEqual(mean_second_derivative_central_result[0], 1.0 / 5.0, delta=self.DELTA)
        self.assertAlmostEqual(mean_second_derivative_central_result[1], -3.0 / 5.0, delta=self.DELTA)

    def test_minimum(self):
        minimum_result = minimum(
            array([[20, 20, 20, 18, 25, 19, 20, 20, 20, 20, 40, 30, 1, 50, 13, 15, 5, 16, 20, 20],
                   [20, 20, 20, 2, 19, 4, 20, 20, 20, 4, 15, 6, 30, 7, 9, 18, 4, 10, 20, 20]])).to_numpy()
        self.assertAlmostEqual(minimum_result[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(minimum_result[1], 2, delta=self.DELTA)

    def test_number_crossing_m(self):
        number_crossing_m_result = number_crossing_m(
            array([[1, 2, 1, 1, -3, -4, 7, 8, 9, 10, -2, 1, -3, 5, 6, 7, -10],
                   [1, 2, 1, 1, -3, -4, 7, 8, 9, 10, -2, 1, -3, 5, 6, 7, -10]]), 0).to_numpy()

        self.assertAlmostEqual(number_crossing_m_result[0], 7, delta=self.DELTA)
        self.assertAlmostEqual(number_crossing_m_result[1], 7, delta=self.DELTA)

    def test_mean(self):
        mean_result = mean(array([[20, 20, 20, 18, 25, 19, 20, 20, 20, 20, 40, 30, 1, 50, 1, 1, 5, 1, 20, 20],
                                  [20, 20, 20, 2, 19, 1, 20, 20, 20, 1, 15, 1, 30, 1, 1, 18, 4, 1, 20, 20]])).to_numpy()
        self.assertAlmostEqual(mean_result[0], 18.55, delta=self.DELTA)
        self.assertAlmostEqual(mean_result[1], 12.7, delta=self.DELTA)

    def test_median(self):
        median_result = median(array([[20, 20, 20, 18, 25, 19, 20, 20, 20, 20, 40, 30, 1, 50, 1, 1, 5, 1, 20, 20],
                                      [20, 20, 20, 2, 19, 1, 20, 20, 20, 1, 15, 1, 30, 1, 1, 18, 4, 1, 20,
                                       20]])).to_numpy()
        self.assertAlmostEqual(median_result[0], 20, delta=self.DELTA)
        self.assertAlmostEqual(median_result[1], 18.5, delta=self.DELTA)

    def test_mean_change(self):
        mean_change_result = mean_change(array([[0, 1, 2, 3, 4, 5],
                                                [8, 10, 12, 14, 16, 18]])).to_numpy()
        self.assertAlmostEqual(mean_change_result[0], 5 / 6, delta=self.DELTA)
        self.assertAlmostEqual(mean_change_result[1], 10 / 6, delta=self.DELTA)

    def test_max_langevin_fixed_point(self):
        max_langevin_fixed_point_result = max_langevin_fixed_point(
            array([[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]), 7, 2).to_numpy()
        self.assertAlmostEqual(max_langevin_fixed_point_result[0], 4.562970585, delta=1e-4)
        self.assertAlmostEqual(max_langevin_fixed_point_result[1], 4.562970585, delta=1e-4)

    def test_fft_aggregated(self):
        fft_aggregated_result = fft_aggregated(
            array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
                  dtype.f32)).to_numpy().flatten()
        self.assertAlmostEqual(fft_aggregated_result[0], 1.135143, delta=1e-4)
        self.assertAlmostEqual(fft_aggregated_result[1], 2.368324, delta=1e-4)
        self.assertAlmostEqual(fft_aggregated_result[2], 1.248777, delta=1e-4)
        self.assertAlmostEqual(fft_aggregated_result[3], 3.642666, delta=1e-4)

        self.assertAlmostEqual(fft_aggregated_result[4], 1.135143, delta=1e-4)
        self.assertAlmostEqual(fft_aggregated_result[5], 2.368324, delta=1e-4)
        self.assertAlmostEqual(fft_aggregated_result[6], 1.248777, delta=1e-4)
        self.assertAlmostEqual(fft_aggregated_result[7], 3.642666, delta=1e-4)

    def test_number_peaks(self):
        result = number_peaks(array([[3, 0, 0, 4, 0, 0, 13], [3, 0, 0, 4, 0, 0, 13]]), 2).to_numpy()
        self.assertAlmostEqual(result[0], 1, delta=1e-4)
        self.assertAlmostEqual(result[1], 1, delta=1e-4)

    def test_percentage_of_reocurring_datapoints_to_all_datapoints(self):
        result = percentage_of_reoccurring_datapoints_to_all_datapoints(
            array([[3, 0, 0, 4, 0, 0, 13], [3, 0, 0, 4, 0, 0, 13]]), False).to_numpy()
        self.assertAlmostEqual(result[0], 0.25, delta=1e-4)
        self.assertAlmostEqual(result[1], 0.25, delta=1e-4)

    def test_quantile(self):
        result = quantile(array([[0, 0, 0, 0, 3, 4, 13], [0, 0, 0, 0, 3, 4, 13]]),
                          array([0.6], dtype.f32)).to_numpy()
        self.assertAlmostEqual(result[0], 1.79999999, delta=1e-4)
        self.assertAlmostEqual(result[1], 1.79999999, delta=1e-4)

    def test_ratio_beyond_r_sigma(self):
        result = ratio_beyond_r_sigma(array([[3, 0, 0, 4, 0, 0, 13], [3, 0, 0, 4, 0, 0, 13]]),
                                      0.5).to_numpy()
        self.assertAlmostEqual(result[0], 0.7142857142857143, delta=1e-4)
        self.assertAlmostEqual(result[1], 0.7142857142857143, delta=1e-4)

    def test_sample_entropy(self):
        result = sample_entropy(array([[3, 0, 0, 4, 0, 0, 13], [3, 0, 0, 4, 0, 0, 13]])).to_numpy()
        self.assertAlmostEqual(result[0][0], 1.2527629, delta=1e-4)
        self.assertAlmostEqual(result[0][1], 1.2527629, delta=1e-4)

    def test_skewness(self):
        result = skewness(array([[3, 0, 0, 4, 0, 0, 13], [3, 0, 0, 4, 0, 0, 13]])).to_numpy()
        self.assertAlmostEqual(result[0], 2.038404735373753, delta=1e-4)
        self.assertAlmostEqual(result[1], 2.038404735373753, delta=1e-4)

    def test_standard_deviation(self):
        result = standard_deviation(
            array([[20, 20, 20, 18, 25, 19, 20, 20, 20, 20, 40, 30, 1, 50, 1, 1, 5, 1, 20, 20],
                   [20, 20, 20, 2, 19, 1, 20, 20, 20, 1, 15, 1, 30, 1, 1, 18, 4, 1, 20, 20]])).to_numpy()
        self.assertAlmostEqual(result[0], 12.363150892875165, delta=1e-4)
        self.assertAlmostEqual(result[1], 9.51367436903324, delta=1e-4)

    def test_sum_of_reoccurring_datapoints(self):
        result = sum_of_reoccurring_datapoints(
            array([[3, 3, 0, 4, 0, 13, 13], [3, 3, 0, 4, 0, 13, 13]])).to_numpy()
        self.assertAlmostEqual(result[0], 32, delta=1e-4)
        self.assertAlmostEqual(result[1], 32, delta=1e-4)

    def test_symmetry_looking(self):
        result = symmetry_looking(array([[20, 20, 20, 18, 25, 19, 20, 20, 20, 20, 40, 30, 1, 50, 1, 1, 5, 1, 20, 20],
                                         [20, 20, 20, 2, 19, 1, 20, 20, 20, 1, 15, 1, 30, 1, 1, 18, 4, 1, 20, 20]]),
                                  0.1).to_numpy()
        self.assertEqual(result[0], bool(1))
        self.assertEqual(result[1], bool(0))

    def test_value_count(self):
        result = value_count(array(data=[[20, 20, 20, 18, 25, 19, 20, 20, 20, 20, 40, 30, 1, 50, 1, 1, 5, 1, 20, 20],
                                         [20, 20, 20, 2, 19, 1, 20, 20, 20, 1, 15, 1, 30, 1, 1, 18, 4, 1, 20, 20]]),
                             20).to_numpy()
        self.assertAlmostEqual(result[0], 9, delta=1e-4)
        self.assertAlmostEqual(result[1], 8, delta=1e-4)

    def test_concatenated(self):
        try:
            import arrayfire as af
            a = array([[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10], [1, 11]])
            b = absolute_sum_of_changes(a).to_arrayfire()
            c = af.transpose(b)
            d = array(array_reference=c.arr)
            e = abs_energy(d).to_numpy()
            self.assertAlmostEqual(e[0], 385, delta=self.DELTA)
        except ModuleNotFoundError:
            logging.error("This test needs the Arrayfire package in order to be executed.")


if __name__ == '__main__':
    unittest.main()
