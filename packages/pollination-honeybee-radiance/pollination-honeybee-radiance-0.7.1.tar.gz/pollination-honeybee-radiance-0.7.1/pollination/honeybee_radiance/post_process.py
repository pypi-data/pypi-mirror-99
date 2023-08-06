from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class ConvertToBinary(Function):
    """Convert a Radiance matrix to a new matrix with 0-1 values."""

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    minimum = Inputs.float(
        description='Minimum range for the values that will be converted to 1.',
        default=-1 * 10**100
    )

    maximum = Inputs.float(
        description='Maximum range for the values that will be converted to 1.',
        default=10**100
    )

    include_min = Inputs.str(
        description='A flag to include the minimum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    include_max = Inputs.str(
        description='A flag to include the maximum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    reverse = Inputs.str(
        description='A flag to reverse the selection logic. This is useful for cases '
        'that you want to all the values outside a certain range to be converted to 1. '
        'By default the input logic will be used as is.', default='comply',
        spec={'type': 'string', 'enum': ['comply', 'reverse']}
    )

    @command
    def convert_to_zero_one(self):
        return 'honeybee-radiance post-process convert-to-binary input.mtx ' \
            '--output binary.mtx --maximum {{self.maximum}} ' \
            '--minimum {{self.minimum}} --{{self.reverse}} ' \
            '--{{self.include_min}}-min --{{self.include_max}}-max'

    # outputs
    output_mtx = Outputs.file(
        description='Newly created binary matrix.', path='binary.mtx'
    )


@dataclass
class Count(Function):
    """Count values in a row that meet a certain criteria."""

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    minimum = Inputs.float(
        description='Minimum range for the values that should be counted.',
        default=-1 * 10**100
    )

    maximum = Inputs.float(
        description='Maximum range for the values that should be counted.',
        default=10**100
    )

    include_min = Inputs.str(
        description='A flag to include the minimum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    include_max = Inputs.str(
        description='A flag to include the maximum threshold itself. By default the '
        'threshold value will be included.', default='include',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    reverse = Inputs.str(
        description='A flag to reverse the selection logic. This is useful for cases '
        'that you want to all the values outside a certain range. By default the input '
        'logic will be used as is.', default='comply',
        spec={'type': 'string', 'enum': ['comply', 'reverse']}
    )

    @command
    def count_values(self):
        return 'honeybee-radiance post-process count input.mtx ' \
            '--output counter.mtx --maximum {{self.maximum}} ' \
            '--minimum {{self.minimum}} --{{self.reverse}} ' \
            '--{{self.include_min}}-min --{{self.include_max}}-max'

    # outputs
    output_mtx = Outputs.file(
        description='Newly created binary matrix.', path='counter.mtx'
    )


@dataclass
class SumRow(Function):
    """Postprocess a Radiance matrix and add all the numbers in each row.

    This function is useful for translating Radiance results to outputs like radiation
    to total radiation. Input matrix must be in ASCII format. The header in the input
    file will be ignored.
    """

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    @command
    def sum_mtx_row(self):
        return 'honeybee-radiance post-process sum-row input.mtx --output sum.mtx'

    # outputs
    output_mtx = Outputs.file(description='Newly created sum matrix.', path='sum.mtx')


@dataclass
class AverageRow(Function):
    """Postprocess a Radiance matrix and average all the numbers in each row."""

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    @command
    def average_mtx_row(self):
        return 'honeybee-radiance post-process average-row input.mtx ' \
            '--output average.mtx'

    # outputs
    output_mtx = Outputs.file(
        description='Newly created average matrix.', path='average.mtx'
    )


@dataclass
class AnnualDaylightMetrics(Function):
    """Calculate annual daylight metrics for annual daylight simulation."""

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='raw_results'
    )

    schedule = Inputs.file(
        description='Path to an annual schedule file. Values should be 0-1 separated '
        'by new line. If not provided an 8-5 annual schedule will be created.',
        path='schedule.txt', optional=True
    )

    thresholds = Inputs.str(
        description='A string to change the threshold for daylight autonomy and useful '
        'daylight illuminance. Valid keys are -t for daylight autonomy threshold, -lt '
        'for the lower threshold for useful daylight illuminance and -ut for the upper '
        'threshold. The defult is -t 300 -lt 100 -ut 3000. The order of the keys is not '
        'important and you can include one or all of them. For instance if you only '
        'want to change the upper threshold to 2000 lux you should use -ut 2000 as '
        'the input.', default='-t 300 -lt 100 -ut 3000'
    )

    @command
    def calculate_annual_metrics(self):
        return 'honeybee-radiance post-process annual-daylight raw_results ' \
            '--schedule schedule.txt {{self.thresholds}} --sub_folder ../metrics'

    # outputs
    annual_metrics = Outputs.folder(
        description='Annual metrics folder. This folder includes all the other '
        'subfolders which are also exposed as separate outputs.', path='metrics'
    )

    daylight_autonomy = Outputs.folder(
        description='Daylight autonomy results.', path='metrics/da'
    )

    continuous_daylight_autonomy = Outputs.folder(
        description='Continuous daylight autonomy results.', path='metrics/cda'
    )

    useful_daylight_illuminance_lower = Outputs.folder(
        description='Lower useful daylight illuminance results.',
        path='metrics/udi_lower'
    )

    useful_daylight_illuminance = Outputs.folder(
        description='Useful daylight illuminance results.', path='metrics/udi'
    )

    useful_daylight_illuminance_upper = Outputs.folder(
        description='Upper useful daylight illuminance results.',
        path='metrics/udi_upper'
    )
