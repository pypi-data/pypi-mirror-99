# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2021, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
import pytest
from numpy.testing import assert_allclose
import numpy as np
    
def create_evaluation_model():
    import biosteam as bst
    from chaospy.distributions import Uniform
    sys = bst.System(None, ())
    model = bst.Model(sys)
    
    parameter_box = [100.]
    @model.parameter(bounds=[90, 110],
                     distribution=Uniform(90, 110),
                     units='kg/hr')
    def set_parameter(parameter_1):
        parameter_box[0] = parameter_1
    
    @model.parameter(bounds=[0., 1.],
                     distribution=Uniform(0., 1.))
    def set_parameter(parameter_2): ...
    
    @model.metric
    def good_metric():
        p = parameter_box[0]
        return 2. * p * p / (p + 100.) 
    
    switch_box = [False]
    @model.metric
    def bad_metric():
        give_nan = switch_box[0]
        switch_box[0] = not give_nan
        p = parameter_box[0]
        return float('Nan') if give_nan else 2. * p * p / (p + 100.) 
    
    @model.metric
    def non_correlated_metric():
        return float(switch_box[0])
    
    sample = model.sample(1000, 'L')
    model.load_samples(sample)
    model.evaluate()
    return model

@pytest.fixture
def model():
    return create_evaluation_model()
    
def test_pearson_r(model):
    with pytest.raises(ValueError):
        rho, p = model.pearson_r(filter='none')
    
    rho, p = model.pearson_r(filter='propagate nan')
    NaN = float('NaN')
    expected = np.array([[1., NaN, 0.],
                         [0,  NaN, 0.]])
    index = ~np.isnan(expected)
    assert_allclose(rho.values[index], expected[index], atol=0.15)
    
    with pytest.raises(ValueError):
        rho, p = model.pearson_r(filter='raise nan error')
    
    rho, p = model.pearson_r(filter='omit nan')
    expected = np.array([[1., 1., 0.],
                         [0,  0., 0.]])
    assert_allclose(rho, expected, atol=0.15)
    assert_allclose(rho, model.pearson_r(filter='omit nan')[0], atol=0.01)

def test_spearman_r(model):
    rho, p = model.spearman_r()
    NaN = float('NaN')
    expected = np.array([[1., NaN, 0.],
                         [0,  NaN, 0.]])
    index = ~np.isnan(expected)
    assert_allclose(rho.values[index], expected[index], atol=0.15)
    
    rho, p = model.spearman_r(filter='omit nan')
    expected = np.array([[1., 1., 0.],
                         [0,  0., 0.]])
    assert_allclose(rho, expected, atol=0.15)
    assert_allclose(rho, model.spearman_r(filter='omit nan')[0], atol=0.01)
    
def test_kendall_tau(model):
    rho, p = model.kendall_tau()
    NaN = float('NaN')
    expected = np.array([[1., NaN, 0.],
                         [0,  NaN, 0.]])
    index = ~np.isnan(expected)
    assert_allclose(rho.values[index], expected[index], atol=0.15)
    
    tau, p = model.kendall_tau(filter='omit nan')
    expected = np.array([[1., 1., 0.],
                         [0,  0., 0.]])
    assert_allclose(tau, expected, atol=0.15)
    assert_allclose(tau, model.kendall_tau(filter='omit nan')[0])
    
def test_kolmogorov_smirnov_d(model):
    rho, p = model.kolmogorov_smirnov_d()
    NaN = float('NaN')
    expected = np.array([[0.17, NaN, 1.0],
                         [1.0,  NaN, 0.5]])
    index = ~np.isnan(expected)
    assert_allclose(rho.values[index], expected[index], atol=0.15)
    
    d, p = model.kolmogorov_smirnov_d(filter='omit nan')
    expected = np.array([[0.17, 0.194, 1.0],
                         [1.0,  1.0, 0.5]])
    assert_allclose(d, expected, atol=0.15)
    assert_allclose(d, model.kolmogorov_smirnov_d(filter='omit nan')[0])
    
def test_model_index():
    from biorefineries.sugarcane import sugarcane_sys, flowsheet as f
    import biosteam as bst
    
    # Make sure repeated metrics raise an error
    biorefinery = bst.process_tools.UnitGroup('Biorefinery', sugarcane_sys.units)
    heating_duty = bst.Metric('Heating duty', biorefinery.get_heating_duty, 'GJ/hr')
    heating_duty_repeated = bst.Metric('Heating duty', biorefinery.get_heating_duty, 'GJ/hr')
    with pytest.raises(ValueError):
        model = bst.Model(sugarcane_sys, [heating_duty, heating_duty_repeated])
    
    model = bst.Model(sugarcane_sys, [heating_duty])
    
    # Make sure repeated parameters raise an error
    R301 = f.unit.R301
    @model.parameter(element=R301)
    def set_efficiency(efficiency):
        R301.efficiency = efficiency
    
    with pytest.raises(ValueError):
        @model.parameter(element=R301)
        def set_efficiency(efficiency):
            R301.efficiency = efficiency
    
    bst.default()
    
def test_model_sample(model):
    # Just make sure they run
    for rule in ('MORRIS', 'FAST', 'RBD', 'SOBOL'): model.sample(100, rule)
    problem = model.problem()
    for rule in ('MORRIS', 'FAST', 'RBD', 'SOBOL'): model.sample(100, rule, problem=problem)
    
def test_model_exception_hook():
    import biosteam as bst
    import pytest
    from biorefineries import lipidcane as lc
    from chaospy import distributions as shape
    from warnings import simplefilter
    import numpy as np
    bst.settings.set_thermo(lc.chemicals)
    simplefilter("ignore")
    IRR_metric = bst.Metric('Internal rate of return', lc.lipidcane_tea.solve_IRR)
    metrics = [IRR_metric]
    lipidcane_model = bst.Model(lc.lipidcane_sys, metrics)
    baseline = lc.lipidcane.F_mass
    distribution = shape.Triangle(-baseline , baseline , 2*baseline) # Negative value should fail
    
    @lipidcane_model.parameter(element=lc.lipidcane, distribution=distribution, units='kg/hr')
    def set_lipidcane_flow_rate(flow_rate):
        lc.lipidcane.F_mass = flow_rate
    
    samples = lipidcane_model.sample(15, 'L')
    lipidcane_model.load_samples(samples)
    
    # Without an exception hook, the same behavior will result (NaN values for failed evaluations)
    lipidcane_model.evaluate()
    assert np.isnan(lipidcane_model.table.values).any()
    
    InfeasibleRegion = bst.exceptions.InfeasibleRegion
    
    # This will provide a more understandable IRR result for infeasible regions
    def exception_hook(exception, sample): 
        if isinstance(exception, InfeasibleRegion):
            return [0]
        else: raise exception
    lipidcane_model.exception_hook = exception_hook
    lipidcane_model.evaluate()
    assert not np.isnan(lipidcane_model.table.values).any()
    
    # This will raise an exception due to negative flow rates
    def exception_hook(exception, sample): 
        if isinstance(exception, InfeasibleRegion):
            raise exception
    lipidcane_model.exception_hook = exception_hook
    with pytest.raises(InfeasibleRegion): lipidcane_model.evaluate()
    
    # This will raise an exception regardless
    def exception_hook(exception, sample): 
        raise exception
    lipidcane_model.exception_hook = exception_hook
    with pytest.raises(InfeasibleRegion): lipidcane_model.evaluate()
    
    # Here is another cool thing we could do in the case where 
    # some metrics are expected to fail
    bad_metric = bst.Metric('bad metric', lambda: 1/0)
    lipidcane_model.metrics = (IRR_metric, bad_metric)
    lipidcane_model.load_samples(samples) # Metrics changed, so need to reload sample
    def exception_hook(exception, sample): 
        if not isinstance(exception, ZeroDivisionError): return
        lc.lipidcane_sys.simulate()
        values = []
        for i in lipidcane_model.metrics:
            try: x = i()
            except: x = None
            values.append(x)
        return values
    lipidcane_model.exception_hook = exception_hook
    lipidcane_model.evaluate()
    bad_metric_results = lipidcane_model.table[bad_metric.index]
    IRR_metric_results = lipidcane_model.table[IRR_metric.index]
    assert np.isnan(bad_metric_results).all()
    assert not np.isnan(IRR_metric_results).all()
    
    # Note that the possibilities are infinite here...
    