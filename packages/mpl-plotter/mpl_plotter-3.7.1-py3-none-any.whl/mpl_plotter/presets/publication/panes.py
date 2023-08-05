import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mpl_plotter.presets.publication.two_d import line
from mpl_plotter.setup import figure
from mpl_plotter.color.schemes import one


class Lines:

    """
    Pane plots
    """
    @classmethod
    def n_pane_single(cls, x, y,
                      labels=None,
                      filename=None, where_does_this_go=None,
                      **kwargs):
        """
        :param where_does_this_go: Are these plots of the numerical, analytical, or validation data
        """

        fig = figure((6.86*len(y), 3.5))

        for i in range(len(y)):
            ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
            line(x=x, y=y[0], color=one()[i], ax=ax_transient, fig=fig,
                 y_label=labels[i] if not isinstance(labels, type(None)) else None,
                 **kwargs)

        if not isinstance(filename, type(None)) and not isinstance(where_does_this_go, type(None)):
            plt.savefig(f"{where_does_this_go}/{filename}.pdf")
            plt.show()

    @classmethod
    def n_pane_comparison(cls, x, y, y1,
                          labels=None, legend_labels=None,
                          filename=None, where_does_this_go=None,
                          **kwargs):
        """
        :param where_does_this_go: Is this validation or verification
        """

        if not len(y) == len(y1):
            raise ValueError(f"Arrays y, y1 have different lengths: {len(y)} and {len(y1)}")

        fig = figure((6.86*len(y), 3.5))

        for i in range(len(y)):
            ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
            if i < (len(y)-1):
                cls.comparison(x, [y[i], y1[i]], ax_transient, fig,
                               labels[i] if not isinstance(labels, type(None)) else None)
            else:
                cls.comparison(x, [y[i], y1[i]], ax_transient, fig,
                               labels[i] if not isinstance(labels, type(None)) else None,
                               plot_label1=legend_labels[0] if not isinstance(legend_labels, type(None)) else None,
                               plot_label2=legend_labels[1] if not isinstance(legend_labels, type(None)) else None,
                               legend=True if not isinstance(legend_labels, type(None)) else False,
                               legend_loc=(0.875, 0.425),
                               **kwargs)

        plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)

        if not isinstance(filename, type(None)) and not isinstance(where_does_this_go, type(None)):
            legend = (c for c in ax_transient.get_children() if isinstance(c, mpl.legend.Legend))
            plt.savefig(f"{where_does_this_go}/{filename}.pdf",
                        bbox_extra_artists=legend, bbox_inches='tight')
            plt.show()

    """
    Single line plots
    """

    @classmethod
    def comparison(cls, x, y,
                   ax=None, fig=None,
                   label=None,
                   plot_label1=None, plot_label2=None,
                   legend=False, legend_loc=None,
                   **kwargs):
        if np.all(y[0] == y[0][0]):
            a = y[0]
            b = y[1]
            color1 = one()[0]
            color2 = one()[1]
        elif np.all(y[1] == y[1][0]):
            a = y[1]
            b = y[0]
            color1 = one()[1]
            color2 = one()[0]
        else:
            a = y[0]
            b = y[1]
            color1 = one()[0]
            color2 = one()[1]

        line(x=x, y=a, color=color1,
             plot_label=plot_label1, resize_axes=False, grid=False,
             ax=ax if not isinstance(ax, type(None)) else None, fig=fig if not isinstance(fig, type(None)) else None
             )
        line(x=x, y=b, color=color2,
             y_label=label, plot_label=plot_label2,
             legend=legend, legend_loc=legend_loc,
             y_bounds=[min(y[0].min(), y[1].min()), max(y[0].max(), y[1].max())],
             custom_y_tick_locations=[min(y[0].min(), y[1].min()), max(y[0].max(), y[1].max())],
             ax=ax if not isinstance(ax, type(None)) else None, fig=fig if not isinstance(fig, type(None)) else None,
             **kwargs
             )
