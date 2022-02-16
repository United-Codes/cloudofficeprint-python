# Install cloudofficeprint using  pip install cloudofficeprint
import cloudofficeprint as cop  # Import the cloudofficeprint libary.
# Main object that holds the data
collection = cop.elements.ElementCollection()

# ---------------line_chart
line1 = cop.elements.LineSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    name='line1',
    smooth=True,
    symbol='diamond',
    symbol_size=10,
    color='red',
    line_width='0.2cm',
    line_style='sysDashDotDot'
)
line2 = cop.elements.LineSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    name='line2',
    smooth=True,
    symbol='square',
    symbol_size=12,
    color='blue',
    line_width='2px',
    line_style='sysDash'
)
line_chart = cop.elements.LineChart(
    name='line_chart_name',
    lines=(line1, line2)
)

collection.add(line_chart)

# --------------------bar_chart-----------
bars1 = cop.elements.BarSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    name='bars1',
    color='red'
)
bars2 = cop.elements.BarSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    name='bars2',
    color='blue'
)
bar_chart = cop.elements.BarChart(
    name='bar_chart_name',
    bars=(bars1, bars2)
)
collection.add(bar_chart)

# -------------pie_chart----------
pies1 = cop.elements.PieSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    name='pies1',
    colors=('red', None, 'blue')
)
pies2 = cop.elements.PieSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    name='pies2',
    colors=('green', 'blue', None)
)
pies_chart = cop.elements.PieChart(
    name='pie_chart_name',
    pies=(pies1, pies2)
)
collection.add(pies_chart)

# ---------------area_chart------------
area1 = cop.elements.AreaSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    name='area1',
    color='red',
    opacity=50
)
area2 = cop.elements.AreaSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    name='area2',
    color='blue',
    opacity=80
)
area_chart = cop.elements.AreaChart(
    name='area_chart_name',
    areas=(area1, area2)
)
collection.add(area_chart)

# -----------------bubble_chart----------
bubble1 = cop.elements.BubbleSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    sizes=(5, 6, 2),
    name='bubble1',
    color='red'
)
bubble2 = cop.elements.BubbleSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    sizes=(5, 6, 2),
    name='bubble2',
    color='blue'
)
bubble_chart = cop.elements.BubbleChart(
    name='bubble_chart_name',
    bubbles=(bubble1, bubble2)
)
collection.add(bubble_chart)

# ---------------stock_chart
stock1 = cop.elements.StockSeries(
    x=(1, 2, 3),
    high=(4, 5, 6),
    low=(7, 8, 9),
    close=(10, 11, 12),
    open_=(13, 14, 15),
    volume=(16, 17, 18),
    name='stock1'
)
stock2 = cop.elements.StockSeries(
    x=(1, 2, 3),
    high=(4, 5, 6),
    low=(7, 8, 9),
    close=(10, 11, 12),
    open_=(13, 14, 15),
    volume=(16, 17, 18),
    name='stock2'
)
stock_chart = cop.elements.StockChart(
    name='stock_chart_name',
    stocks=(stock1, stock2)
)
# collection.add(stock_chart)

# ----------------combined_chart-------
axis = cop.elements.ChartAxisOptions()
column1 = cop.elements.ColumnSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    name='column1'
)
column2 = cop.elements.ColumnSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    name='column2'
)
column_chart = cop.elements.ColumnChart(
    name='column_chart',
    columns=(column1, column2)
)
line1 = cop.elements.LineSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    name='line1',
    symbol='square'
)
line2 = cop.elements.LineSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    name='line2',
    symbol='square'
)
line_chart_options = cop.elements.ChartOptions(
    x_axis=axis,
    y_axis=axis,
    width=50,
    background_color='gray',
    background_opacity=50
)
line_chart = cop.elements.LineChart(
    name='line_chart',
    lines=(line1, line2),
    options=line_chart_options
)
bar1 = cop.elements.BarSeries(
    x=('a', 'b', 'c'),
    y=(1, 2, 3),
    name='bar1'
)
bar2 = cop.elements.BarSeries(
    x=('a', 'b', 'c'),
    y=(4, 5, 6),
    name='bar2'
)
bar_chart_options = cop.elements.ChartOptions(
    x_axis=axis,
    y_axis=axis,
    width=100,
    height=100,
    rounded_corners=False
)
bar_chart = cop.elements.BarChart(
    name='bar_chart',
    bars=(bar1, bar2),
    options=bar_chart_options
)
combined_chart = cop.elements.CombinedChart(
    name='combined_chart_name',
    charts=(column_chart, line_chart),
    secondaryCharts=(bar_chart,)
)
collection.add(combined_chart)

# configure server
# For running on localhost you do not need api_key else replace below "YOUR_API_KEY" with your api key.
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key="YOUR_API_KEY")
)
# Create print job
# PrintJob combines template, data, server and an optional output configuration
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.docx"),
)
# Execute print job and save response to file
response = printjob.execute()
response.to_file("output/output")
