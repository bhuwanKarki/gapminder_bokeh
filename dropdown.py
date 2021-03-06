# -*- coding: utf-8 -*-
import pandas as pd
from bokeh.io import output_file, show,curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource,CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row
from bokeh.models import Slider,Select
filepath="gapminder.csv"
df=pd.read_csv(filepath)
data=pd.DataFrame(df)

source = ColumnDataSource(data={
    'x': data["fertility"].loc[data["Year"]==1970],
    'y': data["life"].loc[data["Year"]==1970],
    'country': data["Country"].loc[data["Year"]==1970],
    'pop': (data["population"].loc[data["Year"]==1970] / 20000000) + 2,
    'region': data["region"].loc[data["Year"]==1970],
})
regions_list = data.region.unique().tolist()

xmin, xmax = min(data.fertility), max(data.fertility)
ymin, ymax = min(data.life),max(data.life)

color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

plot = figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field="region", transform=color_mapper), legend="region")

# Set the legend.location attribute of the plot to 'top_right'
plot.legend.location = 'top_right'
plot.xaxis.axis_label ='Fertility (children per woman)'

# Set the y-axis label
plot.yaxis.axis_label = 'Life Expectancy (years)'

def update_plot(attr, old, new):
    # Read the current value off the slider and 2 dropdowns: yr, x, y
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # Set new_data
    new_data = {
        'x': data[x].loc[data["Year"] == yr],
        'y': data[y].loc[data["Year"] == yr],
        'country': data["Country"].loc[data["Year"] == yr],
        'pop': (data["population"].loc[data["Year"] == yr] / 20000000) + 2,
        'region': data["region"].loc[data["Year"] == yr],
    }
    # Assign new_data to source.data
    source.data = new_data

    # Set the range of all axes
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    # Add title to plot
    plot.title.text = 'Gapminder data for %d' % yr

# Create a dropdown slider widget: slider
slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year')

# Attach the callback to the 'value' property of slider
slider.on_change('value', update_plot)

# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x-axis data'
)

# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y-axis data'
)

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change("value",update_plot)

#add a hover
hover=HoverTool(tooltips=[("Country","@country")])
plot.add_tools(hover)


# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)


