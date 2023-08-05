from mpl_plotter.two_d import line as mpl_line, scatter as mpl_scatter
from mpl_plotter.presets.precision.config import precision


class line(mpl_line):

    def __init__(self, x, y, **kwargs):

        input = {**precision, **kwargs}

        super().__init__(x=x, y=y, **input)


class scatter(mpl_scatter):

    def __init__(self, x, y, **kwargs):

        input = {**precision, **kwargs}

        super().__init__(x=x, y=y, **input)
