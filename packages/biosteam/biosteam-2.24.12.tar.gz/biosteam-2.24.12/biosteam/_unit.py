# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2021, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
import numpy as np
import pandas as pd
from graphviz import Digraph
from ._graphics import UnitGraphics, box_graphics
from thermosteam import Stream
from ._heat_utility import HeatUtility
from .utils import Inlets, Outlets, NotImplementedMethod, \
                   format_title, static, ignore_docking_warnings
from ._power_utility import PowerUtility
from .digraph import finalize_digraph
from thermosteam.utils import thermo_user, registered
from thermosteam.units_of_measure import convert
import biosteam as bst

__all__ = ('Unit',)

_count = [0]
def count():
    _count[0] += 1
    print(_count)

# %% Inlet and outlet representation

def repr_ins_and_outs(ins, outs, T, P, flow, composition, N, IDs, data):
    info = ''
    if ins:
        info += 'ins...\n'
        i = 0
        for stream in ins:
            unit = stream._source
            source_info = f'  from  {type(unit).__name__}-{unit}\n' if unit else '\n'
            if stream and data:
                stream_info = stream._info(T, P, flow, composition, N, IDs)
                index = stream_info.index('\n')
                info += f'[{i}] {stream}' + source_info + stream_info[index+1:] + '\n'
            else:
                info += f'[{i}] {stream}' + source_info
            i += 1
    if outs:
        info += 'outs...\n'
        i = 0
        for stream in outs:
            unit = stream._sink
            sink_info = f'  to  {type(unit).__name__}-{unit}\n' if unit else '\n'
            if stream and data:
                stream_info = stream._info(T, P, flow, composition, N, IDs)
                index = stream_info.index('\n')
                info += f'[{i}] {stream}' + sink_info + stream_info[index+1:] + '\n'
            else:
                info += f'[{i}] {stream}' + sink_info
            i += 1
    info = info.replace('\n ', '\n    ')
    return info[:-1]

# %% Unit Operation

@thermo_user
@registered(ticket_name='U')
class Unit:
    """
    Abstract parent class for Unit objects. Child objects must contain
    `_run`, `_design` and `_cost` methods to estimate stream outputs of a
    Unit and find design and cost information.  

    **Abstract class methods**
    
    reset_cache()
        Reset unit operartion cache.
    _setup()
        Set stream conditions and constant data.
    _run()
        Run simulation and update output streams.
    _design()
        Add design requirements to the `design_results` dictionary.
    _cost()
        Add itemized purchse costs to the `purchase_costs` dictionary.

    **Abstract class attributes**
    
    **line='Unit'**
        [str] Name denoting the type of Unit class. Defaults to the class
        name of the first child class.
    **_BM** 
        dict[str, float] Bare module factors for each purchase cost item.
    **_units**
        [dict] Units of measure for `design_results` dictionary.
    **_N_ins=1**
        [int] Expected number of input streams.
    **_N_outs=2**
        [int] Expected number of output streams.
    **_ins_size_is_fixed=True**
        [bool] Whether the number of streams in ins is fixed.
    **_outs_size_is_fixed=True**
        [bool] Whether the number of streams in outs is fixed.
    **_N_heat_utilities=0**
        [int] Number of heat utilities created with each instance.
    **auxiliary_unit_names=()
        tuple[str] Name of attributes that are auxiliary units. These units
        will be accounted for in the purchase and installed equipment costs
        without having add these costs in the `purchase_costs` dictionary.
    **_equipment_lifetime=None**
        [int] or dict[str, int] Lifetime of equipment. Defaults to lifetime of
        production venture. Use an integer to specify the lifetime is for all
        items in the unit purchase costs. Use a dictionary to specify the 
        lifetime of each purchase cost item.
    **_graphics**
        [biosteam.Graphics, abstract, optional] Settings for diagram
        representation. Defaults to a box with the same number of input
        and output edges as `_N_ins` and `_N_outs`.

    Parameters
    ----------
    ID='' : str, defaults to a unique ID
        A unique identification. If ID is None, unit will not be
        registered in flowsheet.
    ins=None : Iterable[:class:`~thermosteam.Stream`, or str], :class:`~thermosteam.Stream`, or str
        Inlet streams or IDs to initialize input streams.
        If empty, default IDs will be given. If None, defaults to missing streams.
    outs=() : Iterable[:class:`~thermosteam.Stream`, or str], :class:`~thermosteam.Stream`, or str
        Outlet streams or IDs to initialize output streams.
        If empty, default IDs will be given.
        If None, leave streams missing.
    thermo=None : :class:`~thermosteam.Thermo`
        Thermo object to initialize inlet and outlet streams. Defaults to
        `biosteam.settings.get_thermo()`.
    
    Attributes
    ----------
    ins : Inlets[:class:`~thermosteam.Stream`]
        Input streams.
    outs : Outlets[:class:`~thermosteam.Stream`]
        Output streams.
    power_utility : PowerUtility
        Electricity rate requirements are stored here (not including auxiliary units).
    heat_utilities : tuple[:class:`~biosteam.HeatUtility`]
        Cooling and heating requirements are stored here (not including auxiliary units).
    design_results : dict
        All design requirements (not including auxiliary units).
    purchase_costs : dict[str, float]
        Itemized purchase costs (not including auxiliary units).
    thermo : Thermo
        The thermodynamic property package used by the unit.
    
    Examples
    --------
    :doc:`tutorial/Creating_a_Unit`
    
    :doc:`tutorial/Using_-pipe-_notation`
    
    :doc:`tutorial/Inheriting_from_Unit`
    
    :doc:`tutorial/Unit_decorators`
    
    """ 
    
    def __init_subclass__(cls,
                          isabstract=False,
                          new_graphics=True):
        dct = cls.__dict__
        if 'line' not in dct:
            cls.line = format_title(cls.__name__)
        if 'ticket_name' not in dct:
            line = cls.line.lower()
            if 'centrifuge' in line: cls.ticket_name = 'C'
            elif 'distillation' in line: cls.ticket_name = 'D'
            elif 'evaporator' in line: cls.ticket_name = 'E'
            elif 'flash' in line: cls.ticket_name = 'F'
            elif ('cooler' in line 
                  or 'condenser' in line
                  or 'heater' in line 
                  or 'boiler' in line
                  or 'heat exchanger' in line): cls.ticket_name = 'H'
            elif 'mixer' in line: cls.ticket_name = 'M'
            elif 'pump' in line: cls.ticket_name = 'P'
            elif 'reactor' in line or 'digestion' in line or 'ferment' in line: cls.ticket_name = 'R'
            elif 'split' in line: cls.ticket_name = 'S'
            elif 'tank' in line: cls.ticket_name = 'T'
            elif 'junction' == line: cls.ticket_name = 'J'
            elif 'specification' in line: cls.ticket_name = 'PS'
            else: cls.ticket_name = 'U'
        if '_graphics' not in dct and new_graphics:
            # Set new graphics for specified line
            cls._graphics = UnitGraphics.box(cls._N_ins, cls._N_outs)
        if not isabstract:
            if not hasattr(cls, '_BM'): cls._BM = {}
            if not hasattr(cls, '_units'): cls._units = {}
            if not hasattr(cls, '_equipment_lifetime'): cls._equipment_lifetime = {}
            if not cls._run:
                if cls._N_ins == 1 and cls._N_outs == 1:
                    static(cls)
                else:
                    raise NotImplementedError(
                        "Unit subclass with multiple inlet or outlet streams "
                        "must implement a '_run' method unless the "
                        "'isabstract' keyword argument is True"
                    )
        if '__init__' in dct and '_stacklevel' not in dct:
            cls._stacklevel += 1
        
    ### Abstract Attributes ###
    
    # tuple[str] Name of attributes that are auxiliary units. These units
    # will be accounted for in the purchase and installed equipment costs
    # without having add these costs in the `purchase_costs` dictionary
    auxiliary_unit_names = ()
    
    # [int] Expected number of inlet streams
    _N_ins = 1  
    
    # [int] Expected number of outlet streams
    _N_outs = 1
    
    # [bool] Whether the number of streams in ins is fixed
    _ins_size_is_fixed = True
    
    # [bool] Whether the number of streams in outs is fixed
    _outs_size_is_fixed = True
    
    # [int] number of heat utilities
    _N_heat_utilities = 0
    
    # [StreamLinkOptions] Options for linking streams
    _stream_link_options = None
    
    # [biosteam Graphics] A Graphics object for diagram representation
    _graphics = box_graphics

    # [int] Used for piping warnings. Should be equal to 6 plus the number of
    # wrappers to Unit.__init__
    _stacklevel = 5
    
    # [str] The general type of unit, regardless of class
    line = 'Unit'

    ### Other defaults ###
    
    def __init__(self, ID='', ins=None, outs=(), thermo=None):
        self._register(ID)
        self._specification = None
        self._load_thermo(thermo)
        self._init_ins(ins)
        self._init_outs(outs)
        self._init_utils()
        self._init_results()
        self._assert_compatible_property_package()
    
    def _init_ins(self, ins):
        # Inlets[:class:`~thermosteam.Stream`] Input streams
        self._ins = Inlets(self, self._N_ins, ins, self._thermo, self._ins_size_is_fixed, self._stacklevel)
    
    def _init_outs(self, outs):
        # Outlets[:class:`~thermosteam.Stream`] Output streams
        self._outs = Outlets(self, self._N_outs, outs, self._thermo, self._outs_size_is_fixed, self._stacklevel)
    
    def _init_utils(self):
        # tuple[HeatUtility] All heat utilities associated to unit
        self.heat_utilities = tuple([HeatUtility() for i in
                                     range(self._N_heat_utilities)])
        
        # [PowerUtility] Electric utility associated to unit
        self.power_utility = PowerUtility()
    
    def _init_results(self):
        # [dict] All purchase cost results in USD.
        self.purchase_costs = {}
        
        # [dict] All design results.
        self.design_results = {}
        
        # [dict] Greenhouse gas emissions
        self._GHGs = {}
    
    def _assert_compatible_property_package(self):
        chemicals = self.chemicals
        streams = self._ins + self._outs
        assert all([s.chemicals is chemicals for s in streams if s]), (
            "unit operation chemicals are incompatible with inlet and outlet streams; "
            "try using the `thermo` keyword argument to initialize the unit operation "
            "with a compatible thermodynamic property package"
        )
    
    def disconnect(self):
        self._ins[:] = ()
        self._outs[:] = ()
    
    def get_node(self):
        """Return unit node attributes for graphviz."""
        try: self._load_stream_links()
        except: pass
        if bst.MINIMAL_UNIT_DIAGRAMS:
            return self._graphics.get_minimal_node(self)
        else:
            return self._graphics.get_node_tailored_to_unit(self)
    
    def get_design_result(self, key, units):
        return convert(self.design_results[key], self._units[key], units)
    
    @ignore_docking_warnings
    def take_place_of(self, other):
        """Replace inlets and outlets from this unit with that of another unit."""
        self.ins[:] = other.ins
        self.outs[:] = other.outs
    
    # Forward pipping
    def __sub__(self, other):
        """Source streams."""
        isa = isinstance
        int_types = (int, np.int)
        if isa(other, (Unit, bst.System)):
            other._ins[:] = self._outs
            return other
        elif isa(other, int_types):
            return self.outs[other]
        elif isa(other, Stream):
            self._outs[:] = (other,)
            return self
        elif isa(other, (tuple, list, np.ndarray)):
            if all([isa(i, int_types) for i in other]):
                return [self._outs[i] for i in other]
            else:
                self._outs[:] = other
                return self
        else:
            return other.__rsub__(self)

    def __rsub__(self, other):
        """Sink streams."""
        isa = isinstance
        int_types = (int, np.int)
        if isa(other, int_types):
            return self._ins[other]
        elif isa(other, Stream):
            self._ins[:] = (other,)
            return self
        elif isa(other, (tuple, list, np.ndarray)):
            if all([isa(i, int_types) for i in other]):
                return [self._ins[i] for i in other]
            else:
                self._ins[:] = other
                return self
        else:
            raise ValueError(f"cannot pipe '{type(other).__name__}' object")

    # Backwards pipping
    __pow__ = __sub__
    __rpow__ = __rsub__
    
    # Abstract methods
    reset_cache = NotImplementedMethod
    _run = NotImplementedMethod
    _setup = NotImplementedMethod
    _design = NotImplementedMethod
    _cost = NotImplementedMethod
    
    def _get_design_info(self): 
        return ()
    def _get_cost_info(self): 
        return [(i.capitalize().replace('_', ' '), j.purchase_cost) for i,j in 
                zip(self.auxiliary_unit_names, self.auxiliary_units)]
        
    def _load_stream_links(self):
        options = self._stream_link_options
        if options:
            s_in = self._ins[0]
            s_out = self._outs[0]
            s_out.link_with(s_in, options.flow, options.phase, options.TP)
    
    def _summary(self):
        """Calculate all results from unit run."""
        self._design()
        self._cost()
    
    @property
    def specification(self):
        """Design or process specification."""
        return self._specification
    @specification.setter
    def specification(self, specification):
        if specification:
            if not callable(specification):
                raise AttributeError("specification must be callable")
        self._specification = specification
    
    @property
    def purchase_cost(self):
        """Total purchase cost [USD]."""
        return (sum(self.purchase_costs.values())
                + sum([i.purchase_cost for i in self.auxiliary_units]))
    
    @property
    def installed_cost(self):
        """Total installed equipment cost [USD]."""
        BM = self._BM
        try:
            installed_cost = sum([BM[i]*j for i,j in self.purchase_costs.items()])
        except KeyError:
            missing = set(self.purchase_costs).difference(BM)
            raise NotImplementedError("the following purchase cost items have "
                                      "no defined bare module factor in the "
                                     f"'{type(self).__name__}._BM' dictionary: {missing}")
        
        return sum([i.installed_cost for i in self.auxiliary_units],
                   installed_cost)
    
    @property
    def installed_costs(self):
        """dict[str, float] Installed equipment costs [USD]."""
        BM = self._BM
        try:
            installed_costs = {i: BM[i]*j for i,j in self.purchase_costs.items()}
        except KeyError:
            missing = set(self.purchase_costs).difference(BM)
            raise NotImplementedError("the following purchase cost items have "
                                      "no defined bare module factor in the "
                                     f"'{type(self).__name__}._BM' dictionary: {missing}")
        getfield = getattr
        for i in self.auxiliary_unit_names:
            installed_costs[i] = getfield(self, i).installed_cost
        return installed_costs
    
    @property
    def utility_cost(self):
        """Total utility cost [USD/hr]."""
        return sum([i.cost for i in self.heat_utilities]) + self.power_utility.cost

    @property
    def auxiliary_units(self):
        """tuple[Unit] All associated auxiliary units."""
        getfield = getattr
        return tuple([getfield(self, i) for i in self.auxiliary_unit_names])

    def mass_balance_error(self):
        """Return error in stoichiometric mass balance. If positive,
        mass is being created. If negative, mass is being destroyed."""
        return self.F_mass_out - self.F_mass_in

    def atomic_balance_error(self):
        """Return a dictionary of errors in stoichiometric atomic balances. 
        If value is positive, the atom is being created. If negative, the atom 
        is being destroyed."""
        from chemicals import elements
        mol = sum([i.mol for i in self.outs]) - sum([i.mol for i in self.ins])
        formula_array = self.chemicals.formula_array
        unbalanced_array = formula_array @ mol
        return elements.array_to_atoms(unbalanced_array)

    def simulate(self):
        """
        Run rigourous simulation and determine all design requirements.
        No design specifications are solved.
        """
        self._load_stream_links()
        self._setup()
        (self._specification or self._run)()
        self._summary()

    def results(self, with_units=True, include_utilities=True,
                include_total_cost=True, include_installed_cost=False,
                include_zeros=True, external_utilities=(), key_hook=None):
        """
        Return key results from simulation as a DataFrame if `with_units`
        is True or as a Series otherwise.
        """
        # TODO: Divide this into functions
        def addkey(key):
            if key_hook: key = key_hook(key)
            keys.append(key)
        
        keys = []; 
        vals = []; addval = vals.append
        if with_units:
            if include_utilities:
                power_utility = self.power_utility
                if power_utility:
                    addkey(('Power', 'Rate'))
                    addval(('kW', power_utility.rate))
                    if include_zeros or power_utility.cost:
                        addkey(('Power', 'Cost'))
                        addval(('USD/hr', power_utility.cost))
                for heat_utility in HeatUtility.sum_by_agent(self.heat_utilities + external_utilities):
                    if heat_utility:
                        ID = heat_utility.ID.replace('_', ' ').capitalize()
                        addkey((ID, 'Duty'))
                        addval(('kJ/hr', heat_utility.duty))
                        addkey((ID, 'Flow'))
                        addval(('kmol/hr', heat_utility.flow))
                        if include_zeros or heat_utility.cost: 
                            addkey((ID, 'Cost'))
                            addval(('USD/hr', heat_utility.cost))
            units = self._units
            Cost = self.purchase_costs
            for ki, vi in self.design_results.items():
                addkey(('Design', ki))
                addval((units.get(ki, ''), vi))
            for ki, vi, ui in self._get_design_info():
                addkey(('Design', ki))
                addval((ui, vi))
            for ki, vi in Cost.items():
                addkey(('Purchase cost', ki))
                addval(('USD', vi))
            for ki, vi in self._get_cost_info():
                addkey(('Purchase cost', ki))
                addval(('USD', vi))
            if include_total_cost:
                addkey(('Total purchase cost', ''))
                addval(('USD', self.purchase_cost))
                if include_installed_cost:
                    addkey(('Installed equipment cost', ''))
                    addval(('USD', self.installed_cost))
                utility_cost = self.utility_cost
                if include_zeros or utility_cost: 
                    addkey(('Utility cost', ''))
                    addval(('USD/hr', utility_cost))
            if self._GHGs:
                a, b = self._totalGHG
                GHG_units =  self._GHG_units
                for ko, vo in self._GHGs.items():
                    for ki, vi in vo.items():
                        addkey((ko, ki))
                        addval((GHG_units.get(ko, ''), vi))
                a_key, b_key = GHG_units.keys()
                a_unit, b_unit = GHG_units.values()
                addkey(('Total ' + a_key, ''))
                addval((a_unit, a))
                addkey(('Total ' + b_key, ''))
                addval((b_unit, b))
            if not keys: return None
            df = pd.DataFrame(vals,
                              pd.MultiIndex.from_tuples(keys),
                              ('Units', self.ID))
            df.columns.name = self.line
            return df
        else:
            if include_utilities:
                power_utility = self.power_utility
                if power_utility:
                    addkey(('Power', 'Rate'))
                    addval(power_utility.rate)
                    if include_zeros or power_utility.cost:
                        addkey(('Power', 'Cost'))
                        addval(power_utility.cost)
                for heat_utility in HeatUtility.sum_by_agent(self.heat_utilities + external_utilities):
                    if heat_utility:
                        ID = heat_utility.ID.replace('_', ' ').capitalize()
                        addkey((ID, 'Duty'))
                        addval(heat_utility.duty)
                        addkey((ID, 'Flow'))
                        addval(heat_utility.flow)
                        if include_zeros or heat_utility.cost:
                            addkey((ID, 'Cost'))
                            addval(heat_utility.cost)
            for ki, vi in self.design_results.items():
                addkey(('Design', ki))
                addval(vi)
            for ki, vi, ui in self._get_design_info():
                addkey(('Design', ki))
                addval(vi)
            for ki, vi in self._get_cost_info():
                addkey(('Purchase cost', ki))
                addval(vi)
            for ki, vi in self.purchase_costs.items():
                addkey(('Purchase cost', ki))
                addval(vi)    
            if self._GHGs:
                GHG_units = self._GHG_units
                for ko, vo in self._GHGs.items():
                    for ki, vi in vo.items():
                        addkey((ko, ki))
                        addval(vi)
                a, b = self._totalGHG
                a_key, b_key = GHG_units.keys()
                addkey(('Total ' + a_key, ''))
                addval(a)
                addkey(('Total ' + b_key, ''))
                addval(b)
            if include_total_cost:
                addkey(('Total purchase cost', ''))
                addval(self.purchase_cost)
                if include_installed_cost:
                    addkey(('Installed equipment cost', ''))
                    addval(self.installed_cost)
                utility_cost = self.utility_cost
                if include_zeros or utility_cost:
                    addkey(('Utility cost', ''))
                    addval(utility_cost)
            if not keys: return None
            series = pd.Series(vals, pd.MultiIndex.from_tuples(keys))
            series.name = self.ID
            return series

    @property
    def thermo(self):
        """Thermodynamic property package"""
        return self._thermo
    @property
    def ins(self):
        """All input streams."""
        return self._ins    
    @property
    def outs(self):
        """All output streams."""
        return self._outs

    def _add_upstream_neighbors_to_set(self, set, ends=None):
        """Add upsteam neighboring units to set."""
        for s in self._ins:
            u_source = s._source
            if not u_source: continue
            if not ends or s in ends:
                set.add(u_source)

    def _add_downstream_neighbors_to_set(self, set, ends=None):
        """Add downstream neighboring units to set."""
        for s in self._outs:
            u_sink = s._sink
            if not u_sink: continue
            if not ends or s in ends:
                set.add(u_sink)

    def get_downstream_units(self, ends=None):
        """Return a set of all units downstream."""
        downstream_units = set()
        outer_periphery = set()
        self._add_downstream_neighbors_to_set(outer_periphery, ends)
        inner_periphery = None
        old_length = -1
        new_length = 0
        while new_length != old_length:
            old_length = new_length
            inner_periphery = outer_periphery
            downstream_units.update(inner_periphery)
            outer_periphery = set()
            for unit in inner_periphery:
                unit._add_downstream_neighbors_to_set(outer_periphery, ends)
            new_length = len(downstream_units)
        return downstream_units
    
    def get_upstream_units(self, ends=None):
        """Return a set of all units upstream."""
        upstream_units = set()
        outer_periphery = set()
        self._add_upstream_neighbors_to_set(outer_periphery, ends)
        inner_periphery = None
        old_length = -1
        new_length = 0
        while new_length != old_length:
            old_length = new_length
            inner_periphery = outer_periphery
            upstream_units.update(inner_periphery)
            outer_periphery = set()
            for unit in inner_periphery:
                unit._add_upstream_neighbors_to_set(outer_periphery, ends)
            new_length = len(upstream_units)
        return upstream_units
    
    def neighborhood(self, radius=1, upstream=True, downstream=True):
        """
        Return a set of all neighboring units within given radius.
        
        Parameters
        ----------
        radius : int
                 Maxium number streams between neighbors.
        downstream=True : bool, optional
            Whether to include downstream operations
        upstream=True : bool, optional
            Whether to include upstream operations
        
        """
        radius -= 1
        neighborhood = set()
        if radius < 0: return neighborhood
        if upstream:self._add_upstream_neighbors_to_set(neighborhood)
        if downstream: self._add_downstream_neighbors_to_set(neighborhood)
        direct_neighborhood = neighborhood
        for i in range(radius):
            neighbors = set()
            for unit in direct_neighborhood:
                if upstream: unit._add_upstream_neighbors_to_set(neighbors)
                if downstream: unit._add_downstream_neighbors_to_set(neighbors)
            if neighbors == direct_neighborhood: break
            direct_neighborhood = neighbors
            neighborhood.update(direct_neighborhood)
        return neighborhood

    def get_digraph(self, format='png', **graph_attrs):
        ins = self.ins
        outs = self.outs
        graphics = self._graphics

        # Make a Digraph handle
        f = Digraph(name='unit', filename='unit', format=format)
        f.attr('graph', ratio='0.5', outputorder='edgesfirst',
               nodesep='1.1', ranksep='0.8', maxiter='1000')  # Specifications
        f.attr(rankdir='LR', **graph_attrs)  # Left to right

        # If many streams, keep streams close
        if (len(ins) >= 3) or (len(outs) >= 3):
            f.attr('graph', nodesep='0.4')

        # Initialize node arguments based on unit and make node
        node = graphics.get_node_tailored_to_unit(self)
        f.node(**node)

        # Set stream node attributes
        f.attr('node', shape='rarrow', fillcolor='#79dae8',
               style='filled', orientation='0', width='0.6',
               height='0.6', color='black', peripheries='1')

        # Make nodes and edges for input streams
        di = 0  # Destination position of stream
        for stream in ins:
            if not stream: continue
            f.node(stream.ID)
            edge_in = graphics.edge_in
            if di >= len(edge_in): di = 0
            f.attr('edge', arrowtail='none', arrowhead='none',
                   tailport='e', **edge_in[di])
            f.edge(stream.ID, node['name'])
            di += 1

        # Make nodes and edges for output streams
        oi = 0  # Origin position of stream
        for stream in outs:
            if not stream: continue
            f.node(stream.ID) 
            edge_out = graphics.edge_out  
            if oi >= len(edge_out): oi = 0
            f.attr('edge', arrowtail='none', arrowhead='none',
                   headport='w', **edge_out[oi])
            f.edge(node['name'], stream.ID)
            oi += 1
        return f

    def diagram(self, radius=0, upstream=True, downstream=True, 
                file=None, format='png', display=True, **graph_attrs):
        """
        Display a `Graphviz <https://pypi.org/project/graphviz/>`__ diagram
        of the unit and all neighboring units within given radius.
        
        Parameters
        ----------
        radius : int
                 Maxium number streams between neighbors.
        downstream=True : bool, optional
            Whether to show downstream operations
        upstream=True : bool, optional
            Whether to show upstream operations
        file : Must be one of the following:
            * [str] File name to save diagram.
            * [None] Display diagram in console.
        format : str
                 Format of file.
        display : bool, optional
            Whether to display diagram in console or to return the graphviz 
            object.
        
        """
        if radius > 0:
            neighborhood = self.neighborhood(radius, upstream, downstream)
            neighborhood.add(self)
            sys = bst.System('', neighborhood)
            return sys.diagram('thorough', file, format, **graph_attrs)
        f = self.get_digraph(format, **graph_attrs)
        if display or file: 
            finalize_digraph(f, file, format)
        else:
            return f
    
    ### Net input and output flows ###
    
    # Molar flow rates
    @property
    def mol_in(self):
        """Molar flows going in [kmol/hr]."""
        return sum([s.mol for s in self._ins if s])
    @property
    def mol_out(self):
        """Molar flows going out [kmol/hr]."""
        return sum([s.mol for s in self._outs if s])

    @property
    def z_mol_in(self):
        """Molar fractions going in [kmol/hr]."""
        return self._mol_in/self.F_mol_in
    @property
    def z_mol_out(self):
        """Molar fractions going in."""
        return self._mol_out/self.F_mol_out

    @property
    def F_mol_in(self):
        """Net molar flow going in [kmol/hr]."""
        return sum([s.F_mol for s in self._ins if s])
    @property
    def F_mol_out(self):
        """Net molar flow going out [kmol/hr]."""
        return sum([s.F_mol for s in self._outs if s])

    # Mass flow rates
    @property
    def mass_in(self):
        """Mass flows going in [kg/hr]."""
        return sum([s.mol for s in self._ins if s]) * self._thermo.chemicals.MW
    @property
    def mass_out(self):
        """Mass flows going out [kg/hr]."""
        return sum([s.mol for s in self._outs if s]) * self._thermo.chemicals.MW

    @property
    def z_mass_in(self):
        """Mass fractions going in."""
        return self.mass_in/self.F_mass_in
    @property
    def z_mass_out(self):
        """Mass fractions going out."""
        return self.mass_out/self.F_mass_out

    @property
    def F_mass_in(self):
        """Net mass flow going in [kg/hr]."""
        return self.mass_in.sum()
    @property
    def F_mass_out(self):
        """Net mass flow going out [kg/hr]."""
        return self.mass_out.sum()

    # Volumetric flow rates
    @property
    def vol_in(self):
        """Volumetric flows going in [m3/hr]."""
        return sum([s.vol for s in self._ins if s])
    @property
    def F_vol_in(self):
        """Net volumetric flow going in [m3/hr]."""
        return sum(self.vol_in)

    @property
    def z_vol_in(self):
        """Volumetric fractions going in."""
        return self.vol_in/self.F_vol_in
    @property
    def vol_out(self):
        """Volumetric flows going out [m3/hr]."""
        return sum([s.vol for s in self._outs if s])

    @property
    def F_vol_out(self):
        """Net volumetric flow going out [m3/hr]."""
        return sum(self.vol_out)
    @property
    def z_vol_out(self):
        """Volumetric fractions going out."""
        return self.vol_out/self.F_vol_out

    # Enthalpy flow rates
    @property
    def H_in(self):
        """Enthalpy flow going in [kJ/hr]."""
        return sum([s.H for s in self._ins if s])

    @property
    def H_out(self):
        """Enthalpy flow going out [kJ/hr]."""
        return sum([s.H for s in self._outs if s])

    @property
    def Hf_in(self):
        """Enthalpy of formation flow going in [kJ/hr]."""
        return sum([s.Hf for s in self._ins if s])

    @property
    def Hf_out(self):
        """Enthalpy of formation flow going out [kJ/hr]."""
        return sum([s.Hf for s in self._outs if s])

    @property
    def Hnet(self):
        """Net enthalpy flow, including enthalpies of formation [kJ/hr]."""
        return self.H_out - self.H_in + self.Hf_out - self.Hf_in
    
    # Representation
    def _info(self, T, P, flow, composition, N, IDs, data):
        """Information on unit."""
        if self.ID:
            info = f'{type(self).__name__}: {self.ID}\n'
        else:
            info = f'{type(self).__name__}\n'
        return info + repr_ins_and_outs(self.ins, self.outs, T, P, flow, composition, N, IDs, data)

    def show(self, T=None, P=None, flow=None, composition=None, N=None, IDs=None, data=True):
        """Prints information on unit."""
        print(self._info(T, P, flow, composition, N, IDs, data))
    
    def _ipython_display_(self):
        if bst.ALWAYS_DISPLAY_DIAGRAMS: self.diagram()
        self.show()

    def __repr__(self):
        if self.ID:
            return f'<{type(self).__name__}: {self.ID}>'
        else:
            return f'<{type(self).__name__}>'

del thermo_user, registered