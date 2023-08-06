"""
The idea is to make a generic ggplot-ish engine. Then, you can run "to_mpl()", "to_plotly()", etc. to
generate the graphic.

The goal is to provide a flexible plotting framework.
>>> from uplot import *
>>> plot(x, y)
"""

# https://altair-viz.github.io/getting_started/overview.html

from IPython import get_ipython
from IPython.display import display, HTML, SVG
from copy import deepcopy
import os.path
import pandas as pd
import sys
from tempfile import NamedTemporaryFile
from typelike import ArrayLike, NumberLike
import yaml

# test

# TODO facet wrap (?) pandas does this, maybe back into it that way
# this is not a high priority for me
"""
>>> import uplot as u
>>> # facet_wrap => for every column in data, create line
>>> u.figure(data) + u.line() + u.facet_wrap(n_col=4)  
>>> # facet_grid => for every unique label in column, create and xy line
>>> u.figure(data) + u.line() + u.facet_grid(column='label', x='x', y='y', n_col=4)    
"""

# Include directory
include_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_include')

# TODO lazy load this please
with open(os.path.join(include_dir, 'mpl_markers.yml'), 'r') as stream:
    mpl_markers = yaml.safe_load(stream.read())

with open(os.path.join(include_dir, 'mpl_line_styles.yml'), 'r') as stream:
    mpl_line_styles = yaml.safe_load(stream.read())


# Style defaults
# TODO make this customizable; allow user to specify different style in options
# https://matplotlib.org/3.2.2/gallery/style_sheets/style_sheets_reference.html
def set_mpl_theme():
    import matplotlib.pyplot as plt
    plt.style.use(os.path.join(include_dir, 'uplot.mplstyle'))


_style_defaults = {
    'legend': False
}


# https://ggplot2-book.org/polishing.html
# TODO one day think about SVG bounding box https://matplotlib.org/3.2.2/api/backend_svg_api.html
class Figure:
    def __init__(self, data=None, style=None):
        self._data = data
        self._style = style if style is not None else {}
        self._geometry_objects = []

    # Add a new Geometry
    def __add__(self, other):
        # Deepcopy self
        obj = deepcopy(self)

        # Type check
        if not isinstance(other, Geometry):
            raise AttributeError('must be Geometry instance')

        # Add Geometry
        obj.add_geometry(other)

        # Return
        return obj

    def __repr__(self):
        if not _is_pycharm():
            self.to_mpl(show=True)
        return super().__repr__()

    @property
    def geometry_objects(self):
        """
        Access the Geometry objects of the Figure.

        Returns
        -------
        list
        """

        # If there is nothing, return points
        if not self._geometry_objects:
            return [Line(style={'line_style': 'none', 'marker': 'circle'})]

        # Otherwise, return our saved geometry objects
        return self._geometry_objects

    # Add Geometry
    def add_geometry(self, geometry):
        """
        Add a child instance of Geometry to the Figure in place.

        Parameters
        ----------
        geometry : Geometry
            Child instance of Geometry.
        """

        # Make sure we have an instance of Geometry
        if not isinstance(geometry, Geometry):
            raise AttributeError('must be child of Geometry')

        # Tell the geometry who owns it
        geometry._figure = self

        # Add the figure object
        self._geometry_objects.append(geometry)

    # Get style from the dictionary
    def get_style(self, style, default=None, index=None):
        if style in self._style:
            result = self._style[style]
        else:
            result = _style_defaults.get(style, default)

        if isinstance(result, ArrayLike) and index is not None:
            result = result[index]
        return result

    # Show figure
    def show(self):
        """
        Show Figure using the default backend.
        """

        self.to_mpl(show=True)

    # Convert figure to matplotlib
    # noinspection PyShadowingNames
    def to_mpl(self, show=False, save_as=None):
        """
        Convert to matplotlib objects.

        Parameters
        ----------
        show : bool
            Should the figure be displayed?
        save_as : None or str
            If str is provided, filename to save the figure as.

        Returns
        -------
        matplotlib.pyplot.Figure, matplotlib.pyplot.Axis
            Returned only if `show` = False.
        """

        # Make sure pyplot is loaded
        import matplotlib.pyplot as plt
        set_mpl_theme()

        # Create the figure and axis
        height, width = self.get_style('height'), self.get_style('width')
        figsize = None
        if height is not None and width is not None:
            figsize = (width, height)
        figure = plt.figure(figsize=figsize)  # type: plt.Figure
        axis = figure.add_subplot()

        # Iterate through geometry objects and draw
        for geometry in self.geometry_objects:
            # noinspection PyProtectedMember
            geometry._to_mpl(figure, axis)

        # Canvas
        # figure.patch.set_facecolor(self.get_style('background'))

        # Set plot elements
        axis.set_xlabel(self.get_style('x_title'))
        axis.set_ylabel(self.get_style('y_title'))
        axis.set_xlim(self.get_style('x_min'), self.get_style('x_max'))
        axis.set_ylim(self.get_style('y_min'), self.get_style('y_max'))
        # TODO https://matplotlib.org/3.1.0/api/dates_api.html#matplotlib.dates.IndexDateFormatter set up date format
        # n_minor_ticks, n_major_ticks = self.get_style('n_minor_ticks'), self.get_style('n_major_ticks')
        # if n_minor_x_ticks is not None:
        #     # axis.tick_params(which='minor', length=n_minor_ticks)
        #     axis.xaxis.set_minor_locator(plt.MaxNLocator(n_minor_ticks))
        # if n_x_major_x_ticks is not None:
        #     # axis.tick_params(which='major', length=n_major_ticks)
        #     axis.xaxis.set_major_locator(plt.MaxNLocator(n_major_ticks))
        axis.tick_params(axis='x', labelrotation=self.get_style('x_rotation'))

        # Legend
        if self.get_style('legend'):
            axis.legend(bbox_to_anchor=(1., 0.5), loc='center left')

        # Should we save?
        if save_as is not None:
            # TODO there will have to be a way to include some arguments here
            figure.savefig(save_as)

        # Return
        if show:
            if _is_jupyter():
                # _display_svg(figure)
                return None
            else:
                figure.show()
            plt.close(figure)
            return None
        else:
            return figure, axis

    def to_plotnine(self):
        # https: // stackoverflow.com / questions / 19921842 / plotting - multiple - time - series - on - the - same - plot - using - ggplot
        pass

    # noinspection PyShadowingNames
    def to_plotly(self, height='4.8in', width='6.4in'):
        import plotly.graph_objects as go
        figure = go.Figure()
        for geometry in self.geometry_objects:
            # noinspection PyProtectedMember
            geometry._to_plotly(figure)
        display(HTML(figure.to_html(default_height=height, default_width=width)))


class Geometry(Figure):
    def __init__(self, data=None, style=None):
        super().__init__(data, style)
        self._figure = None

    def __add__(self, other):
        raise NotImplementedError

    def add_geometry(self, geometry):
        raise NotImplementedError

    # Get data from the Geometry first, then its parent
    def _get_data(self):
        # Get data from the Geometry first, then its parent
        data = self._data
        if data is None and isinstance(self._figure, Figure):
            data = self._figure._data

        # If there is still no data, throw an error
        if data is None:
            raise AttributeError('data does not exist')

        # If the data is not a DataFrame, throw an error
        if not isinstance(data, pd.DataFrame):
            raise AttributeError('data must be pandas DataFrame')

        # Return
        return data


# class Style:
#     def __init__(self, **kwargs):
#         self._kwargs = kwargs


class Bar(Geometry):
    def __init__(self, data=None, style=None):
        super().__init__(data, style)

    # noinspection PyShadowingNames
    def _to_mpl(self, figure, axis):
        # Get data
        data = self._get_data()
        x = data.index.values

        # Loop over all columns
        for i, column in enumerate(self._data.columns):
            # Get y for column
            y = self._data[column].values
            label = self.get_style('label', default=column, index=i)
            axis.bar(x, y, label=label)


class Error(Geometry):
    def __init__(self, data=None, style=None):
        super().__init__(data, style)

    # noinspection PyShadowingNames
    def _to_mpl(self, figure, axis):
        # Get data
        data = self._get_data()
        x = data.index.values

        # Loop over all columns
        for i, column in enumerate(data.columns):
            # Get y for column
            y = data[column].values
            label = self.get_style('label', default=column, index=i)
            color = self.get_style('color', index=i)
            line_style = self.get_style('line_style', index=i)
            if line_style is not None:
                line_style = mpl_line_styles[line_style]
            marker = self.get_style('marker', index=i)
            if marker is not None:
                marker = mpl_markers[marker]
            axis.plot(x, y, label=label, color=color, linestyle=line_style, marker=marker)


class Line(Geometry):
    def __init__(self, data=None, style=None):
        super().__init__(data, style)

    # noinspection PyShadowingNames
    def _to_mpl(self, figure, axis):
        # Get data
        data = self._get_data()
        x = data.index.values

        # Loop over all columns
        for i, column in enumerate(data.columns):
            # Get y for column
            y = data[column].values
            label = self.get_style('label', default=column, index=i)
            color = self.get_style('color', index=i)
            line_style = self.get_style('line_style', index=i)
            if line_style is not None:
                line_style = mpl_line_styles[line_style]
            marker = self.get_style('marker', index=i)
            if marker is not None:
                marker = mpl_markers[marker]
            axis.plot(x, y, label=label, color=color, linestyle=line_style, marker=marker)

    # noinspection PyShadowingNames
    def _to_plotly(self, figure):
        import plotly.graph_objects as go

        # Get data
        data = self._get_data()
        x = data.index.values

        # Loop over all columns
        for i, column in enumerate(data.columns):
            # Get y for column
            y = data[column].values
            label = self.get_style('label', default=column, index=i)
            # marker = self.get_style('marker', index=i)
            # if marker is not None:
            #     marker = markers_mpl[marker]
            figure.add_trace(go.Scatter(x=x, y=y, mode='lines', name=label))


#
# class Point(Geometry):
#     def __init__(self, data=None, style=None):
#         super().__init__(data, style)
#
#     # noinspection PyShadowingNames
#     def to_mpl(self, figure, axis):
#         x = self._data.index.values
#         for column in self._data.columns:
#             y = self._data[column].values
#             # TODO label override from style
#             axis.plot(x, y, 'o', label=column)


def figure(data=None, x=None, y=None, style=None):
    """
    Create a figure.

    Parameters
    ----------
    data : pandas.DataFrame
        If provided, uses the data in `data` for the figure.
    x : str or ArrayLike
        If provided, and `data` is not set, this is the independent variable.
    y : str or ArrayLike
        If provided, and `data` is not set, this is the dependent variable.
    style : dict
        If provided, list of style elements.

    Returns
    -------
    Figure
        Instance of Figure object.
    """

    # Coerce data
    data = _coerce_data_x_y(data, x, y)

    # Create Figure
    element = Figure(data, style)

    # Set figure attributes
    # ...

    # Return
    return element


def bar(x=None, y=None, style=None):
    data = _coerce_x_y(x, y)
    style = _coerce_style(style, defaults={'line_style': 'solid'})
    geometry = Bar(data, style)
    return geometry


def error(x=None, y=None, y_err=None, style=None):
    pass


def line(data=None, x=None, y=None, style=None):
    """
    Convenience function to create a Line object.

    Parameters
    ----------
    data : pandas.DataFrame
        If provided, uses the data in `data` for the object.
    x : str or ArrayLike
        If provided, and `data` is not set, this is the independent variable.
    y : str or ArrayLike
        If provided, and `data` is not set, this is the dependent variable.
    style : dict
        If provided, list of style elements.

    Returns
    -------
    Line
        Instance of Line object.
    """

    data = _coerce_data_x_y(data, x, y)
    style = _coerce_style(style, defaults={'line_style': 'solid'})
    element = Line(data, style)
    return element


def hline(y=None, style=None):
    if not isinstance(y, NumberLike):
        raise AttributeError('y must be a number')
    style = _coerce_style(style, defaults={'line_style': 'solid'})
    # return HorizontalLine(y, style)
    pass


def point(x=None, y=None, style=None):
    data = _coerce_x_y(x, y)
    style = _coerce_style(style, defaults={'marker': 'circle'})
    element = Line(data, style=style)
    return element


# Extract label from pandas if possible
def _get_label(x, default='x'):
    label = default
    if isinstance(x, pd.Series):
        label = x.name
    return label


# Coerce x and y into expected types and formats
# TODO is there a need for this and _coerce_data_x_y?? I don't think so.
def _coerce_x_y(x, y):
    # Sanity check
    if x is None:
        raise AttributeError('cannot parse data')

    # Create data
    data = None
    if y is None:
        data = x
        x = None

    # Coerce data, x, and y
    return _coerce_data_x_y(data, x, y)


# Coerce data and x and y into expected types and formats
def _coerce_data_x_y(data, x, y):
    # If data is not set
    if data is None:
        # If both of x and y are arrays, build DataFrame
        if isinstance(x, ArrayLike) and isinstance(y, ArrayLike):
            # Make sure y is an array of arrays (for simplicity)
            if isinstance(y, pd.Series) or not isinstance(y[0], ArrayLike):
                y = [y]

            # Build DataFrame
            x_label = _get_label(x, default='x')
            data = pd.DataFrame({x_label: x}).set_index(x_label)
            len_y = len(y)
            for i, yi in enumerate(y):
                if len_y == 1:
                    y_label_default = 'y'
                else:
                    y_label_default = 'y' + str(i)
                y_label = _get_label(yi, default=y_label_default)
                data[y_label] = yi if not isinstance(yi, pd.Series) else yi.values

        # If data is not set, and x and y are not arrays, we don't know what we're doing
        elif x is not None or y is not None:
            raise AttributeError('must pass data or x and y arrays')

    # Otherwise, if data is a DataFrame, extract out x and y columns
    elif isinstance(data, pd.DataFrame):
        # Create a copy of the DataFrame
        data = data.copy()

        # Set the index
        if x is not None:
            data = data.set_index(x)

        # Extract columns (need to create a copy so we're not working on a slice)
        if y is not None:
            data = data[y].copy()

    # Otherwise, if data is a Series, convert to DataFrame
    elif isinstance(data, pd.Series):
        data = data.to_frame()

    # Else
    else:
        raise AttributeError('cannot process input')

    # Return the DataFrame
    return data


def _coerce_style(style, defaults=None):
    if style is None:
        style = {}
    style = {key.lower(): value for key, value in style.items()}
    if defaults is not None:
        for key in defaults:
            if key not in style:
                style[key] = defaults[key]
    return style


#
# (
#     figure(style={'xtitle': '$x$', 'ytitle': '$y$', 'legend': True})
#     + line([1, 2, 3], [4, 5, 6], style={'marker': 'circle', 'label': 'y1'})
#     + line([1, 2, 3], [6, 5, 4], style={'marker': 'circle', 'label': 'y2'})
# ).to_mpl(show=True)

# Check if we are in PyCharm
def _is_pycharm():
    return '_pydev_imps' in sys.modules


# Check if we are in a Jupyter window
def _is_jupyter():
    """

    Exclude QtConsole:
    'qtconsole' not in sys.modules

    Exclude PyCharm:
    '_pydev_imps' not in sys.modules

    Returns
    -------

    """
    return get_ipython() and 'qtconsole' not in sys.modules and not _is_pycharm()


# Display SVG in IPython (for matplotlib)
def _display_svg(fig):
    with NamedTemporaryFile(delete=False) as tempfile:
        filename = str(tempfile.name) + '.svg'
    fig.savefig(fname=filename, transparent=True)
    display(SVG(filename))
    os.remove(filename)
