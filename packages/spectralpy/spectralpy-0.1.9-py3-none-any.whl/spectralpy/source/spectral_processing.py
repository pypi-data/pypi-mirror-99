"""
TODO: Add power spectrum plotting for pandas as well as numpy, separate out the two.
"""
import numpy as np
import pandas as pd
from scipy.signal.windows import hann
from sugarplot import plt, prettifyPlot
from spectralpy import sampling_period, title_to_quantity, to_standard_quantity, quantity_to_title
from pint import UnitRegistry
import re
ureg = UnitRegistry()

def power_spectrum(data, window='box', siding='single'):
    """
    Computes the single-or double-sided power spectrum with different types
    of filetring (hann, boxcar)

    :param data: data to be transformed
    :param window: window type - hann or box
    :param siding: 'single' or 'double' sided spectrum.

    """
    data_length = len(data)

    if window == 'box' or window == 'boxcar':
        window_data = 1
    elif window == 'hann':
        hann_normalized = hann(data_length) / \
            np.sqrt(np.mean(np.square(hann(data_length))))
        window_data = hann_normalized
    else:
        raise ValueError(
            f'Window type {window} not supported. Supported types are \
            box and hann')
    if isinstance(data, np.ndarray):
        power_spectrum = power_spectrumNumpy(
            data, window_data, siding=siding)
    elif isinstance(data, pd.DataFrame):
        power_spectrum = power_spectrum_pandas(
            data, window_data=window_data, siding=siding)
    else:
        raise ValueError(f"Function not implemented for type {type(data)},"+
                         "only np.ndarray, pd.DataFrame.")

    return power_spectrum

def power_spectrum_pandas(data, window_data=1, siding='single'):
    """
    Implementation of powerSpectrum for a pandas DataFrame.

    :param window_data: Raw window data to multiply the time-domain data by
    :param siding: single or double (sinusoidal or exponential)
    """
    Ts = sampling_period(data)
    sampling_frequency = (1 / Ts).to(ureg.Hz)
    sampling_frequency_Hz = (1 / Ts).to(ureg.Hz).magnitude

    power_quantity = title_to_quantity(data.columns.values[1])**2
    power_quantity = to_standard_quantity(power_quantity)
    power_title = quantity_to_title(power_quantity)
    frequency_title = quantity_to_title(sampling_frequency)

    half_data_length = int((len(data)/2+1))
    if siding == 'double':
        frequencies = np.linspace(-sampling_frequency_Hz/2,
                                  sampling_frequency_Hz/2,
                                  2*half_data_length - 1)
    elif siding == 'single':
        frequencies = np.linspace(0, sampling_frequency_Hz/2,
                                  half_data_length)
    else: raise ValueError(f'No such siding {siding}')


    fft_data = power_quantity.magnitude * power_spectrumNumpy(
        data.iloc[:,1].values,
        window_data=window_data, siding=siding)
    overall_data = pd.DataFrame(
        {frequency_title: frequencies, power_title: fft_data})
    return overall_data

def power_spectrumNumpy(data, window_data, siding='single'):
    """
    Implementation of powerSpectrum for numpy arrays.

    :param data: Input data (numpy array)
    :param window_data: Raw window data to multiply the data by
    :param siding: single or double (sinusoidal or complex)
    :returns power_spectrum: Power spectrum as a numpy array
    """
    bare_fft = np.fft.fft(data * window_data / len(data))
    power_spectrum = np.square(np.abs(bare_fft))
    half_data_length = int((len(data)/2+1))
    if siding == 'single':
        # Change PSD from e^jx to sin(x)
        power_spectrum = \
            2 * power_spectrum[0:half_data_length]
        # DC component does not need to be corrected.
        power_spectrum[0] /= 2

    return power_spectrum
