import pytest
import numpy as np
import pandas as pd
from numpy.testing import assert_equal, assert_allclose
from spectralpy import sampling_period, title_to_quantity, to_standard_quantity, frequency_bin_size, quantity_to_title
from pint import UnitRegistry

@pytest.fixture
def ureg():
    return UnitRegistry()

def testExtractSamplingPeriod(ureg):
    data = pd.DataFrame({'Time (ms)': [0, 0.1, 0.2, 0.3, 0.4],
                         'Values': [0, 1, 2, 3, 4]})
    actual_period = sampling_period(data)
    desired_period = ureg.ms * 0.1
    assert actual_period == desired_period

def test_quantity_to_title(ureg):
    quantity = ureg.mV*1.0
    desired_title = 'Voltage (mV)'
    actual_title = quantity_to_title(quantity)
    assert_equal(actual_title, desired_title)

    quantity = ureg.nA**2*1.0
    desired_title = 'Power (nA ** 2)'
    actual_title = quantity_to_title(quantity)
    assert_equal(actual_title, desired_title)


def testExtractTimeUnits(ureg):
    unit_string = 'Time (s)'
    desired_unit = 1 * ureg.s
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'time (ms)'
    desired_unit = 1 * ureg.ms
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Time (us)'
    desired_unit = 1 * ureg.us
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Time (ns)'
    desired_unit = 1 * ureg.ns
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Time (ps)'
    desired_unit = 1 * ureg.ps
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

def testExtractElectricalUnits(ureg):
    unit_string = 'Photocurrent (pA)'
    desired_unit = 1 * ureg.pA
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Photocurrent (nA)'
    desired_unit = 1 * ureg.nA
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Current (uA)'
    desired_unit = 1 * ureg.uA
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Jordans (mA)'
    desired_unit = 1 * ureg.mA
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'More Current (A)'
    desired_unit = 1 * ureg.A
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Photovoltage (V)'
    desired_unit = 1 * ureg.V
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Photovoltage (mV)'
    desired_unit = 1 * ureg.mV
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Photovoltage (uV)'
    desired_unit = 1 * ureg.uV
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

    unit_string = 'Photovoltage (nV)'
    desired_unit = 1 * ureg.nV
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

def testExtractSquaredUnits(ureg):
    unit_string = 'Voltage (mV^2)'
    desired_unit = 1 * ureg.mV ** 2
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

def test_title_to_quantity_squared_2(ureg):
    unit_string = 'Voltage (mV ** 2)'
    desired_unit = 1 * ureg.mV ** 2
    actual_unit = title_to_quantity(unit_string)
    assert desired_unit == actual_unit

def testToStandardUnit(ureg):
    quantity = 0.1 * ureg.mV
    desired_quantity = 0.1 * 1e-3 * ureg.V
    actual_quantity = to_standard_quantity(quantity)
    assert desired_quantity == actual_quantity

    quantity = 0.1 * ureg.mV ** 2
    desired_quantity = 0.1 * 1e-6 * ureg.V ** 2
    actual_quantity = to_standard_quantity(quantity)
    assert desired_quantity == actual_quantity

def test_frequency_bin_size(ureg):
    psd_data = pd.DataFrame({
            'Frequency (Hz)': [1.5, 3.0, 4.5],
            'Power (V^2)': [0, 1, 2]})
    actual_quantity = frequency_bin_size(psd_data)
    desired_quantity = 1*ureg.Hz*1.5
    assert actual_quantity == desired_quantity

def tearDown(ureg):
    pass # Tear down to be run after every test case

@classmethod
def tearDownClass(ureg):
    pass # Tear down to be run after entire script
