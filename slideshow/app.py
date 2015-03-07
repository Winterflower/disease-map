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
import time
from threading import Thread

import numpy as np
import scipy.special

from bokeh.embed import autoload_server
from bokeh.models import GlyphRenderer
from bokeh.plotting import cursession, figure, output_server, push

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def render_plot():
    """
    Get the script tags from each plot object and "insert" them into the template.

    This also starts different threads for each update function, so you can have
    a non-blocking update.
    """
    plot, session = distribution()
    tag = autoload_server(plot, session)

    return render_template('app.html', map=tag)


def distribution():

    mu, sigma = 0, 0.5

    measured = np.random.normal(mu, sigma, 1000)
    hist, edges = np.histogram(measured, density=True, bins=20)

    x = np.linspace(-2, 2, 1000)
    pdf = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))
    cdf = (1 + scipy.special.erf((x - mu) / np.sqrt(2 * sigma ** 2))) / 2

    output_server("distribution_reveal")

    p = figure(title="Interactive plots",
               background_fill="#E5E5E5")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="#333333", line_color="#E5E5E5", line_width=3)

    # Use `line` renderers to display the PDF and CDF
    p.line(x, pdf, line_color="#348abd", line_width=8, alpha=0.7, legend="PDF")
    p.line(x, cdf, line_color="#7a68a6", line_width=8, alpha=0.7, legend="CDF")

    p.legend.orientation = "top_left"

    p.xaxis.axis_label = 'x'
    p.xgrid[0].grid_line_color = "white"
    p.xgrid[0].grid_line_width = 3

    p.yaxis.axis_label = 'Pr(x)'
    p.ygrid[0].grid_line_color = "white"
    p.ygrid[0].grid_line_width = 3

    push()

    return p, cursession()


if __name__ == '__main__':
    app.run(debug=True)
