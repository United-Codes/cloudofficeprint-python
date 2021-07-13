import apexofficeprint as aop

"""This file contains tests for all the possible charts"""

def test_chart_options():
    x_axis = aop.elements.ChartAxisOptions(
        orientation='minMax',
        min=5,
        max=10,
        date=aop.elements.ChartDateOptions(
            format='unix',
            code='mm/yy',
            unit='months',
            step=1
        ),
        title='title_x',
        values=True,
        values_style=aop.elements.ChartTextStyle(
            italic=True,
            bold=True,
            color='red',
            font='Arial'
        ),
        title_style=aop.elements.ChartTextStyle(
            italic=True,
            bold=False,
            color='blue',
            font='Arial'
        ),
        title_rotation=45,
        major_grid_lines=True,
        major_unit=2,
        minor_grid_lines=True,
        minor_unit=1,
        formatCode='General'
    )
    y_axis = aop.elements.ChartAxisOptions(
        orientation='minMax',
        min=5,
        max=10,
        title='title_y',
        values=True,
        values_style=aop.elements.ChartTextStyle(
            italic=True,
            bold=True,
            color='red',
            font='Arial'
        ),
        title_style=aop.elements.ChartTextStyle(
            italic=True,
            bold=False,
            color='blue',
            font='Arial'
        ),
        title_rotation=45,
        major_grid_lines=True,
        major_unit=2,
        minor_grid_lines=True,
        minor_unit=1,
        formatCode='General'
    )
    y2_axis = y_axis
    options = aop.elements.ChartOptions(
        x_axis=x_axis,
        y_axis=y_axis,
        y2_axis=y2_axis,
        width=500,
        height=500,
        border=True,
        rounded_corners=False,
        background_color='green',
        background_opacity=50,
        title='title_chart',
        title_style=aop.elements.ChartTextStyle(
            italic=False,
            bold=True,
            color='red',
            font='Arial'
        ),
        grid=True
    )
    options.set_legend(
        position='l',
        style=aop.elements.ChartTextStyle(
            italic=True,
            bold=True,
            color='blue',
            font='Arial'
        )
    )
    options.set_data_labels(
        separator=';',
        series_name=False,
        category_name=False,
        legend_key=True,
        value=False,
        percentage=True,
        position='r'
    )
    options_expected = {
        'axis': {
            'x': {
                    'orientation': 'minMax',
                    'min': 5,
                    'max': 10,
                    'type': 'date',
                    'date': {
                        'format': 'unix',
                        'code': 'mm/yy',
                        'unit': 'months',
                        'step': 1,
                    },
                    'title': 'title_x',
                    'showValues': True,
                    'valuesStyle': {
                        'italic': True,
                        'bold': True,
                        'color': 'red',
                        'font': 'Arial',
                    },
                    'titleStyle': {
                        'italic': True,
                        'bold': False,
                        'color': 'blue',
                        'font': 'Arial',
                    },
                    'titleRotation': 45,
                    'majorGridlines': True,
                    'majorUnit': 2,
                    'minorGridlines': True,
                    'minorUnit': 1,
                    'formatCode': 'General',
            },
            'y': {
                    'orientation': 'minMax',
                    'min': 5,
                    'max': 10,
                    'title': 'title_y',
                    'showValues': True,
                    'valuesStyle': {
                        'italic': True,
                        'bold': True,
                        'color': 'red',
                        'font': 'Arial',
                    },
                    'titleStyle': {
                        'italic': True,
                        'bold': False,
                        'color': 'blue',
                        'font': 'Arial',
                    },
                    'titleRotation': 45,
                    'majorGridlines': True,
                    'majorUnit': 2,
                    'minorGridlines': True,
                    'minorUnit': 1,
                    'formatCode': 'General',
            },
            'y2': {
                    'orientation': 'minMax',
                    'min': 5,
                    'max': 10,
                    'title': 'title_y',
                    'showValues': True,
                    'valuesStyle': {
                        'italic': True,
                        'bold': True,
                        'color': 'red',
                        'font': 'Arial',
                    },
                    'titleStyle': {
                        'italic': True,
                        'bold': False,
                        'color': 'blue',
                        'font': 'Arial',
                    },
                    'titleRotation': 45,
                    'majorGridlines': True,
                    'majorUnit': 2,
                    'minorGridlines': True,
                    'minorUnit': 1,
                    'formatCode': 'General',
            },
        },
        'width': 500,
        'height': 500,
        'border': True,
        'roundedCorners': False,
        'backgroundColor': 'green',
        'backgroundOpacity': 50,
        'title': 'title_chart',
        'titleStyle': {
            'italic': False,
            'bold': True,
            'color': 'red',
            'font': 'Arial',
        },
        'grid': True,
        'legend': {
            'showLegend': True,
            'position': 'l',
            'style': {
                'italic': True,
                'bold': True,
                'color': 'blue',
                'font': 'Arial',
            }
        },
        'dataLabels': {
            'showDataLabels': True,
            'separator': ';',
            'showSeriesName': False,
            'showCategoryName': False,
            'showLegendKey': True,
            'showValue': False,
            'showPercentage': True,
            'position': 'r',
        },
    }
    assert options.as_dict == options_expected


def test_chart_line():
    """Test for LineChart. Also serves as a test for RadarChart (RadarSeries is equivalent to LineSeries)"""
    line1 = aop.elements.LineSeries(
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
    line2 = aop.elements.LineSeries(
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
    line_chart = aop.elements.LineChart(
        name='test_name',
        lines=(line1, line2)
    )
    line_chart_expected = {
        'test_name': {
            'lines': [
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 1
                        },
                        {
                            'x': 'b',
                            'y': 2
                        },
                        {
                            'x': 'c',
                            'y': 3
                        }
                    ],
                    'name': 'line1',
                    'smooth': True,
                    'symbol': 'diamond',
                    'symbolSize': 10,
                    'color': 'red',
                    'lineWidth': '0.2cm',
                    'lineStyle': 'sysDashDotDot'
                },
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 4
                        },
                        {
                            'x': 'b',
                            'y': 5
                        },
                        {
                            'x': 'c',
                            'y': 6
                        }
                    ],
                    'name': 'line2',
                    'smooth': True,
                    'symbol': 'square',
                    'symbolSize': 12,
                    'color': 'blue',
                    'lineWidth': '2px',
                    'lineStyle': 'sysDash'
                }
            ],
            'type': 'line'
        }
    }
    assert line_chart.as_dict == line_chart_expected


def test_chart_bar():
    """Test for BarChart. Also serves as the test for: 
    BarStackedChart, BarStackedPercentChart, ColumnChart, ColumnStackedChart, ColumnStackedPercentChart 
    and ScatterChart because their constructors take the same argument types (i.e. XYSeries).
    """
    bars1 = aop.elements.BarSeries(
        x=('a', 'b', 'c'),
        y=(1, 2, 3),
        name='bars1',
        color='red'
    )
    bars2 = aop.elements.BarSeries(
        x=('a', 'b', 'c'),
        y=(4, 5, 6),
        name='bars2',
        color='blue'
    )
    bar_chart = aop.elements.BarChart(
        name='bar_chart',
        bars=(bars1, bars2)
    )
    bar_chart_expected = {
        'bar_chart': {
            'bars': [
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 1
                        },
                        {
                            'x': 'b',
                            'y': 2
                        },
                        {
                            'x': 'c',
                            'y': 3
                        }
                    ],
                    'name': 'bars1',
                    'color': 'red'
                },
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 4
                        },
                        {
                            'x': 'b',
                            'y': 5
                        },
                        {
                            'x': 'c',
                            'y': 6
                        }
                    ],
                    'name': 'bars2',
                    'color': 'blue'
                },
            ],
            'type': 'bar'
        }
    }
    assert bar_chart.as_dict == bar_chart_expected


def test_chart_pie():
    """Test for PieChart. Also serves as the test for Pie3DChart and DoughnutChart, 
    because their constructors take the same argument types (i.e. PieSeries).
    """
    pies1 = aop.elements.PieSeries(
        x=('a', 'b', 'c'),
        y=(1, 2, 3),
        name='pies1',
        colors=('red', None, 'blue')
    )
    pies2 = aop.elements.PieSeries(
        x=('a', 'b', 'c'),
        y=(4, 5, 6),
        name='pies2',
        colors=('green', 'blue', None)
    )
    pies_chart = aop.elements.PieChart(
        name='pie_chart',
        pies=(pies1, pies2)
    )
    pies_chart_expected = {
        'pie_chart': {
            'pies': [
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 1,
                            'color': 'red'
                        },
                        {
                            'x': 'b',
                            'y': 2
                        },
                        {
                            'x': 'c',
                            'y': 3,
                            'color': 'blue'
                        }
                    ],
                    'name': 'pies1'
                },
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 4,
                            'color': 'green'
                        },
                        {
                            'x': 'b',
                            'y': 5,
                            'color': 'blue'
                        },
                        {
                            'x': 'c',
                            'y': 6
                        }
                    ],
                    'name': 'pies2'
                },
            ],
            'type': 'pie'
        }
    }
    assert pies_chart.as_dict == pies_chart_expected


def test_chart_area():
    """Test for AreaChart"""
    area1 = aop.elements.AreaSeries(
        x=('a', 'b', 'c'),
        y=(1, 2, 3),
        name='area1',
        color='red',
        opacity=50
    )
    area2 = aop.elements.AreaSeries(
        x=('a', 'b', 'c'),
        y=(4, 5, 6),
        name='area2',
        color='blue',
        opacity=80
    )
    area_chart = aop.elements.AreaChart(
        name='area_chart',
        areas=(area1, area2)
    )
    area_chart_expected = {
        'area_chart': {
            'areas': [
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 1
                        },
                        {
                            'x': 'b',
                            'y': 2
                        },
                        {
                            'x': 'c',
                            'y': 3
                        },
                    ],
                    'name': 'area1',
                    'color': 'red',
                    'opacity': 50
                },
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 4
                        },
                        {
                            'x': 'b',
                            'y': 5
                        },
                        {
                            'x': 'c',
                            'y': 6
                        },
                    ],
                    'name': 'area2',
                    'color': 'blue',
                    'opacity': 80
                }
            ],
            'type': 'area'
        }
    }
    assert area_chart.as_dict == area_chart_expected


def test_chart_bubble():
    """Test for BubbleChart"""
    bubble1 = aop.elements.BubbleSeries(
        x=('a', 'b', 'c'),
        y=(1, 2, 3),
        sizes=(5, 6, 2),
        name='bubble1',
        color='red'
    )
    bubble2 = aop.elements.BubbleSeries(
        x=('a', 'b', 'c'),
        y=(4, 5, 6),
        sizes=(5, 6, 2),
        name='bubble2',
        color='blue'
    )
    bubble_chart = aop.elements.BubbleChart(
        name='bubble_chart',
        bubbles=(bubble1, bubble2)
    )
    bubble_chart_expected = {
        'bubble_chart': {
            'bubbles': [
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 1,
                            'size': 5
                        },
                        {
                            'x': 'b',
                            'y': 2,
                            'size': 6
                        },
                        {
                            'x': 'c',
                            'y': 3,
                            'size': 2
                        },
                    ],
                    'name': 'bubble1',
                    'color': 'red'
                },
                {
                    'data': [
                        {
                            'x': 'a',
                            'y': 4,
                            'size': 5
                        },
                        {
                            'x': 'b',
                            'y': 5,
                            'size': 6
                        },
                        {
                            'x': 'c',
                            'y': 6,
                            'size': 2
                        },
                    ],
                    'name': 'bubble2',
                    'color': 'blue'
                }
            ],
            'type': 'bubble'
        }
    }
    assert bubble_chart.as_dict == bubble_chart_expected


def test_chart_stock():
    """Test for StockChart"""
    stock1 = aop.elements.StockSeries(
        x=(1, 2, 3),
        high=(4, 5, 6),
        low=(7, 8, 9),
        close=(10, 11, 12),
        open_=(13, 14, 15),
        volume=(16, 17, 18),
        name='stock1'
    )
    stock2 = aop.elements.StockSeries(
        x=(1, 2, 3),
        high=(4, 5, 6),
        low=(7, 8, 9),
        close=(10, 11, 12),
        open_=(13, 14, 15),
        volume=(16, 17, 18),
        name='stock2'
    )
    stock_chart = aop.elements.StockChart(
        name='stock_chart',
        stocks=(stock1, stock2)
    )
    stock_chart_expected = {
        'stock_chart': {
            'stocks': [
                {
                    'data': [
                        {
                            'x': 1,
                            'high': 4,
                            'low': 7,
                            'close': 10,
                            'open': 13,
                            'volume': 16,
                        },
                        {
                            'x': 2,
                            'high': 5,
                            'low': 8,
                            'close': 11,
                            'open': 14,
                            'volume': 17,
                        },
                        {
                            'x': 3,
                            'high': 6,
                            'low': 9,
                            'close': 12,
                            'open': 15,
                            'volume': 18,
                        }
                    ],
                    'name': 'stock1'
                },
                {
                    'data': [
                        {
                            'x': 1,
                            'high': 4,
                            'low': 7,
                            'close': 10,
                            'open': 13,
                            'volume': 16,
                        },
                        {
                            'x': 2,
                            'high': 5,
                            'low': 8,
                            'close': 11,
                            'open': 14,
                            'volume': 17,
                        },
                        {
                            'x': 3,
                            'high': 6,
                            'low': 9,
                            'close': 12,
                            'open': 15,
                            'volume': 18,
                        }
                    ],
                    'name': 'stock2'
                }
            ],
            'type': 'stock'
        }
    }
    assert stock_chart.as_dict == stock_chart_expected


def test_chart_combined():
    axis = aop.elements.ChartAxisOptions()
    column1 = aop.elements.ColumnSeries(
        x=('a', 'b', 'c'),
        y=(1, 2, 3),
        name='column1'
    )
    column2 = aop.elements.ColumnSeries(
        x=('a', 'b', 'c'),
        y=(4, 5, 6),
        name='column2'
    )
    column_chart = aop.elements.ColumnChart(
        name='column_chart',
        columns=(column1, column2)
    )
    line1 = aop.elements.LineSeries(
        x=('a', 'b', 'c'),
        y=(1, 2, 3),
        name='line1',
        symbol='square'
    )
    line2 = aop.elements.LineSeries(
        x=('a', 'b', 'c'),
        y=(4, 5, 6),
        name='line2',
        symbol='square'
    )
    line_chart_options = aop.elements.ChartOptions(
    x_axis=axis,
    y_axis=axis,
    width=50,
    background_color='gray',
    background_opacity=50
    )
    line_chart = aop.elements.LineChart(
        name='line_chart',
        lines=(line1, line2),
        options=line_chart_options
    )
    bar1 = aop.elements.BarSeries(
        x=('a', 'b', 'c'),
        y=(1, 2, 3),
        name='bar1'
    )
    bar2 = aop.elements.BarSeries(
        x=('a', 'b', 'c'),
        y=(4, 5, 6),
        name='bar2'
    )
    bar_chart_options = aop.elements.ChartOptions(
        x_axis=axis,
        y_axis=axis,
        width=100,
        height=100,
        rounded_corners=False
    )
    bar_chart = aop.elements.BarChart(
        name='bar_chart',
        bars=(bar1, bar2),
        options=bar_chart_options
    )
    combined_chart = aop.elements.CombinedChart(
        name='combined_chart',
        charts=(column_chart, line_chart),
        secondaryCharts=(bar_chart,)
    )
    combined_chart_expected = {
        'combined_chart': {
            'multiples': [
                {
                    'columns': [
                        {
                            'data': [
                                {
                                    'x': 'a',
                                    'y': 1
                                },
                                {
                                    'x': 'b',
                                    'y': 2
                                },
                                {
                                    'x': 'c',
                                    'y': 3
                                }
                            ],
                            'name': 'column1'
                        },
                        {
                            'data': [
                                {
                                    'x': 'a',
                                    'y': 4
                                },
                                {
                                    'x': 'b',
                                    'y': 5
                                },
                                {
                                    'x': 'c',
                                    'y': 6
                                }
                            ],
                            'name': 'column2'
                        }
                    ],
                    'type': 'column'
                },
                {
                    'lines': [
                        {
                            'data': [
                                {
                                    'x': 'a',
                                    'y': 1
                                },
                                {
                                    'x': 'b',
                                    'y': 2
                                },
                                {
                                    'x': 'c',
                                    'y': 3
                                }
                            ],
                            'name': 'line1',
                            'symbol': 'square'
                        },
                        {
                            'data': [
                                {
                                    'x': 'a',
                                    'y': 4
                                },
                                {
                                    'x': 'b',
                                    'y': 5
                                },
                                {
                                    'x': 'c',
                                    'y': 6
                                }
                            ],
                            'name': 'line2',
                            'symbol': 'square'
                        }
                    ],
                    'type': 'line'
                },
                {
                    'bars': [
                        {
                            'data': [
                                {
                                    'x': 'a',
                                    'y2': 1
                                },
                                {
                                    'x': 'b',
                                    'y2': 2
                                },
                                {
                                    'x': 'c',
                                    'y2': 3
                                }
                            ],
                            'name': 'bar1'
                        },
                        {
                            'data': [
                                {
                                    'x': 'a',
                                    'y2': 4
                                },
                                {
                                    'x': 'b',
                                    'y2': 5
                                },
                                {
                                    'x': 'c',
                                    'y2': 6
                                }
                            ],
                            'name': 'bar2'
                        }
                    ],
                    'type': 'bar'
                }
            ],
            'options': {
                'axis': {
                    'x': {},
                    'y': {}
                },
                'width': 50,
                'backgroundColor': 'gray',
                'backgroundOpacity': 50
            },
            'type': 'multiple'
        }
    }
    assert combined_chart.as_dict == combined_chart_expected


def test_chart_aop():
    aop_chart = aop.elements.AOPChart(
        name='aop_chart',
        x_data=('a', 'b', 'c'),
        y_datas=((1, 2, 3), (4, 5, 6)),
        title='aop_chart_title',
        date=aop.elements.AOPChartDateOptions(
            format='d/m/yyyy',
            unit='days',
            step=1
        ),
        x_title='x-axis',
        y_title='y-axis',
        y2_title='y2-axis',
        x2_title='x2-axis'
    )
    aop_chart_expected = {
        'aop_chart': {
            'xAxis': {
                'data': ['a', 'b', 'c'],
                'title': 'x-axis',
                'date': {
                    'format': 'd/m/yyyy',
                    'unit': 'days',
                    'step': 1
                }
            },
            'yAxis': {
                'series': [
                    {
                        'name': 'series 1',
                        'data': [1, 2, 3]
                    },
                    {
                        'name': 'series 2',
                        'data': [4, 5, 6]
                    }
                ],
                'title': 'y-axis'
            },
            'title': 'aop_chart_title',
            'x2Axis': {
                'title': 'x2-axis'
            },
            'y2Axis': {
                'title': 'y2-axis'
            }
        }
    }
    assert aop_chart.as_dict == aop_chart_expected

    # Test for y_datas = dictionary
    aop_chart = aop.elements.AOPChart(
        name='aop_chart',
        x_data=('a', 'b', 'c'),
        y_datas={
            'first_series': (1, 2, 3),
            'second_series': (4, 5, 6)
        },
        title='aop_chart_title',
        date=aop.elements.AOPChartDateOptions(
            format='d/m/yyyy',
            unit='days',
            step=1
        ),
        x_title='x-axis',
        y_title='y-axis',
        y2_title='y2-axis',
        x2_title='x2-axis'
    )
    aop_chart_expected = {
        'aop_chart': {
            'xAxis': {
                'data': ['a', 'b', 'c'],
                'title': 'x-axis',
                'date': {
                    'format': 'd/m/yyyy',
                    'unit': 'days',
                    'step': 1
                }
            },
            'yAxis': {
                'series': [
                    {
                        'name': 'first_series',
                        'data': [1, 2, 3]
                    },
                    {
                        'name': 'second_series',
                        'data': [4, 5, 6]
                    }
                ],
                'title': 'y-axis'
            },
            'title': 'aop_chart_title',
            'x2Axis': {
                'title': 'x2-axis'
            },
            'y2Axis': {
                'title': 'y2-axis'
            }
        }
    }
    assert aop_chart.as_dict == aop_chart_expected

def run():
    test_chart_options()
    test_chart_line()
    test_chart_bar()
    test_chart_pie()
    test_chart_area()
    test_chart_bubble()
    test_chart_stock()
    test_chart_combined()
    test_chart_aop()

if __name__ == '__main__':
    run()
