import pint
import re
ureg = pint.UnitRegistry()

def sampling_period(data):
    """
    Extracts the sample period from a pandas DataFrame assuming that data is evenly spaced in time. Uses the difference in time between the first and second data points to determine the sampling period  and sampling frequency.

    :param data: Pandas array with Time (including units, i.e. Time (ms)). 
    :returns sampling_period: Sampling period as a pint quantity.
    """
    # For now, assume time is the first variable in the column
    columns_names = data.columns.values
    time_column = 0
    time_string = columns_names[time_column]
    delta_time = data[time_string][1] - data[time_string][0]

    sampling_period = delta_time * title_to_quantity(time_string)
    return sampling_period

def frequency_bin_size(data):
    """
    Extracts the frequency bin (in Hz, as a pint unit) from a PSD dataset.

    :param data: Input power spectral density as a Pandas Array
    :returns bin_size: frequency bin size as a pint unit
    """
    column_names = data.columns.values
    frequency_column = 0
    frequency_string = column_names[frequency_column]
    delta_frequency = data[frequency_string].iloc[1] - data[frequency_string].iloc[0]

    bin_size = delta_frequency * title_to_quantity(frequency_string)
    return bin_size

def title_to_quantity(quantity_string):
    """
    Extracts unit from a column name such as Time (ms).
    """
    # Search for anything in parentheses, interpret as a unit.
    # Squared units are fine.
    unit_pattern = re.compile(r'[\(][\w]+[\^]*[\s]*[\*]*[\s]*[\d]*[\)]')
    match = unit_pattern.search(quantity_string)
    if match == None:
        raise ValueError(f'Cannot match units of string {quantity_string}')

    bare_unit_string = match.group()[1:-1] # remove parentheses
    quantity = 1 * ureg.parse_expression(bare_unit_string)
    return quantity

def quantity_to_title(quantity):
    """
    Converts a quantity into a standard title
    """
    title_mapping = {
        ureg.V: 'Voltage',
        ureg.A: 'Current',
        ureg.ohm: 'Impedance',
        ureg.V**2: 'Power',
        ureg.A**2: 'Power',
        ureg.ohm**2: 'Power',
        ureg.Hz: 'Frequency',
        ureg.s: 'Time',
    }
    standard_unit = to_standard_quantity(quantity).units
    title = title_mapping[standard_unit] + ' ({:~})'.format(quantity.units)
    return title

def to_standard_quantity(quantity):
    """
    :param quantity: Pint quantity in non-standard form (i.e. mV)
    """
    unit = quantity.units
    return_tuple = ureg.parse_unit_name(str(unit))
    if len(return_tuple) == 1:
        (prefix, base_unit, _) = return_tuple[0]
    else: # We have some power quantities to deal with
        unit_power = int(str(unit)[-1])
        unit_base_str = str(unit)[:-5]
        (prefix, base_unit, _) = ureg.parse_unit_name(unit_base_str)[0]
        base_unit = ureg.Quantity(1, base_unit)**unit_power

    new_quantity = quantity.magnitude * ureg.Quantity(1, unit).to(base_unit)
    return new_quantity
