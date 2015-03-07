# -*- coding: utf-8 -*-
"""
In this example, we want to show you how you can take isolated blocks of code
(featuring different kinds of Bokeh visualizations) and rearrange them in a
bigger (encompassing) flask-based application without losing the independence
of each example. This is the reason of some weirdness through the code.
We are using this "building blocks" approach here because we believe it has some
conceptual advantages for people trying to quickly understand, and more
importantly, use the embed API, in a more complex way than just a simple script.
"""

from bokeh.embed import autoload_server
from visualization import generate_figure

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def render_plot():
    """
    Get the script tags from each plot object and "insert" them into the template.

    This also starts different threads for each update function, so you can have
    a non-blocking update.
    """
    # FIXME: do not hardcode the csv file path
    tag = autoload_server(*generate_figure('data/testdata.csv'))

    return render_template('app.html', map=tag)


if __name__ == '__main__':
    app.run(debug=True)
