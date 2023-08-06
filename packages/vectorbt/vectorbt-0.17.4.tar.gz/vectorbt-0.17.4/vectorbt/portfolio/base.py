"""Base class for modeling portfolio and measuring its performance.

Provides the class `vectorbt.portfolio.base.Portfolio` for modeling portfolio performance
and calculating various risk and performance metrics. It uses Numba-compiled
functions from `vectorbt.portfolio.nb` for most computations and record classes based on
`vectorbt.records.base.Records` for evaluating events such as orders, logs, trades, positions and drawdowns.

The job of the `Portfolio` class is to create a series of positions allocated 
against a cash component, produce an equity curve, incorporate basic transaction costs
and produce a set of statistics about its performance. In particular it outputs
position/profit metrics and drawdown information.

## Workflow

The workflow of `Portfolio` is simple:

1. Receives a set of inputs, such as entry and exit signals
2. Uses them to generate and fill orders in form of records (simulation part)
3. Calculates a broad range of risk & performance metrics based on these records (analysis part)

It basically builds upon the `vectorbt.portfolio.orders.Orders` class. To simplify creation of order
records and keep track of balances, it exposes several convenience methods with prefix `from_`.
For example, you can use `Portfolio.from_signals` method to generate orders from entry and exit signals.
Alternatively, you can use `Portfolio.from_order_func` to run a custom order function on each tick.
The results are then automatically passed to the constructor method of `Portfolio` and you will
receive a portfolio instance ready to be used for performance analysis.

This way, one can simulate and analyze his/her strategy in a couple of lines.

### Example

The following example does something crazy: it checks candlestick data of 6 major cryptocurrencies
in 2020 against every single pattern found in TA-Lib, and translates them into signals:

```python-repl
>>> import numpy as np
>>> import pandas as pd
>>> from datetime import datetime
>>> import talib
>>> import vectorbt as vbt

>>> # Fetch price history
>>> symbols = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'BNB-USD', 'BCH-USD', 'LTC-USD']
>>> start = datetime(2020, 1, 1)
>>> end = datetime(2020, 9, 1)
>>> # OHLCV by column
>>> ohlcv = vbt.YFData.download(symbols, start=start, end=end).concat()

>>> ohlcv['Open'].head()
symbol          BTC-USD     ETH-USD   XRP-USD    BNB-USD     BCH-USD  \
Date
2020-01-01  7194.892090  129.630661  0.192912  13.730962  204.671295
2020-01-02  7202.551270  130.820038  0.192708  13.698126  204.354538
2020-01-03  6984.428711  127.411263  0.187948  13.035329  196.007690
2020-01-04  7345.375488  134.168518  0.193521  13.667442  222.536560
2020-01-05  7410.451660  135.072098  0.194367  13.888340  225.779831

symbol        LTC-USD
Date
2020-01-01  41.326534
2020-01-02  42.018085
2020-01-03  39.863129
2020-01-04  42.383526
2020-01-05  43.291382

>>> # Run every single pattern recognition indicator and combine results
>>> result = pd.DataFrame.vbt.empty_like(ohlcv['Open'], fill_value=0.)
>>> for pattern in talib.get_function_groups()['Pattern Recognition']:
...     PRecognizer = vbt.IndicatorFactory.from_talib(pattern)
...     pr = PRecognizer.run(ohlcv['Open'], ohlcv['High'], ohlcv['Low'], ohlcv['Close'])
...     result = result + pr.integer

>>> # Don't look into future
>>> result = result.vbt.fshift(1)

>>> # Treat each number as order value in USD
>>> size = result / ohlcv['Open']

>>> # Simulate portfolio
>>> portfolio = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001)

>>> # Visualize portfolio value
>>> portfolio.value().vbt.plot()
```

![](/vectorbt/docs/img/portfolio_value.png)

## Broadcasting

`Portfolio` is very flexible towards inputs:

* Accepts both Series and DataFrames as inputs
* Broadcasts inputs to the same shape using vectorbt's own broadcasting rules
* Many inputs (such as `fees`) can be passed as a single value, value per column/row, or as a matrix
* Implements flexible indexing wherever possible to save memory

## Grouping

One of the key features of `Portfolio` is the ability to group columns. Groups can be specified by
`group_by`, which can be anything from positions or names of column levels, to a NumPy array with
actual groups. Groups can be formed to share capital between columns or to compute metrics
for a combined portfolio of multiple independent columns.

For example, let's divide our portfolio into two groups sharing the same cash:

```python-repl
>>> # Simulate combined portfolio
>>> group_by = pd.Index([
...     'first', 'first', 'first',
...     'second', 'second', 'second'
... ], name='group')
>>> comb_portfolio = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001,
...     group_by=group_by, cash_sharing=True)

>>> # Get total profit per group
>>> comb_portfolio.total_profit()
group
first     26221.571200
second    10141.952674
Name: total_profit, dtype: float64
```

Not only can you analyze each group, but also each column in the group:

```python-repl
>>> # Get total profit per column
>>> comb_portfolio.total_profit(group_by=False)
symbol
BTC-USD     5792.120252
ETH-USD    16380.039692
XRP-USD     4049.411256
BNB-USD     6081.253551
BCH-USD      400.573418
LTC-USD     3660.125705
Name: total_profit, dtype: float64
```

In the same way, you can introduce new grouping to the method itself:

```python-repl
>>> # Get total profit per group
>>> portfolio.total_profit(group_by=group_by)
group
first     26221.571200
second    10141.952674
Name: total_profit, dtype: float64
```

!!! note
    If cash sharing is enabled, grouping can be disabled but cannot be modified.

## Indexing

Like any other class subclassing `vectorbt.base.array_wrapper.Wrapping`, we can do pandas indexing
on a `Portfolio` instance, which forwards indexing operation to each object with columns:

```python-repl
>>> portfolio['BTC-USD']
<vectorbt.portfolio.base.Portfolio at 0x7fac7517ac88>

>>> portfolio['BTC-USD'].total_profit()
5792.120252189081
```

Combined portfolio is indexed by group:

```python-repl
>>> comb_portfolio['first']
<vectorbt.portfolio.base.Portfolio at 0x7fac5756b828>

>>> comb_portfolio['first'].total_profit()
26221.57120014546
```

!!! note
    Changing index (time axis) is not supported. The object should be treated as a Series
    rather than a DataFrame; for example, use `portfolio.iloc[0]` instead of `portfolio.iloc[:, 0]`.

    Indexing behavior depends solely upon `vectorbt.base.array_wrapper.ArrayWrapper`.
    For example, if `group_select` is enabled indexing will be performed on groups,
    otherwise on single columns. You can pass wrapper arguments with `wrapper_kwargs`.

## Logging

To collect more information on how a specific order was processed or to be able to track the whole
simulation from the beginning to the end, you can turn on logging.

```python-repl
>>> # Simulate portfolio with logging
>>> portfolio = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001, log=True)

>>> portfolio.logs.records
        id  idx  col  group  cash_now  shares_now  val_price_now  value_now  \
0        0    0    0      0       inf    0.000000    7194.892090        inf
1        1    1    0      0       inf    0.000000    7202.551270        inf
2        2    2    0      0       inf    0.000000    6984.428711        inf
...    ...  ...  ...    ...       ...         ...            ...        ...
1461  1461  241    5      5       inf  272.389644      57.207737        inf
1462  1462  242    5      5       inf  274.137659      62.844059        inf
1463  1463  243    5      5       inf  282.093860      61.105076        inf

          size  size_type  ...   log  new_cash  new_shares  res_size  \
0          NaN          0  ...  True       inf    0.000000       NaN
1     0.000000          0  ...  True       inf    0.000000       NaN
2     0.000000          0  ...  True       inf    0.000000       NaN
...        ...        ...  ...   ...       ...         ...       ...
1461  1.748015          0  ...  True       inf  274.137659  1.748015
1462  7.956202          0  ...  True       inf  282.093860  7.956202
1463 -1.636525          0  ...  True       inf  280.457335  1.636525

        res_price  res_fees  res_side  res_status  res_status_info  order_id
0             NaN       NaN        -1           1                0        -1
1             NaN       NaN        -1           1                5        -1
2             NaN       NaN        -1           1                5        -1
...           ...       ...       ...         ...              ...       ...
1461    57.264945    0.1001         0           0               -1      1070
1462    62.906903    0.5005         0           0               -1      1071
1463    61.043971    0.0999         1           0               -1      1072

[1464 rows x 30 columns]
```

Just as orders, logs are also records and thus can be easily analyzed:

```python-repl
>>> from vectorbt.portfolio.enums import OrderStatus

>>> portfolio.logs.map_field('res_status', value_map=OrderStatus).value_counts()
symbol   BTC-USD  ETH-USD  XRP-USD  BNB-USD  BCH-USD  LTC-USD
Ignored       60       72       67       66       67       59
Filled       184      172      177      178      177      185
```

Logging can also be turned on just for one order, row, or column, since as many other
variables it's specified per order and can broadcast automatically.

!!! note
    Logging can slow down simulation.

## Caching

`Portfolio` heavily relies upon caching. If a method or a property requires heavy computation,
it's wrapped with `vectorbt.utils.decorators.cached_method` and `vectorbt.utils.decorators.cached_property`
respectively. Caching can be disabled globally via `vectorbt.settings`.

!!! note
    Because of caching, class is meant to be immutable and all properties are read-only.
    To change any attribute, use the `copy` method and pass the attribute as keyword argument.

If you're running out of memory when working with large arrays, make sure to disable caching
and then store most important time series manually. For example, if you're interested in Sharpe
ratio or other metrics based on returns, run and save `Portfolio.returns` and then use the
`vectorbt.returns.accessors.ReturnsAccessor` to analyze them. Do not use methods akin to
`Portfolio.sharpe_ratio` because they will re-calculate returns each time.

Alternatively, you can precisely point at attributes and methods that should or shouldn't
be cached. For example, you can blacklist the entire `Portfolio` class except a few most called
methods such as `Portfolio.cash_flow` and `Portfolio.share_flow`:

```python-repl
>>> vbt.settings.caching['blacklist'].append('Portfolio')
>>> vbt.settings.caching['whitelist'].extend([
...     'Portfolio.cash_flow',
...     'Portfolio.share_flow'
... ])
```

Define rules for one instance of `Portfolio`:

```python-repl
>>> vbt.settings.caching['blacklist'].append(portfolio)
>>> vbt.settings.caching['whitelist'].extend([
...     portfolio.cash_flow,
...     portfolio.share_flow
... ])
```

!!! note
    Note that the above approach doesn't work for cached properties.
    Use tuples of the instance and the property name instead, such as `(portfolio, 'orders')`.

To reset caching:

```python-repl
>>> vbt.settings.caching.reset()
```

## Saving and loading

Like any other class subclassing `vectorbt.utils.config.Pickleable`, we can save a `Portfolio`
instance to the disk with `Portfolio.save` and load it with `Portfolio.load`:

```python-repl
>>> portfolio = vbt.Portfolio.from_orders(
...     ohlcv['Close'], size, price=ohlcv['Open'],
...     init_cash='autoalign', fees=0.001, slippage=0.001, freq='1D')
>>> portfolio.sharpe_ratio()
symbol
BTC-USD    1.743437
ETH-USD    2.800903
XRP-USD    1.607904
BNB-USD    1.805373
BCH-USD    0.269392
LTC-USD    1.040494
Name: sharpe_ratio, dtype: float64

>>> portfolio.save('portfolio_config')
>>> portfolio = vbt.Portfolio.load('portfolio_config')
>>> portfolio.sharpe_ratio()
symbol
BTC-USD    1.743437
ETH-USD    2.800903
XRP-USD    1.607904
BNB-USD    1.805373
BCH-USD    0.269392
LTC-USD    1.040494
Name: sharpe_ratio, dtype: float64
```

!!! note
    Save files won't include neither cached results nor global defaults. For example,
    passing `incl_unrealized` as None will also use None when the portfolio is loaded from disk.
    Make sure to either pass all arguments explicitly or to save and load the `vectorbt.settings` config.
"""

import numpy as np
import pandas as pd
from inspect import signature
from collections import OrderedDict
import warnings

from vectorbt.utils import checks
from vectorbt.utils.decorators import cached_property, cached_method
from vectorbt.utils.enum import convert_str_enum_value
from vectorbt.utils.config import merge_dicts
from vectorbt.utils.random import set_seed
from vectorbt.utils.colors import adjust_opacity
from vectorbt.utils.widgets import make_subplots
from vectorbt.base.reshape_fns import to_1d, to_2d, broadcast, broadcast_to
from vectorbt.base.array_wrapper import ArrayWrapper, Wrapping
from vectorbt.generic import nb as generic_nb
from vectorbt.generic.drawdowns import Drawdowns
from vectorbt.signals.generators import RAND, RPROB
from vectorbt.portfolio import nb
from vectorbt.portfolio.orders import Orders
from vectorbt.portfolio.trades import Trades, Positions
from vectorbt.portfolio.logs import Logs
from vectorbt.portfolio.enums import (
    InitCashMode,
    CallSeqType,
    SizeType,
    ConflictMode,
    Direction
)


def _mean_agg_func(df):
    """Compute mean for `Portfolio.stats`."""
    return df.mean(axis=0)


def add_returns_methods(func_names):
    """Class decorator to add `vectorbt.returns.accessors.ReturnsAccessor` methods to `Portfolio`."""

    def wrapper(cls):
        for func_name in func_names:
            if isinstance(func_name, tuple):
                ret_func_name = func_name[0]
            else:
                ret_func_name = func_name

            def returns_method(
                    self,
                    *args,
                    group_by=None,
                    year_freq=None,
                    _ret_func_name=ret_func_name,
                    active_returns=False,
                    in_sim_order=False,
                    reuse_returns=None,
                    **kwargs):
                if reuse_returns is not None:
                    returns = reuse_returns
                else:
                    if active_returns:
                        returns = self.active_returns(group_by=group_by)
                    else:
                        returns = self.returns(group_by=group_by, in_sim_order=in_sim_order)
                returns_acc = returns.vbt.returns(freq=self.wrapper.freq, year_freq=year_freq)
                # Select only those arguments in kwargs that are also in the method's signature
                # This is done for Portfolio.stats which passes the same kwargs to multiple methods
                method = getattr(returns_acc, _ret_func_name)
                sig = signature(method)
                arg_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
                new_kwargs = {}
                for arg_name in arg_names:
                    if arg_name in kwargs:
                        new_kwargs[arg_name] = kwargs[arg_name]
                return method(*args, **new_kwargs)

            if isinstance(func_name, tuple):
                func_name = func_name[1]
            returns_method.__name__ = func_name
            returns_method.__qualname__ = f"{cls.__name__}.{func_name}"
            returns_method.__doc__ = f"See `vectorbt.returns.accessors.ReturnsAccessor.{ret_func_name}`."
            setattr(cls, func_name, cached_method(returns_method))
        return cls

    return wrapper


@add_returns_methods([
    ('daily', 'daily_returns'),
    ('annual', 'annual_returns'),
    ('cumulative', 'cumulative_returns'),
    ('annualized', 'annualized_return'),
    'annualized_volatility',
    'calmar_ratio',
    'omega_ratio',
    'sharpe_ratio',
    'deflated_sharpe_ratio',
    'downside_risk',
    'sortino_ratio',
    'information_ratio',
    'beta',
    'alpha',
    'tail_ratio',
    'value_at_risk',
    'cond_value_at_risk',
    'capture',
    'up_capture',
    'down_capture',
    'drawdown',
    'max_drawdown'
])
class Portfolio(Wrapping):
    """Class for modeling portfolio and measuring its performance.

    Args:
        wrapper (ArrayWrapper): Array wrapper.

            See `vectorbt.base.array_wrapper.ArrayWrapper`.
        close (array_like): Reference price, such as close.
        order_records (array_like): A structured NumPy array of order records.
        log_records (array_like): A structured NumPy array of log records.
        init_cash (InitCashMode, float or array_like of float): Initial capital.
        cash_sharing (bool): Whether to share cash within the same group.
        call_seq (array_like of int): Sequence of calls per row and group.
        incl_unrealized (bool): Whether to include unrealized P&L in statistics.
        use_filled_close (bool): Whether to forward-backward fill NaN values in `close`.

            Doesn't affect simulation and only used for total profit and market value.

            See `Portfolio.fill_close`.

    !!! note
        Use class methods with `from_` prefix to build a portfolio.
        The `__init__` method is reserved for indexing purposes.

    !!! note
        This class is meant to be immutable. To change any attribute, use `Portfolio.copy`."""

    def __init__(self, wrapper, close, order_records, log_records, init_cash,
                 cash_sharing, call_seq, incl_unrealized=None, use_filled_close=None):
        Wrapping.__init__(
            self,
            wrapper,
            close=close,
            order_records=order_records,
            log_records=log_records,
            init_cash=init_cash,
            cash_sharing=cash_sharing,
            call_seq=call_seq,
            incl_unrealized=incl_unrealized,
            use_filled_close=use_filled_close
        )
        # Get defaults
        from vectorbt import settings

        if incl_unrealized is None:
            incl_unrealized = settings.portfolio['incl_unrealized']
        if use_filled_close is None:
            use_filled_close = settings.portfolio['use_filled_close']

        # Store passed arguments
        self._close = broadcast_to(close, wrapper.dummy(group_by=False))
        self._order_records = order_records
        self._log_records = log_records
        self._init_cash = init_cash
        self._cash_sharing = cash_sharing
        self._call_seq = call_seq
        self._incl_unrealized = incl_unrealized
        self._use_filled_close = use_filled_close

    def _indexing_func(self, pd_indexing_func, **kwargs):
        """Perform indexing on `Portfolio`."""
        new_wrapper, _, group_idxs, col_idxs = \
            self.wrapper._indexing_func_meta(pd_indexing_func, column_only_select=True, **kwargs)
        new_close = new_wrapper.wrap(to_2d(self.close, raw=True)[:, col_idxs], group_by=False)
        new_order_records = self.orders._col_idxs_records(col_idxs)
        new_log_records = self.logs._col_idxs_records(col_idxs)
        if isinstance(self._init_cash, int):
            new_init_cash = self._init_cash
        else:
            new_init_cash = to_1d(self._init_cash, raw=True)[group_idxs if self.cash_sharing else col_idxs]
        new_call_seq = self.call_seq.values[:, col_idxs]

        return self.copy(
            wrapper=new_wrapper,
            close=new_close,
            order_records=new_order_records,
            log_records=new_log_records,
            init_cash=new_init_cash,
            call_seq=new_call_seq
        )

    # ############# Class methods ############# #

    @classmethod
    def from_holding(cls, close, **kwargs):
        """Simulate portfolio from holding.

        Based on `Portfolio.from_signals`."""
        return cls.from_signals(close, True, False, accumulate=False, **kwargs)

    @classmethod
    def from_random_signals(cls, close, n=None, prob=None, entry_prob=None, exit_prob=None,
                            param_product=False, seed=None, run_kwargs=None, **kwargs):
        """Simulate portfolio from random entry and exit signals.

        Generates signals based either on the number of signals `n` or the probability
        of encountering a signal `prob`.

        If `n` is set, see `vectorbt.signals.generators.RAND`.
        If `prob` is set, see `vectorbt.signals.generators.RPROB`.

        Based on `Portfolio.from_signals`."""
        from vectorbt import settings

        if entry_prob is None:
            entry_prob = prob
        if exit_prob is None:
            exit_prob = prob
        if seed is None:
            seed = settings.portfolio['seed']
        if run_kwargs is None:
            run_kwargs = {}

        if n is not None and (entry_prob is not None or exit_prob is not None):
            raise ValueError("Either n or entry_prob and exit_prob should be set")
        if n is not None:
            rand = RAND.run(
                n=n,
                input_shape=close.shape,
                input_index=close.vbt.wrapper.index,
                input_columns=close.vbt.wrapper.columns,
                seed=seed,
                **run_kwargs
            )
            entries = rand.entries
            exits = rand.exits
        elif entry_prob is not None and exit_prob is not None:
            rprob = RPROB.run(
                entry_prob=entry_prob,
                exit_prob=exit_prob,
                param_product=param_product,
                input_shape=close.shape,
                input_index=close.vbt.wrapper.index,
                input_columns=close.vbt.wrapper.columns,
                seed=seed,
                **run_kwargs
            )
            entries = rprob.entries
            exits = rprob.exits
        else:
            raise ValueError("At least n or entry_prob and exit_prob should be set")

        return cls.from_signals(close, entries, exits, seed=seed, **kwargs)

    @classmethod
    def from_signals(cls, close, entries, exits, size=None, size_type=None, direction=None, price=None,
                     fees=None, fixed_fees=None, slippage=None, min_size=None, max_size=None,
                     reject_prob=None, allow_partial=None, raise_reject=None, accumulate=None, log=None,
                     conflict_mode=None, close_first=None, val_price=None, init_cash=None, cash_sharing=None,
                     call_seq=None, max_orders=None, max_logs=None, seed=None, group_by=None,
                     broadcast_kwargs=None, wrapper_kwargs=None, freq=None, **kwargs):
        """Simulate portfolio from entry and exit signals.

        Starting with initial cash `init_cash`, for each signal in `entries`, enters a long/short position
        by buying/selling `size` of shares. For each signal in `exits`, closes the position by
        selling/buying shares. Depending upon accumulation, each entry signal may increase
        the position and each exit signal may decrease the position. When both entry and exit signals
        are present, ignores them by default. When grouping is enabled with `group_by`, will compute
        the performance of the entire group. When `cash_sharing` is enabled, will share the cash among
        all columns in the group.

        Args:
            close (array_like): Reference price, such as close.
                Will broadcast.

                Will be used for calculating unrealized P&L and portfolio value.
            entries (array_like of bool): Boolean array of entry signals.
                Will broadcast.

                Becomes a long signal if `direction` is `all` or `longonly`, otherwise short.
            exits (array_like of bool): Boolean array of exit signals.
                Will broadcast.

                Becomes a short signal if `direction` is `all` or `longonly`, otherwise long.
            size (float or array_like): Size to order.
                Will broadcast.

                * Set to any number to buy/sell some fixed amount of shares.
                    Longs are limited by cash in the account, while shorts are unlimited.
                * Set to `np.inf` to buy shares for all cash, or `-np.inf` to sell shares for
                    initial margin of 100%. If `direction` is not `all`, `-np.inf` will close the position.
                * Set to `np.nan` or 0 to skip.

                !!! note
                    Sign will be ignored.
            size_type (SizeType or array_like): See `vectorbt.portfolio.enums.SizeType`.
                Will broadcast.

                Only `SizeType.Shares` and `SizeType.Percent` are supported.
                Other modes such as target percentage are not compatible with signals since
                their logic may contradict the direction of the signal.

                !!! note
                    `SizeType.Percent` does not support position reversal. Switch to a single
                    direction or use `close_first`.

                See warning on `size_type` in `Portfolio.from_orders`.
            direction (Direction or array_like): See `vectorbt.portfolio.enums.Direction`.
                Will broadcast.
            price (array_like of float): Order price.
                Defaults to `close`. Will broadcast.
            fees (float or array_like): Fees in percentage of the order value.
                Will broadcast. Note that 0.01 = 1%.
            fixed_fees (float or array_like): Fixed amount of fees to pay per order.
                Will broadcast.
            slippage (float or array_like): Slippage in percentage of price.
                Will broadcast. Note that 0.01 = 1%.
            min_size (float or array_like): Minimum size for an order to be accepted.
                Will broadcast.
            max_size (float or array_like): Maximum size for an order.
                Will broadcast.

                Will be partially filled if exceeded. You might not be able to properly close
                the position if accumulation is enabled and `max_size` is too low.
            reject_prob (float or array_like): Order rejection probability.
                Will broadcast.
            allow_partial (bool or array_like): Whether to allow partial fills.
                Will broadcast.

                Does not apply when size is `np.inf`.
            raise_reject (bool or array_like): Whether to raise an exception if order gets rejected.
                Will broadcast.
            log (bool or array_like): Whether to log orders.
                Will broadcast.
            accumulate (bool or array_like): Whether to accumulate signals.
                Will broadcast.

                Behaves similarly to `Portfolio.from_orders`.
            conflict_mode (ConflictMode or array_like): See `vectorbt.portfolio.enums.ConflictMode`.
                Will broadcast.
            close_first (bool or array_like): Whether to close the position first before reversal.
                Will broadcast.

                Otherwise reverses the position with a single order and within the same tick.
                Takes only effect under `Direction.All`. Requires a second signal to enter
                the opposite position. This allows to define parameters such as `fixed_fees` for long
                and short positions separately.
            val_price (array_like of float): Asset valuation price.
                Defaults to `price` if set, otherwise to previous `close`.

                See `val_price` in `Portfolio.from_orders`.
            init_cash (InitCashMode, float or array_like of float): Initial capital.

                See `init_cash` in `Portfolio.from_order_func`.
            cash_sharing (bool): Whether to share cash within the same group.

                See `cash_sharing` in `Portfolio.from_orders`.
            call_seq (CallSeqType or array_like of int): Default sequence of calls per row and group.

                See `call_seq` in `Portfolio.from_orders`.
            max_orders (int): Size of the order records array.
                Defaults to the number of elements in the broadcasted shape.

                Set to a lower number if you run out of memory.
            max_logs (int): Size of the log records array.
                Defaults to the number of elements in the broadcasted shape if any of the `log` is True,
                otherwise to 1.

                Set to a lower number if you run out of memory.
            seed (int): Seed to be set for both `call_seq` and at the beginning of the simulation.
            group_by (any): Group columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            broadcast_kwargs (dict): Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`.
            wrapper_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper`.
            freq (any): Index frequency in case `close.index` is not datetime-like.
            **kwargs: Keyword arguments passed to the `__init__` method.

        All broadcastable arguments will be broadcast using `vectorbt.base.reshape_fns.broadcast`
        but keep original shape to utilize flexible indexing and to save memory.

        For defaults, see `vectorbt.settings.portfolio`.

        !!! hint
            If you generated signals using close price, don't forget to shift your signals by one tick
            forward, for example, with `signals.vbt.fshift(1)`. In general, make sure to use a price
            that comes after the signal.

        Also see notes and hints for `Portfolio.from_orders`.

        ## Example

        Some of the ways of how signals are interpreted:

        ```python-repl
        >>> import pandas as pd
        >>> import vectorbt as vbt

        >>> close = pd.Series([1, 2, 3, 4, 5])
        >>> entries = pd.Series([True, True, True, False, False])
        >>> exits = pd.Series([False, False, True, True, True])

        >>> # Entry opens long, exit closes long
        >>> portfolio = vbt.Portfolio.from_signals(
        ...     close, entries, exits, size=1., direction='longonly')
        >>> portfolio.share_flow()
        0    1.0
        1    0.0
        2    0.0
        3   -1.0
        4    0.0
        dtype: float64

        >>> # Entry opens short, exit closes short
        >>> portfolio = vbt.Portfolio.from_signals(
        ...     close, entries, exits, size=1., direction='shortonly')
        >>> portfolio.share_flow()
        0   -1.0
        1    0.0
        2    0.0
        3    1.0
        4    0.0
        dtype: float64

        >>> # Entry opens long and closes short, exit closes long and opens short
        >>> # Reversal within one tick
        >>> portfolio = vbt.Portfolio.from_signals(
        ...     close, entries, exits, size=1., direction='all')
        >>> portfolio.share_flow()
        0    1.0
        1    0.0
        2    0.0
        3   -2.0
        4    0.0
        dtype: float64

        >>> # Reversal within two ticks
        >>> # First signal closes position, second signal opens the opposite one
        >>> portfolio = vbt.Portfolio.from_signals(
        ...     close, entries, exits, size=1., direction='all',
        ...     close_first=True)
        >>> portfolio.share_flow()
        0    1.0
        1    0.0
        2    0.0
        3   -1.0
        4   -1.0
        dtype: float64

        >>> # If entry and exit, chooses exit
        >>> portfolio = vbt.Portfolio.from_signals(
        ...     close, entries, exits, size=1., direction='all',
        ...     close_first=True, conflict_mode='exit')
        >>> portfolio.share_flow()
        0    1.0
        1    0.0
        2   -1.0
        3   -1.0
        4    0.0
        dtype: float64

        >>> # Entry means long order, exit means short order
        >>> # Acts similar to `from_orders`
        >>> portfolio = vbt.Portfolio.from_signals(
        ...     close, entries, exits, size=1., direction='all',
        ...     accumulate=True)
        >>> portfolio.share_flow()
        0    1.0
        1    1.0
        2    0.0
        3   -1.0
        4   -1.0
        dtype: float64

        >>> # Testing multiple parameters (via broadcasting)
        >>> from vectorbt.portfolio.enums import Direction

        >>> portfolio = vbt.Portfolio.from_signals(
        ...     close, entries, exits, direction=[list(Direction)],
        ...     broadcast_kwargs=dict(columns_from=Direction._fields))
        >>> portfolio.share_flow()
            Long  Short    All
        0  100.0 -100.0  100.0
        1    0.0    0.0    0.0
        2    0.0    0.0    0.0
        3 -100.0   50.0 -200.0
        4    0.0    0.0    0.0
        ```
        """
        # Get defaults
        from vectorbt import settings

        if size is None:
            size = settings.portfolio['size']
        if size_type is None:
            size_type = settings.portfolio['signal_size_type']
        size_type = convert_str_enum_value(SizeType, size_type)
        if direction is None:
            direction = settings.portfolio['signal_direction']
        direction = convert_str_enum_value(Direction, direction)
        if price is None:
            price = close
        if fees is None:
            fees = settings.portfolio['fees']
        if fixed_fees is None:
            fixed_fees = settings.portfolio['fixed_fees']
        if slippage is None:
            slippage = settings.portfolio['slippage']
        if min_size is None:
            min_size = settings.portfolio['min_size']
        if max_size is None:
            max_size = settings.portfolio['max_size']
        if reject_prob is None:
            reject_prob = settings.portfolio['reject_prob']
        if allow_partial is None:
            allow_partial = settings.portfolio['allow_partial']
        if raise_reject is None:
            raise_reject = settings.portfolio['raise_reject']
        if log is None:
            log = settings.portfolio['log']
        if accumulate is None:
            accumulate = settings.portfolio['accumulate']
        if conflict_mode is None:
            conflict_mode = settings.portfolio['conflict_mode']
        conflict_mode = convert_str_enum_value(ConflictMode, conflict_mode)
        if close_first is None:
            close_first = settings.portfolio['close_first']
        if val_price is None:
            if price is None:
                if checks.is_pandas(close):
                    val_price = close.vbt.fshift(1)
                else:
                    val_price = np.require(close, dtype=np.float_)
                    val_price = np.roll(val_price, 1, axis=0)
                    val_price[0] = np.nan
            else:
                val_price = price
        if init_cash is None:
            init_cash = settings.portfolio['init_cash']
        init_cash = convert_str_enum_value(InitCashMode, init_cash)
        if isinstance(init_cash, int) and init_cash in InitCashMode:
            init_cash_mode = init_cash
            init_cash = np.inf
        else:
            init_cash_mode = None
        if cash_sharing is None:
            cash_sharing = settings.portfolio['cash_sharing']
        if call_seq is None:
            call_seq = settings.portfolio['call_seq']
        call_seq = convert_str_enum_value(CallSeqType, call_seq)
        auto_call_seq = False
        if isinstance(call_seq, int):
            if call_seq == CallSeqType.Auto:
                call_seq = CallSeqType.Default
                auto_call_seq = True
        if seed is None:
            seed = settings.portfolio['seed']
        if seed is not None:
            set_seed(seed)
        if freq is None:
            freq = settings.portfolio['freq']
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        if wrapper_kwargs is None:
            wrapper_kwargs = {}
        if not wrapper_kwargs.get('group_select', True) and cash_sharing:
            raise ValueError("group_select cannot be disabled if cash_sharing=True")

        # Broadcast inputs
        # Only close is broadcast, others can remain unchanged thanks to flexible indexing
        broadcastable_args = (
            close,
            entries,
            exits,
            size,
            size_type,
            direction,
            price,
            fees,
            fixed_fees,
            slippage,
            min_size,
            max_size,
            reject_prob,
            allow_partial,
            raise_reject,
            accumulate,
            log,
            conflict_mode,
            close_first,
            val_price
        )
        keep_raw = [False] + [True] * (len(broadcastable_args) - 1)
        broadcast_kwargs = merge_dicts(dict(require_kwargs=dict(requirements='W')), broadcast_kwargs)
        broadcasted_args = broadcast(*broadcastable_args, **broadcast_kwargs, keep_raw=keep_raw)
        close = broadcasted_args[0]
        if not checks.is_pandas(close):
            close = pd.Series(close) if close.ndim == 1 else pd.DataFrame(close)
        target_shape_2d = (close.shape[0], close.shape[1] if close.ndim > 1 else 1)
        wrapper = ArrayWrapper.from_obj(close, freq=freq, group_by=group_by, **wrapper_kwargs)
        cs_group_lens = wrapper.grouper.get_group_lens(group_by=None if cash_sharing else False)
        init_cash = np.require(np.broadcast_to(init_cash, (len(cs_group_lens),)), dtype=np.float_)
        group_lens = wrapper.grouper.get_group_lens(group_by=group_by)
        if checks.is_any_array(call_seq):
            call_seq = nb.require_call_seq(broadcast(call_seq, to_shape=target_shape_2d, to_pd=False))
        else:
            call_seq = nb.build_call_seq(target_shape_2d, group_lens, call_seq_type=call_seq)
        if max_orders is None:
            max_orders = target_shape_2d[0] * target_shape_2d[1]
        if max_logs is None:
            max_logs = target_shape_2d[0] * target_shape_2d[1]
        if not np.any(log):
            max_logs = 1

        # Perform calculation
        order_records, log_records = nb.simulate_from_signals_nb(
            target_shape_2d,
            cs_group_lens,  # group only if cash sharing is enabled to speed up
            init_cash,
            call_seq,
            auto_call_seq,
            *broadcasted_args[1:],
            max_orders,
            max_logs,
            close.ndim == 2
        )

        # Create an instance
        return cls(
            wrapper,
            close,
            order_records,
            log_records,
            init_cash if init_cash_mode is None else init_cash_mode,
            cash_sharing,
            call_seq,
            **kwargs
        )

    @classmethod
    def from_orders(cls, close, size, size_type=None, direction=None, price=None, fees=None,
                    fixed_fees=None, slippage=None, min_size=None, max_size=None, reject_prob=None,
                    allow_partial=None, raise_reject=None, log=None, val_price=None, init_cash=None,
                    cash_sharing=None, call_seq=None, max_orders=None, max_logs=None, seed=None,
                    group_by=None, broadcast_kwargs=None, wrapper_kwargs=None, freq=None, **kwargs):
        """Simulate portfolio from orders.

        Starting with initial cash `init_cash`, orders the number of shares specified in `size`
        for `price`.

        Args:
            close (array_like): Reference price, such as close.
                Will broadcast.

                Will be used for calculating unrealized P&L and portfolio value.
            size (float or array_like): Size to order.
                Will broadcast.

                Behavior depends upon `size_type` and `direction`. For `SizeType.Shares`:

                * Set to any number to buy/sell some fixed amount of shares.
                    Longs are limited by cash in the account, while shorts are unlimited.
                * Set to `np.inf` to buy shares for all cash, or `-np.inf` to sell shares for
                    initial margin of 100%. If `direction` is not `all`, `-np.inf` will close the position.
                * Set to `np.nan` or 0 to skip.

                For any target size:

                * Set to any number to buy/sell amount of shares relative to current holdings or value.
                * Set to 0 to close the current position.
                * Set to `np.nan` to skip.
            size_type (SizeType or array_like): See `vectorbt.portfolio.enums.SizeType`.
                Will broadcast.

                !!! note
                    `SizeType.Percent` does not support position reversal. Switch to a single direction.

                !!! warning
                    Be cautious using `SizeType.Percent` with `call_seq` set to 'auto'.
                    To execute sell orders before buy orders, the value of each order in the group
                    needs to be approximated in advance. But since `SizeType.Percent` depends
                    upon cash balance, which cannot be calculated in advance, the latest cash balance
                    is used. This can yield wrong call sequence for buy orders.
            direction (Direction or array_like): See `vectorbt.portfolio.enums.Direction`.
                Will broadcast.
            price (array_like of float): Order price.
                Defaults to `close`. Will broadcast.
            fees (float or array_like): Fees in percentage of the order value.
                Will broadcast. Note that 0.01 = 1%.
            fixed_fees (float or array_like): Fixed amount of fees to pay per order.
                Will broadcast.
            slippage (float or array_like): Slippage in percentage of price.
                Will broadcast. Note that 0.01 = 1%.
            min_size (float or array_like): Minimum size for an order to be accepted.
                Will broadcast.
            max_size (float or array_like): Maximum size for an order.
                Will broadcast.

                Will be partially filled if exceeded.
            reject_prob (float or array_like): Order rejection probability.
                Will broadcast.
            allow_partial (bool or array_like): Whether to allow partial fills.
                Will broadcast.

                Does not apply when size is `np.inf`.
            raise_reject (bool or array_like): Whether to raise an exception if order gets rejected.
                Will broadcast.
            log (bool or array_like): Whether to log orders.
                Will broadcast.
            val_price (array_like of float): Asset valuation price.
                Defaults to `price`. Will broadcast.

                Used at the time of decision making to calculate value of each asset in the group,
                for example, to convert target value into target shares.

                !!! note
                    Make sure to use timestamp for `val_price` that comes before timestamps of
                    all orders in the group with cash sharing (previous `close` for example),
                    otherwise you're cheating yourself.
            init_cash (InitCashMode, float or array_like of float): Initial capital.

                See `init_cash` in `Portfolio.from_order_func`.
            cash_sharing (bool): Whether to share cash within the same group.

                !!! warning
                    Introduces cross-asset dependencies.

                    This method presumes that in a group of assets that share the same capital all
                    orders will be executed within the same tick and retain their price regardless
                    of their position in the queue, even though they depend upon each other and thus
                    cannot be executed in parallel.
            call_seq (CallSeqType or array_like of int): Default sequence of calls per row and group.

                Each value in this sequence should indicate the position of column in the group to
                call next. Processing of `call_seq` goes always from left to right.
                For example, `[2, 0, 1]` would first call column 'c', then 'a', and finally 'b'.

                * Use `vectorbt.portfolio.enums.CallSeqType` to select a sequence type.
                * Set to array to specify custom sequence. Will not broadcast.

                If `CallSeqType.Auto` selected, rearranges calls dynamically based on order value.
                Calculates value of all orders per row and group, and sorts them by this value.
                Sell orders will be executed first to release funds for buy orders.

                !!! warning
                    `CallSeqType.Auto` should be used with caution:

                    * It not only presumes that order prices are known beforehand, but also that
                        orders can be executed in arbitrary order and still retain their price.
                        In reality, this is hardly the case: after processing one asset, some time
                        has passed and the price for other assets might have already changed.
                    * Even if you're able to specify a slippage large enough to compensate for
                        this behavior, slippage itself should depend upon execution order.
                        This method doesn't let you do that.
                    * If one order is rejected, it still may execute next orders and possibly
                        leave them without required funds.

                    For more control, use `Portfolio.from_order_func`.
            max_orders (int): Size of the order records array.
                Defaults to the number of elements in the broadcasted shape.

                Set to a lower number if you run out of memory.
            max_logs (int): Size of the log records array.
                Defaults to the number of elements in the broadcasted shape if any of the `log` is True,
                otherwise to 1.

                Set to a lower number if you run out of memory.
            seed (int): Seed to be set for both `call_seq` and at the beginning of the simulation.
            group_by (any): Group columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            broadcast_kwargs (dict): Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`.
            wrapper_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper`.
            freq (any): Index frequency in case `close.index` is not datetime-like.
            **kwargs: Keyword arguments passed to the `__init__` method.

        All broadcastable arguments will be broadcast using `vectorbt.base.reshape_fns.broadcast`
        but keep original shape to utilize flexible indexing and to save memory.

        For defaults, see `vectorbt.settings.portfolio`.

        !!! note
            When `call_seq` is not `CallSeqType.Auto`, at each timestamp, processing of the assets in
            a group goes strictly in order defined in `call_seq`. This order can't be changed dynamically.

            This has one big implication for this particular method: the last asset in the call stack
            cannot be processed until other assets are processed. This is the reason why rebalancing
            cannot work properly in this setting: one has to specify percentages for all assets beforehand
            and then tweak the processing order to sell to-be-sold assets first in order to release funds
            for to-be-bought assets. This can be automatically done by using `CallSeqType.Auto`.

        !!! hint
            All broadcastable arguments can be set per frame, series, row, column, or element.

        ## Example

        Buy 10 shares each tick:
        ```python-repl
        >>> import pandas as pd
        >>> import vectorbt as vbt

        >>> close = pd.Series([1, 2, 3, 4, 5])
        >>> portfolio = vbt.Portfolio.from_orders(close, 10)

        >>> portfolio.shares()
        0    10.0
        1    20.0
        2    30.0
        3    40.0
        4    40.0
        dtype: float64
        >>> portfolio.cash()
        0    90.0
        1    70.0
        2    40.0
        3     0.0
        4     0.0
        dtype: float64
        ```

        Reverse each position by first closing it:
        ```python-repl
        >>> size = [1, 0, -1, 0, 1]
        >>> portfolio = vbt.Portfolio.from_orders(close, size, size_type='targetpercent')

        >>> portfolio.shares()
        0    100.000000
        1      0.000000
        2    -66.666667
        3      0.000000
        4     26.666667
        dtype: float64
        >>> portfolio.cash()
        0      0.000000
        1    200.000000
        2    400.000000
        3    133.333333
        4      0.000000
        dtype: float64
        ```

        Equal-weighted portfolio as in `vectorbt.portfolio.nb.simulate_nb` example:
        It's more compact but has less control over execution:

        ```python-repl
        >>> import numpy as np

        >>> np.random.seed(42)
        >>> close = pd.DataFrame(np.random.uniform(1, 10, size=(5, 3)))
        >>> size = pd.Series(np.full(5, 1/3))  # each column 33.3%
        >>> size[1::2] = np.nan  # skip every second tick

        >>> portfolio = vbt.Portfolio.from_orders(
        ...     close,  # acts both as reference and order price here
        ...     size,
        ...     size_type='targetpercent',
        ...     call_seq='auto',  # first sell then buy
        ...     group_by=True,  # one group
        ...     cash_sharing=True,  # assets share the same cash
        ...     fees=0.001, fixed_fees=1., slippage=0.001  # costs
        ... )

        >>> portfolio.holding_value(group_by=False).vbt.plot()
        ```

        ![](/vectorbt/docs/img/simulate_nb.png)
        """
        # Get defaults
        from vectorbt import settings

        if size is None:
            size = settings.portfolio['size']
        if size_type is None:
            size_type = settings.portfolio['size_type']
        size_type = convert_str_enum_value(SizeType, size_type)
        if direction is None:
            direction = settings.portfolio['order_direction']
        direction = convert_str_enum_value(Direction, direction)
        if price is None:
            price = close
        if fees is None:
            fees = settings.portfolio['fees']
        if fixed_fees is None:
            fixed_fees = settings.portfolio['fixed_fees']
        if slippage is None:
            slippage = settings.portfolio['slippage']
        if min_size is None:
            min_size = settings.portfolio['min_size']
        if max_size is None:
            max_size = settings.portfolio['max_size']
        if reject_prob is None:
            reject_prob = settings.portfolio['reject_prob']
        if allow_partial is None:
            allow_partial = settings.portfolio['allow_partial']
        if raise_reject is None:
            raise_reject = settings.portfolio['raise_reject']
        if log is None:
            log = settings.portfolio['log']
        if val_price is None:
            val_price = price
        if init_cash is None:
            init_cash = settings.portfolio['init_cash']
        init_cash = convert_str_enum_value(InitCashMode, init_cash)
        if isinstance(init_cash, int) and init_cash in InitCashMode:
            init_cash_mode = init_cash
            init_cash = np.inf
        else:
            init_cash_mode = None
        if cash_sharing is None:
            cash_sharing = settings.portfolio['cash_sharing']
        if call_seq is None:
            call_seq = settings.portfolio['call_seq']
        call_seq = convert_str_enum_value(CallSeqType, call_seq)
        auto_call_seq = False
        if isinstance(call_seq, int):
            if call_seq == CallSeqType.Auto:
                call_seq = CallSeqType.Default
                auto_call_seq = True
        if seed is None:
            seed = settings.portfolio['seed']
        if seed is not None:
            set_seed(seed)
        if freq is None:
            freq = settings.portfolio['freq']
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        if wrapper_kwargs is None:
            wrapper_kwargs = {}
        if not wrapper_kwargs.get('group_select', True) and cash_sharing:
            raise ValueError("group_select cannot be disabled if cash_sharing=True")

        # Broadcast inputs
        # Only close is broadcast, others can remain unchanged thanks to flexible indexing
        broadcastable_args = (
            close,
            size,
            size_type,
            direction,
            price,
            fees,
            fixed_fees,
            slippage,
            min_size,
            max_size,
            reject_prob,
            allow_partial,
            raise_reject,
            log,
            val_price
        )
        keep_raw = [False] + [True] * (len(broadcastable_args) - 1)
        broadcast_kwargs = merge_dicts(dict(require_kwargs=dict(requirements='W')), broadcast_kwargs)
        broadcasted_args = broadcast(*broadcastable_args, **broadcast_kwargs, keep_raw=keep_raw)
        close = broadcasted_args[0]
        if not checks.is_pandas(close):
            close = pd.Series(close) if close.ndim == 1 else pd.DataFrame(close)
        target_shape_2d = (close.shape[0], close.shape[1] if close.ndim > 1 else 1)
        wrapper = ArrayWrapper.from_obj(close, freq=freq, group_by=group_by, **wrapper_kwargs)
        cs_group_lens = wrapper.grouper.get_group_lens(group_by=None if cash_sharing else False)
        init_cash = np.require(np.broadcast_to(init_cash, (len(cs_group_lens),)), dtype=np.float_)
        group_lens = wrapper.grouper.get_group_lens(group_by=group_by)
        if checks.is_any_array(call_seq):
            call_seq = nb.require_call_seq(broadcast(call_seq, to_shape=target_shape_2d, to_pd=False))
        else:
            call_seq = nb.build_call_seq(target_shape_2d, group_lens, call_seq_type=call_seq)
        if max_orders is None:
            max_orders = target_shape_2d[0] * target_shape_2d[1]
        if max_logs is None:
            max_logs = target_shape_2d[0] * target_shape_2d[1]
        if not np.any(log):
            max_logs = 1

        # Perform calculation
        order_records, log_records = nb.simulate_from_orders_nb(
            target_shape_2d,
            cs_group_lens,  # group only if cash sharing is enabled to speed up
            init_cash,
            call_seq,
            auto_call_seq,
            *broadcasted_args[1:],
            max_orders,
            max_logs,
            close.ndim == 2
        )

        # Create an instance
        return cls(
            wrapper,
            close,
            order_records,
            log_records,
            init_cash if init_cash_mode is None else init_cash_mode,
            cash_sharing,
            call_seq,
            **kwargs
        )

    @classmethod
    def from_order_func(cls, close, order_func_nb, *order_args, target_shape=None, keys=None,
                        init_cash=None, cash_sharing=None, call_seq=None, active_mask=None,
                        prep_func_nb=None, prep_args=None, group_prep_func_nb=None, group_prep_args=None,
                        row_prep_func_nb=None, row_prep_args=None, segment_prep_func_nb=None,
                        segment_prep_args=None, row_wise=None, max_orders=None, max_logs=None,
                        seed=None, group_by=None, broadcast_kwargs=None, wrapper_kwargs=None, freq=None, **kwargs):
        """Build portfolio from a custom order function.

        For details, see `vectorbt.portfolio.nb.simulate_nb`.

        if `row_wise` is True, also see `vectorbt.portfolio.nb.simulate_row_wise_nb`.

        Args:
            close (array_like): Reference price, such as close.
                Will broadcast to `target_shape`.

                Will be used for calculating unrealized P&L and portfolio value.
            order_func_nb (callable): Order generation function.
            *order_args: Arguments passed to `order_func_nb`.
            target_shape (tuple): Target shape to iterate over. Defaults to `close.shape`.
            keys (sequence): Outermost column level.

                Each element should correspond to one iteration over columns in `close`.
                Should be set only if `target_shape` is bigger than `close.shape`.
            init_cash (InitCashMode, float or array_like of float): Initial capital.

                By default, will broadcast to the number of columns.
                If cash sharing is enabled, will broadcast to the number of groups.
                See `vectorbt.portfolio.enums.InitCashMode` to find optimal initial cash.

                !!! note
                    Mode `InitCashMode.AutoAlign` is applied after the portfolio is initialized
                    to set the same initial cash for all columns/groups. Changing grouping
                    will change the initial cash, so be aware when indexing.
            cash_sharing (bool): Whether to share cash within the same group.

                !!! warning
                    Introduces cross-asset dependencies.
            call_seq (CallSeqType or array_like of int): Default sequence of calls per row and group.

                * Use `vectorbt.portfolio.enums.CallSeqType` to select a sequence type.
                * Set to array to specify custom sequence. Will not broadcast.

                !!! note
                    CallSeqType.Auto should be implemented manually.
                    Use `auto_call_seq_ctx_nb` in `segment_prep_func_nb`.
            active_mask (int or array_like of bool): Mask of whether a particular segment should be executed.

                Supplying an integer will activate every n-th row (just for convenience).
                Supplying a boolean will broadcast to the number of rows and groups.
            prep_func_nb (callable): Simulation preparation function.
            prep_args (tuple): Packed arguments passed to `prep_func_nb`.

                Defaults to `()`.
            group_prep_func_nb (callable): Group preparation function.

                Called only if `row_wise` is False.
            group_prep_args (tuple): Packed arguments passed to `group_prep_func_nb`.

                Defaults to `()`.
            row_prep_func_nb (callable): Row preparation function.

                Called only if `row_wise` is True.
            row_prep_args (tuple): Packed arguments passed to `row_prep_func_nb`.

                Defaults to `()`.
            segment_prep_func_nb (callable): Segment preparation function.
            segment_prep_args (tuple): Packed arguments passed to `segment_prep_func_nb`.

                Defaults to `()`.
            row_wise (bool): Whether to iterate over rows rather than columns/groups.

                See `vectorbt.portfolio.nb.simulate_row_wise_nb`.
            max_orders (int): Size of the order records array.
                Defaults to the number of elements in the broadcasted shape.

                Set to a lower number if you run out of memory.
            max_logs (int): Size of the log records array.
                Defaults to the number of elements in the broadcasted shape.

                Set to a lower number if you run out of memory.
            seed (int): Seed to be set for both `call_seq` and at the beginning of the simulation.
            group_by (any): Group columns. See `vectorbt.base.column_grouper.ColumnGrouper`.
            broadcast_kwargs (dict): Keyword arguments passed to `vectorbt.base.reshape_fns.broadcast`.
            wrapper_kwargs (dict): Keyword arguments passed to `vectorbt.base.array_wrapper.ArrayWrapper`.
            freq (any): Index frequency in case `close.index` is not datetime-like.
            **kwargs: Keyword arguments passed to the `__init__` method.

        For defaults, see `vectorbt.settings.portfolio`.

        !!! note
            All passed functions should be Numba-compiled.

            Objects passed as arguments to both functions will not broadcast to `target_shape`
            as their purpose is unknown. You should broadcast manually or use flexible indexing.

            Also see notes on `Portfolio.from_orders`.

        !!! note
            In contrast to other methods, the valuation price is previous `close`
            instead of order price, since the price of an order is unknown before call.
            You can still set valuation price explicitly in `segment_prep_func_nb`.

        ## Example

        Buy 10 shares each tick:
        ```python-repl
        >>> import pandas as pd
        >>> from numba import njit
        >>> import vectorbt as vbt
        >>> from vectorbt.portfolio.nb import create_order_nb

        >>> @njit
        ... def order_func_nb(oc, size):
        ...     return create_order_nb(size=size, price=oc.close[oc.i, oc.col])

        >>> close = pd.Series([1, 2, 3, 4, 5])
        >>> portfolio = vbt.Portfolio.from_order_func(close, order_func_nb, 10)

        >>> portfolio.shares()
        0    10.0
        1    20.0
        2    30.0
        3    40.0
        4    40.0
        dtype: float64
        >>> portfolio.cash()
        0    90.0
        1    70.0
        2    40.0
        3     0.0
        4     0.0
        dtype: float64
        ```

        Reverse each position by first closing it. Keep state of last position to determine
        which position to open next (just as an example, there are easier ways to do this):
        ```python-repl
        >>> import numpy as np

        >>> @njit
        ... def group_prep_func_nb(gc):
        ...     last_pos_state = np.array([-1])
        ...     return (last_pos_state,)

        >>> @njit
        ... def order_func_nb(oc, last_pos_state):
        ...     if oc.shares_now > 0:
        ...         size = -oc.shares_now  # close long
        ...     elif oc.shares_now < 0:
        ...         size = -oc.shares_now  # close short
        ...     else:
        ...         if last_pos_state[0] == 1:
        ...             size = -np.inf  # open short
        ...             last_pos_state[0] = -1
        ...         else:
        ...             size = np.inf  # open long
        ...             last_pos_state[0] = 1
        ...
        ...     return create_order_nb(size=size, price=oc.close[oc.i, oc.col])

        >>> portfolio = vbt.Portfolio.from_order_func(
        ...     close, order_func_nb, group_prep_func_nb=group_prep_func_nb)

        >>> portfolio.shares()
        0    100.0
        1      0.0
        2   -100.0
        3      0.0
        4     20.0
        dtype: float64
        >>> portfolio.cash()
        0      0.0
        1    200.0
        2    500.0
        3    100.0
        4      0.0
        dtype: float64
        ```

        Equal-weighted portfolio as in `vectorbt.portfolio.nb.simulate_nb` example:
        ```python-repl
        >>> from vectorbt.portfolio.nb import auto_call_seq_ctx_nb
        >>> from vectorbt.portfolio.enums import SizeType, Direction

        >>> @njit
        ... def group_prep_func_nb(gc):
        ...     '''Define empty arrays for each group.'''
        ...     size = np.empty(gc.group_len, dtype=np.float_)
        ...     size_type = np.empty(gc.group_len, dtype=np.int_)
        ...     direction = np.empty(gc.group_len, dtype=np.int_)
        ...     temp_float_arr = np.empty(gc.group_len, dtype=np.float_)
        ...     return size, size_type, direction, temp_float_arr

        >>> @njit
        ... def segment_prep_func_nb(sc, size, size_type, direction, temp_float_arr):
        ...     '''Perform rebalancing at each segment.'''
        ...     for k in range(sc.group_len):
        ...         col = sc.from_col + k
        ...         size[k] = 1 / sc.group_len
        ...         size_type[k] = SizeType.TargetPercent
        ...         direction[k] = Direction.LongOnly
        ...         sc.last_val_price[col] = sc.close[sc.i, col]
        ...     auto_call_seq_ctx_nb(sc, size, size_type, direction, temp_float_arr)
        ...     return size, size_type, direction

        >>> @njit
        ... def order_func_nb(oc, size, size_type, direction, fees, fixed_fees, slippage):
        ...     '''Place an order.'''
        ...     col_i = oc.call_seq_now[oc.call_idx]
        ...     return create_order_nb(
        ...         size=size[col_i],
        ...         size_type=size_type[col_i],
        ...         price=oc.close[oc.i, oc.col],
        ...         fees=fees, fixed_fees=fixed_fees, slippage=slippage,
        ...         direction=direction[col_i]
        ...     )

        >>> np.random.seed(42)
        >>> close = np.random.uniform(1, 10, size=(5, 3))
        >>> fees = 0.001
        >>> fixed_fees = 1.
        >>> slippage = 0.001

        >>> portfolio = vbt.Portfolio.from_order_func(
        ...     close,  # acts both as reference and order price here
        ...     order_func_nb, fees, fixed_fees, slippage,  # order_args as *args
        ...     active_mask=2,  # rebalance every second tick
        ...     group_prep_func_nb=group_prep_func_nb,
        ...     segment_prep_func_nb=segment_prep_func_nb,
        ...     cash_sharing=True, group_by=True,  # one group with cash sharing
        ... )

        >>> portfolio.holding_value(group_by=False).vbt.plot()
        ```

        ![](/vectorbt/docs/img/simulate_nb.png)
        """
        # Get defaults
        from vectorbt import settings

        if not checks.is_pandas(close):
            if not checks.is_any_array(close):
                close = np.asarray(close)
            close = pd.Series(close) if close.ndim == 1 else pd.DataFrame(close)
        if target_shape is None:
            target_shape = close.shape
        if init_cash is None:
            init_cash = settings.portfolio['init_cash']
        init_cash = convert_str_enum_value(InitCashMode, init_cash)
        if isinstance(init_cash, int) and init_cash in InitCashMode:
            init_cash_mode = init_cash
            init_cash = np.inf
        else:
            init_cash_mode = None
        if cash_sharing is None:
            cash_sharing = settings.portfolio['cash_sharing']
        if call_seq is None:
            call_seq = settings.portfolio['call_seq']
        call_seq = convert_str_enum_value(CallSeqType, call_seq)
        if isinstance(call_seq, int):
            if call_seq == CallSeqType.Auto:
                raise ValueError("CallSeqType.Auto should be implemented manually. "
                                 "Use auto_call_seq_ctx_nb in segment_prep_func_nb.")
        if active_mask is None:
            active_mask = True
        if row_wise is None:
            row_wise = settings.portfolio['row_wise']
        if seed is None:
            seed = settings.portfolio['seed']
        if seed is not None:
            set_seed(seed)
        if freq is None:
            freq = settings.portfolio['freq']
        if broadcast_kwargs is None:
            broadcast_kwargs = {}
        require_kwargs = dict(require_kwargs=dict(requirements='W'))
        broadcast_kwargs = merge_dicts(require_kwargs, broadcast_kwargs)
        if wrapper_kwargs is None:
            wrapper_kwargs = {}
        if not wrapper_kwargs.get('group_select', True) and cash_sharing:
            raise ValueError("group_select cannot be disabled if cash_sharing=True")

        # Broadcast inputs
        target_shape_2d = (target_shape[0], target_shape[1] if len(target_shape) > 1 else 1)
        if close.shape != target_shape:
            if len(close.vbt.wrapper.columns) <= target_shape_2d[1]:
                if target_shape_2d[1] % len(close.vbt.wrapper.columns) != 0:
                    raise ValueError("Cannot broadcast close to target_shape")
                if keys is None:
                    keys = pd.Index(np.arange(target_shape_2d[1]), name='iteration_idx')
                tile_times = target_shape_2d[1] // len(close.vbt.wrapper.columns)
                close = close.vbt.tile(tile_times, keys=keys)
        close = broadcast(close, to_shape=target_shape, **broadcast_kwargs)
        wrapper = ArrayWrapper.from_obj(close, freq=freq, group_by=group_by, **wrapper_kwargs)
        cs_group_lens = wrapper.grouper.get_group_lens(group_by=None if cash_sharing else False)
        init_cash = np.require(np.broadcast_to(init_cash, (len(cs_group_lens),)), dtype=np.float_)
        group_lens = wrapper.grouper.get_group_lens(group_by=group_by)
        if isinstance(active_mask, int):
            _active_mask = np.full((target_shape_2d[0], len(group_lens)), False)
            _active_mask[0::active_mask] = True
            active_mask = _active_mask
        else:
            active_mask = broadcast(
                active_mask,
                to_shape=(target_shape_2d[0], len(group_lens)),
                to_pd=False,
                **require_kwargs
            )
        if checks.is_any_array(call_seq):
            call_seq = nb.require_call_seq(broadcast(call_seq, to_shape=target_shape_2d, to_pd=False))
        else:
            call_seq = nb.build_call_seq(target_shape_2d, group_lens, call_seq_type=call_seq)
        if max_orders is None:
            max_orders = target_shape_2d[0] * target_shape_2d[1]
        if max_logs is None:
            max_logs = target_shape_2d[0] * target_shape_2d[1]

        # Prepare arguments
        if prep_func_nb is None:
            prep_func_nb = nb.empty_prep_nb
        if prep_args is None:
            prep_args = ()
        if group_prep_func_nb is None:
            group_prep_func_nb = nb.empty_prep_nb
        if group_prep_args is None:
            group_prep_args = ()
        if row_prep_func_nb is None:
            row_prep_func_nb = nb.empty_prep_nb
        if row_prep_args is None:
            row_prep_args = ()
        if segment_prep_func_nb is None:
            segment_prep_func_nb = nb.empty_prep_nb
        if segment_prep_args is None:
            segment_prep_args = ()

        # Perform calculation
        if row_wise:
            order_records, log_records = nb.simulate_row_wise_nb(
                target_shape_2d,
                to_2d(close, raw=True),
                group_lens,
                init_cash,
                cash_sharing,
                call_seq,
                active_mask,
                prep_func_nb,
                prep_args,
                row_prep_func_nb,
                row_prep_args,
                segment_prep_func_nb,
                segment_prep_args,
                order_func_nb,
                order_args,
                max_orders,
                max_logs
            )
        else:
            order_records, log_records = nb.simulate_nb(
                target_shape_2d,
                to_2d(close, raw=True),
                group_lens,
                init_cash,
                cash_sharing,
                call_seq,
                active_mask,
                prep_func_nb,
                prep_args,
                group_prep_func_nb,
                group_prep_args,
                segment_prep_func_nb,
                segment_prep_args,
                order_func_nb,
                order_args,
                max_orders,
                max_logs
            )

        # Create an instance
        return cls(
            wrapper,
            close,
            order_records,
            log_records,
            init_cash if init_cash_mode is None else init_cash_mode,
            cash_sharing,
            call_seq,
            **kwargs
        )

    # ############# Properties ############# #

    @property
    def wrapper(self):
        """Array wrapper."""
        if self.cash_sharing:
            # Allow only disabling grouping when needed (but not globally, see regroup)
            return self._wrapper.copy(
                allow_enable=False,
                allow_modify=False
            )
        return self._wrapper

    def regroup(self, group_by, **kwargs):
        """Regroup this object.

        See `vectorbt.base.array_wrapper.Wrapping.regroup`."""
        if self.cash_sharing:
            if self.wrapper.grouper.is_grouping_modified(group_by=group_by):
                raise ValueError("Cannot modify grouping globally when cash_sharing=True")
        return Wrapping.regroup(self, group_by, **kwargs)

    @property
    def cash_sharing(self):
        """Whether to share cash within the same group."""
        return self._cash_sharing

    @property
    def call_seq(self, wrap_kwargs=None):
        """Sequence of calls per row and group."""
        return self.wrapper.wrap(self._call_seq, group_by=False, **merge_dicts({}, wrap_kwargs))

    @property
    def incl_unrealized(self):
        """Whether to include unrealized trade P&L in statistics."""
        return self._incl_unrealized

    @property
    def use_filled_close(self):
        """Whether to forward-backward fill NaN values in `Portfolio.close`."""
        return self._use_filled_close

    # ############# Reference price ############# #

    @property
    def close(self):
        """Price per share series."""
        return self._close

    @cached_method
    def fill_close(self, ffill=True, bfill=True, wrap_kwargs=None):
        """Fill NaN values of `Portfolio.close`.
        Use `ffill` and `bfill` to fill forwards and backwards respectively."""
        close = to_2d(self.close, raw=True)
        if ffill and np.any(np.isnan(close[-1, :])):
            close = generic_nb.ffill_nb(close)
        if bfill and np.any(np.isnan(close[0, :])):
            close = generic_nb.ffill_nb(close[::-1, :])[::-1, :]
        return self.wrapper.wrap(close, group_by=False, **merge_dicts({}, wrap_kwargs))

    # ############# Records ############# #

    @property
    def order_records(self):
        """A structured NumPy array of order records."""
        return self._order_records

    @cached_property
    def orders(self):
        """`Portfolio.get_orders` with default arguments."""
        return Orders(self.wrapper, self.order_records, self.close)

    def get_orders(self, group_by=None):
        """Get order records.

        See `vectorbt.portfolio.orders.Orders`."""
        return self.orders.regroup(group_by=group_by)

    @property
    def log_records(self):
        """A structured NumPy array of log records."""
        return self._log_records

    @cached_property
    def logs(self):
        """`Portfolio.get_logs` with default arguments."""
        return Logs(self.wrapper, self.log_records)

    def get_logs(self, group_by=None):
        """Get log records.

        See `vectorbt.portfolio.logs.Logs`."""
        return self.logs.regroup(group_by=group_by)

    @cached_property
    def trades(self):
        """`Portfolio.get_trades` with default arguments."""
        return Trades.from_orders(self.orders)

    def get_trades(self, group_by=None):
        """Get trade records.

        See `vectorbt.portfolio.trades.Trades`."""
        return self.trades.regroup(group_by=group_by)

    @cached_property
    def positions(self):
        """`Portfolio.get_positions` with default arguments."""
        return Positions.from_trades(self.trades)

    def get_positions(self, group_by=None):
        """Get position records.

        See `vectorbt.portfolio.trades.Positions`."""
        return self.positions.regroup(group_by=group_by)

    @cached_property
    def drawdowns(self):
        """`Portfolio.get_drawdowns` with default arguments."""
        return self.get_drawdowns()

    @cached_method
    def get_drawdowns(self, **kwargs):
        """Get drawdown records from `Portfolio.value`.

        See `vectorbt.generic.drawdowns.Drawdowns`.

        `**kwargs` are passed to `Portfolio.value`."""
        return Drawdowns.from_ts(self.value(**kwargs), freq=self.wrapper.freq)

    # ############# Shares ############# #

    @cached_method
    def share_flow(self, direction='all', wrap_kwargs=None):
        """Get share flow series per column."""
        direction = convert_str_enum_value(Direction, direction)
        share_flow = nb.share_flow_nb(
            self.wrapper.shape_2d,
            self.orders.values,
            self.orders.col_mapper.col_map,
            direction
        )
        return self.wrapper.wrap(share_flow, group_by=False, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def shares(self, direction='all', wrap_kwargs=None):
        """Get share series per column."""
        direction = convert_str_enum_value(Direction, direction)
        share_flow = to_2d(self.share_flow(direction='all'), raw=True)
        shares = nb.shares_nb(share_flow)
        if direction == Direction.LongOnly:
            shares = np.where(shares > 0, shares, 0.)
        if direction == Direction.ShortOnly:
            shares = np.where(shares < 0, -shares, 0.)
        return self.wrapper.wrap(shares, group_by=False, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def pos_mask(self, direction='all', group_by=None, wrap_kwargs=None):
        """Get position mask per column/group."""
        direction = convert_str_enum_value(Direction, direction)
        shares = to_2d(self.shares(direction=direction), raw=True)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            pos_mask = to_2d(self.pos_mask(direction=direction, group_by=False), raw=True)
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            pos_mask = nb.pos_mask_grouped_nb(pos_mask, group_lens)
        else:
            pos_mask = shares != 0
        return self.wrapper.wrap(pos_mask, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def pos_coverage(self, direction='all', group_by=None, wrap_kwargs=None):
        """Get position coverage per column/group."""
        direction = convert_str_enum_value(Direction, direction)
        shares = to_2d(self.shares(direction=direction), raw=True)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            pos_mask = to_2d(self.pos_mask(direction=direction, group_by=False), raw=True)
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            pos_coverage = nb.pos_coverage_grouped_nb(pos_mask, group_lens)
        else:
            pos_coverage = np.mean(shares != 0, axis=0)
        wrap_kwargs = merge_dicts(dict(name_or_index='pos_coverage'), wrap_kwargs)
        return self.wrapper.wrap_reduced(pos_coverage, group_by=group_by, **wrap_kwargs)

    # ############# Cash ############# #

    @cached_method
    def cash_flow(self, group_by=None, short_cash=True, wrap_kwargs=None):
        """Get cash flow series per column/group.

        When `short_cash` is set to False, cash never goes above the initial level,
        because an operation always costs money."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            cash_flow = to_2d(self.cash_flow(group_by=False), raw=True)
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            cash_flow = nb.cash_flow_grouped_nb(cash_flow, group_lens)
        else:
            cash_flow = nb.cash_flow_nb(
                self.wrapper.shape_2d,
                self.orders.values,
                self.orders.col_mapper.col_map,
                short_cash
            )
        return self.wrapper.wrap(cash_flow, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_property
    def init_cash(self):
        """`Portfolio.get_init_cash` with default arguments."""
        return self.get_init_cash()

    @cached_method
    def get_init_cash(self, group_by=None, wrap_kwargs=None):
        """Initial amount of cash per column/group with default arguments.

        !!! note
            If initial cash is found automatically and no own cash is used throughout simulation
            (for example, when shorting), initial cash will be set to 1 instead of 0 to
            enable smooth calculation of returns."""
        if isinstance(self._init_cash, int):
            cash_flow = to_2d(self.cash_flow(group_by=group_by), raw=True)
            cash_min = np.min(np.cumsum(cash_flow, axis=0), axis=0)
            init_cash = np.where(cash_min < 0, np.abs(cash_min), 1.)
            if self._init_cash == InitCashMode.AutoAlign:
                init_cash = np.full(init_cash.shape, np.max(init_cash))
        else:
            init_cash = to_1d(self._init_cash, raw=True)
            if self.wrapper.grouper.is_grouped(group_by=group_by):
                group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
                init_cash = nb.init_cash_grouped_nb(init_cash, group_lens, self.cash_sharing)
            else:
                group_lens = self.wrapper.grouper.get_group_lens()
                init_cash = nb.init_cash_nb(init_cash, group_lens, self.cash_sharing)
        wrap_kwargs = merge_dicts(dict(name_or_index='init_cash'), wrap_kwargs)
        return self.wrapper.wrap_reduced(init_cash, group_by=group_by, **wrap_kwargs)

    @cached_method
    def cash(self, group_by=None, in_sim_order=False, short_cash=True, wrap_kwargs=None):
        """Get cash balance series per column/group."""
        if in_sim_order and not self.cash_sharing:
            raise ValueError("Cash sharing must be enabled for in_sim_order=True")

        cash_flow = to_2d(self.cash_flow(group_by=group_by, short_cash=short_cash), raw=True)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            init_cash = to_1d(self.get_init_cash(group_by=group_by), raw=True)
            cash = nb.cash_grouped_nb(
                self.wrapper.shape_2d,
                cash_flow,
                group_lens,
                init_cash
            )
        else:
            group_lens = self.wrapper.grouper.get_group_lens()
            if self.wrapper.grouper.is_grouping_disabled(group_by=group_by) and in_sim_order:
                init_cash = to_1d(self.init_cash, raw=True)
                call_seq = to_2d(self.call_seq, raw=True)
                cash = nb.cash_in_sim_order_nb(cash_flow, group_lens, init_cash, call_seq)
            else:
                init_cash = to_1d(self.get_init_cash(group_by=False), raw=True)
                cash = nb.cash_nb(cash_flow, group_lens, init_cash)
        return self.wrapper.wrap(cash, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    # ############# Performance ############# #

    @cached_method
    def holding_value(self, direction='all', group_by=None, wrap_kwargs=None):
        """Get holding value series per column/group."""
        direction = convert_str_enum_value(Direction, direction)
        close = to_2d(self.close, raw=True).copy()
        shares = to_2d(self.shares(direction=direction), raw=True)
        close[shares == 0] = 0.  # for price being NaN
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            holding_value = to_2d(self.holding_value(direction=direction, group_by=False), raw=True)
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            holding_value = nb.holding_value_grouped_nb(holding_value, group_lens)
        else:
            holding_value = nb.holding_value_nb(close, shares)
        return self.wrapper.wrap(holding_value, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def gross_exposure(self, direction='all', group_by=None, wrap_kwargs=None):
        """Get gross exposure."""
        holding_value = to_2d(self.holding_value(group_by=group_by, direction=direction), raw=True)
        cash = to_2d(self.cash(group_by=group_by, short_cash=False), raw=True)
        gross_exposure = nb.gross_exposure_nb(holding_value, cash)
        return self.wrapper.wrap(gross_exposure, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def net_exposure(self, group_by=None, wrap_kwargs=None):
        """Get net exposure."""
        long_exposure = to_2d(self.gross_exposure(direction='longonly', group_by=group_by), raw=True)
        short_exposure = to_2d(self.gross_exposure(direction='shortonly', group_by=group_by), raw=True)
        net_exposure = long_exposure - short_exposure
        return self.wrapper.wrap(net_exposure, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def value(self, group_by=None, in_sim_order=False, wrap_kwargs=None):
        """Get portfolio value series per column/group.

        By default, will generate portfolio value for each asset based on cash flows and thus
        independent from other assets, with initial cash and shares being that of the entire group.
        Useful for generating returns and comparing assets within the same group.

        When `group_by` is False and `in_sim_order` is True, returns value generated in
        simulation order (see [row-major order](https://en.wikipedia.org/wiki/Row-_and_column-major_order).
        This value cannot be used for generating returns as-is. Useful to analyze how value
        evolved throughout simulation."""
        cash = to_2d(self.cash(group_by=group_by, in_sim_order=in_sim_order), raw=True)
        holding_value = to_2d(self.holding_value(group_by=group_by), raw=True)
        if self.wrapper.grouper.is_grouping_disabled(group_by=group_by) and in_sim_order:
            group_lens = self.wrapper.grouper.get_group_lens()
            call_seq = to_2d(self.call_seq, raw=True)
            value = nb.value_in_sim_order_nb(cash, holding_value, group_lens, call_seq)
            # price of NaN is already addressed by ungrouped_value_nb
        else:
            value = nb.value_nb(cash, holding_value)
        return self.wrapper.wrap(value, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def total_profit(self, group_by=None, wrap_kwargs=None):
        """Get total profit per column/group.

        Calculated directly from order records (fast).

        Uses filled close if `Portfolio.use_filled_close` is True."""
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            total_profit = to_1d(self.total_profit(group_by=False), raw=True)
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            total_profit = nb.total_profit_grouped_nb(
                total_profit,
                group_lens
            )
        else:
            if self.use_filled_close:
                close = to_2d(self.fill_close(), raw=True)
            else:
                close = to_2d(self.close, raw=True)
            total_profit = nb.total_profit_nb(
                self.wrapper.shape_2d,
                close,
                self.orders.values,
                self.orders.col_mapper.col_map
            )
        wrap_kwargs = merge_dicts(dict(name_or_index='total_profit'), wrap_kwargs)
        return self.wrapper.wrap_reduced(total_profit, group_by=group_by, **wrap_kwargs)

    @cached_method
    def final_value(self, group_by=None, wrap_kwargs=None):
        """Get total profit per column/group."""
        init_cash = to_1d(self.get_init_cash(group_by=group_by), raw=True)
        total_profit = to_1d(self.total_profit(group_by=group_by), raw=True)
        final_value = nb.final_value_nb(total_profit, init_cash)
        wrap_kwargs = merge_dicts(dict(name_or_index='final_value'), wrap_kwargs)
        return self.wrapper.wrap_reduced(final_value, group_by=group_by, **wrap_kwargs)

    @cached_method
    def total_return(self, group_by=None, wrap_kwargs=None):
        """Get total profit per column/group."""
        init_cash = to_1d(self.get_init_cash(group_by=group_by), raw=True)
        total_profit = to_1d(self.total_profit(group_by=group_by), raw=True)
        total_return = nb.total_return_nb(total_profit, init_cash)
        wrap_kwargs = merge_dicts(dict(name_or_index='total_return'), wrap_kwargs)
        return self.wrapper.wrap_reduced(total_return, group_by=group_by, **wrap_kwargs)

    @cached_method
    def returns(self, group_by=None, in_sim_order=False, wrap_kwargs=None):
        """Get return series per column/group based on portfolio value."""
        value = to_2d(self.value(group_by=group_by, in_sim_order=in_sim_order), raw=True)
        if self.wrapper.grouper.is_grouping_disabled(group_by=group_by) and in_sim_order:
            group_lens = self.wrapper.grouper.get_group_lens()
            init_cash_grouped = to_1d(self.init_cash, raw=True)
            call_seq = to_2d(self.call_seq, raw=True)
            returns = nb.returns_in_sim_order_nb(value, group_lens, init_cash_grouped, call_seq)
        else:
            init_cash = to_1d(self.get_init_cash(group_by=group_by), raw=True)
            returns = nb.returns_nb(value, init_cash)
        return self.wrapper.wrap(returns, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def active_returns(self, group_by=None, wrap_kwargs=None):
        """Get active return series per column/group.

        This type of returns is based solely on cash flows and holding value rather than portfolio value.
        It ignores passive cash and thus it will return the same numbers irrespective of the amount of
        cash currently available, even `np.inf`. The scale of returns is comparable to that of going
        all in and keeping available cash at zero."""
        cash_flow = to_2d(self.cash_flow(group_by=group_by), raw=True)
        holding_value = to_2d(self.holding_value(group_by=group_by), raw=True)
        active_returns = nb.active_returns_nb(cash_flow, holding_value)
        return self.wrapper.wrap(active_returns, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def market_value(self, group_by=None, wrap_kwargs=None):
        """Get market (benchmark) value series per column/group.

        If grouped, evenly distributes initial cash among assets in the group.

        Uses filled close if `Portfolio.use_filled_close` is True.

        !!! note
            Does not take into account fees and slippage. For this, create a separate portfolio."""
        if self.use_filled_close:
            close = to_2d(self.fill_close(), raw=True)
        else:
            close = to_2d(self.close, raw=True)
        if self.wrapper.grouper.is_grouped(group_by=group_by):
            group_lens = self.wrapper.grouper.get_group_lens(group_by=group_by)
            init_cash_grouped = to_1d(self.get_init_cash(group_by=group_by), raw=True)
            market_value = nb.market_value_grouped_nb(close, group_lens, init_cash_grouped)
        else:
            init_cash = to_1d(self.get_init_cash(group_by=False), raw=True)
            market_value = nb.market_value_nb(close, init_cash)
        return self.wrapper.wrap(market_value, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def market_returns(self, group_by=None, wrap_kwargs=None):
        """Get return series per column/group based on market (benchmark) value."""
        market_value = to_2d(self.market_value(group_by=group_by), raw=True)
        init_cash = to_1d(self.get_init_cash(group_by=group_by), raw=True)
        market_returns = nb.returns_nb(market_value, init_cash)
        return self.wrapper.wrap(market_returns, group_by=group_by, **merge_dicts({}, wrap_kwargs))

    @cached_method
    def total_market_return(self, group_by=None, wrap_kwargs=None):
        """Get total market (benchmark) return."""
        market_value = to_2d(self.market_value(group_by=group_by), raw=True)
        total_market_return = nb.total_market_return_nb(market_value)
        wrap_kwargs = merge_dicts(dict(name_or_index='total_market_return'), wrap_kwargs)
        return self.wrapper.wrap_reduced(total_market_return, group_by=group_by, **wrap_kwargs)

    @cached_method
    def stats(self, column=None, group_by=None, incl_unrealized=None, active_returns=False,
              in_sim_order=False, agg_func=_mean_agg_func, wrap_kwargs=None, **kwargs):
        """Compute various statistics on this portfolio.

        `kwargs` will be passed to each `vectorbt.returns.accessors.ReturnsAccessor` method.

        Can either return aggregated statistics by reducing metrics of all columns with
        `agg_func` (mean by default) or return statistics for a single column if `column`
        was specified or portfolio contains only one column of data. To display rich data types
        such as durations correctly, use an aggregation function that can be applied on `pd.Series`.

        !!! note
            Use `column` only if caching is enabled, otherwise it may re-compute the same
            objects multiple times."""
        if self.wrapper.freq is None:
            raise ValueError("Couldn't parse the frequency of index. You must set `freq`.")

        # Pre-calculate
        trades = self.get_trades(group_by=group_by)
        if incl_unrealized is None:
            incl_unrealized = self.incl_unrealized
        if not incl_unrealized:
            trades = trades.closed
        drawdowns = self.get_drawdowns(group_by=group_by)
        if active_returns:
            returns = self.active_returns(group_by=group_by)
        else:
            returns = self.returns(group_by=group_by, in_sim_order=in_sim_order)

        # Run stats
        stats_df = pd.DataFrame({
            'Start': self.wrapper.index[0],
            'End': self.wrapper.index[-1],
            'Duration': self.wrapper.shape[0] * self.wrapper.freq,
            'Init. Cash': self.get_init_cash(group_by=group_by),
            'Total Profit': self.total_profit(group_by=group_by),
            'Total Return [%]': self.total_return(group_by=group_by) * 100,
            'Benchmark Return [%]': self.total_market_return(group_by=group_by) * 100,
            'Position Coverage [%]': self.pos_coverage(group_by=group_by) * 100,
            'Max. Drawdown [%]': -drawdowns.max_drawdown() * 100,
            'Avg. Drawdown [%]': -drawdowns.avg_drawdown() * 100,
            'Max. Drawdown Duration': drawdowns.max_duration(),
            'Avg. Drawdown Duration': drawdowns.avg_duration(),
            'Num. Trades': trades.count(),
            'Win Rate [%]': trades.win_rate() * 100,
            'Best Trade [%]': trades.returns.max() * 100,
            'Worst Trade [%]': trades.returns.min() * 100,
            'Avg. Trade [%]': trades.returns.mean() * 100,
            'Max. Trade Duration': trades.duration.max(wrap_kwargs=dict(time_units=True)),
            'Avg. Trade Duration': trades.duration.mean(wrap_kwargs=dict(time_units=True)),
            'Expectancy': trades.expectancy(),
            'SQN': trades.sqn(),
            'Gross Exposure': self.gross_exposure(group_by=group_by).mean(),
            'Sharpe Ratio': self.sharpe_ratio(reuse_returns=returns, **kwargs),
            'Sortino Ratio': self.sortino_ratio(reuse_returns=returns, **kwargs),
            'Calmar Ratio': self.calmar_ratio(reuse_returns=returns, **kwargs)
        }, index=self.wrapper.grouper.get_columns(group_by=group_by))

        # Select columns or reduce
        if self.wrapper.get_ndim(group_by=group_by) == 1:
            wrap_kwargs = merge_dicts(dict(name_or_index=stats_df.columns), wrap_kwargs)
            return self.wrapper.wrap_reduced(stats_df.iloc[0], group_by=group_by, **wrap_kwargs)
        if column is not None:
            return stats_df.loc[column]
        if agg_func is not None:
            if agg_func == _mean_agg_func:
                warnings.warn("Taking mean across columns. To return a DataFrame, pass agg_func=None.", stacklevel=2)
                func_name = 'stats_mean'
            else:
                func_name = 'stats_' + agg_func.__name__
            agg_stats_sr = pd.Series(index=stats_df.columns, name=func_name)
            agg_stats_sr.iloc[:3] = stats_df.iloc[0, :3]
            agg_stats_sr.iloc[3:] = agg_func(stats_df.iloc[:, 3:])
            return agg_stats_sr
        return stats_df

    def returns_stats(self, column=None, group_by=None, active_returns=False, in_sim_order=False,
                      agg_func=_mean_agg_func, year_freq=None, **kwargs):
        """Compute various statistics on returns of this portfolio.

        For keyword arguments and notes, see `Portfolio.stats`.

        `kwargs` will be passed to `vectorbt.returns.accessors.ReturnsAccessor.stats` method.
        If `benchmark_rets` is not set, uses `Portfolio.market_returns`."""
        # Pre-calculate
        if active_returns:
            returns = self.active_returns(group_by=group_by)
        else:
            returns = self.returns(group_by=group_by, in_sim_order=in_sim_order)

        # Run stats
        if 'benchmark_rets' not in kwargs:
            kwargs['benchmark_rets'] = self.market_returns(group_by=group_by)
        stats_obj = returns.vbt.returns(freq=self.wrapper.freq, year_freq=year_freq).stats(**kwargs)

        # Select columns or reduce
        if checks.is_series(stats_obj):
            return stats_obj
        if column is not None:
            return stats_obj.loc[column]
        if agg_func is not None:
            if agg_func == _mean_agg_func:
                warnings.warn("Taking mean across columns. To return a DataFrame, pass agg_func=None.", stacklevel=2)
                func_name = 'stats_mean'
            else:
                func_name = 'stats_' + agg_func.__name__
            agg_stats_sr = pd.Series(index=stats_obj.columns, name=func_name)
            agg_stats_sr.iloc[:3] = stats_obj.iloc[0, :3]
            agg_stats_sr.iloc[3:] = agg_func(stats_obj.iloc[:, 3:])
            return agg_stats_sr
        return stats_obj

    # ############# Plotting ############# #

    subplot_settings = OrderedDict(
        orders=dict(
            title="Orders",
            can_plot_groups=False
        ),
        trades=dict(
            title="Trades",
            can_plot_groups=False
        ),
        positions=dict(
            title="Positions",
            can_plot_groups=False
        ),
        trade_pnl=dict(
            title="Trade PnL",
            can_plot_groups=False
        ),
        position_pnl=dict(
            title="Position PnL",
            can_plot_groups=False
        ),
        cum_returns=dict(
            title="Cumulative Returns"
        ),
        share_flow=dict(
            title="Share Flow",
            can_plot_groups=False
        ),
        cash_flow=dict(
            title="Cash Flow"
        ),
        shares=dict(
            title="Shares",
            can_plot_groups=False
        ),
        cash=dict(
            title="Cash"
        ),
        holding_value=dict(
            title="Holding Value"
        ),
        value=dict(
            title="Value"
        ),
        drawdowns=dict(
            title="Drawdowns"
        ),
        underwater=dict(
            title="Underwater"
        ),
        gross_exposure=dict(
            title="Gross Exposure"
        ),
        net_exposure=dict(
            title="Net Exposure"
        )
    )
    """Settings of subplots supported by `Portfolio.plot`."""

    def plot(self, *,
             column=None,
             subplots=None,
             group_by=None,
             show_titles=True,
             hide_id_labels=True,
             group_id_labels=True,
             hline_shape_kwargs=None,
             make_subplots_kwargs=None,
             **kwargs):  # pragma: no cover
        """Plot various parts of this portfolio.

        Args:
            subplots (list of str or list of tuple): List of subplots to plot.

                Each element can be either:

                * a subplot name, as listed in `Portfolio.subplot_settings`
                * a tuple of a subplot name and a dict as in `Portfolio.subplot_settings` but with an
                    additional optional key `plot_func`. The plot function should accept current portfolio
                    object (with column already selected), other keyword arguments (optionally), and
                    the figure object `fig` as the last keyword argument. It will also pass the following
                    arguments if any of them can be found in the function's signature:

                    * `add_trace_kwargs`
                    * `xref`
                    * `yref`
                    * `xaxis`
                    * `yaxis`
                    * `x_domain`
                    * `y_domain`
            column (str): Name of the column/group to plot.

                Takes effect if portfolio contains multiple columns.
            group_by (any): Group columns. See `vectorbt.base.column_grouper.ColumnGrouper`.

                Used to select `group`.
            show_titles (bool): Whether to show the title in the top left corner of each subplot.
            hide_id_labels (bool): Whether to hide identical legend labels.

                Two labels are identical if their name, marker style and line style match.
            group_id_labels (bool): Whether to group identical legend labels.
            hline_shape_kwargs (dict): Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for horizontal lines.
            make_subplots_kwargs (dict): Keyword arguments passed to `plotly.subplots.make_subplots`.
            **kwargs: Additional keyword arguments.

                Can contain keyword arguments for each subplot, each specified as `{subplot_name}_kwargs`.
                Other keyword arguments are used to update layout of the figure.

        ## Example

        Plot portfolio of a random strategy:
        ```python-repl
        >>> import numpy as np
        >>> import pandas as pd
        >>> from datetime import datetime
        >>> import vectorbt as vbt

        >>> start = datetime(2020, 1, 1)
        >>> end = datetime(2020, 9, 1)
        >>> close = vbt.YFData.download("BTC-USD", start=start, end=end).get('Close')

        >>> np.random.seed(42)
        >>> size = pd.Series.vbt.empty_like(close, fill_value=0.)
        >>> n_orders = 20
        >>> rand_idxs = np.random.randint(0, len(size), size=n_orders)
        >>> size.iloc[rand_idxs] = np.random.uniform(-1, 1, size=n_orders)
        >>> portfolio = vbt.Portfolio.from_orders(
        ...     close, size, direction='longonly',
        ...     init_cash='auto', freq='1D')
        >>> portfolio.plot()
        ```

        ![](/vectorbt/docs/img/portfolio_plot.png)

        You can choose any of the subplots in `Portfolio.subplot_settings`, in any order:

        ```python-repl
        >>> from vectorbt.utils.colors import adjust_opacity

        >>> portfolio.plot(
        ...     subplots=['drawdowns', 'underwater'],
        ...     drawdowns_kwargs=dict(top_n=3),
        ...     underwater_kwargs=dict(
        ...         trace_kwargs=dict(
        ...             line_color='#FF6F00',
        ...             fillcolor=adjust_opacity('#FF6F00', 0.3)
        ...         )
        ...     )
        ... )
        ```

        ![](/vectorbt/docs/img/portfolio_plot_drawdowns.png)

        You can also create a custom subplot by creating a placeholder that can be written later:

        ```python-repl
        >>> fig = portfolio.plot(subplots=[
        ...     'orders',
        ...     ('order_size', dict(
        ...         title='Order Size',
        ...         can_plot_groups=False
        ...     ))  # placeholder
        ... ])

        >>> size.rename('Order Size').vbt.plot(add_trace_kwargs=dict(row=2, col=1), fig=fig)
        ```

        Alternatively, you can pass a plot function:

        ```python-repl
        >>> def plot_order_size(portfolio, add_trace_kwargs=None, fig=None):
        ...     size.rename('Order Size').vbt.plot(add_trace_kwargs=add_trace_kwargs, fig=fig)

        >>> portfolio.plot(subplots=[
        ...     'orders',
        ...     ('order_size', dict(
        ...         title='Order Size',
        ...         can_plot_groups=False,
        ...         plot_func=plot_order_size
        ...     ))
        ... ])
        ```

        ![](/vectorbt/docs/img/portfolio_plot_custom.png)
        """
        from vectorbt.settings import color_schema, layout

        # Select one column/group
        self_col = self.select_series(column=column, group_by=group_by)

        if subplots is None:
            if self_col.wrapper.grouper.is_grouped():
                subplots = ['cum_returns']
            else:
                subplots = ['orders', 'trade_pnl', 'cum_returns']
        elif subplots == 'all':
            if self_col.wrapper.grouper.is_grouped():
                supported_subplots = filter(lambda x: x[1].get('can_plot_groups', True), self.subplot_settings.items())
            else:
                supported_subplots = self.subplot_settings.items()
            subplots = list(list(zip(*supported_subplots))[0])
        if not isinstance(subplots, list):
            subplots = [subplots]
        if len(subplots) == 0:
            raise ValueError("You must select at least one subplot")
        if hline_shape_kwargs is None:
            hline_shape_kwargs = {}
        hline_shape_kwargs = merge_dicts(
            dict(
                type='line',
                line=dict(
                    color='gray',
                    dash="dash",
                )
            ),
            hline_shape_kwargs
        )
        if make_subplots_kwargs is None:
            make_subplots_kwargs = {}

        # Set up figure
        rows = make_subplots_kwargs.pop('rows', len(subplots))
        cols = make_subplots_kwargs.pop('cols', 1)
        width = kwargs.get('width', layout['width'] + 50)
        height = kwargs.get('height', (layout['height'] - 50) * rows if rows > 1 else layout['height'])
        specs = make_subplots_kwargs.pop('specs', [[{} for _ in range(cols)] for _ in range(rows)])
        row_col_tuples = []
        for row, row_spec in enumerate(specs):
            for col, col_spec in enumerate(row_spec):
                if col_spec is not None:
                    row_col_tuples.append((row + 1, col + 1))
        shared_xaxes = make_subplots_kwargs.pop('shared_xaxes', True)
        shared_yaxes = make_subplots_kwargs.pop('shared_yaxes', False)
        if height is not None:
            vertical_spacing = make_subplots_kwargs.pop('vertical_spacing', 40)
            if vertical_spacing is not None and vertical_spacing > 1:
                vertical_spacing /= height
        else:
            vertical_spacing = make_subplots_kwargs.pop('vertical_spacing', None)
        horizontal_spacing = make_subplots_kwargs.pop('horizontal_spacing', None)
        if width is not None:
            if horizontal_spacing is not None and horizontal_spacing > 1:
                horizontal_spacing /= width
        if show_titles:
            _subplot_titles = []
            for name in subplots:
                if isinstance(name, tuple):
                    _subplot_titles.append(name[1].get('title', None))
                else:
                    _subplot_titles.append(self_col.subplot_settings[name]['title'])
        else:
            _subplot_titles = None
        fig = make_subplots(
            rows=rows,
            cols=cols,
            specs=specs,
            shared_xaxes=shared_xaxes,
            shared_yaxes=shared_yaxes,
            subplot_titles=_subplot_titles,
            vertical_spacing=vertical_spacing,
            horizontal_spacing=horizontal_spacing,
            **make_subplots_kwargs
        )
        default_layout = dict(
            autosize=True,
            width=width,
            height=height,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=(1 + 30 / height) if height is not None else 1.02,
                xanchor="right",
                x=1,
                traceorder='normal'
            )
        )
        fig.update_layout(default_layout)

        def _add_hline(value, x_domain, yref):
            fig.add_shape(**merge_dicts(dict(
                xref="paper",
                yref=yref,
                x0=x_domain[0],
                y0=value,
                x1=x_domain[1],
                y1=value
            ), hline_shape_kwargs))

        def _get_arg_names(method):
            return [
                p.name for p in signature(method).parameters.values()
                if p.kind != p.VAR_POSITIONAL and p.kind != p.VAR_KEYWORD
            ]

        def _extract_method_kwargs(method, kwargs):
            arg_names = _get_arg_names(method)
            method_kwargs = {}
            for name in arg_names:
                if name in kwargs:
                    method_kwargs[name] = kwargs.pop(name)
            return method_kwargs

        # Show subplots
        for i, name in enumerate(subplots):
            row, col = row_col_tuples[i]
            xref = 'x' if i == 0 else 'x' + str(i + 1)
            yref = 'y' if i == 0 else 'y' + str(i + 1)
            xaxis = 'xaxis' if i == 0 else 'xaxis' + str(i + 1)
            yaxis = 'yaxis' if i == 0 else 'yaxis' + str(i + 1)
            x_domain = fig.layout[xaxis]['domain']
            y_domain = fig.layout[yaxis]['domain']

            if isinstance(name, tuple):
                _name, settings = name
                can_plot_groups = settings.get('can_plot_groups', True)
                if self_col.wrapper.grouper.is_grouped() and not can_plot_groups:
                    raise TypeError(f"Group is not supported by custom subplot with name '{_name}'")
                plot_func = settings.get('plot_func', None)

                if plot_func is not None:
                    arg_names = _get_arg_names(plot_func)
                    custom_kwargs = dict()
                    if 'add_trace_kwargs' in arg_names:
                        custom_kwargs['add_trace_kwargs'] = dict(row=row, col=col)
                    if 'xref' in arg_names:
                        custom_kwargs['xref'] = xref
                    if 'yref' in arg_names:
                        custom_kwargs['yref'] = yref
                    if 'xaxis' in arg_names:
                        custom_kwargs['xaxis'] = xaxis
                    if 'yaxis' in arg_names:
                        custom_kwargs['yaxis'] = yaxis
                    if 'x_domain' in arg_names:
                        custom_kwargs['x_domain'] = x_domain
                    if 'y_domain' in arg_names:
                        custom_kwargs['y_domain'] = y_domain
                    custom_kwargs = merge_dicts(custom_kwargs, kwargs.pop(f'{_name}_kwargs', {}))
                    plot_func(self_col, **custom_kwargs, fig=fig)

                fig.layout[xaxis]['title'] = 'Date'
                fig.layout[yaxis]['title'] = settings.get('title', None)
                    
            else:
                settings = self.subplot_settings[name]
                can_plot_groups = settings.get('can_plot_groups', True)
                if self_col.wrapper.grouper.is_grouped() and not can_plot_groups:
                    raise TypeError(f"Group is not supported by subplot with name '{name}'")

                if name == 'orders':
                    orders_kwargs = kwargs.pop('orders_kwargs', {})
                    method_kwargs = _extract_method_kwargs(self_col.get_orders, orders_kwargs)
                    self_col.get_orders(**method_kwargs).plot(
                        **orders_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Price'
    
                elif name == 'trades':
                    trades_kwargs = kwargs.pop('trades_kwargs', {})
                    method_kwargs = _extract_method_kwargs(self_col.get_trades, trades_kwargs)
                    self_col.get_trades(**method_kwargs).plot(
                        **trades_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), xref=xref, yref=yref, fig=fig)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Price'
    
                elif name == 'positions':
                    positions_kwargs = kwargs.pop('positions_kwargs', {})
                    method_kwargs = _extract_method_kwargs(self_col.get_positions, positions_kwargs)
                    self_col.get_positions(**method_kwargs).plot(
                        **positions_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), xref=xref, yref=yref, fig=fig)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Price'
    
                elif name == 'trade_pnl':
                    trade_pnl_kwargs = merge_dicts(dict(
                        hline_shape_kwargs=hline_shape_kwargs
                    ), kwargs.pop('trade_pnl_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.get_trades, trade_pnl_kwargs)
                    self_col.get_trades(**method_kwargs).plot_pnl(
                        **trade_pnl_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), xref=xref, yref=yref, fig=fig)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'PnL'
    
                elif name == 'position_pnl':
                    position_pnl_kwargs = kwargs.pop('position_pnl_kwargs', {})
                    method_kwargs = _extract_method_kwargs(self_col.get_positions, position_pnl_kwargs)
                    self_col.get_positions(**method_kwargs).plot_pnl(
                        **position_pnl_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), xref=xref, yref=yref, fig=fig)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'PnL'
    
                elif name == 'cum_returns':
                    cum_returns_kwargs = merge_dicts(dict(
                        benchmark_rets=self_col.market_returns(),
                        main_kwargs=dict(
                            trace_kwargs=dict(
                                line_color=color_schema['purple'],
                                name='Value'
                            )
                        ),
                        hline_shape_kwargs=hline_shape_kwargs
                    ), kwargs.pop('cum_returns_kwargs', {}))
                    active_returns = cum_returns_kwargs.pop('active_returns', False)
                    in_sim_order = cum_returns_kwargs.pop('in_sim_order', False)
                    if active_returns:
                        returns = self_col.active_returns()
                    else:
                        returns = self_col.returns(in_sim_order=in_sim_order)
                    returns.vbt.returns.plot_cum_returns(
                        **cum_returns_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), xref=xref, yref=yref, fig=fig)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Cumulative Returns'
    
                elif name == 'drawdowns':
                    drawdowns_kwargs = merge_dicts(dict(
                        ts_trace_kwargs=dict(
                            line_color=color_schema['purple'],
                            name='Value'
                        )
                    ), kwargs.pop('drawdowns_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.get_drawdowns, drawdowns_kwargs)
                    self_col.get_drawdowns(**method_kwargs).plot(
                        **drawdowns_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), xref=xref, yref=yref, fig=fig)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Value'
    
                elif name == 'underwater':
                    underwater_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['red'],
                            fillcolor=adjust_opacity(color_schema['red'], 0.3),
                            fill='tozeroy',
                            name='Drawdown'
                        )
                    ), kwargs.pop('underwater_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.drawdown, underwater_kwargs)
                    self_col.drawdown(**method_kwargs).vbt.plot(
                        **underwater_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(0, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Drawdown'
                    fig.layout[yaxis]['tickformat'] = '%'
    
                elif name == 'share_flow':
                    share_flow_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['brown'],
                            name='Shares'
                        )
                    ), kwargs.pop('share_flow_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.share_flow, share_flow_kwargs)
                    self_col.share_flow(**method_kwargs).vbt.plot(
                        **share_flow_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(0, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Share Flow'
    
                elif name == 'cash_flow':
                    cash_flow_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['green'],
                            name='Cash'
                        )
                    ), kwargs.pop('cash_flow_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.cash_flow, cash_flow_kwargs)
                    self_col.cash_flow(**method_kwargs).vbt.plot(
                        **cash_flow_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(0, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Cash Flow'
    
                elif name == 'shares':
                    shares_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['brown'],
                            name='Shares'
                        ),
                        pos_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['brown'], 0.3)
                        ),
                        neg_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['orange'], 0.3)
                        ),
                        other_trace_kwargs='hidden'
                    ), kwargs.pop('shares_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.shares, shares_kwargs)
                    self_col.shares(**method_kwargs).vbt.plot_against(
                        0, **shares_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(0, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Shares'
    
                elif name == 'cash':
                    cash_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['green'],
                            name='Cash'
                        ),
                        pos_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['green'], 0.3)
                        ),
                        neg_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['red'], 0.3)
                        ),
                        other_trace_kwargs='hidden'
                    ), kwargs.pop('cash_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.cash, cash_kwargs)
                    self_col.cash(**method_kwargs).vbt.plot_against(
                        0, **cash_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(self_col.init_cash, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Cash'
    
                elif name == 'holding_value':
                    holding_value_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['cyan'],
                            name='Holding Value'
                        ),
                        pos_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['cyan'], 0.3)
                        ),
                        neg_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['orange'], 0.3)
                        ),
                        other_trace_kwargs='hidden'
                    ), kwargs.pop('holding_value_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.holding_value, holding_value_kwargs)
                    self_col.holding_value(**method_kwargs).vbt.plot_against(
                        0, **holding_value_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(0, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Holding Value'
    
                elif name == 'value':
                    value_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['purple'],
                            name='Value'
                        ),
                        other_trace_kwargs='hidden'
                    ), kwargs.pop('value_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.value, value_kwargs)
                    self_col.value(**method_kwargs).vbt.plot_against(
                        self_col.init_cash, **value_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(self_col.init_cash, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Value'
    
                elif name == 'gross_exposure':
                    gross_exposure_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['pink'],
                            name='Exposure'
                        ),
                        pos_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['orange'], 0.3)
                        ),
                        neg_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['pink'], 0.3)
                        ),
                        other_trace_kwargs='hidden'
                    ), kwargs.pop('gross_exposure_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.gross_exposure, gross_exposure_kwargs)
                    self_col.gross_exposure(**method_kwargs).vbt.plot_against(
                        1, **gross_exposure_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(1, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Gross Exposure'
    
                elif name == 'net_exposure':
                    net_exposure_kwargs = merge_dicts(dict(
                        trace_kwargs=dict(
                            line_color=color_schema['pink'],
                            name='Exposure'
                        ),
                        pos_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['pink'], 0.3)
                        ),
                        neg_trace_kwargs=dict(
                            fillcolor=adjust_opacity(color_schema['orange'], 0.3)
                        ),
                        other_trace_kwargs='hidden'
                    ), kwargs.pop('net_exposure_kwargs', {}))
                    method_kwargs = _extract_method_kwargs(self_col.net_exposure, net_exposure_kwargs)
                    self_col.net_exposure(**method_kwargs).vbt.plot_against(
                        0, **net_exposure_kwargs,
                        add_trace_kwargs=dict(row=row, col=col), fig=fig)
                    _add_hline(0, x_domain, yref)
                    fig.layout[xaxis]['title'] = 'Date'
                    fig.layout[yaxis]['title'] = 'Net Exposure'

        # Remove duplicate legend labels
        found_ids = dict()
        unique_idx = 0
        for trace in fig.data:
            if 'name' in trace:
                name = trace['name']
            else:
                name = None
            if 'marker' in trace:
                marker = trace['marker']
            else:
                marker = {}
            if 'symbol' in marker:
                marker_symbol = marker['symbol']
            else:
                marker_symbol = None
            if 'color' in marker:
                marker_color = marker['color']
            else:
                marker_color = None
            if 'line' in trace:
                line = trace['line']
            else:
                line = {}
            if 'dash' in line:
                line_dash = line['dash']
            else:
                line_dash = None
            if 'color' in line:
                line_color = line['color']
            else:
                line_color = None

            id = (name, marker_symbol, marker_color, line_dash, line_color)
            if id in found_ids:
                if hide_id_labels:
                    trace['showlegend'] = False
                if group_id_labels:
                    trace['legendgroup'] = found_ids[id]
            else:
                if group_id_labels:
                    trace['legendgroup'] = unique_idx
                found_ids[id] = unique_idx
                unique_idx += 1

        # Remove all except the last title if sharing the same axis
        if shared_xaxes:
            i = 0
            for row in range(rows):
                for col in range(cols):
                    if specs[row][col] is not None:
                        xaxis = 'xaxis' if i == 0 else 'xaxis' + str(i + 1)
                        if row < rows - 1:
                            fig.layout[xaxis]['title'] = None
                        i += 1
        if shared_yaxes:
            i = 0
            for row in range(rows):
                for col in range(cols):
                    if specs[row][col] is not None:
                        yaxis = 'yaxis' if i == 0 else 'yaxis' + str(i + 1)
                        if col > 0:
                            fig.layout[yaxis]['title'] = None
                        i += 1

        fig.update_layout(kwargs)
        return fig
