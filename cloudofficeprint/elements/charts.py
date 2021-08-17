from typing import Any, Dict, Iterable, List, Tuple, FrozenSet, Union
from abc import ABC, abstractmethod
from .elements import Element


class ChartTextStyle:
    """Class for defining the styling of the text for a chart."""

    def __init__(self,
                 italic: bool = None,
                 bold: bool = None,
                 color: str = None,
                 font: str = None):
        """
        Args:
            italic (bool, optional): Whether or not the text should be in italic. Defaults to None.
            bold (bool, optional): Whether or not the text should be in bold. Defaults to None.
            color (str, optional): The color of the text. Defaults to None.
            font (str, optional): The font of the text. Defaults to None.
        """
        self.italic: bool = italic
        self.bold: bool = bold
        self.color: str = color
        self.font: str = font

    @property
    def as_dict(self) -> Dict:
        """The dict representation of this ChartTextStyle object.

        Returns:
            Dict: dict representation of this ChartTextStyle object
        """
        result = {}

        if self.italic is not None:
            result["italic"] = self.italic
        if self.bold is not None:
            result["bold"] = self.bold
        if self.color is not None:
            result["color"] = self.color
        if self.font is not None:
            result["font"] = self.font

        return result


class ChartDateOptions:
    """Class for defining the date options for a chart."""

    def __init__(self,
                 format: str = None,
                 code: str = None,
                 unit: str = None,
                 step: Union[int, str] = None):
        """
        Args:
            format (str, optional): The format to display the date on the chart's axis (e.g. unix). Defaults to None.
            code (str, optional): The code for the date (e.g. dd/mm/yyyy). Defaults to None.
            unit (str, optional): The unit to be used for spacing the axis values (e.g. months). Defaults to None.
            step (Union[int, str], optional): How many of the above unit should be used for spacing the axis values (automatic if undefined).
                This option is not supported in LibreOffice. Defaults to None.
        """
        self.format: str = format
        self.code: str = code
        self.unit: str = unit
        self.step: Union[int, str] = step

    @property
    def as_dict(self) -> Dict:
        """The dict representation for this ChartDateOptions object.

        Returns:
            Dict: dict representation for this ChartDateOptions object
        """
        result = {}

        if self.format is not None:
            result["format"] = self.format
        if self.code is not None:
            result["code"] = self.code
        if self.unit is not None:
            result["unit"] = self.unit
        if self.step is not None:
            result["step"] = self.step

        return result


class ChartAxisOptions:
    """Class for defining the axis options for a chart."""

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
                 minor_unit: Union[int, float] = None,
                 formatCode: str = None):
        """
        Args:
            orientation (str, optional): The orientation of the axis, 'minMax' or 'maxMin'. Defaults to None.
            min (Union[int, float], optional): Minimum of the axis. Defaults to None.
            max (Union[int, float], optional): Maximum of the axis. Defaults to None.
            date (ChartDateOptions, optional): Date options, only for stock charts. Defaults to None.
            title (str, optional): Title of the axis. Defaults to None.
            values (bool, optional): Whether or not to show the values on the axis. Defaults to None.
            values_style (ChartTextStyle, optional): Styling for the values. Defaults to None.
            title_style (ChartTextStyle, optional): Styling for the title. Defaults to None.
            title_rotation (int, optional): Title rotation in degrees, clockwise from horizontal axis. Defaults to None.
            major_grid_lines (bool, optional): Whether or not to show the major grid lines. Defaults to None.
            major_unit (Union[int, float], optional): Automatic when undefined, spacing between major grid lines and axis values. Defaults to None.
            minor_grid_lines (bool, optional): Whether or not to show the minor grid lines. Defaults to None.
            minor_unit (Union[int, float], optional): Automatic when undefined, spacing between minor grid lines and axis values. Defaults to None.
            formatCode (str, optional): Format code for axis data, "General", "Number" ... Defaults to None.
        """
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
        self.format_code: str = formatCode

    @property
    def as_dict(self) -> Dict:
        """The dict representation of these chart axis options.

        Returns:
            Dict: dict representation of these chart axis options
        """
        result = {}

        if self.orientation is not None:
            result["orientation"] = self.orientation
        if self.min is not None:
            result["min"] = self.min
        if self.max is not None:
            result["max"] = self.max
        if self.date is not None:
            result["type"] = "date"
            result["date"] = self.date.as_dict
        if self.title is not None:
            result["title"] = self.title
        if self.values is not None:
            result["showValues"] = self.values
        if self.values_style is not None:
            result["valuesStyle"] = self.values_style.as_dict
        if self.title_style is not None:
            result["titleStyle"] = self.title_style.as_dict
        if self.title_rotation is not None:
            result["titleRotation"] = self.title_rotation
        if self.major_grid_lines is not None:
            result["majorGridlines"] = self.major_grid_lines
        if self.major_unit is not None:
            result["majorUnit"] = self.major_unit
        if self.minor_grid_lines is not None:
            result["minorGridlines"] = self.minor_grid_lines
        if self.minor_unit is not None:
            result["minorUnit"] = self.minor_unit
        if self.format_code is not None:
            result["formatCode"] = self.format_code

        return result


class ChartOptions():
    """Options object for a `Chart`."""

    def __init__(self,
                 x_axis: ChartAxisOptions = None,
                 y_axis: ChartAxisOptions = None,
                 y2_axis: ChartAxisOptions = None,
                 width: int = None,
                 height: int = None,
                 border: bool = None,
                 rounded_corners: bool = None,
                 background_color: str = None,
                 background_opacity: int = None,
                 title: str = None,
                 title_style: ChartTextStyle = None,
                 grid: bool = None):
        """
        Args:
            x_axis (ChartAxisOptions, optional): The options for the x-axis. Defaults to None.
            y_axis (ChartAxisOptions, optional): The options for the y-axis. Note: date options for the y axis are ignored by the Cloud Office Print server. Defaults to None.
            y2_axis (ChartAxisOptions, optional): The options for the y2-axis. Note: date options for the y2 axis are ignored by the Cloud Office Print server. Defaults to None.
            width (int, optional): Width of the chart. Defaults to None.
            height (int, optional): Height of the chart. Defaults to None.
            border (bool, optional): Whether or not the chart should have a border. Defaults to None.
            rounded_corners (bool, optional): Whether or not the chart should have rounded corners. Note: displaying rounded corners is not supported by LibreOffice. Defaults to None.
            background_color (str, optional): Background color for the entire chart. Defaults to None.
            background_opacity (int, optional): The opacity of the background color for the entire chart.
                Note: backgroundOpacity is ignored if backgroundColor is not specified or if backgroundColor is specified in a color space which includes an alpha channel (e.g. rgba(0,191,255,0.5)).
                In the latter case, the alpha channel in backgroundColor is used. Defaults to None.
            title (str, optional): The title of the chart. Defaults to None.
            title_style (ChartTextStyle, optional): The styling for the title of the chart. Defaults to None.
            grid (bool, optional): Whether or not the chart should have a grid. Defaults to None.
        """
        self._legend_options: dict = None
        self._data_labels_options: dict = None

        self.x_axis: ChartAxisOptions = x_axis
        self.y_axis: ChartAxisOptions = y_axis
        self.y2_axis: ChartAxisOptions = y2_axis
        self.width: int = width
        self.height: int = height
        self.border: bool = border
        self.rounded_corners: bool = rounded_corners
        self.background_color: str = background_color
        self.background_opacity: int = background_opacity
        self.title: str = title
        self.title_style: ChartTextStyle = title_style
        self.grid: bool = grid

    def set_legend(self, position: str = 'r', style: ChartTextStyle = None):
        """Setter for the legend of the chart.

        Args:
            position (str, optional): Position of the legend.  'l': left, 'r': right, 'b': bottom, 't': top. Defaults to 'r'.
            style (ChartTextStyle, optional): The styling for the text of the legend. Defaults to None.
        """
        self._legend_options = {
            "showLegend": True
        }
        self._legend_options["position"] = position
        if style is not None:
            self._legend_options["style"] = style.as_dict

    def remove_legend(self):
        """Setter for removing the legend from the chart."""
        self._legend_options = None

    def set_data_labels(self,
                        separator: str = None,
                        series_name: bool = None,
                        category_name: bool = None,
                        legend_key: bool = None,
                        value: bool = None,
                        percentage: bool = None,
                        position: str = None):
        """Setter for the data labels for the chart.

        Args:
            separator (str, optional): Seperator : can be either false or anything else for example \n or \t or ; or (, if false). Defaults to None.
            series_name (bool, optional): Whether or not to include the series name in the data label. Defaults to None.
            category_name (bool, optional): Whether or not to include the series category name in the data label. Defaults to None.
            legend_key (bool, optional): Whether or not to include the legend key (i.e. the color of the series) in the data label. Defaults to None.
            value (bool, optional): Whether or not to include the actual value in the data label. Defaults to None.
            percentage (bool, optional): Whether or not to include the percentage in the data label. By default True for pie/pie3d and doughnut. Defaults to None.
            position (str, optional): The position of the data label.
                Can be 'center', 'left', 'right', 'above', 'below', 'insideBase', 'bestFit', 'outsideEnd', 'insideEnd'.
                Note that not all options might be available for specific charts. Defaults to None.
        """
        self._data_labels_options = {
            "showDataLabels": True
        }

        if separator is not None:
            self._data_labels_options["separator"] = separator
        if series_name is not None:
            self._data_labels_options["showSeriesName"] = series_name
        if category_name is not None:
            self._data_labels_options["showCategoryName"] = category_name
        if legend_key is not None:
            self._data_labels_options["showLegendKey"] = legend_key
        if value is not None:
            self._data_labels_options["showValue"] = value
        if percentage is not None:
            self._data_labels_options["showPercentage"] = percentage
        if position is not None:
            self._data_labels_options["position"] = position

    def remove_data_labels(self):
        """Setter to remove the data labels from the chart."""
        self._data_labels_options = None

    @property
    def as_dict(self) -> Dict:
        """The dict representation of this ChartOptions object.

        Returns:
            Dict: dict representation of this ChartOptions object
        """
        result = {
            "axis": {
            }
        }

        if self.x_axis is not None:
            result['axis']['x'] = self.x_axis.as_dict
        if self.y_axis is not None:
            result['axis']['y'] = self.y_axis.as_dict
        if self.y2_axis is not None:
            result["axis"]["y2"] = self.y2_axis.as_dict
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        if self.border is not None:
            result["border"] = self.border
        if self.rounded_corners is not None:
            result["roundedCorners"] = self.rounded_corners
        if self.background_color is not None:
            result["backgroundColor"] = self.background_color
        if self.background_opacity is not None:
            result["backgroundOpacity"] = self.background_opacity
        if self.title is not None:
            result["title"] = self.title
        if self.title_style is not None:
            result["titleStyle"] = self.title_style.as_dict
        if self.grid is not None:
            result["grid"] = self.grid
        if self._legend_options is not None:
            result["legend"] = self._legend_options
        if self._data_labels_options is not None:
            result["dataLabels"] = self._data_labels_options

        return result


class Series(ABC):
    """Abstract base class for a series."""

    def __init__(self, name: str = None):
        self.name: str = name

    @property
    @abstractmethod
    def data(self):
        """Get the data used in the series. E.g. x-values, y-values, ..."""
        pass

    @property
    def as_dict(self) -> Dict:
        """The dict representation of this Series object.

        Returns:
            Dict: dict representation of this Series object
        """
        result = {
            "data": self.data
        }

        if self.name is not None:
            result["name"] = self.name

        return result


class XYSeries(Series):
    """A series for the case where the data consists of x-values and y-values."""

    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 name: str = None,
                 color: str = None):
        """
        Args:
            x (Iterable[Union[int, float, str]]): The data for the x-axis.
            y (Iterable[Union[int, float]]): The data for the y-axis.
            name (str, optional): The name of the series. Defaults to None.
            color (str, optional): The color in which the series should be shown on a chart.
                Can be html/css colors or hex values. Defaults to None.
        """
        super().__init__(name)
        self.x: Iterable[Union[int, float, str]] = x
        self.y: Iterable[Union[int, float]] = y
        self.color: str = color

    @property
    def data(self):
        return [{
            "x": x,
            "y": y
        } for x, y in zip(self.x, self.y)]

    @classmethod
    def from_dataframe(cls, data: 'pandas.DataFrame', name: str = None) -> 'XYSeries':
        """Generate an XYSeries from a [Pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

        Args:
            data (pandas.DataFrame): Pandas dataframe containing the data for the x- and y-axis.
            name (str): The name for the series.

        Returns:
            XYSeries: XYSeries generated from a Pandas dataframe
        """
        x = list(data.iloc[:, 0])
        y = list(data.iloc[:, 1])
        return cls(x, y, name=name)

    @property
    def as_dict(self) -> Dict:
        result = super().as_dict

        if self.color is not None:
            result['color'] = self.color

        return result


class PieSeries(XYSeries):
    """A series for pie charts."""

    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 name: str = None,
                 colors: Iterable[str] = None):
        """
        Args:
            x (Iterable[Union[int, float, str]]): The data for the x-axis.
            y (Iterable[Union[int, float]]): The data for the y-axis.
            name (str, optional): The name of the series. Defaults to None.
            colors (Iterable[str], optional): Should be an iterable that contains the color for each specific pie slice.
                If no colors are specified, the document's theme color is used.
                If some colors are specified, but not for all data points, random colors will fill the gaps.
                The value for non-specified colors must be None.
                Warning: this is not the same as self.color of XYSeries, which is the color for the entire series, but this is not applicable to PieSeries.
                Defaults to None.
        """
        super().__init__(x, y, name)
        self.colors = colors

    @property
    def as_dict(self) -> Dict:
        result = super().as_dict

        if self.colors is not None:
            # Add the color for each slice to 'data'
            for i in range(len(tuple(self.colors))):
                if self.colors[i] is not None:
                    result["data"][i]['color'] = self.colors[i]

        return result


class AreaSeries(XYSeries):
    """A series for an area chart."""

    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 name: str = None,
                 color: str = None,
                 opacity: float = None):
        """
        Args:
            x (Iterable[Union[int, float, str]]): The data for the x-axis.
            y (Iterable[Union[int, float]]): The data for the y-axis.
            name (str, optional): The name of the series. Defaults to None.
            color (str, optional): The color in which the series should be shown on a chart.
                Can be html/css colors or hex values. Defaults to None.
            opacity (float, optional): The opacity for the color of the series. Defaults to None.
        """
        super().__init__(x, y, name, color)
        self.opacity: float = opacity

    @property
    def as_dict(self) -> Dict:
        result = super().as_dict

        if self.opacity is not None:
            result["opacity"] = self.opacity

        return result


class LineSeries(XYSeries):
    """A series for a line chart."""

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
        """
        Args:
            x (Iterable[Union[int, float, str]]): The data for the x-axis.
            y (Iterable[Union[int, float]]): The data for the y-axis.
            name (str, optional): The name of the series. Defaults to None.
            smooth (bool, optional): Whether or not the corners of the angles formed in the data-points are smoothened. Defaults to None.
            symbol (str, optional): Symbol representing the datapoints. Can be square (default), diamond or triangle. Defaults to None.
            symbol_size (Union[str, int], optional): Size of the symbol representing the data-points in (in em, pt, px, cm or in), by default: automatic. Defaults to None.
            color (str, optional): The color in which the series should be shown on a chart.
                Can be html/css colors or hex values. Defaults to None.
            line_width (str, optional): Thickness of the connecting line in em, pt, px, cm or in. Defaults to None.
            line_style (str, optional): Style of the line. Supported options can be found online on the [Cloud Office Print documentation](https://www.cloudofficeprint.com/docs/#line). Defaults to None.
        """
        # TODO: update website for line_style argument?
        super().__init__(x, y, name, color)
        self.smooth: bool = smooth
        self.symbol: str = symbol
        self.symbol_size: Union[str, int] = symbol_size
        self.line_width: str = line_width
        self.line_style: str = line_style

    @property
    def as_dict(self) -> Dict:
        result = super().as_dict

        if self.smooth is not None:
            result["smooth"] = self.smooth
        if self.symbol is not None:
            result["symbol"] = self.symbol
        if self.symbol_size is not None:
            result["symbolSize"] = self.symbol_size
        if self.line_width is not None:
            result["lineWidth"] = self.line_width
        if self.line_style is not None:
            result["lineStyle"] = self.line_style

        return result


class BubbleSeries(XYSeries):
    """A series for a bubble chart."""

    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 y: Iterable[Union[int, float]],
                 sizes: Iterable[Union[int, float]],
                 name: str = None,
                 color: str = None):
        """
        Args:
            x (Iterable[Union[int, float, str]]): The data for the x-axis.
            y (Iterable[Union[int, float]]): The data for the y-axis.
            sizes (Iterable[Union[int, float]]): An iterable containing the sizes for each bubble of the series.
            name (str, optional): The name of the series. Defaults to None.
            color (str, optional): The color in which the series should be shown on a chart.
                Can be html/css colors or hex values. Defaults to None.
        """
        super().__init__(x, y, name, color)
        self.sizes: Iterable[Union[int, float]] = sizes

    @property
    def data(self) -> List[Dict[str, Any]]:
        return [{
            "x": x,
            "y": y,
            "size": size
        } for x, y, size in zip(self.x, self.y, self.sizes)]

    @classmethod
    def from_dataframe(cls, data: 'pandas.DataFrame', name: str = None) -> 'BubbleSeries':
        """Generate a BubbleSeries from a [Pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

        Args:
            data (pandas.DataFrame): Pandas dataframe containing the data for the x- and y-axis and the sizes for the bubbles.
            name (str): The name for the series.

        Returns:
            BubbleSeries: BubbleSeries generated from a Pandas dataframe
        """
        x = list(data.iloc[:, 0])
        y = list(data.iloc[:, 1])
        sizes = list(data.iloc[:, 2])
        return cls(x, y, sizes, name=name)


class StockSeries(Series):
    """A series for candlestick charts."""

    def __init__(self,
                 x: Iterable[Union[int, float, str]],
                 high: Iterable[Union[int, float]],
                 low: Iterable[Union[int, float]],
                 close: Iterable[Union[int, float]],
                 open_: Iterable[Union[int, float]] = None,
                 volume: Iterable[Union[int, float]] = None,
                 name: str = None):
        """
        Args:
            x (Iterable[Union[int, float, str]]): The data for the x-axis.
            high (Iterable[Union[int, float]]): The data for the hight prices.
            low (Iterable[Union[int, float]]): The data for the low prices.
            close (Iterable[Union[int, float]]): The data for the closing prices.
            open_ (Iterable[Union[int, float]], optional): The data for the opening prices. Defaults to None.
            volume (Iterable[Union[int, float]], optional): The data for the volumes. Defaults to None.
            name (str, optional): The name of the series. Defaults to None.
        """
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
            if self.open is not None:
                result[i]["open"] = self.open[i]
            if self.volume is not None:
                result[i]["volume"] = self.volume[i]

        return result

    @classmethod
    def from_dataframe(cls, data: 'pandas.DataFrame', name: str = None) -> 'StockSeries':
        """Generate a StockSeries from a [Pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

        Args:
            data (pandas.DataFrame): Pandas dataframe containing the x, high, low and possibly volume and open data.
            name (str): The name for the series.

        Returns:
            StockSeries: StockSeries generated from a Pandas dataframe
        """
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
BarSeries = BarStackedSeries = BarStackedPercentSeries = ColumnSeries = ColumnStackedSeries = ColumnStackedPercentSeries = ScatterSeries = XYSeries
RadarSeries = LineSeries


class Chart(Element, ABC):
    """The abstract base class for a chart."""

    def __init__(self, name: str, options: Union[ChartOptions, dict] = None):
        """
        Args:
            name (str): The name of the chart.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        Element.__init__(self, name)
        self.options: Union[ChartOptions, dict] = options

    @property
    @abstractmethod
    def as_dict(self) -> Dict:
        pass

    def _get_dict(self, updates: dict) -> Dict:
        """Update the given dict with the chart options and return the result.

        Args:
            updates (dict): the dict that needs to be updated with the chart options

        Returns:
            Dict: the input dict, updated with the chart options
        """
        result = {}
        if self.options is not None:
            result["options"] = self.options if isinstance(
                self.options, dict) else self.options.as_dict
        result.update(updates)
        return {self.name: result}

    @property
    def available_tags(self) -> FrozenSet[str]:
        return frozenset({"{$" + self.name + "}"})


class LineChart(Chart):
    """Class for a line chart"""

    def __init__(self, name: str, lines: Tuple[Union[LineSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            lines (Tuple[Union[LineSeries, XYSeries]]): Iterable of line series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.lines: Tuple[Union[LineSeries, XYSeries]] = lines

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "lines": [line.as_dict for line in self.lines],
            "type": "line"
        })


class BarChart(Chart):
    """Class for a bar chart"""

    def __init__(self, name: str, bars: Tuple[Union[BarSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            bars (Tuple[Union[BarSeries, XYSeries]]): Iterable of bar series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.bars: Tuple[Union[BarSeries, XYSeries]] = bars

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "bar"
        })


class BarStackedChart(Chart):
    """Class for a stacked bar chart"""

    def __init__(self, name: str, bars: Tuple[Union[BarStackedSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            bars (Tuple[Union[BarSeries, XYSeries]]): Iterable of stacked bar series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.bars: Tuple[Union[BarStackedSeries, XYSeries]] = bars

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "barStacked"
        })


class BarStackedPercentChart(Chart):
    """Class for a stacked bar chart with the x-axis expressed in percentage"""

    def __init__(self, name: str, bars: Tuple[Union[BarStackedPercentSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            bars (Tuple[Union[BarSeries, XYSeries]]): Iterable of stacked bar (percentage) series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.bars: Tuple[Union[BarStackedPercentSeries, XYSeries]] = bars

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "bars": [bar.as_dict for bar in self.bars],
            "type": "barStackedPercent"
        })


class ColumnChart(Chart):
    """Class for a column chart"""

    def __init__(self, name: str, columns: Tuple[Union[ColumnSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            columns (Tuple[Union[ColumnSeries, XYSeries]]): Iterable of column series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnSeries, XYSeries]] = columns

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "column"
        })


class ColumnStackedChart(Chart):
    """Class for a stacked column chart"""

    def __init__(self, name: str, columns: Tuple[Union[ColumnStackedSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            columns (Tuple[Union[ColumnSeries, XYSeries]]): Iterable of stacked column series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnStackedSeries, XYSeries]] = columns

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "columnStacked"
        })


class ColumnStackedPercentChart(Chart):
    """Class for a stacked column chart with the x-axis expressed in percentage"""

    def __init__(self, name: str, columns: Tuple[Union[ColumnStackedPercentSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            columns (Tuple[Union[ColumnSeries, XYSeries]]): Iterable of stacked column (percentage) series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.columns: Tuple[Union[ColumnStackedPercentSeries,
                                  XYSeries]] = columns

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "columns": [col.as_dict for col in self.columns],
            "type": "columnStackedPercent"
        })


class PieChart(Chart):
    """Class for a pie chart"""

    def __init__(self, name: str, pies: Tuple[Union[PieSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            pies (Tuple[Union[PieSeries, XYSeries]]): Iterable of pie series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.pies: Tuple[Union[PieSeries, XYSeries]] = pies

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "pies": [pie.as_dict for pie in self.pies],
            "type": "pie"
        })


class Pie3DChart(Chart):
    """Class for a 3D pie chart"""

    def __init__(self, name: str, pies: Tuple[Union[PieSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            pies (Tuple[Union[PieSeries, XYSeries]]): Iterable of 3D pie series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.pies: Tuple[Union[PieSeries, XYSeries]] = pies

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "pies": [pie.as_dict for pie in self.pies],
            "type": "pie3d"
        })


class DoughnutChart(Chart):
    """Class for a doughnut chart"""

    def __init__(self, name: str, doughnuts: Tuple[Union[PieSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            doughnuts (Tuple[Union[PieSeries, XYSeries]]): Iterable of doughnut series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.doughnuts: Tuple[Union[PieSeries, XYSeries]] = doughnuts

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "doughnuts": [nut.as_dict for nut in self.doughnuts],
            "type": "doughnut"
        })


class RadarChart(Chart):
    """Class for a radar chart"""

    def __init__(self, name: str, radars: Tuple[Union[RadarSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            radars (Tuple[Union[RadarSeries, XYSeries]]): Iterable of radar series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.radars: Tuple[Union[RadarSeries, XYSeries]] = radars

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "radars": [radar.as_dict for radar in self.radars],
            "type": "radar"
        })


class AreaChart(Chart):
    """Class for an area chart"""

    def __init__(self, name: str, areas: Tuple[Union[AreaSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            areas (Tuple[Union[AreaSeries, XYSeries]]): Iterable of area series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.areas: Tuple[Union[AreaSeries, XYSeries]] = areas

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "areas": [area.as_dict for area in self.areas],
            "type": "area"
        })


class ScatterChart(Chart):
    """Class for a scatter chart"""

    def __init__(self, name: str, scatters: Tuple[Union[ScatterSeries, XYSeries]], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            scatters (Tuple[Union[ScatterSeries, XYSeries]]): Iterable of scatter series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.scatters: Tuple[Union[ScatterSeries, XYSeries]] = scatters

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "scatters": [scatter.as_dict for scatter in self.scatters],
            "type": "scatter"
        })


class BubbleChart(Chart):
    """Class for a bubble chart"""

    def __init__(self, name: str, bubbles: Tuple[BubbleSeries], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            bubbles (Tuple[BubbleSeries]): Iterable of bubble series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.bubbles: Tuple[BubbleSeries] = bubbles

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "bubbles": [bub.as_dict for bub in self.bubbles],
            "type": "bubble"
        })


class StockChart(Chart):
    """Class for a candlestick chart"""

    def __init__(self, name: str, stocks: Tuple[StockSeries], options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            stocks (Tuple[StockSeries]): Iterable of stock series.
            options (Union[ChartOptions, dict], optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.stocks: Tuple[StockSeries] = stocks

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "stocks": [stock.as_dict for stock in self.stocks],
            "type": "stock"
        })


def _replace_key_recursive(obj: Dict, old_key: str, new_key: str) -> Dict:
    """Recursively replace the keys in a (possibly) nested dictionary with a new name.
    Objects with key "options" will not be modified (y-axis stays y-axis).

    Args:
        obj (Dict): input dictionary
        old_key (str): old name of the key
        new_key (str): new name of the key

    Returns:
        Dict: input dictionary with the old key name replaced by the new key name
    """
    for key, value in obj.items():
        if isinstance(value, dict):
            if key != 'options':
                obj[key] = _replace_key_recursive(value, old_key, new_key)
        elif isinstance(value, list):
            for i in range(len(value)):
                value[i] = _replace_key_recursive(value[i], old_key, new_key)
    if old_key in obj:
        obj[new_key] = obj.pop(old_key)
    return obj


class CombinedChart(Chart):
    """Class for a combined chart. It is possible to combine more than 2 types of chart but there can only be two value axes."""

    def __init__(self, name: str, charts: Iterable[Chart], secondaryCharts: Iterable[Chart] = None, options: ChartOptions = None):
        """
        Args:
            name (str): The name of the chart.
            charts (Iterable[Chart]): Charts for the first y-axis.
            secondaryCharts (Iterable[Chart], optional): Charts for the secondary y-axis. Defaults to None.
            options (ChartOptions, optional): The options for the chart. Defaults to None.
        """
        super().__init__(name, options)
        self.charts: Iterable[Chart] = charts
        self.secondaryCharts: Iterable[Chart] = secondaryCharts

    def _get_modified_chart_dicts(self) -> List[Dict]:
        """Replace the y-axis with the y2-axis for the secondary charts.
        Add the dict representation for each chart to a list and return that list.

        Returns:
            List[Dict]: list containing the dict representation for each chart, after processing
        """
        primary_list = list(self.charts)
        secondary_list = list(self.secondaryCharts)
        dict_list = []
        for chart in primary_list:
            chart_dict_full = chart.as_dict
            chart_dict = chart_dict_full[chart.name]
            dict_list.append(chart_dict)
        for chart in secondary_list:
            chart_dict_full = chart.as_dict
            chart_dict = chart_dict_full[chart.name]
            dict_list.append(_replace_key_recursive(chart_dict, "y", "y2"))
        return dict_list

    @property
    def as_dict(self) -> Dict:
        return self._get_dict({
            "type": "multiple",
            "multiples": self._get_modified_chart_dicts()
        })
