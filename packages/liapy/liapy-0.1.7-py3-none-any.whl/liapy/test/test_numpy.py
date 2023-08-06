"""
Interestingly, this is off by a bit (about 0.6% when measuring 10 periods). This appears to converge to the correct answer when an increasing number of periods are included and an increasing number of points on the sinewave are sampled. If we want better accuracy than this we will need to perform some data interpolation i.e. (filtering)
"""
import unittest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from matplotlib import pyplot as plt
from liapy import LIA

class TestLIANumpy(unittest.TestCase):
    def setUp(self):
        self.data_length= 1000
        self.sampling_frequency = 9700.0
        self.signal_rms_amplitude = 0.036
        self.signal_frequency = 105.4
        self.phase_delay = 0.34
        samples_per_period = self.sampling_frequency / self.signal_frequency

        number_periods = int(np.floor(self.data_length / (self.sampling_frequency / self.signal_frequency)))
        number_sync_points = number_periods + 1
        indices = np.arange(0, number_sync_points, 1)
        self.sync_points = (1/2*self.sampling_frequency / self.signal_frequency * \
                           (1 + 2*indices + self.phase_delay/np.pi)).astype(np.int)

        times = np.arange(0, self.data_length*1/self.sampling_frequency, 1/self.sampling_frequency)
        self.test_data = self.signal_rms_amplitude * np.sqrt(2) * \
            np.sin(2*np.pi*self.signal_frequency* times - self.phase_delay)
        self.lia = LIA(sampling_frequency=self.sampling_frequency,
                data=self.test_data, sync_points=self.sync_points)

    def testLIASetup(self):
        assert_equal(self.lia.sampling_frequency, self.sampling_frequency)
        assert_equal(self.test_data, self.lia.data)
        assert_equal(self.data_length, self.lia.data_length)

    def testLIaExtractSignalFrequency(self):
        assert_equal(self.lia.extractSignalFrequency(), 105.32030401737242)

    def testLIAExtractAmplitude(self):
        signal_rms_amplitude = self.lia.extractSignalAmplitude(self.signal_frequency)
        #plt.plot(self.test_data[self.sync_points[0]:self.sync_points[-1]])
        assert_equal(isinstance(signal_rms_amplitude, float), True)
        assert_equal(signal_rms_amplitude, 0.035917003718687314) # We can't get exactly the right amplitude, but we can get pretty close.

