from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure, show
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties
from bokeh.layouts import column
from streamlit_bokeh import streamlit_bokeh
import streamlit as st
import geopandas as gpd
from bokeh.models import (ColumnDataSource, HoverTool, CustomJS, TapTool, Select, SetValue)

st.set_page_config(page_title="Koralmbahnregion-Index Überblick", layout="wide")



gkzList =  ['20101', '20201', '20402', '20403', '20405', '20409', '20412', '20414', '20415', '20416', 
             '20417', '20418', '20419', '20421', '20424', '20425', '20428', '20432', '20435', '20441', 
            '20442', '20501', '20502', '20504', '20512', '20515', '20520', '20523', '20527', '20534', 
             '20721', '20722', '20725', '20727', '20801', '20802', '20803', '20804', '20805', '20806', 
             '20807', '20808', '20810', '20812', '20813', '20815', '20817', '20901', '20905', '20909', 
             '20911', '20913', '20914', '20918', '20923', '21002', '21003', '60101', '60305', '60318', 
             '60323', '60324', '60326', '60329', '60341', '60344', '60345', '60346', '60347', '60348', 
             '60349', '60350', '60351', '60608', '60611', '60613', '60617', '60618', '60619', '60623', 
             '60624', '60626', '60628', '60629', '60632', '60639', '60641', '60642', '60645', '60646', 
             '60647', '60648', '60651', '60653', '60654', '60655', '60656', '60659', '60660', '60661', 
             '60662', '60663', '60664', '60665', '60666', '60667', '60668', '60669', '60670', '61001', 
             '61002', '61007', '61008', '61012', '61013', '61016', '61017', '61019', '61020', '61021', 
             '61024', '61027', '61030', '61032', '61033', '61043', '61045', '61049', '61050', '61051', 
             '61052', '61053', '61054', '61055', '61057', '61059', '61060', '61061', '61611', '61612', 
             '61615', '61618', '61624', '61625', '61626', '61629', '61631', '61633', '61701', '61710', 
             '61716', '61719', '61727', '61729', '61730', '61731', '61740', '61746', '61748', '61751', 
             '61760', '61761', '61762', '61763', '61764', '61765', '61766', '62125', '62232', '62252', 
             '62266', '62269', '62271', '62311', '62314', '62330', '62343', '62377', '62380', '62381', 
             '62382', '62383', '62384', '62385', '62388', '62389']
gkzList.extend([''] * 233)

gdf = gpd.read_file('koralm2025.json') # read geojson file
gdf = gdf.explode(ignore_index=True) # make multipolygon to separate polygons
gdf = gdf.drop(index=179) # delete exclave hitzendorf
    
# extract coordinates from gdf
gdf['x'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[0]), axis=1)
gdf['y'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[1]), axis=1)

# prep data
lenGDF = len(gdf)
source = ColumnDataSource(data=dict(
        x=gdf['x'].tolist(),
        y=gdf['y'].tolist(),
        gemeinde=gdf['Gemeindename'].tolist(), 
        gkz=gdf['Gemeindenummer'].tolist(),
        line_color=['black'] * lenGDF,
        line_width=[0.5] * lenGDF,
        fill_color=['#CC79A7' if gkz in gkzList 
                    else "#FFB81C" if gkz.startswith('2') 
                    else "#5B8C5A" for gkz in gdf['Gemeindenummer']],
        flag=[1 if gkz in gkzList else 0 for gkz in gdf['Gemeindenummer']]  
    ))

    
# Create a Bokeh figure OG!!!
p = figure(
        title="",
        tools="",
        x_axis_location=None, 
        y_axis_location=None,
        tooltips=[("", "@gemeinde")],
        width=1572//2,  #og width=1572//2,
        height=966//2,  #og height=966//2,
        aspect_scale=0.75,
        match_aspect=True
    )

p.grid.grid_line_color = None
    
# Add patches to the figure
patches = p.patches(
        'x', 
        'y', 
        source=source,
        fill_alpha=1,
        line_color='line_color', 
        line_width='line_width',
        fill_color='fill_color'
    )
    
    
# Add hover tool
hover = HoverTool()
hover.tooltips = [("", "@gemeinde")]
hover.renderers = [patches]
p.add_tools(hover)

p.toolbar.logo = None
p.toolbar_location = None

pp = column(p, sizing_mode="stretch_width")
#col1, col2, col3= st.columns([8, 0.5, 2])
#with col1:
streamlit_bokeh(pp, use_container_width=True, key="plot1")
