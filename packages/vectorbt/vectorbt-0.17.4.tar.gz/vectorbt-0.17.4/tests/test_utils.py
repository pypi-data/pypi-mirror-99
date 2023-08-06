import numpy as np
import pandas as pd
from numba import njit
import pytest
import os
from collections import namedtuple
from itertools import product, combinations
import asyncio
import pytz
import dateparser

from vectorbt import settings
from vectorbt.utils import checks, config, decorators, math, array, random, enum, params, attr, datetime, schedule
from datetime import datetime as _datetime, timedelta as _timedelta, time as _time, timezone as _timezone

from tests.utils import hash

seed = 42


# ############# config.py ############# #

class TestConfig:
    def test_config(self):
        conf = config.Config({'a': 0, 'b': {'c': 1}}, frozen=False)
        conf['b']['d'] = 2

        conf = config.Config({'a': 0, 'b': {'c': 1}}, frozen=True)
        conf['a'] = 2

        with pytest.raises(Exception) as e_info:
            conf['d'] = 2

        with pytest.raises(Exception) as e_info:
            conf.update(d=2)

        conf.update(d=2, force_update=True)
        assert conf['d'] == 2

        conf = config.Config({'a': 0, 'b': {'c': 1}}, read_only=True)

        with pytest.raises(Exception) as e_info:
            conf['a'] = 2

        with pytest.raises(Exception) as e_info:
            del conf['a']

        with pytest.raises(Exception) as e_info:
            conf.pop('a')

        with pytest.raises(Exception) as e_info:
            conf.popitem()

        with pytest.raises(Exception) as e_info:
            conf.clear()

        with pytest.raises(Exception) as e_info:
            conf.update(a=2)

        assert isinstance(conf.merge_with(dict(b=dict(d=2))), config.Config)
        assert conf.merge_with(dict(b=dict(d=2)), read_only=True).read_only
        assert conf.merge_with(dict(b=dict(d=2)))['b']['d'] == 2

        conf = config.Config({'a': 0, 'b': {'c': [1, 2]}})
        conf['a'] = 1
        conf['b']['c'].append(3)
        conf['b']['d'] = 2
        assert conf == {'a': 1, 'b': {'c': [1, 2, 3], 'd': 2}}
        conf.reset()
        assert conf == {'a': 0, 'b': {'c': [1, 2]}}

    def test_get_func_kwargs(self):
        def f(a, *args, b=2, **kwargs):
            pass

        assert config.get_func_kwargs(f) == {'b': 2}

    def test_merge_dicts(self):
        assert config.merge_dicts({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
        assert config.merge_dicts({'a': 1}, {'a': 2}) == {'a': 2}
        assert config.merge_dicts({'a': {'b': 2}}, {'a': {'c': 3}}) == {'a': {'b': 2, 'c': 3}}
        assert config.merge_dicts({'a': {'b': 2}}, {'a': {'b': 3}}) == {'a': {'b': 3}}

    def test_configured(self):
        class H(config.Configured):
            def __init__(self, a, b=2, **kwargs):
                super().__init__(a=a, b=b, **kwargs)

        assert H(1).config == {'a': 1, 'b': 2}
        assert H(1).copy(b=3).config == {'a': 1, 'b': 3}
        assert H(1).copy(c=4).config == {'a': 1, 'b': 2, 'c': 4}
        assert H(pd.Series([1, 2, 3])) == H(pd.Series([1, 2, 3]))
        assert H(pd.Series([1, 2, 3])) != H(pd.Series([1, 2, 4]))
        assert H(pd.DataFrame([1, 2, 3])) == H(pd.DataFrame([1, 2, 3]))
        assert H(pd.DataFrame([1, 2, 3])) != H(pd.DataFrame([1, 2, 4]))
        assert H(pd.Index([1, 2, 3])) == H(pd.Index([1, 2, 3]))
        assert H(pd.Index([1, 2, 3])) != H(pd.Index([1, 2, 4]))
        assert H(np.array([1, 2, 3])) == H(np.array([1, 2, 3]))
        assert H(np.array([1, 2, 3])) != H(np.array([1, 2, 4]))
        assert H(None) == H(None)
        assert H(None) != H(10.)


# ############# decorators.py ############# #

class TestDecorators:
    def test_class_or_instancemethod(self):
        class G:
            @decorators.class_or_instancemethod
            def g(self_or_cls):
                if isinstance(self_or_cls, type):
                    return True  # class
                return False  # instance

        assert G.g()
        assert not G().g()

    def test_custom_property(self):
        class G:
            @decorators.custom_property(some='key')
            def cache_me(self): return np.random.uniform()

        assert 'some' in G.cache_me.kwargs
        assert G.cache_me.kwargs['some'] == 'key'

    def test_custom_method(self):
        class G:
            @decorators.custom_method(some='key')
            def cache_me(self): return np.random.uniform()

        assert 'some' in G.cache_me.kwargs
        assert G.cache_me.kwargs['some'] == 'key'

    def test_cached_property(self):
        np.random.seed(seed)

        class G:
            @decorators.cached_property
            def cache_me(self): return np.random.uniform()

        g = G()
        cached_number = g.cache_me
        assert g.cache_me == cached_number

        class G:
            @decorators.cached_property(hello="world", hello2="world2")
            def cache_me(self): return np.random.uniform()

        assert 'hello' in G.cache_me.kwargs
        assert G.cache_me.kwargs['hello'] == 'world'

        g = G()
        g2 = G()

        class G3(G):
            pass

        g3 = G3()

        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3

        # clear_cache method
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        G.cache_me.clear_cache(g)
        assert g.cache_me != cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3

        # test blacklist

        # instance + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append((g, 'cache_me'))
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('cache_me')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # instance
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append(g)
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # class + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append((G, 'cache_me'))
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # class
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append(G)
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # class name + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('G.cache_me')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('G')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # improper class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('g')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # kwargs
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append({'hello': 'world'})
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append({'hello': 'world', 'hello2': 'world2'})
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append({'hello': 'world', 'hello2': 'world2', 'hello3': 'world3'})
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # disabled globally
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # test whitelist

        # instance + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append((g, 'cache_me'))
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('cache_me')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        # instance
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append(g)
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # class + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append((G, 'cache_me'))
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # class
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append(G)
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # class name + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('G.cache_me')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('G')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # improper class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('g')
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

        # kwargs
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append({'hello': 'world'})
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append({'hello': 'world', 'hello2': 'world2'})
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me == cached_number
        assert g2.cache_me == cached_number2
        assert g3.cache_me == cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append({'hello': 'world', 'hello2': 'world2', 'hello3': 'world3'})
        cached_number = g.cache_me
        cached_number2 = g2.cache_me
        cached_number3 = g3.cache_me
        assert g.cache_me != cached_number
        assert g2.cache_me != cached_number2
        assert g3.cache_me != cached_number3
        settings.caching.reset()

    def test_cached_method(self):
        np.random.seed(seed)

        class G:
            @decorators.cached_method
            def cache_me(self, b=10): return np.random.uniform()

        g = G()
        cached_number = g.cache_me
        assert g.cache_me == cached_number

        class G:
            @decorators.cached_method(hello="world", hello2="world2")
            def cache_me(self, b=10): return np.random.uniform()

        assert 'hello' in G.cache_me.kwargs
        assert G.cache_me.kwargs['hello'] == 'world'

        g = G()
        g2 = G()

        class G3(G):
            pass

        g3 = G3()

        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3

        # clear_cache method
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        G.cache_me.clear_cache(g)
        assert g.cache_me() != cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3

        # test blacklist

        # function
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append(g.cache_me)
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # instance + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append((g, 'cache_me'))
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('cache_me')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # instance
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append(g)
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # class + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append((G, 'cache_me'))
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # class
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append(G)
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # class name + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('G.cache_me')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('G')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # improper class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append('g')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # kwargs
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append({'hello': 'world'})
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append({'hello': 'world', 'hello2': 'world2'})
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['blacklist'].append({'hello': 'world', 'hello2': 'world2', 'hello3': 'world3'})
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # disabled globally
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # test whitelist

        # function
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append(g.cache_me)
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # instance + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append((g, 'cache_me'))
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('cache_me')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        # instance
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append(g)
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # class + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append((G, 'cache_me'))
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # class
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append(G)
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # class name + name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('G.cache_me')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('G')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # improper class name
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append('g')
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # kwargs
        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append({'hello': 'world'})
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append({'hello': 'world', 'hello2': 'world2'})
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() == cached_number
        assert g2.cache_me() == cached_number2
        assert g3.cache_me() == cached_number3
        settings.caching.reset()

        G.cache_me.clear_cache(g)
        G.cache_me.clear_cache(g2)
        G3.cache_me.clear_cache(g3)
        settings.caching['enabled'] = False
        settings.caching['whitelist'].append({'hello': 'world', 'hello2': 'world2', 'hello3': 'world3'})
        cached_number = g.cache_me()
        cached_number2 = g2.cache_me()
        cached_number3 = g3.cache_me()
        assert g.cache_me() != cached_number
        assert g2.cache_me() != cached_number2
        assert g3.cache_me() != cached_number3
        settings.caching.reset()

        # disabled by non-hashable args
        G.cache_me.clear_cache(g)
        cached_number = g.cache_me(b=np.zeros(1))
        assert g.cache_me(b=np.zeros(1)) != cached_number


# ############# attr.py ############# #

class TestAttrs:
    def test_deep_getattr(self):
        class A:
            def a(self, x, y=None):
                return x + y

        class B:
            def a(self):
                return A()

            def b(self, x):
                return x

            @property
            def b_prop(self):
                return 1

        class C:
            @property
            def b(self):
                return B()

            @property
            def c(self):
                return 0

        with pytest.raises(Exception) as e_info:
            _ = attr.deep_getattr(A(), 'a')
        with pytest.raises(Exception) as e_info:
            _ = attr.deep_getattr(A(), ('a',))
        with pytest.raises(Exception) as e_info:
            _ = attr.deep_getattr(A(), ('a', 1))
        with pytest.raises(Exception) as e_info:
            _ = attr.deep_getattr(A(), ('a', (1,)))
        assert attr.deep_getattr(A(), ('a', (1,), {'y': 1})) == 2
        assert attr.deep_getattr(C(), 'c') == 0
        assert attr.deep_getattr(C(), ['c']) == 0
        assert attr.deep_getattr(C(), ['b', ('b', (1,))]) == 1
        assert attr.deep_getattr(C(), ['b', ('a',), ('a', (1,), {'y': 1})]) == 2
        assert attr.deep_getattr(C(), 'b.b_prop') == 1

    def test_traverse_attr_kwargs(self):
        class A:
            @decorators.custom_property(some_key=0)
            def a(self): pass

        class B:
            @decorators.cached_property(some_key=0, child_cls=A)
            def a(self): pass

            @decorators.custom_method(some_key=1)
            def b(self): pass

        class C:
            @decorators.cached_method(some_key=0, child_cls=B)
            def b(self): pass

            @decorators.custom_property(some_key=1)
            def c(self): pass

        assert hash(str(attr.traverse_attr_kwargs(C))) == 2963162802907041721
        assert hash(str(attr.traverse_attr_kwargs(C, key='some_key'))) == 2963162802907041721
        assert hash(str(attr.traverse_attr_kwargs(C, key='some_key', value=1))) == 8774823009175420311
        assert hash(str(attr.traverse_attr_kwargs(C, key='some_key', value=(0, 1)))) == 2963162802907041721


# ############# checks.py ############# #

class TestChecks:
    def test_is_pandas(self):
        assert not checks.is_pandas(0)
        assert not checks.is_pandas(np.array([0]))
        assert checks.is_pandas(pd.Series([1, 2, 3]))
        assert checks.is_pandas(pd.DataFrame([1, 2, 3]))

    def test_is_series(self):
        assert not checks.is_series(0)
        assert not checks.is_series(np.array([0]))
        assert checks.is_series(pd.Series([1, 2, 3]))
        assert not checks.is_series(pd.DataFrame([1, 2, 3]))

    def test_is_frame(self):
        assert not checks.is_frame(0)
        assert not checks.is_frame(np.array([0]))
        assert not checks.is_frame(pd.Series([1, 2, 3]))
        assert checks.is_frame(pd.DataFrame([1, 2, 3]))

    def test_is_array(self):
        assert not checks.is_any_array(0)
        assert checks.is_any_array(np.array([0]))
        assert checks.is_any_array(pd.Series([1, 2, 3]))
        assert checks.is_any_array(pd.DataFrame([1, 2, 3]))

    def test_is_numba_func(self):
        def test_func(x):
            return x

        @njit
        def test_func_nb(x):
            return x

        assert not checks.is_numba_func(test_func)
        assert checks.is_numba_func(test_func_nb)

    def test_is_hashable(self):
        assert checks.is_hashable(2)
        assert not checks.is_hashable(np.asarray(2))

    def test_is_index_equal(self):
        assert checks.is_index_equal(
            pd.Index([0]),
            pd.Index([0])
        )
        assert not checks.is_index_equal(
            pd.Index([0]),
            pd.Index([1])
        )
        assert not checks.is_index_equal(
            pd.Index([0], name='name'),
            pd.Index([0])
        )
        assert checks.is_index_equal(
            pd.Index([0], name='name'),
            pd.Index([0]),
            strict=False
        )
        assert not checks.is_index_equal(
            pd.MultiIndex.from_arrays([[0], [1]]),
            pd.Index([0])
        )
        assert checks.is_index_equal(
            pd.MultiIndex.from_arrays([[0], [1]]),
            pd.MultiIndex.from_arrays([[0], [1]])
        )
        assert checks.is_index_equal(
            pd.MultiIndex.from_arrays([[0], [1]], names=['name1', 'name2']),
            pd.MultiIndex.from_arrays([[0], [1]], names=['name1', 'name2'])
        )
        assert not checks.is_index_equal(
            pd.MultiIndex.from_arrays([[0], [1]], names=['name1', 'name2']),
            pd.MultiIndex.from_arrays([[0], [1]], names=['name3', 'name4'])
        )

    def test_is_default_index(self):
        assert checks.is_default_index(pd.DataFrame([[1, 2, 3]]).columns)
        assert checks.is_default_index(pd.Series([1, 2, 3]).to_frame().columns)
        assert checks.is_default_index(pd.Index([0, 1, 2]))
        assert not checks.is_default_index(pd.Index([0, 1, 2], name='name'))

    def test_is_equal(self):
        assert checks.is_equal(np.arange(3), np.arange(3), np.array_equal)
        assert not checks.is_equal(np.arange(3), None, np.array_equal)
        assert not checks.is_equal(None, np.arange(3), np.array_equal)
        assert checks.is_equal(None, None, np.array_equal)

    def test_is_namedtuple(self):
        assert checks.is_namedtuple(namedtuple('Hello', ['world'])(*range(1)))
        assert not checks.is_namedtuple((0,))

    def test_method_accepts_argument(self):
        def test(a, *args, b=2, **kwargs):
            pass

        assert checks.method_accepts_argument(test, 'a')
        assert not checks.method_accepts_argument(test, 'args')
        assert checks.method_accepts_argument(test, '*args')
        assert checks.method_accepts_argument(test, 'b')
        assert not checks.method_accepts_argument(test, 'kwargs')
        assert checks.method_accepts_argument(test, '**kwargs')
        assert not checks.method_accepts_argument(test, 'c')

    def test_is_deep_equal(self):
        sr = pd.Series([1, 2, 3], index=pd.Index(['a', 'b', 'c'], name='index'), name='name')
        sr2 = pd.Series([1., 2., 3.], index=sr.index, name=sr.name)
        sr3 = pd.Series([np.nan, 2., 3.], index=sr.index, name=sr.name)
        sr4 = pd.Series([np.nan, 2., 3. + 1e-15], index=sr.index, name=sr.name)
        assert checks.is_deep_equal(sr, sr.copy())
        assert checks.is_deep_equal(sr2, sr2.copy())
        assert checks.is_deep_equal(sr3, sr3.copy())
        assert checks.is_deep_equal(sr4, sr4.copy())
        assert not checks.is_deep_equal(sr, sr2)
        assert checks.is_deep_equal(sr3, sr4)
        assert not checks.is_deep_equal(sr3, sr4, rtol=0, atol=1e-16)
        assert not checks.is_deep_equal(sr3, sr4, check_exact=True)
        assert not checks.is_deep_equal(sr, sr.rename('name2'))
        assert checks.is_deep_equal(sr.index, sr.copy().index)
        assert not checks.is_deep_equal(sr.index, sr.copy().index[:-1])
        assert not checks.is_deep_equal(sr.index, sr.copy().rename('indx2'))
        assert checks.is_deep_equal(sr.to_frame(), sr.to_frame().copy())
        assert not checks.is_deep_equal(sr, sr.to_frame().copy())
        assert not checks.is_deep_equal(sr.to_frame(), sr.copy())

        arr = np.array([1, 2, 3])
        arr2 = np.array([1., 2., 3.])
        arr3 = np.array([np.nan, 2., 3.])
        arr4 = np.array([np.nan, 2., 3 + 1e-15])
        assert checks.is_deep_equal(arr, arr.copy())
        assert checks.is_deep_equal(arr2, arr2.copy())
        assert checks.is_deep_equal(arr3, arr3.copy())
        assert checks.is_deep_equal(arr4, arr4.copy())
        assert not checks.is_deep_equal(arr, arr2)
        assert checks.is_deep_equal(arr3, arr4)
        assert not checks.is_deep_equal(arr3, arr4, rtol=0, atol=1e-16)
        assert not checks.is_deep_equal(arr3, arr4, check_exact=True)

        records_arr = np.asarray([
            (1, 1.),
            (2, 2.),
            (3, 3.),
        ], dtype=np.dtype([
            ('a', np.int32),
            ('b', np.float64)
        ]))
        records_arr2 = np.asarray([
            (1., 1.),
            (2., 2.),
            (3., 3.),
        ], dtype=np.dtype([
            ('a', np.float64),
            ('b', np.float64)
        ]))
        records_arr3 = np.asarray([
            (np.nan, 1.),
            (2., 2.),
            (3., 3.),
        ], dtype=np.dtype([
            ('a', np.float64),
            ('b', np.float64)
        ]))
        records_arr4 = np.asarray([
            (np.nan, 1.),
            (2., 2.),
            (3. + 1e-15, 3.),
        ], dtype=np.dtype([
            ('a', np.float64),
            ('b', np.float64)
        ]))
        assert checks.is_deep_equal(records_arr, records_arr.copy())
        assert checks.is_deep_equal(records_arr2, records_arr2.copy())
        assert checks.is_deep_equal(records_arr3, records_arr3.copy())
        assert checks.is_deep_equal(records_arr4, records_arr4.copy())
        assert not checks.is_deep_equal(records_arr, records_arr2)
        assert checks.is_deep_equal(records_arr3, records_arr4)
        assert not checks.is_deep_equal(records_arr3, records_arr4, rtol=0, atol=1e-16)
        assert not checks.is_deep_equal(records_arr3, records_arr4, check_exact=True)

        assert checks.is_deep_equal([sr, arr, records_arr], [sr, arr, records_arr])
        assert not checks.is_deep_equal([sr, arr, records_arr], [sr, arr, records_arr2])
        assert not checks.is_deep_equal([sr, arr, records_arr], [sr, records_arr, arr])
        assert checks.is_deep_equal(
            {'sr': sr, 'arr': arr, 'records_arr': records_arr},
            {'sr': sr, 'arr': arr, 'records_arr': records_arr}
        )
        assert not checks.is_deep_equal(
            {'sr': sr, 'arr': arr, 'records_arr': records_arr},
            {'sr': sr, 'arr': arr, 'records_arr2': records_arr}
        )
        assert not checks.is_deep_equal(
            {'sr': sr, 'arr': arr, 'records_arr': records_arr},
            {'sr': sr, 'arr': arr, 'records_arr': records_arr2}
        )

        assert checks.is_deep_equal(0, 0)
        assert not checks.is_deep_equal(0, False)
        assert not checks.is_deep_equal(0, 1)
        assert checks.is_deep_equal(lambda x: x, lambda x: x)
        assert not checks.is_deep_equal(lambda x: x, lambda x: 2 * x)

    def test_assert_in(self):
        checks.assert_in(0, (0, 1))
        with pytest.raises(Exception) as e_info:
            checks.assert_in(2, (0, 1))

    def test_assert_numba_func(self):
        def test_func(x):
            return x

        @njit
        def test_func_nb(x):
            return x

        checks.assert_numba_func(test_func_nb)
        with pytest.raises(Exception) as e_info:
            checks.assert_numba_func(test_func)

    def test_assert_not_none(self):
        checks.assert_not_none(0)
        with pytest.raises(Exception) as e_info:
            checks.assert_not_none(None)

    def test_assert_type(self):
        checks.assert_type(0, int)
        checks.assert_type(np.zeros(1), (np.ndarray, pd.Series))
        checks.assert_type(pd.Series([1, 2, 3]), (np.ndarray, pd.Series))
        with pytest.raises(Exception) as e_info:
            checks.assert_type(pd.DataFrame([1, 2, 3]), (np.ndarray, pd.Series))

    def test_assert_subclass(self):
        class A:
            pass

        class B(A):
            pass

        class C(B):
            pass

        checks.assert_subclass(B, A)
        checks.assert_subclass(C, B)
        checks.assert_subclass(C, A)
        with pytest.raises(Exception) as e_info:
            checks.assert_subclass(A, B)

    def test_assert_type_equal(self):
        checks.assert_type_equal(0, 1)
        checks.assert_type_equal(np.zeros(1), np.empty(1))
        with pytest.raises(Exception) as e_info:
            checks.assert_type(0, np.zeros(1))

    def test_assert_dtype(self):
        checks.assert_dtype(np.zeros(1), np.float)
        checks.assert_dtype(pd.Series([1, 2, 3]), np.int)
        checks.assert_dtype(pd.DataFrame({'a': [1, 2], 'b': [3, 4]}), np.int)
        with pytest.raises(Exception) as e_info:
            checks.assert_dtype(pd.DataFrame({'a': [1, 2], 'b': [3., 4.]}), np.int)

    def test_assert_subdtype(self):
        checks.assert_subdtype([0], np.number)
        checks.assert_subdtype(np.array([1, 2, 3]), np.number)
        checks.assert_subdtype(pd.DataFrame({'a': [1, 2], 'b': [3., 4.]}), np.number)
        with pytest.raises(Exception) as e_info:
            checks.assert_subdtype(np.array([1, 2, 3]), np.float)
        with pytest.raises(Exception) as e_info:
            checks.assert_subdtype(pd.DataFrame({'a': [1, 2], 'b': [3., 4.]}), np.float)

    def test_assert_dtype_equal(self):
        checks.assert_dtype_equal([1], [1, 1, 1])
        checks.assert_dtype_equal(pd.Series([1, 2, 3]), pd.DataFrame([[1, 2, 3]]))
        checks.assert_dtype_equal(pd.DataFrame([[1, 2, 3.]]), pd.DataFrame([[1, 2, 3.]]))
        with pytest.raises(Exception) as e_info:
            checks.assert_dtype_equal(pd.DataFrame([[1, 2, 3]]), pd.DataFrame([[1, 2, 3.]]))

    def test_assert_ndim(self):
        checks.assert_ndim(0, 0)
        checks.assert_ndim(np.zeros(1), 1)
        checks.assert_ndim(pd.Series([1, 2, 3]), (1, 2))
        checks.assert_ndim(pd.DataFrame([1, 2, 3]), (1, 2))
        with pytest.raises(Exception) as e_info:
            checks.assert_ndim(np.zeros((3, 3, 3)), (1, 2))

    def test_assert_len_equal(self):
        checks.assert_len_equal([[1]], [[2]])
        checks.assert_len_equal([[1]], [[2, 3]])
        with pytest.raises(Exception) as e_info:
            checks.assert_len_equal([[1]], [[2], [3]])

    def test_assert_shape_equal(self):
        checks.assert_shape_equal(0, 1)
        checks.assert_shape_equal([1, 2, 3], np.asarray([1, 2, 3]))
        checks.assert_shape_equal([1, 2, 3], pd.Series([1, 2, 3]))
        checks.assert_shape_equal(np.zeros((3, 3)), pd.Series([1, 2, 3]), axis=0)
        checks.assert_shape_equal(np.zeros((2, 3)), pd.Series([1, 2, 3]), axis=(1, 0))
        with pytest.raises(Exception) as e_info:
            checks.assert_shape_equal(np.zeros((2, 3)), pd.Series([1, 2, 3]), axis=(0, 1))

    def test_assert_index_equal(self):
        checks.assert_index_equal(pd.Index([1, 2, 3]), pd.Index([1, 2, 3]))
        with pytest.raises(Exception) as e_info:
            checks.assert_index_equal(pd.Index([1, 2, 3]), pd.Index([2, 3, 4]))

    def test_assert_meta_equal(self):
        index = ['x', 'y', 'z']
        columns = ['a', 'b', 'c']
        checks.assert_meta_equal(np.array([1, 2, 3]), np.array([1, 2, 3]))
        checks.assert_meta_equal(pd.Series([1, 2, 3], index=index), pd.Series([1, 2, 3], index=index))
        checks.assert_meta_equal(pd.DataFrame([[1, 2, 3]], columns=columns), pd.DataFrame([[1, 2, 3]], columns=columns))
        with pytest.raises(Exception) as e_info:
            checks.assert_meta_equal(pd.Series([1, 2]), pd.DataFrame([1, 2]))

        with pytest.raises(Exception) as e_info:
            checks.assert_meta_equal(pd.DataFrame([1, 2]), pd.DataFrame([1, 2, 3]))

        with pytest.raises(Exception) as e_info:
            checks.assert_meta_equal(pd.DataFrame([1, 2, 3]), pd.DataFrame([1, 2, 3], index=index))

        with pytest.raises(Exception) as e_info:
            checks.assert_meta_equal(pd.DataFrame([[1, 2, 3]]), pd.DataFrame([[1, 2, 3]], columns=columns))

    def test_assert_array_equal(self):
        index = ['x', 'y', 'z']
        columns = ['a', 'b', 'c']
        checks.assert_array_equal(np.array([1, 2, 3]), np.array([1, 2, 3]))
        checks.assert_array_equal(pd.Series([1, 2, 3], index=index), pd.Series([1, 2, 3], index=index))
        checks.assert_array_equal(pd.DataFrame([[1, 2, 3]], columns=columns),
                                  pd.DataFrame([[1, 2, 3]], columns=columns))
        with pytest.raises(Exception) as e_info:
            checks.assert_array_equal(np.array([1, 2]), np.array([1, 2, 3]))

    def test_assert_level_not_exists(self):
        i = pd.Index(['x', 'y', 'z'], name='i')
        multi_i = pd.MultiIndex.from_arrays([['x', 'y', 'z'], ['x2', 'y2', 'z2']], names=['i', 'i2'])
        checks.assert_level_not_exists(i, 'i2')
        checks.assert_level_not_exists(multi_i, 'i3')
        with pytest.raises(Exception) as e_info:
            checks.assert_level_not_exists(i, 'i')
            checks.assert_level_not_exists(multi_i, 'i')

    def test_assert_equal(self):
        checks.assert_equal(0, 0)
        checks.assert_equal(False, False)
        with pytest.raises(Exception) as e_info:
            checks.assert_equal(0, 1)

    def test_assert_dict_valid(self):
        checks.assert_dict_valid(dict(a=2, b=3), [['a', 'b', 'c']])
        with pytest.raises(Exception) as e_info:
            checks.assert_dict_valid(dict(a=2, b=3, d=4), [['a', 'b', 'c']])
        checks.assert_dict_valid(dict(a=2, b=3, c=dict(d=4, e=5)), [['a', 'b', 'c'], ['d', 'e']])
        with pytest.raises(Exception) as e_info:
            checks.assert_dict_valid(dict(a=2, b=3, c=dict(d=4, f=5)), [['a', 'b', 'c'], ['d', 'e']])


# ############# math.py ############# #

class TestMath:
    def test_is_close(self):
        a = 0.3
        b = 0.1 + 0.2

        # test scalar
        assert math.is_close_nb(a, a)
        assert math.is_close_nb(a, b)
        assert math.is_close_nb(-a, -b)
        assert not math.is_close_nb(-a, b)
        assert not math.is_close_nb(a, -b)
        assert math.is_close_nb(1e10 + a, 1e10 + b)

        # test np.nan
        assert not math.is_close_nb(np.nan, b)
        assert not math.is_close_nb(a, np.nan)

        # test np.inf
        assert not math.is_close_nb(np.inf, b)
        assert not math.is_close_nb(a, np.inf)
        assert not math.is_close_nb(-np.inf, b)
        assert not math.is_close_nb(a, -np.inf)
        assert not math.is_close_nb(-np.inf, -np.inf)
        assert not math.is_close_nb(np.inf, np.inf)
        assert not math.is_close_nb(-np.inf, np.inf)

    def test_is_close_or_less(self):
        a = 0.3
        b = 0.1 + 0.2

        # test scalar
        assert math.is_close_or_less_nb(a, a)
        assert math.is_close_or_less_nb(a, b)
        assert math.is_close_or_less_nb(-a, -b)
        assert math.is_close_or_less_nb(-a, b)
        assert not math.is_close_or_less_nb(a, -b)
        assert math.is_close_or_less_nb(1e10 + a, 1e10 + b)

        # test np.nan
        assert not math.is_close_or_less_nb(np.nan, b)
        assert not math.is_close_or_less_nb(a, np.nan)

        # test np.inf
        assert not math.is_close_or_less_nb(np.inf, b)
        assert math.is_close_or_less_nb(a, np.inf)
        assert math.is_close_or_less_nb(-np.inf, b)
        assert not math.is_close_or_less_nb(a, -np.inf)
        assert not math.is_close_or_less_nb(-np.inf, -np.inf)
        assert not math.is_close_or_less_nb(np.inf, np.inf)
        assert math.is_close_or_less_nb(-np.inf, np.inf)

    def test_is_less(self):
        a = 0.3
        b = 0.1 + 0.2

        # test scalar
        assert not math.is_less_nb(a, a)
        assert not math.is_less_nb(a, b)
        assert not math.is_less_nb(-a, -b)
        assert math.is_less_nb(-a, b)
        assert not math.is_less_nb(a, -b)
        assert not math.is_less_nb(1e10 + a, 1e10 + b)

        # test np.nan
        assert not math.is_less_nb(np.nan, b)
        assert not math.is_less_nb(a, np.nan)

        # test np.inf
        assert not math.is_less_nb(np.inf, b)
        assert math.is_less_nb(a, np.inf)
        assert math.is_less_nb(-np.inf, b)
        assert not math.is_less_nb(a, -np.inf)
        assert not math.is_less_nb(-np.inf, -np.inf)
        assert not math.is_less_nb(np.inf, np.inf)
        assert math.is_less_nb(-np.inf, np.inf)

    def test_is_addition_zero(self):
        a = 0.3
        b = 0.1 + 0.2

        assert not math.is_addition_zero_nb(a, b)
        assert math.is_addition_zero_nb(-a, b)
        assert math.is_addition_zero_nb(a, -b)
        assert not math.is_addition_zero_nb(-a, -b)

    def test_add_nb(self):
        a = 0.3
        b = 0.1 + 0.2

        assert math.add_nb(a, b) == a + b
        assert math.add_nb(-a, b) == 0
        assert math.add_nb(a, -b) == 0
        assert math.add_nb(-a, -b) == -(a + b)


# ############# array.py ############# #

class TestArray:
    def test_is_sorted(self):
        assert array.is_sorted(np.array([0, 1, 2, 3, 4]))
        assert array.is_sorted(np.array([0, 1]))
        assert array.is_sorted(np.array([0]))
        assert not array.is_sorted(np.array([1, 0]))
        assert not array.is_sorted(np.array([0, 1, 2, 4, 3]))
        # nb
        assert array.is_sorted_nb(np.array([0, 1, 2, 3, 4]))
        assert array.is_sorted_nb(np.array([0, 1]))
        assert array.is_sorted_nb(np.array([0]))
        assert not array.is_sorted_nb(np.array([1, 0]))
        assert not array.is_sorted_nb(np.array([0, 1, 2, 4, 3]))

    def test_insert_argsort_nb(self):
        a = np.random.uniform(size=1000)
        A = a.copy()
        I = np.arange(len(A))
        array.insert_argsort_nb(A, I)
        np.testing.assert_array_equal(np.sort(a), A)
        np.testing.assert_array_equal(a[I], A)

    def test_get_ranges_arr(self):
        np.testing.assert_array_equal(
            array.get_ranges_arr(0, 3),
            np.array([0, 1, 2])
        )
        np.testing.assert_array_equal(
            array.get_ranges_arr(0, [1, 2, 3]),
            np.array([0, 0, 1, 0, 1, 2])
        )
        np.testing.assert_array_equal(
            array.get_ranges_arr([0, 3], [3, 6]),
            np.array([0, 1, 2, 3, 4, 5])
        )

    def test_uniform_summing_to_one_nb(self):
        @njit
        def set_seed():
            np.random.seed(seed)

        set_seed()
        np.testing.assert_array_almost_equal(
            array.uniform_summing_to_one_nb(10),
            np.array([
                5.808361e-02, 9.791091e-02, 2.412011e-05, 2.185215e-01,
                2.241184e-01, 2.456528e-03, 1.308789e-01, 1.341822e-01,
                8.453816e-02, 4.928569e-02
            ])
        )
        assert np.sum(array.uniform_summing_to_one_nb(10)) == 1

    def test_renormalize(self):
        assert array.renormalize(0, [0, 10], [0, 1]) == 0
        assert array.renormalize(10, [0, 10], [0, 1]) == 1
        np.testing.assert_array_equal(
            array.renormalize(np.array([0, 2, 4, 6, 8, 10]), [0, 10], [0, 1]),
            np.array([0., 0.2, 0.4, 0.6, 0.8, 1.])
        )
        np.testing.assert_array_equal(
            array.renormalize_nb(np.array([0, 2, 4, 6, 8, 10]), [0, 10], [0, 1]),
            np.array([0., 0.2, 0.4, 0.6, 0.8, 1.])
        )

    def test_min_rel_rescale(self):
        np.testing.assert_array_equal(
            array.min_rel_rescale(np.array([2, 4, 6]), [10, 20]),
            np.array([10., 15., 20.])
        )
        np.testing.assert_array_equal(
            array.min_rel_rescale(np.array([5, 6, 7]), [10, 20]),
            np.array([10., 12., 14.])
        )
        np.testing.assert_array_equal(
            array.min_rel_rescale(np.array([5, 5, 5]), [10, 20]),
            np.array([10., 10., 10.])
        )

    def test_max_rel_rescale(self):
        np.testing.assert_array_equal(
            array.max_rel_rescale(np.array([2, 4, 6]), [10, 20]),
            np.array([10., 15., 20.])
        )
        np.testing.assert_array_equal(
            array.max_rel_rescale(np.array([5, 6, 7]), [10, 20]),
            np.array([14.285714285714286, 17.142857142857142, 20.])
        )
        np.testing.assert_array_equal(
            array.max_rel_rescale(np.array([5, 5, 5]), [10, 20]),
            np.array([20., 20., 20.])
        )

    def test_rescale_float_to_int_nb(self):
        @njit
        def set_seed():
            np.random.seed(seed)

        set_seed()
        np.testing.assert_array_equal(
            array.rescale_float_to_int_nb(np.array([0.3, 0.3, 0.3, 0.1]), [10, 20], 70),
            np.array([17, 14, 22, 17])
        )
        assert np.sum(array.rescale_float_to_int_nb(np.array([0.3, 0.3, 0.3, 0.1]), [10, 20], 70)) == 70


# ############# random.py ############# #


class TestRandom:
    def test_set_seed(self):
        random.set_seed(seed)

        def test_seed():
            return np.random.uniform(0, 1)

        assert test_seed() == 0.3745401188473625

        if 'NUMBA_DISABLE_JIT' not in os.environ or os.environ['NUMBA_DISABLE_JIT'] != '1':
            @njit
            def test_seed_nb():
                return np.random.uniform(0, 1)

            assert test_seed_nb() == 0.3745401188473625


# ############# enum.py ############# #

Enum = namedtuple('Enum', ['Attr1', 'Attr2'])(*range(2))


class TestEnum:
    def test_caseins_getattr(self):
        assert enum.caseins_getattr(Enum, 'Attr1') == 0
        assert enum.caseins_getattr(Enum, 'attr1') == 0
        assert enum.caseins_getattr(Enum, 'Attr2') == 1
        assert enum.caseins_getattr(Enum, 'attr2') == 1
        with pytest.raises(Exception) as e_info:
            enum.caseins_getattr(Enum, 'Attr3')

    def test_convert_str_enum_value(self):
        assert enum.convert_str_enum_value(Enum, 0) == 0
        assert enum.convert_str_enum_value(Enum, 10) == 10
        assert enum.convert_str_enum_value(Enum, 10.) == 10.
        assert enum.convert_str_enum_value(Enum, 'Attr1') == 0
        assert enum.convert_str_enum_value(Enum, 'attr1') == 0
        assert enum.convert_str_enum_value(Enum, ('attr1', 'attr2')) == (0, 1)
        assert enum.convert_str_enum_value(Enum, [['attr1', 'attr2']]) == [[0, 1]]

    def test_to_value_map(self):
        assert enum.to_value_map(Enum) == {-1: None, 0: 'Attr1', 1: 'Attr2'}


# ############# params.py ############# #

class TestParams:
    def test_create_param_combs(self):
        assert params.create_param_combs(
            (combinations, [0, 1, 2, 3], 2)) == [
                   [0, 0, 0, 1, 1, 2],
                   [1, 2, 3, 2, 3, 3]
               ]
        assert params.create_param_combs(
            (product, (combinations, [0, 1, 2, 3], 2), [4, 5])) == [
                   [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2],
                   [1, 1, 2, 2, 3, 3, 2, 2, 3, 3, 3, 3],
                   [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5]
               ]
        assert params.create_param_combs(
            (product, (combinations, [0, 1, 2], 2), (combinations, [3, 4, 5], 2))) == [
                   [0, 0, 0, 0, 0, 0, 1, 1, 1],
                   [1, 1, 1, 2, 2, 2, 2, 2, 2],
                   [3, 3, 4, 3, 3, 4, 3, 3, 4],
                   [4, 5, 5, 4, 5, 5, 4, 5, 5]
               ]


# ############# datetime.py ############# #

class TestDatetime:
    def test_to_timedelta(self):
        assert datetime.to_timedelta('d') == pd.to_timedelta('1d')

    def test_get_utc_tz(self):
        assert datetime.get_utc_tz().utcoffset(_datetime.now()) == _timedelta(0)

    def test_get_local_tz(self):
        assert datetime.get_local_tz().utcoffset(_datetime.now()) == _datetime.now().astimezone(None).utcoffset()

    def test_convert_tzaware_time(self):
        assert datetime.convert_tzaware_time(
            _time(12, 0, 0, tzinfo=datetime.get_utc_tz()), _timezone(_timedelta(hours=2))) == \
               _time(14, 0, 0, tzinfo=_timezone(_timedelta(hours=2)))

    def test_tzaware_to_naive_time(self):
        assert datetime.tzaware_to_naive_time(
            _time(12, 0, 0, tzinfo=datetime.get_utc_tz()), _timezone(_timedelta(hours=2))) == _time(14, 0, 0)

    def test_naive_to_tzaware_time(self):
        assert datetime.naive_to_tzaware_time(
            _time(12, 0, 0), _timezone(_timedelta(hours=2))) == \
               datetime.convert_tzaware_time(
                   _time(12, 0, 0, tzinfo=datetime.get_local_tz()), _timezone(_timedelta(hours=2)))

    def test_convert_naive_time(self):
        assert datetime.convert_naive_time(
            _time(12, 0, 0), _timezone(_timedelta(hours=2))) == \
               datetime.tzaware_to_naive_time(
                   _time(12, 0, 0, tzinfo=datetime.get_local_tz()), _timezone(_timedelta(hours=2)))

    def test_is_tz_aware(self):
        assert not datetime.is_tz_aware(pd.Timestamp('2020-01-01'))
        assert datetime.is_tz_aware(pd.Timestamp('2020-01-01', tz=datetime.get_utc_tz()))

    def test_to_timezone(self):
        assert datetime.to_timezone('UTC') == pytz.UTC
        assert datetime.to_timezone('Europe/Berlin') == pytz.timezone('Europe/Berlin')
        assert datetime.to_timezone('+0500') == _timezone(_timedelta(hours=5))
        assert datetime.to_timezone(_timezone(_timedelta(hours=1))) == _timezone(_timedelta(hours=1))
        assert datetime.to_timezone(pytz.timezone('Europe/Berlin')) == pytz.timezone('Europe/Berlin')
        assert datetime.to_timezone(1) == _timezone(_timedelta(hours=1))
        assert datetime.to_timezone(0.5) == _timezone(_timedelta(hours=0.5))
        with pytest.raises(Exception) as e_info:
            _ = datetime.to_timezone('+05')

    def test_to_tzaware_datetime(self):
        assert datetime.to_tzaware_datetime(0.5) == \
               _datetime(1970, 1, 1, 0, 0, 0, 500000, tzinfo=datetime.get_utc_tz())
        assert datetime.to_tzaware_datetime(0) == \
               _datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=datetime.get_utc_tz())
        assert datetime.to_tzaware_datetime(pd.Timestamp('2020-01-01').value) == \
               _datetime(2020, 1, 1).replace(tzinfo=datetime.get_utc_tz())
        assert datetime.to_tzaware_datetime('2020-01-01') == \
               _datetime(2020, 1, 1).replace(tzinfo=datetime.get_local_tz())
        assert datetime.to_tzaware_datetime(pd.Timestamp('2020-01-01')) == \
               _datetime(2020, 1, 1).replace(tzinfo=datetime.get_local_tz())
        assert datetime.to_tzaware_datetime(pd.Timestamp('2020-01-01', tz=datetime.get_utc_tz())) == \
               _datetime(2020, 1, 1).replace(tzinfo=datetime.get_utc_tz())
        assert datetime.to_tzaware_datetime(_datetime(2020, 1, 1)) == \
               _datetime(2020, 1, 1).replace(tzinfo=datetime.get_local_tz())
        assert datetime.to_tzaware_datetime(_datetime(2020, 1, 1, tzinfo=datetime.get_utc_tz())) == \
               _datetime(2020, 1, 1).replace(tzinfo=datetime.get_utc_tz())
        assert datetime.to_tzaware_datetime(
            _datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.get_utc_tz()), tz=datetime.get_local_tz()) == \
               _datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.get_utc_tz()).astimezone(datetime.get_local_tz())
        with pytest.raises(Exception) as e_info:
            _ = datetime.to_tzaware_datetime('2020-01-001')

    def test_datetime_to_ms(self):
        assert datetime.datetime_to_ms(_datetime(2020, 1, 1)) == \
               1577836800000 - _datetime(2020, 1, 1).astimezone(None).utcoffset().total_seconds() * 1000
        assert datetime.datetime_to_ms(_datetime(2020, 1, 1, tzinfo=datetime.get_utc_tz())) == 1577836800000


# ############# schedule.py ############# #


class TestScheduleManager:
    def test_every(self):
        manager = schedule.ScheduleManager()
        job = manager.every()
        assert job.interval == 1
        assert job.unit == 'seconds'
        assert job.at_time is None
        assert job.start_day is None

        job = manager.every(10, 'minutes')
        assert job.interval == 10
        assert job.unit == 'minutes'
        assert job.at_time is None
        assert job.start_day is None

        job = manager.every('hour')
        assert job.interval == 1
        assert job.unit == 'hours'
        assert job.at_time is None
        assert job.start_day is None

        job = manager.every('10:30')
        assert job.interval == 1
        assert job.unit == 'days'
        assert job.at_time == _time(10, 30)
        assert job.start_day is None

        job = manager.every('day', '10:30')
        assert job.interval == 1
        assert job.unit == 'days'
        assert job.at_time == _time(10, 30)
        assert job.start_day is None

        job = manager.every('day', _time(9, 30, tzinfo=datetime.get_utc_tz()))
        assert job.interval == 1
        assert job.unit == 'days'
        assert job.at_time == datetime.tzaware_to_naive_time(
            _time(9, 30, tzinfo=datetime.get_utc_tz()), datetime.get_local_tz())
        assert job.start_day is None

        job = manager.every('monday')
        assert job.interval == 1
        assert job.unit == 'weeks'
        assert job.at_time is None
        assert job.start_day == 'monday'

        job = manager.every('wednesday', '13:15')
        assert job.interval == 1
        assert job.unit == 'weeks'
        assert job.at_time == _time(13, 15)
        assert job.start_day == 'wednesday'

        job = manager.every('minute', ':17')
        assert job.interval == 1
        assert job.unit == 'minutes'
        assert job.at_time == _time(0, 0, 17)
        assert job.start_day is None

    def test_start(self):
        kwargs = dict(call_count=0)

        def job_func(kwargs):
            kwargs['call_count'] += 1
            if kwargs['call_count'] == 5:
                raise KeyboardInterrupt

        manager = schedule.ScheduleManager()
        manager.every().do(job_func, kwargs)
        manager.start()
        assert kwargs['call_count'] == 5

    def test_async_start(self):
        kwargs = dict(call_count=0)

        def job_func(kwargs):
            kwargs['call_count'] += 1
            if kwargs['call_count'] == 5:
                raise schedule.CancelledError

        manager = schedule.ScheduleManager()
        manager.every().do(job_func, kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(manager.async_start())
        assert kwargs['call_count'] == 5
