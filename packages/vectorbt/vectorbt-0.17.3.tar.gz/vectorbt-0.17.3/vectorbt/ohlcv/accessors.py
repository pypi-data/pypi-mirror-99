"""Custom pandas accessors.

Methods can be accessed as follows:

* `OHLCVDFAccessor` -> `pd.DataFrame.vbt.ohlcv.*`

The accessors inherit `vectorbt.base.accessors`.

!!! note
    Accessors do not utilize caching."""

import numpy as np
import plotly.graph_objects as go

from vectorbt.root_accessors import register_dataframe_accessor
from vectorbt.utils import checks
from vectorbt.utils.widgets import FigureWidget, make_subplots
from vectorbt.utils.config import merge_dicts
from vectorbt.generic.accessors import GenericDFAccessor


@register_dataframe_accessor('ohlcv')
class OHLCVDFAccessor(GenericDFAccessor):  # pragma: no cover
    """Accessor on top of OHLCV data. For DataFrames only.

    Accessible through `pd.DataFrame.vbt.ohlcv`."""

    def __init__(self, obj, column_names=None, **kwargs):
        if not checks.is_pandas(obj):  # parent accessor
            obj = obj._obj
        self._column_names = column_names

        GenericDFAccessor.__init__(self, obj, **kwargs)

    def plot(self,
             plot_type='OHLC',
             display_volume=True,
             ohlc_kwargs=None,
             volume_kwargs=None,
             ohlc_add_trace_kwargs=None,
             volume_add_trace_kwargs=None,
             fig=None,
             **layout_kwargs):
        """Plot OHLCV data.

        Args:
            plot_type: Either 'OHLC' or 'Candlestick'.
            display_volume (bool): If True, displays volume as bar chart.
            ohlc_kwargs (dict): Keyword arguments passed to `plot_type`.
            volume_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Bar`.
            ohlc_add_trace_kwargs (dict): Keyword arguments passed to `add_trace` for OHLC.
            volume_add_trace_kwargs (dict): Keyword arguments passed to `add_trace` for volume.
            fig (plotly.graph_objects.Figure): Figure to add traces to.
            **layout_kwargs: Keyword arguments for layout.

        ## Example

        ```python-repl
        >>> import vectorbt as vbt

        >>> vbt.YFData.download("BTC-USD").get().vbt.ohlcv.plot()
        ```

        ![](/vectorbt/docs/img/ohlcv.png)
        """
        from vectorbt.settings import ohlcv, color_schema

        if ohlc_kwargs is None:
            ohlc_kwargs = {}
        if volume_kwargs is None:
            volume_kwargs = {}
        if ohlc_add_trace_kwargs is None:
            ohlc_add_trace_kwargs = {}
        if volume_add_trace_kwargs is None:
            volume_add_trace_kwargs = {}
        if display_volume:
            ohlc_add_trace_kwargs = merge_dicts(dict(row=1, col=1), ohlc_add_trace_kwargs)
            volume_add_trace_kwargs = merge_dicts(dict(row=2, col=1), volume_add_trace_kwargs)

        column_names = ohlcv['column_names'] if self._column_names is None else self._column_names
        open = self._obj[column_names['open']]
        high = self._obj[column_names['high']]
        low = self._obj[column_names['low']]
        close = self._obj[column_names['close']]

        # Set up figure
        if fig is None:
            if display_volume:
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0, row_heights=[0.7, 0.3])
            else:
                fig = FigureWidget()
            fig.update_layout(
                showlegend=True,
                xaxis=dict(
                    rangeslider_visible=False,
                    showgrid=True
                ),
                yaxis=dict(
                    showgrid=True
                )
            )
            if display_volume:
                fig.update_layout(
                    xaxis2=dict(
                        showgrid=True
                    ),
                    yaxis2=dict(
                        showgrid=True
                    ),
                    bargap=0
                )
        fig.update_layout(**layout_kwargs)
        if plot_type.lower() == 'ohlc':
            plot_type = 'OHLC'
            plot_obj = go.Ohlc
        elif plot_type.lower() == 'candlestick':
            plot_type = 'Candlestick'
            plot_obj = go.Candlestick
        else:
            raise ValueError("Plot type can be either 'OHLC' or 'Candlestick'")
        ohlc = plot_obj(
            x=self.wrapper.index,
            open=open,
            high=high,
            low=low,
            close=close,
            name=plot_type,
            increasing_line_color=color_schema['increasing'],
            decreasing_line_color=color_schema['decreasing']
        )
        ohlc.update(**ohlc_kwargs)
        fig.add_trace(ohlc, **ohlc_add_trace_kwargs)

        if display_volume:
            volume = self._obj[column_names['volume']]

            marker_colors = np.empty(volume.shape, dtype=np.object)
            marker_colors[(close.values - open.values) > 0] = color_schema['increasing']
            marker_colors[(close.values - open.values) == 0] = color_schema['gray']
            marker_colors[(close.values - open.values) < 0] = color_schema['decreasing']
            volume_bar = go.Bar(
                x=self.wrapper.index,
                y=volume,
                marker=dict(
                    color=marker_colors,
                    line_width=0
                ),
                opacity=0.5,
                name='Volume'
            )
            volume_bar.update(**volume_kwargs)
            fig.add_trace(volume_bar, **volume_add_trace_kwargs)

        return fig