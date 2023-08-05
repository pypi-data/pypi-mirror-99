import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mpl_plotter.presets.publication.two_d import line
from mpl_plotter.setup import figure
from mpl_plotter.color.schemes import one

from Alexandria.general.console import print_color


class LinePlots:

    """
    Pane plots
    """

    def n_pane_single(self, t, y, labels, filename, where_does_this_go):
        """
        :param where_does_this_go: Are these plots of the numerical, analytical, or validation data
        """

        fig = figure((6.86*len(y), 3.5))

        for i in range(len(y)):
            ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
            line(x=t, y=y[0], color=one()[i], y_label=labels[0], ax=ax_transient, fig=fig)

        plt.tight_layout()
        plt.savefig(f"{where_does_this_go}/{filename}.pdf")
        plt.show()

    def n_pane_comparison(self, t, y, y1, labels, legend_labels, filename, where_does_this_go):
        """
        :param where_does_this_go: Is this validation or verification
        """

        if not len(y) == len(y1):
            raise ValueError(f"Arrays y, y1 have different lengths: {len(y)} and {len(y1)}")

        fig = figure((6.86*len(y), 3.5))

        for i in range(len(y)):
            ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
            if i < (len(y)-1):
                self.comparison(t, [y[0], y1[0]], ax_transient, fig, labels[0])
            else:
                self.comparison(t, [y[i], y1[i]], ax_transient, fig, labels[3],
                                plot_label1=legend_labels[0], plot_label2=legend_labels[1],
                                legend=True, legend_loc=(0.875, 0.425))

        plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)
        legend = (c for c in ax_transient.get_children() if isinstance(c, mpl.legend.Legend))
        plt.savefig(f"{where_does_this_go}/{filename}.pdf",
                    bbox_extra_artists=legend, bbox_inches='tight')
        plt.show()

    """
    Single line plots
    """

    def single(self, t, y, label, filename=None, save=False):
        line(x=t, y=y, y_label=label)
        plt.tight_layout()
        if save:
            plt.savefig(f"results/analytical/{filename}.pdf")
        plt.show()

    def comparison(self, t, y,
                   ax, fig,
                   label=None,
                   plot_label1=None, plot_label2=None,
                   legend=False, legend_loc=None,):
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
        line(x=t, y=a, color=color1, ax=ax, fig=fig,
             plot_label=plot_label1, resize_axes=False)
        line(x=t, y=b, color=color2, ax=ax, fig=fig,
             y_label=label, plot_label=plot_label2,
             legend=legend, legend_loc=legend_loc,
             y_bounds=[min(y[0].min(), y[1].min()), max(y[0].max(), y[1].max())],
             custom_y_tick_locations=[min(y[0].min(), y[1].min()), max(y[0].max(), y[1].max())])

    def problem(self, s):
        print("We got a problem\n")
        print("Your 'where_does_this_go' variable,\n")
        print_color(f"          {s}\n", "red")
        print("is neither 'numerical', 'analytical', 'flight-data', 'verification' nor 'validation'."
              " Think about that\n")
