
from collections import OrderedDict
from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource


######################
#PARSING THE FILE
######################


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


def generate_bokeh_html(inputfilename):
    inputfileobject = open(inputfilename, 'r')

    #parse csv file
    id, latitude, longitude, status = parse_disease_csv(inputfileobject)

    #create Column Datasource
    source = ColumnDataSource(
        data=dict(
           status=status
        )
    )

    #define tools
    TOOLS = "resize,hover,save"
    p = figure(title="Periodic Table", tools=TOOLS)
    p.plot_width = 1200
    p.toolbar_location = "left"
    p.circle(latitude, longitude, size=20,source=source,
        fill_alpha=0.6, color="blue")

    text_props = {
        "source": source,
        "angle": 0,
        "color": "black",
        "text_align": "left",
        "text_baseline": "middle"
    }
    p.grid.grid_line_color = None
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("disease_status", "@status")])

    return p
