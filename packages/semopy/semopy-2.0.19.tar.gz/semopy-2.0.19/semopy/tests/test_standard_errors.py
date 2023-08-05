#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import numpy as np
import pandas as pd
from itertools import combinations
from ..model import Model
from ..model_means import ModelMeans
from ..model_effects import ModelEffects
from ..examples import multivariate_regression


class TestStandardErrors(unittest.TestCase):
    def evaluate(self, desc: str, data: pd.DataFrame):
        g = data['group'].copy()
        data = data - data.mean()
        data['group'] = g
        model = Model(desc)
        model_means = ModelMeans(desc, intercepts=False)
        model_effects = ModelEffects(desc, intercepts=False)
        assert model.fit(data).success, "Optimization failure."
        r = model_means.fit(data)
        if type(r) is tuple:
            assert r[0].success and r[1].success, "Optimization failure."
        else:
            assert r.success, "Optimization failure."
        r = model_effects.fit(data, group='group')
        if type(r) is tuple:
            assert r[0].success and r[1].success, "Optimization failure."
        else:
            assert r.success, "Optimization failure."
        se = list()
        ins = model.inspect(information='expected')
        ins = ins[ins['op'] == '~'].sort_values(['lval', 'rval'], 0)
        se.append(ins['Std. Err'].values)
        ins = model.inspect(information='observed')
        ins = ins[ins['op'] == '~'].sort_values(['lval', 'rval'], 0)
        se.append(ins['Std. Err'].values)
        ins = model_means.inspect(information='expected')
        ins = ins[ins['op'] == '~'].sort_values(['lval', 'rval'], 0)
        se.append(ins['Std. Err'].values)
        ins = model_means.inspect(information='observed')
        ins = ins[ins['op'] == '~'].sort_values(['lval', 'rval'], 0)
        se.append(ins['Std. Err'].values)
        ins = model_effects.inspect(information='expected')
        ins = ins[ins['op'] == '~'].sort_values(['lval', 'rval'], 0)
        se.append(ins['Std. Err'].values)
        ins = model_effects.inspect(information='observed')
        ins = ins[ins['op'] == '~'].sort_values(['lval', 'rval'], 0)
        se.append(ins['Std. Err'].values)
        for a, b in combinations(se, 2):
            assert np.max(np.abs(a - b) / b) < 1e-1, "Standard errors diverge."

    def test_multivariate_regression(self):
        desc = multivariate_regression.get_model()
        data = multivariate_regression.get_data()
        data['group'] = data.index
        self.evaluate(desc, data)
