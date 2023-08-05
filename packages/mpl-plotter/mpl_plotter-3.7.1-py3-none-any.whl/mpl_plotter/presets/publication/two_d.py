from mpl_plotter.two_d import line as mpl_line, scatter as mpl_scatter
from mpl_plotter.presets.publication.config import publication


class line(mpl_line):

    def __init__(self, x, y, **kwargs):
        input = {**publication, **kwargs}

        super().__init__(x=x, y=y, **input)


class scatter(mpl_scatter):

    def __init__(self, x, y, **kwargs):
        input = {**publication, **kwargs}

        super().__init__(x=x, y=y, **input)
