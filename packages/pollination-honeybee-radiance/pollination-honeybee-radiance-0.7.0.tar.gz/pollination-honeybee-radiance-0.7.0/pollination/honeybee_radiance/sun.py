from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class CreateSunMatrix(Function):
    """Generate a Radiance sun matrix (AKA sun-path)."""

    north = Inputs.int(
        description='An angle for north direction. Default is 0.',
        default=0, spec={'type': 'integer', 'maximum': 360, 'minimum': 0}
    )

    wea = Inputs.file(
        description='Path to a wea file.', extensions=['wea'], path='sky.wea'
    )

    output_type = Inputs.int(
        description='Output type. 0 is for visible and 1 is for solar.', default=0,
        spec={'type': 'integer', 'maximum': 1, 'minimum': 0}
    )

    @command
    def generate_sun_matrix(self):
        return 'gendaymtx -n -D sunpath.mtx -M suns.mod -O{{self.output_type}} ' \
            '-r {{self.north}} -v sky.wea'

    sunpath = Outputs.file(description='Output sunpath matrix.', path='sunpath.mtx')

    sun_modifiers = Outputs.file(
        description='List of sun modifiers in sunpath.', path='suns.mod'
    )


@dataclass
class ParseSunUpHours(Function):
    """Parse sun up hours from sun modifiers file."""

    sun_modifiers = Inputs.file(
        description='Path to sun-modifiers file.', path='suns.mod'
    )

    timestep = Inputs.int(
        description='An integer value to set the timestep of the input hours. If '
        'timestep is set to 1 the time will be offset by -0.5 to align with the start '
        'of the hour. For other timesteps the hour will not be adjusted.', default=1,
        spec={'type': 'integer', 'minimum': 1}
    )

    leap_year = Inputs.str(
        description='A flag to switch between a normal year and a leap year. The '
        'default is a normal year. Use leap-year if the input hours are for a full '
        'year', default='full-year',
        spec={'type': 'string', 'enum': ['full-year', 'leap-year']}
    )

    @command
    def parse_hours(self):
        return 'honeybee-radiance sunpath parse-hours suns.mod ' \
            '--name sun-up-hours.txt --timestep {{self.timestep}} --{{self.leap_year}}'

    sun_up_hours = Outputs.file(
        description='A text file that includes all the sun up hours. Each hour is '
        'separated by a new line.', path='sun-up-hours.txt'
    )
