
from collections import OrderedDict
from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource


######################
#PARSING THE FILE
######################

def getMap(inputfilename):
    from bokeh.browserlib import view
    from bokeh.document import Document
    from bokeh.embed import file_html
    from bokeh.models.glyphs import Circle
    from bokeh.models import (
        GMapPlot, Range1d, ColumnDataSource, LinearAxis,
        PanTool, WheelZoomTool, BoxSelectTool,
        BoxSelectionOverlay, GMapOptions,
        NumeralTickFormatter, PrintfTickFormatter)
    from bokeh.resources import INLINE
    from pop import Population

    x_range = Range1d()
    y_range = Range1d()
    source, avgLat, avgLon = generate_figure(inputfilename)


    map_options = GMapOptions(lat=avgLat, lng=avgLon, zoom=8)

    plot = GMapPlot(
        x_range=x_range, y_range=y_range,
        map_options=map_options,
        title = "Disases"
    )
    plot.map_options.map_type="roadmap"


    circle = Circle(x="lon", y="lat", size=15, fill_color="fill", line_color="black")
    plot.add_glyph(source, circle)

    pan = PanTool()
    wheel_zoom = WheelZoomTool()
    box_select = BoxSelectTool()

    plot.add_tools(pan, wheel_zoom, box_select)

    xaxis = LinearAxis(axis_label="lat", major_tick_in=0, formatter=NumeralTickFormatter(format="0.000"))
    plot.add_layout(xaxis, 'below')

    yaxis = LinearAxis(axis_label="lon", major_tick_in=0, formatter=PrintfTickFormatter(format="%.3f"))
    plot.add_layout(yaxis, 'left')

    overlay = BoxSelectionOverlay(tool=box_select)
    plot.add_layout(overlay)


    # Setup the session
    document = Document()
    session = Session(root_url='http://localhost:5006/', load_from_config=False)
    session.use_doc('population_reveal')
    session.load_document(document)
    # Make the chart
    # Attach the chart to the document
    document.clear()  # Semi-optional - see below
    document.add(plot)
    # Put it on the server
    session.store_document(document)


    return plot, session


def parse_disease_csv(inputfileobject):
    id=[]
    latitude=[]
    longitude=[]
    status=[]

    for line in inputfileobject:
        line_elements=line.split(",")
        id.append(line_elements[0])
        latitude.append(float(line_elements[1]))
        longitude.append(float(line_elements[2]))
        status.append(line_elements[3])
    return id,latitude, longitude, status


def generate_figure(inputfilename):
    inputfileobject = open(inputfilename, 'r')

    #parse csv file
    id, latitude, longitude, status = parse_disease_csv(inputfileobject)

    #create Column Datasource
    source = ColumnDataSource(
        data=dict(
           lat=latitude,
           lon=longitude,
        )
    )
    avgLat = sum(latitude)/len(latitude)
    avgLon = sum(longitude)/len(longitude)

    # #define tools
    # TOOLS = "resize,hover,save"
    # output_server("map")
    # p = figure(title="Periodic Table", tools=TOOLS)
    # p.plot_width = 1200
    # p.toolbar_location = "left"
    # p.circle(latitude, longitude, size=20,source=source,
    #     fill_alpha=0.6, color="blue")

    # text_props = {
    #     "source": source,
    #     "angle": 0,
    #     "color": "black",
    #     "text_align": "left",
    #     "text_baseline": "middle"
    # }
    # p.grid.grid_line_color = None
    # hover = p.select(dict(type=HoverTool))
    # hover.tooltips = OrderedDict([
    #     ("disease_status", "@status")])

    # push()

    return source, avgLon, avgLat
