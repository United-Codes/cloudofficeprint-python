# Install cloudofficeprint using  pip install cloudofficeprint
import cloudofficeprint as cop  # Import the cloudofficeprint libary.
# Main object that holds the data
collection = cop.elements.ElementCollection()

# ---------------line_chart
line1 = cop.elements.LineSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    'line1',
    True,
    'diamond',
    10,
    'red',
    '0.2cm',
    'sysDashDotDot'
)
line2 = cop.elements.LineSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    'line2',
    True,
    'square',
    12,
    'blue',
    '2px',
    'sysDash'
)

# To make line stacked chart you can simply use cop.elements.LineStackedChart
line_chart = cop.elements.LineChart(
    'line_chart_name',
    (line1, line2)
)

collection.add(line_chart)

# --------------------bar_chart-----------
bars1 = cop.elements.BarSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    'bars1',
    'red'
)
bars2 = cop.elements.BarSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    'bars2',
    'blue'
)
bar_chart = cop.elements.BarChart(
    'bar_chart_name',
    (bars1, bars2)
)
collection.add(bar_chart)

# -------------pie_chart----------
pies1 = cop.elements.PieSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    'pies1',
    ('red', None, 'blue')
)
pies2 = cop.elements.PieSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    'pies2',
    ('green', 'blue', None)
)
pies_chart = cop.elements.PieChart(
    'pie_chart_name',
    (pies1, pies2)
)
collection.add(pies_chart)

# ---------------area_chart------------
area1 = cop.elements.AreaSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    'area1',
    'red',
    50
)
area2 = cop.elements.AreaSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    'area2',
    'blue',
    80
)
area_chart = cop.elements.AreaChart(
    'area_chart_name',
    (area1, area2)
)
collection.add(area_chart)

# -----------------bubble_chart----------
bubble1 = cop.elements.BubbleSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    (5, 6, 2),
    'bubble1',
    'red'
)
bubble2 = cop.elements.BubbleSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    (5, 6, 2),
    'bubble2',
    'blue'
)
bubble_chart = cop.elements.BubbleChart(
    'bubble_chart_name',
    (bubble1, bubble2)
)
collection.add(bubble_chart)

# ---------------stock_chart
stock1 = cop.elements.StockSeries(
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (10, 11, 12),
    (13, 14, 15),
    (16, 17, 18),
    'stock1'
)
stock2 = cop.elements.StockSeries(
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (10, 11, 12),
    (13, 14, 15),
    (16, 17, 18),
    'stock2'
)
stock_chart = cop.elements.StockChart(
    'stock_chart_name',
    (stock1, stock2)
)
# collection.add(stock_chart)

# ----------------combined_chart-------
axis = cop.elements.ChartAxisOptions()
column1 = cop.elements.ColumnSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    'column1'
)
column2 = cop.elements.ColumnSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    'column2'
)
column_chart = cop.elements.ColumnChart(
    'column_chart',
    (column1, column2)
)
line1 = cop.elements.LineSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    'line1',
    'square'
)
line2 = cop.elements.LineSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    'line2',
    'square'
)
line_chart_options = cop.elements.ChartOptions(
    axis,
    axis,
    50,
    'gray',
    50
)
line_chart = cop.elements.LineChart(
    'line_chart',
    (line1, line2),
    line_chart_options
)
bar1 = cop.elements.BarSeries(
    ('a', 'b', 'c'),
    (1, 2, 3),
    'bar1'
)
bar2 = cop.elements.BarSeries(
    ('a', 'b', 'c'),
    (4, 5, 6),
    'bar2'
)
bar_chart_options = cop.elements.ChartOptions(
    axis,
    axis,
    100,
    height=100,
    rounded_corners=False
)
bar_chart = cop.elements.BarChart(
    'bar_chart',
    (bar1, bar2),
    bar_chart_options
)
combined_chart = cop.elements.CombinedChart(
    'combined_chart_name',
    (column_chart, line_chart),
    (bar_chart,)
)
collection.add(combined_chart)

# configure server
# For running on localhost you do not need api_key else replace below "YOUR_API_KEY" with your api key.
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig("YOUR_API_KEY")
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
