"""
quick.py
Written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from . import core

import izzy as iz
import pandas as pd
from typelike import ArrayLike


# Histogram
def hist():
    pass


# Pivot and plot
# TODO support 2D histograms
# TODO right now follows format of pandas -- may change (pivot(x, y, z, bins=blah, zbins=blah)
# TODO should the dependency for iz.pivot be removed?
def pivot(df, index, values, aggfunc='mean', bins=10, show=True):
    xy = iz.pivot(df, index=index, values=values, aggfunc=aggfunc, bins=bins)
    figure = core.figure(style={
        'x_title': index,
        'y_title': values
    })
    figure += core.line(xy.index.values, xy.iloc[:, 0].values)
    if show:
        figure.show()
    else:
        return figure


# Plot
def plot(data_or_x, y=None, x_min=None, x_max=None, x_rotation=None, x_title=None, y_min=None, y_max=None, y_title=None,
         height=None, width=None, legend=False, marker=None, show=True):
    """


    Parameters
    ----------
    data_or_x : pandas.DataFrame or ArrayLike
        DataFrame to plot, or the `x` dimension for plotting.
    y : ArrayLike
        (Optional) If present, `y` dimension for plotting. If this is an array of arrays, every interior array will be
        treated as a dependent variable to `x`.
    x_min : number
    x_max : number
    x_title : str
        (Optional) Title of the `x` axis.
    y_min : number
    y_max : number
    y_title : str
        (Optional) Title of the `y` axis.
    x_rotation : float
        (Optional) Rotation of `x` axis tick labels.
    height : float
        (Optional) Height of chart.
    width : float
        (Optional) Width of chart.
    legend : bool or ArrayLike
        If bool, yes or no if the legend should be display. If this is ArrayLike, then these are the legend titles.
    marker : str
        (Optional) Point marker.
    show : bool
        Should the figure be shown? (Default: True)

    Returns
    -------
    matplotlib.pyplot.figure.Figure or None
        Figure or nothing, depending on `show`.
    """

    # Handle data_or_x
    if isinstance(data_or_x, pd.DataFrame):
        data = data_or_x
        x = None

    else:
        data = None
        x = data_or_x

    # Create figure
    figure = core.figure(data=data, x=x, y=y, style={
        'x_min': x_min,
        'x_max': x_max,
        'x_rotation': x_rotation,
        'x_title': x_title,
        'y_min': y_min,
        'y_max': y_max,
        'y_title': y_title,
        'height': height,
        'width': width,
        'legend': legend
    })

    # Start building the figure
    figure += core.line(style={'marker': marker})

    # Return
    if show:
        _ = figure.to_mpl(show=True)
    else:
        return figure.to_mpl(show=False)
