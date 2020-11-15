from typing import Union
from logging import warning
from typing import Iterable, Tuple, FrozenSet
from abc import ABC, abstractmethod
from .elements import Element


class ChartTextStyle:
    def __init__(self,
                 italic: bool = None,
                 bold: bool = None,
                 color: str = None,
                 font: str = None):
        self.italic: bool = italic
        self.bold: bool = bold
        self.color: str = color
        self.font: str = font

    @property
    def as_dict(self):
        result = {}

        if self.italic is not None:
            result["italic"] = self.italic
        if self.bold is not None:
            result["bold"] = self.bold
        if self.color:
            result["color"] = self.color
        if self.font:
            result["font"] = self.font

        return result


class ChartDateOptions:
    def __init__(self,
                 format: str = None,
                 code: str = None,
                 unit: str = None,
                 step: Union[int, str] = None):
        self.format: str = format,
        self.code: str = code,
        self.unit: str = unit,
        self.step: Union[int, str] = step

    @property
    def as_dict(self):
        result = {}

        if self.format:
            result["format"] = self.format
        if self.code:
            result["code"] = self.code
        if self.unit:
            result["unit"] = self.unit
        if self.step:
            result["step"] = self.step

        return result


class ChartAxisOptions:
    def __init__(self,
                 orientation: str = None,
                 min: Union[int, float] = None,
                 max: Union[int, float] = None,
                 date: ChartDateOptions = None,
                 title: str = None,
                 values: bool = None,
                 values_style: ChartTextStyle = None,
                 title_style: ChartTextStyle = None,
                 title_rotation: int = None,
                 major_grid_lines: bool = None,
                 major_unit: Union[int, float] = None,
                 minor_grid_lines: bool = None,
                 minor_unit: Union[int, float] = None):
        self.orientation: str = orientation
        self.min: Union[int, float] = min
        self.max: Union[int, float] = max
        self.date: ChartDateOptions = date
        self.title: str = title
        self.values: bool = values
        self.values_style: ChartTextStyle = values_style
        self.title_style: ChartTextStyle = title_style
        self.title_rotation: int = title_rotation
        self.major_grid_lines: bool = major_grid_lines
        self.major_unit: Union[int, float] = major_unit
        self.minor_grid_lines: bool = minor_grid_lines
        self.minor_unit: Union[int, float] = minor_unit

    @property
    def as_dict(self):
        result = {}

        if self.orientation:
            result["orientation"] = self.orientation
        if self.min:
            result["min"] = self.min
        if self.max:
            result["max"] = self.max
        if self.date:
            result["type"] = "date"
            result["date"] = self.date.as_dict
        if self.title:
            result["title"] = self.title
        if self.values is not None:
            result["showValues"] = self.values
        if self.values_style:
            result["valuesStyle"] = self.values_style.as_dict
        if self.title_style:
            result["titleStyle"] = self.title_style.as_dict
        if self.title_rotation:
            result["titleRotation"] = self.title_rotation
        if self.major_grid_lines is not None:
            result["majorGridlines"] = self.major_grid_lines
        if self.major_unit:
            result["majorUnit"] = self.major_unit
        if self.minor_grid_lines is not None:
            result["minorGridlines"] = self.minor_grid_lines
        if self.minor_unit:
            result["minorUnit"] = self.minor_unit

        return result


class ChartOptions():
    """Options object for a `Chart`."""
    def __init__(self,
                 name: str,
                 x_axis: ChartAxisOptions,
                 y_axis: ChartAxisOptions,
                 y2_axis: ChartAxisOptions = None,
                 width: int = None,
                 height: int = None,
                 border: bool = None,
                 rounded_corners: bool = None,
                 background_color: str = None,
                 background_opacity: int = None,
                 title: str = None,
                 title_style: ChartTextStyle = None):
        self._legend_options: dict = None

        self.x_axis: ChartAxisOptions = x_axis
        self.y_axis: ChartAxisOptions = y_axis
        self.y2_axis: ChartAxisOptions = y2_axis
        if y_axis.date or y2_axis.date:
            warning(
                '"date" options for the y or y2 axes are ignored by the AOP server.')

        self.width: int = width
        self.height: int = height
        self.border: bool = border
        self.rounded_corners: bool = rounded_corners
        self.background_color: str = background_color
        self.background_opacity: int = background_opacity
        self.title: str = title
        self.title_style: ChartTextStyle = title_style

    def set_legend(self, position: str = 'r', style: ChartTextStyle = None):
        self._legend_options = {
            "showLegend": True
        }
        if position:
            self._legend_options["position"] = position
        if style:
            self._legend_options["style"] = style.as_dict

    def remove_legend(self):
        self._legend_options = None

    def set_data_labels(self,
                        separator: bool = None,
                        series_name: bool = None,
                        category_name: bool = None,
                        legend_key: bool = None,
                        value: bool = None,
                        percentage: bool = None,
                        position: str = None):
        self._data_labels_options = {
            "showDataLabels": True
        }
        if separator:
            self._data_labels_options["separator"] = True
        if series_name:
            self._data_labels_options["showSeriesName"] = True
        if category_name:
            self._data_labels_options["showCategoryName"] = True
        if legend_key:
            self._data_labels_options["showLegendKey"] = True
        if value:
            self._data_labels_options["showValue"] = True
        if percentage:
            self._data_labels_options["showPercentage"] = True
        if position:
            self._data_labels_options["position"] = position

    def remove_data_labels(self):
        self._data_labels_options = None

    @property
    def as_dict(self):
        result = {
            "axis": {
                "x": self.x_axis.as_dict,
                "y": self.y_axis.as_dict
            }
        }

        if self.y2_axis:
            result["axis"]["y2"] = self.y2_axis.as_dict
        if self.width:
            result["width"] = self.width
        if self.height:
            result["height"] = self.height
        if self.border is not None:
            result["border"] = self.border
        if self.rounded_corners is not None:
            result["roundedCorners"] = self.rounded_corners
        if self.background_color:
            result["backgroundColor"] = self.background_color
        if self.background_opacity:
            result["backgroundOpacity"] = self.background_opacity
        if self.title:
            result["title"] = self.title
        if self.title_style:
            result["title_style"] = self.title_style.as_dict
        if self._legend_options:
            result["legend"] = self._legend_options
        if self._data_labels_options:
            result["dataLabels"] = self._data_labels_options

        return result


class Series(ABC):
    def __init__(self, name: str = None):
        self.name: str = name

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name

        return result


class XYSeries(Series):
    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 name: str = None):
        super().__init__(name)
        self.x: Iterable[Union[int, float, str]] = x
        self.y: Iterable[Union[int, float]] = y

    @property
    def data(self):
        return [{
            "x": x,
            "y": y
        } for x, y in zip(self.x, self.y)]

    @classmethod
    def from_dataframe(cls, data: 'pandas.DataFrame', name: str = None):
        x = list(data.iloc[:, 0])
        y = list(data.iloc[:, 1])
        return cls(x, y, name=name)


class PieSeries(XYSeries):
    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 name: str = None,
                 color: str = None):
        super().__init__(x, y, name)
        self.color = color

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name
        if self.color:
            result["color"] = self.color

        return result


class AreaSeries(XYSeries):
    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 name: str = None,
                 color: str = None,
                 opacity: float = None):
        super().__init__(x, y, name)
        self.color = color
        self.opacity = opacity

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name
        if self.color:
            result["color"] = self.color
        if self.opacity:
            result["opacity"] = self.opacity

        return result


class LineSeries(XYSeries):
    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 name: str = None,
                 smooth: bool = None,
                 symbol: str = None,
                 symbol_size: Union[str, int] = None,
                 color: str = None,
                 line_width: str = None,
                 line_style: str = None):
        super().__init__(x, y, name)
        self.smooth: bool = smooth
        self.symbol: str = symbol
        self.symbol_size: Union[str, int] = symbol_size
        self.color: str = color
        self.line_width: str = line_width
        self.line_style: str = line_style

    @property
    def as_dict(self):
        result = {
            "data": self.data
        }

        if self.name:
            result["name"] = self.name
        if self.smooth:
            result["smooth"] = self.smooth
        if self.symbol:
            result["symbol"] = self.symbol
        if self.symbol_size:
            result["symbolSize"] = self.symbol_size
        if self.color:
            result["color"] = self.color
        if self.line_width:
            result["lineWidth"] = self.line_width
        if self.line_style:
            result["lineStyle"] = self.line_style

        return result


class BubbleSeries(Series):
    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 sizes: Iterable[Union[int, float]],
                 name: str = None):
        super().__init__(name)
        self.x: Iterable[Union[int, float, str]] = x
        self.y: Iterable[Union[int, float]] = y
        self.sizes: Iterable[Union[int, float]] = sizes

    @property
    def data(self):
        return [{
            "x": x,
            "y": y,
            "size": size
        } for x, y, size in zip(self.x, self.y, self.sizes)]

    @classmethod
    def from_dataframe(cls, data: 'pandas.DataFrame', name: str = None):
        x = list(data.iloc[:, 0])
        y = list(data.iloc[:, 1])
        sizes = list(data.iloc[:, 2])
        return cls(x, y, sizes, name=name)


class StockSeries(Series):
    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 high: Iterable[Union[int, float]],
                 low: Iterable[Union[int, float]],
                 close: Iterable[Union[int, float]],
                 open_: Iterable[Union[int, float]] = None,
                 volume: Iterable[Union[int, float]] = None,
                 name=None):
        super().__init__(name)
        self.x: Iterable[Union[int, float, str]] = x
        self.high: Iterable[Union[int, float]] = high
        self.low: Iterable[Union[int, float]] = low
        self.close: Iterable[Union[int, float]] = close
        # open argument gets a trailing _ because open() is a built-in function
        self.open: Iterable[Union[int, float]] = open_
        self.volume: Iterable[Union[int, float]] = volume

    @property
    def data(self):
        result = [{
            "x": x,
            "high": high,
            "low": low,
            "close": close
        } for x, high, low, close in zip(self.x, self.high, self.low, self.close)]

        for i in range(len(result)):
            if self.open:
                result[i]["open"] = self.open[i]
            if self.volume:
                result[i]["volume"] = self.volume[i]

        return result

    @classmethod
    def from_dataframe(cls, data: 'pandas.DataFrame', name: str = None):
        x = list(data.iloc[:, 0])
        high = list(data["high"])
        low = list(data["low"])
        close = list(data["close"])
        # volume and open are optional
        try:
            open_ = list(data["open"])
        except KeyError:
            open_ = None
        try:
            volume = list(data["volume"])
        except KeyError:
            volume = None
        return cls(x, high, low, close, open_, volume, name=name)


# better to have a series for every possible chart for future-proofing, in case their options diverge later
BarSeries = BarStackedSeries = BarStackedPercentSeries = ColumnSeries = ColumnStackedSeries = ColumnStackedPercentSeries = RadarSeries = ScatterSeries = XYSeries


class Chart(Element, ABC):
    def __init__(self, name: str, options: Union[ChartOptions, dict] = None):
        Element.__init__(self, name)
        self.options: Union[ChartOptions, dict] = options

    @property
    @abstractmethod
    def as_dict(self):
        pass

    def _get_dict(self, updates: dict):
        result = {}
        if self.options:
            result["options"] = self.options if isinstance(
                self.options, dict) else self.options.as_dict
        result.update(updates)
        return {self.name: result}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$" + self.name + "}"})


class LineChart(Chart):
    def __init__(self, name: str, *lines: Union[LineSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.lines: Tuple[Union[LineSeries, XYSeries]] = lines

    @property
    def as_dict(self):
        return self._get_dict({
            "lines": [line.as_dict for line in self.lines],
            "type": "line"
        })


class BarChart(Chart):
    def __init__(self, name: str, *bars: Union[BarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.bars: Tuple[Union[BarSeries, XYSeries]] = bars

    @property
    def as_dict(self):
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "bar"
        })


class BarStackedChart(Chart):
    def __init__(self, name: str, *bars: Union[BarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.bars: Tuple[Union[BarSeries, XYSeries]] = bars

    @property
    def as_dict(self):
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "barStacked"
        })


class BarStackedPercentChart(Chart):
    def __init__(self, name: str, *bars: Union[BarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.bars: Tuple[Union[BarSeries, XYSeries]] = bars

    @property
    def as_dict(self):
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "barStackedPercent"
        })


class ColumnChart(Chart):
    def __init__(self, name: str, *columns: Union[ColumnSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnSeries, XYSeries]] = columns

    @property
    def as_dict(self):
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "column"
        })


class ColumnStackedChart(Chart):
    def __init__(self, name: str, *columns: Union[ColumnSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnSeries, XYSeries]] = columns

    @property
    def as_dict(self):
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "columnStacked"
        })


class ColumnStackedPercentChart(Chart):
    def __init__(self, name: str, *columns: Union[ColumnSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnSeries, XYSeries]] = columns

    @property
    def as_dict(self):
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "columnStackedPercent"
        })


class PieChart(Chart):
    def __init__(self, name: str, *pies: Union[PieSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.pies: Tuple[Union[PieSeries, XYSeries]] = pies

    @property
    def as_dict(self):
        return self._get_dict({
            "pies": [pie.as_dict for pie in self.pies],
            "type": "pie"
        })


class Pie3DChart(Chart):
    def __init__(self, name: str, *pies: Union[PieSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.pies: Tuple[Union[PieSeries, XYSeries]] = pies

    @property
    def as_dict(self):
        return self._get_dict({
            "pies": [pie.as_dict for pie in self.pies],
            "type": "pie3d"
        })


class DoughnutChart(Chart):
    def __init__(self, name: str, *doughnuts: Union[PieSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name)
        self.doughnuts: Tuple[Union[PieSeries, XYSeries]] = doughnuts

    @property
    def as_dict(self):
        return self._get_dict({
            "doughnuts": [nut.as_dict for nut in self.doughnuts],
            "type": "doughnut"
        })


class RadarChart(Chart):
    def __init__(self, name: str, *radars: Union[RadarSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.radars: Tuple[Union[RadarSeries, XYSeries]] = radars

    @property
    def as_dict(self):
        return self._get_dict({
            "radars": [radar.as_dict for radar in self.radars],
            "type": "radar"
        })


class AreaChart(Chart):
    def __init__(self, name: str, *areas: Union[AreaSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.areas: Tuple[Union[AreaSeries, XYSeries]] = areas

    @property
    def as_dict(self):
        return self._get_dict({
            "areas": [area.as_dict for area in self.areas],
            "type": "area"
        })


class ScatterChart(Chart):
    def __init__(self, name: str, *scatters: Union[ScatterSeries, XYSeries], options: ChartOptions = None):
        super().__init__(name, options)
        self.scatters: Tuple[Union[ScatterSeries, XYSeries]] = scatters

    @property
    def as_dict(self):
        return self._get_dict({
            "scatters": [scatter.as_dict for scatter in self.scatters],
            "type": "scatter"
        })


class BubbleChart(Chart):
    def __init__(self, name: str, *bubbles: BubbleSeries, options: ChartOptions = None):
        super().__init__(name, options)
        self.bubbles: Tuple[BubbleSeries] = bubbles

    @property
    def as_dict(self):
        return self._get_dict({
            "bubbles": [bub.as_dict for bub in self.bubbles],
            "type": "bubble"
        })


class StockChart(Chart):
    def __init__(self, name: str, *stocks: StockSeries, options: ChartOptions = None):
        super().__init__(name, options)
        self.stocks: Tuple[StockSeries] = stocks

    @property
    def as_dict(self):
        return self._get_dict({
            "stocks": [stock.as_dict for stock in self.stocks],
            "type": "stock"
        })


def _replace_key_recursive(obj, old_key, new_key):
    for key, value in obj.items():
        if isinstance(value, dict):
            obj[key] = _replace_key_recursive(value, old_key, new_key)
    if old_key in obj:
        obj[new_key] = obj.pop(old_key)
    return obj


class CombinedChart(Chart):
    def __init__(self, name: str, charts: Iterable[Chart], secondaryCharts: Iterable[Chart] = None, options: ChartOptions = None):
        if not options:
            all_options = [chart.options.as_dict for chart in (
                tuple(charts) + tuple(secondaryCharts)) if chart.options]
            options = {}
            # use reversed() to give the first charts precedence (they overwrite the others)
            for options in reversed(all_options):
                options.update(options)

        super().__init__(name, options)
        self.charts = charts
        self.secondaryCharts = secondaryCharts

    def _get_modified_chart_dicts(self):
        primary_list = list(self.charts)
        secondary_list = list(self.secondaryCharts)
        dict_list = []
        for chart in primary_list:
            chart_dict = chart.as_dict
            chart_dict.pop("options", None)
            dict_list.append(chart_dict)
        for chart in secondary_list:
            chart_dict = chart.as_dict
            chart_dict.pop("options", None)
            dict_list.append(_replace_key_recursive(chart_dict, "y", "y2"))
        return dict_list

    @property
    def as_dict(self):
        return self._get_dict({
            "type": "multiple",
            "multiples": self._get_modified_chart_dicts()
        })
