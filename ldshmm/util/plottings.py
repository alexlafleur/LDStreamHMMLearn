import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import probplot

class ComplexPlot():
    cols = 2
    current = 1
    im = None

    def new_plot(self, heading, rows, cols=2):
        plt.figure()
        plt.suptitle(heading)
        self.rows=rows+1
        self.cols = cols


    def add_data_to_plot(self, data, x_labels, y_labels, y_label, minimum, maximum, x_label="taumeta"):
        plt.subplot(self.rows, self.cols, self.current)
        self.im = plt.pcolor(data, vmin=minimum, vmax=maximum, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(x_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        self.current = self.current + 1


    def add_to_plot_separate_colorbar(self, data_naive, data_bayes, x_labels, y_labels, y_label):
        plt.subplot(self.rows,self.cols,self.current)
        plt.pcolor(data_naive, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(y_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel("taumeta")
        plt.ylabel(y_label)
        plt.colorbar()
        #plt.tight_layout(0.5)
        self.current = self.current+1

        plt.subplot(self.rows,self.cols,self.current)
        plt.pcolor(data_bayes, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(y_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel("taumeta")
        plt.ylabel(y_label)
        plt.colorbar()
        #plt.tight_layout(0.5)
        self.current = self.current + 1

    def add_to_plot_same_colorbar (self, data_naive, data_bayes, x_labels, y_labels, y_label, minimum, maximum, x_label="taumeta"):
        plt.subplot(self.rows, self.cols, self.current)
        self.im = plt.pcolor(data_naive, vmin=minimum, vmax=maximum, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(x_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        #plt.tight_layout(0.5)
        self.current = self.current+1

        plt.subplot(self.rows, self.cols, self.current)
        self.im = plt.pcolor(data_bayes, vmin=minimum, vmax=maximum, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(y_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        #plt.tight_layout(0.5)
        self.current = self.current + 1

    def add_to_plot_same_colorbar_new(self, data_naive, data_naive_new, data_bayes, x_labels, y_labels, y_label, minimum, maximum):
        plt.subplot(self.rows, self.cols, self.current)
        self.im = plt.pcolor(data_naive, vmin=minimum, vmax=maximum, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(x_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel("taumeta")
        plt.ylabel(y_label)
        plt.tight_layout(2)
        self.current = self.current+1

        plt.subplot(self.rows, self.cols, self.current)
        self.im = plt.pcolor(data_naive_new, vmin=minimum, vmax=maximum, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(y_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel("taumeta")
        plt.ylabel(y_label)
        plt.tight_layout(2)
        self.current = self.current + 1

        plt.subplot(self.rows, self.cols, self.current)
        self.im = plt.pcolor(data_bayes, vmin=minimum, vmax=maximum, cmap="Reds")
        plt.xticks(np.arange(len(x_labels)), (str(x_label) for x_label in x_labels))
        plt.yticks(np.arange(len(y_labels)), (str(y_label) for y_label in y_labels))
        plt.xlabel("taumeta")
        plt.ylabel(y_label)
        plt.tight_layout(2)
        self.current = self.current + 1

    def save_plot_same_colorbar(self, heading):
        ax = plt.subplot(self.rows, self.cols, self.rows*self.cols)
        cbar = plt.colorbar(self.im, ax=ax, orientation="horizontal")
        labels = cbar.ax.get_xticklabels()
        cbar.ax.tick_params(labelsize=6)
        cbar.ax.set_xticklabels(labels=labels, rotation=45)
        plt.delaxes(ax)

        plt.savefig(heading + ".pdf")


    def save_plot_separate_colorbars(self, heading):
        plt.savefig(heading + ".pdf")

class LinePlot():

    current = 1
    ax = None

    def new_plot(self, heading, rows, cols=2):
        plt.figure()
        plt.suptitle(heading)

        #plt.xlim(xmin=0)
        self.rows=rows
        self.cols=cols

    def new_subplot(self, y_label, x_label):
        if self.ax is not None:
            self.ax.set_xlim(xmin=0)

        self.ax = plt.subplot(self.rows, self.cols, self.current)
        self.ax.set_ylabel(y_label)
        self.ax.set_xlabel(x_label)
        self.current += 1

    def add_line_to_plot(self, line_data, x_values, marker=None):
        if marker is not None:
            self.ax.plot(x_values, line_data, marker=marker)
        else:
            self.ax.plot(x_values, line_data)

    def add_legend(self, x_labels):
        if self.ax is not None:
            self.ax.set_xlim(xmin=0)
        plt.legend([str(x) for x in x_labels], loc='upper center', ncol=4,
                   fancybox=True, fontsize=6)

    def add_to_plot(self, data_naive, data_bayes, x_labels, y_label, evaluated_param_name):
        plt.subplot(self.rows, self.cols, self.current)
        plt.xlabel('taumeta')
        plt.ylabel(y_label)

        for bayes_array_piece in data_naive:
            plt.plot(x_labels, bayes_array_piece, marker='o')

        plt.legend([evaluated_param_name + " = " + str(x) for x in x_labels], loc='upper center', ncol=3,
                   fancybox=True, fontsize=6)
        plt.tight_layout(2)
        plt.xticks(np.linspace(0, x_labels[-1], 5, endpoint=True))
        plt.xlim(1, x_labels[-1]+1)

        self.current = self.current + 1


        plt.subplot(self.rows, self.cols, self.current)
        plt.xlabel('taumeta')
        plt.ylabel(y_label)

        for bayes_array_piece in data_bayes:
            plt.plot(x_labels, bayes_array_piece, marker='o')

        plt.legend([evaluated_param_name + " = " + str(x) for x in x_labels], loc='upper center', ncol=3,
                   fancybox=True, fontsize=6)
        plt.tight_layout(2)
        plt.xticks(x_labels)
        plt.xlim(1, x_labels[-1]+1)
        self.current = self.current + 1

    def save_plot(self, heading):
        plt.savefig(heading + ".pdf")

class ProbPlot():
    cols = 2
    current = 1

    def new_plot(self, rows, cols=2):
        plt.figure()
        self.rows = rows
        self.cols = cols

    def add_to_plot(self, data):
        plt.subplot(self.rows, self.cols, self.current)
        res = probplot(x=data, plot=plt)
        self.current = self.current+1
        plt.tight_layout(0.5)

    def save_plot(self, heading):
        plt.savefig(heading + ".pdf")


class PointPlot():
    cols = 2
    current = 1

    def new_plot(self, heading, rows, num_curves):
        plt.figure()
        plt.suptitle(heading)
        self.rows = rows
        NUM_COLORS = num_curves
        cm = plt.get_cmap('gist_rainbow')
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_color_cycle([cm(1. * i / NUM_COLORS) for i in range(NUM_COLORS)])
        plt.rc('text', usetex=True)


    def add_data_to_plot(self, err_data, x_axis_data, label):
        plt.plot(x_axis_data, err_data, marker='o', label=label)
        plt.xticks(x_axis_data)
        plt.xlabel(r'$log_2 (window\_size)$')
        plt.ylabel(r'$log_2 (E(error))$')

    def create_legend(self):
        plt.legend(loc="upper right", fontsize=8)
        #plt.tight_layout(2)

    def add_to_plot(self, err_data, tmatrix_err_data):
        plt.subplot(self.rows, self.cols, self.current)
        x_axis = range(0, len(err_data))
        plt.plot(x_axis, err_data, marker='o', label="Normal Error")

        x_axis = range(0, len(tmatrix_err_data))
        plt.plot(x_axis, tmatrix_err_data, marker='D', label="Tmatrix Sampler Error")

        plt.legend(loc="upper left", fontsize=4)
        self.current = self.current + 1
        plt.tight_layout(2)

    def save_plot(self, heading):
        plt.savefig(heading + ".png")


def plot_result_heatmap(data_naive, data_bayes, x_labels, y_labels, y_axis_name, type, heading):
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.pcolor(data_naive, cmap="Reds")
    plt.title(heading)
    plt.xticks(np.arange(3), (str(x_label) for x_label in x_labels))
    plt.yticks(np.arange(3), (str(y_label) for y_label in y_labels))
    plt.xlabel("taumeta")
    plt.ylabel(y_axis_name)
    plt.title("Naive " + type)
    plt.colorbar()
    plt.tight_layout(2)

    plt.subplot(1, 2, 2)
    plt.pcolor(data_bayes, cmap="Reds")
    plt.title("Bayes " + type)
    plt.xticks(np.arange(3), (str(x_label) for x_label in x_labels))
    plt.yticks(np.arange(3), (str(y_label) for y_label in y_labels))
    plt.xlabel("taumeta")
    plt.ylabel(y_axis_name)
    plt.colorbar()
    plt.tight_layout(2)

    plt.savefig(heading + ".png")

def plot_result(y_axis1_list, y_axis2_list, type, heading):
    """Plotting function for diagram with two y axes

    Parameters
        ----------
        y_axis1_list : list of elements for first y axis
        y_axis2_list : list of elements for second y axis
        type : string which characterizes the type subplotsof calculation (for instance "naive" or "bayes").
        heading : The custom heading for the plot title

        The two latter ones are just for plotting and saving the resulting plot. The filename will be type+ _ +heading
        """
    t_time = range(0, len(y_axis1_list))

    fig, ax1 = plt.subplots()
    ax1.plot(t_time, y_axis1_list, 'b-')
    ax1.set_xlabel('time t')
    ax1.set_ylabel('performance time')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax2 = ax1.twinx()

    t_time = range(0, len(y_axis2_list))
    ax2.plot(t_time, y_axis2_list, 'r.')
    ax2.set_ylabel('error')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.title(heading)
    plt.savefig(type + '_' + heading + '.png')