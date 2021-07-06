import apexofficeprint as aop
import pprint

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
        )
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
    options_result = {
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
        'title_style': {
            'italic': False,
            'bold': True,
            'color': 'red',
            'font': 'Arial',
        },
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
    assert options.as_dict == options_result

def test_chart_line():
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
    line_chart_result = {
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
    assert line_chart.as_dict == line_chart_result
    

def run():
    test_chart_options()
    test_chart_line()