# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 21:27:22 2018

@author: Administrator
"""

import networkx as nx

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
# from bokeh.palettes import Spectral4
from bokeh.plotting import figure

Spectral4 = ["#2b83ba", "#abdda4", "#fdae61", "#d7191c"]


G=nx.karate_club_graph()
graph = from_networkx(G, nx.spring_layout, scale=1, center=(0,0))


## Simple styple
plot = figure(title="Bokeh Networkx Integration Demonstration", x_range=(-2,2), y_range=(-2, 2),
              tools="", toolbar_location=None)

plot.renderers.append(graph)

output_file("networkx_graph.html")
show(plot)




#### Interactive graph
plot = Plot(plot_width=400, plot_height=400,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
plot.title.text = "Graph Interaction Demonstration"

plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0,0))

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

graph_renderer.selection_policy = NodesAndLinkedEdges()
graph_renderer.inspection_policy = EdgesAndLinkedNodes()

plot.renderers.append(graph_renderer)

output_file("interactive_graphs.html")
show(plot)