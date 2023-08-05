from mpl_plotter.two_d import line as mpl_line, scatter as mpl_scatter
from Alexandria.file.parsers import yaml_parser


class line(mpl_line):

    def __init__(self, x, y, **kwargs):

        input = {**yaml_parser("mpl_plotter/presets/precision/precision.yaml"), **kwargs}

        super().__init__(x=x, y=y, **input)


class scatter(mpl_scatter):

    def __init__(self, x, y, **kwargs):

        input = {**yaml_parser("mpl_plotter/presets/precision/precision.yaml"), **kwargs}

        super().__init__(x=x, y=y, **input)
