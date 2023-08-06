#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/master/LICENSE.txt
for license details.
'''


# %%

import math
import numpy as np
import pandas as pd
from . import ImpactItem, WasteStream
from ._units_of_measure import auom
from .utils.formatting import format_number as f_num

items = ImpactItem._items
isinstance = isinstance
iter = iter
callable = callable

__all__ = ('LCA',)


class LCA:
    '''
    For life cycle assessment (LCA) of a System.
    
    Parameters
    ----------
    system : :class:`biosteam.System`
        System for which this LCA is conducted for.
    lifetime : float
        Lifetime of the LCA.
    lifetime_unit : str
        Unit of lifetime.
    uptime_ratio : float
        Fraction of time that the plant is operating.
    item_quantities : kwargs, :class:`ImpactItem` or str = float/callable or (float/callable, unit)
        Other :class:`ImpactItem` objects (e.g., electricity) and their quantities.
        Note that callable functions are used so that quantity of items can be updated.
    
    '''
    
    __slots__ = ('_system',  '_lifetime', '_uptime_ratio',
                 '_construction_units', '_transportation_units',
                 '_lca_streams', '_impact_indicators',
                 '_other_items', '_other_items_f')
    
    
    def __init__(self, system, lifetime, lifetime_unit='yr', uptime_ratio=1,
                 **item_quantities):
        system.simulate()
        self._construction_units = set()
        self._transportation_units = set()
        self._lca_streams = set()
        self._update_system(system)
        self._update_lifetime(lifetime, lifetime_unit)
        self.uptime_ratio = uptime_ratio
        self._other_items = {}
        self._other_items_f = {}
        for item, val in item_quantities.items():
            try:
                f_quantity, unit = val # unit provided for the quantity
            except:
                f_quantity = val
                unit = ''
            self.add_other_item(item, f_quantity, unit)
            
    
    def _update_system(self, system):
        for u in system.units:
            if u.construction:
                self._construction_units.add(u)
            if u.transportation:
                self._transportation_units.add(u)
        self._construction_units = sorted(self._construction_units,
                                          key=lambda u: u.ID)
        self._transportation_units = sorted(self._transportation_units,
                                            key=lambda u: u.ID)
        for s in (i for i in system.feeds+system.products):
            if s.impact_item:
                self._lca_streams.add(s)
        self._lca_streams = sorted(self._lca_streams, key=lambda s: s.ID)
        self._system = system


    def _update_lifetime(self, lifetime=0., unit='yr'):
        if not unit or unit == 'yr':
            self._lifetime = float(lifetime)
        else:
            converted = auom(unit).convert(float(lifetime), 'yr')
            self._lifetime = converted

    
    def add_other_item(self, item, f_quantity, unit=''):
        '''Add other :class:`ImpactItem` in LCA.'''
        if isinstance(item, str):
            item = items[item]
        fu = item.functional_unit
        if not callable(f_quantity):
            f = lambda: f_quantity
        else:
            f = f_quantity
        quantity = f()
        if unit and unit != fu:
            try:
                quantity = auom(unit).convert(quantity, fu)
            except:
                raise ValueError(f'Conversion of the given unit {unit} to '
                                 f'item functional unit {fu} is not supported.')
        self._other_items_f[item.ID] = {'item':item, 'f_quantity':f, 'unit':unit}
        self.other_items[item.ID] = {'item':item, 'quantity':quantity}
        
    
    def refresh_other_items(self):
        '''Refresh quantities of other items using the given functions.'''
        for item_ID, record in self._other_items_f.items():
            item, f_quantity, unit = record.values()
            self.other_items[item_ID]['quantity'] = f_quantity()
        
        
    def __repr__(self):
        return f'<LCA: {self.system}>'

    def show(self, lifetime_unit='yr'):
        '''Show basic information of this :class:`LCA` object.'''
        lifetime = auom('yr').convert(self.lifetime, lifetime_unit)
        info = f'LCA: {self.system} (lifetime {f_num(lifetime)} {lifetime_unit})'
        info += '\nImpacts:'
        print(info)
        if len(self.indicators) == 0:
            print(' None')
        else:
            index = pd.Index((i.ID+' ('+i.unit+')' for i in self.indicators))
            df = pd.DataFrame({
                'Construction': tuple(self.total_construction_impacts.values()),
                'Transportation': tuple(self.total_transportation_impacts.values()),
                'WasteStream': tuple(self.total_stream_impacts.values()),
                'Others': tuple(self.total_other_impacts.values()),
                'Total': tuple(self.total_impacts.values())
                },
                index=index)
            # print(' '*9+df.to_string().replace('\n', '\n'+' '*9))
            print(df.to_string())
    
    _ipython_display_ = show
    
    
    def get_construction_impacts(self, units, time=None, time_unit='hr'):
        '''
        Return all construction-related impacts for the given unit,
        normalized to a certain time frame.
        '''
        if not (isinstance(units, tuple) or isinstance(units, list) or isinstance(units, set)):
            units = (units,)
        if not time:
            ratio = 1
        else:
            converted = auom(time_unit).convert(float(time), 'hr')
            ratio = converted/self.lifetime_hr
        impacts = dict.fromkeys((i.ID for i in self.indicators), 0.)
        for i in units:
            for j in i.construction:
                impact = j.impacts
                if j.lifetime is not None:
                    factor = math.ceil(time/j.lifetime)
                else:
                    factor = 1.
                for m, n in impact.items():
                    impacts[m] += n*ratio*factor
        return impacts
    
    def get_transportation_impacts(self, units, time=None, time_unit='hr'):
        '''
        Return all transportation-related impacts for the given unit,
        normalized to a certain time frame.
        '''
        if not (isinstance(units, tuple) or isinstance(units, list)
                or isinstance(units, set)):
            units = (units,)
        if not time:
            time = self.lifetime_hr
        else:
            time = auom(time_unit).convert(float(time), 'hr')
        impacts = dict.fromkeys((i.ID for i in self.indicators), 0.)
        for i in units:
            for j in i.transportation:
                impact = j.impacts
                for m, n in impact.items():
                    impacts[m] += n*time/j.interval
        return impacts
    
    
    def get_stream_impacts(self, stream_items=None, exclude=None,
                           kind='all', time=None, time_unit='hr'):
        '''
        Return all stream-related impacts for the given streams,
        normalized to a certain time frame.
        '''
        if not (isinstance(stream_items, tuple) or isinstance(stream_items, list)
                or isinstance(stream_items, set)):
            stream_items = (stream_items,)
        if not (isinstance(exclude, tuple) or isinstance(exclude, list)
                or isinstance(exclude, set)):
            exclude = (exclude,)
        if stream_items == None:
            stream_items = self.stream_inventory
        impacts = dict.fromkeys((i.ID for i in self.indicators), 0.)
        if not time:
            time = self.lifetime_hr
        else:
            time = auom(time_unit).convert(float(time), 'hr')
        for j in stream_items:
            # In case that ws instead of the item is given
            if isinstance(j, WasteStream):
                ws = j
                if j.impact_item:
                    j = ws.impact_item
                else: continue
            else:
                ws = j.linked_stream
            if ws in exclude: continue
            for m, n in j.CFs.items():
                if kind == 'all':
                    pass
                elif kind == 'direct_emission':
                    n = max(n, 0)
                elif kind == 'offset':
                    n = min(n, 0)
                else:
                    raise ValueError('kind can only be "all", "direct_emission", or "offset", '
                                     f'not {kind}.')
                impacts[m] += n*time*ws.F_mass
        return impacts
    
    def get_other_impacts(self):
        '''
        Return all additional impacts from "other" :class:`ImpactItems` objects,
        based on defined quantity.
        '''
        self.refresh_other_items()
        impacts = dict.fromkeys((i.ID for i in self.indicators), 0.)
        other_dct = self.other_items         
        for i in other_dct.keys():
            item = items[i]
            for m, n in item.CFs.items():
                impacts[m] += n*other_dct[i]['quantity']
        return impacts
    
    def get_total_impacts(self, exclude=None, time=None, time_unit='hr'):
        '''Return total impacts, normalized to a certain time frame.'''
        impacts = dict.fromkeys((i.ID for i in self.indicators), 0.)
        ws_impacts = self.get_stream_impacts(stream_items=self.stream_inventory,
                                             exclude=exclude, time=time, time_unit=time_unit)
        for i in (self.total_construction_impacts,
                  self.total_transportation_impacts,
                  ws_impacts,
                  self.total_other_impacts):
            for m, n in i.items():
                impacts[m] += n
        return impacts

    def get_allocated_impacts(self, streams=(), allocate_by='mass'):
        '''
        Allocate total impacts to one or multiple streams.
        
        Parameters
        ----------
        streams : :class:`WasteStream` or sequence
            One or a sequence of streams. Note that impacts of these streams will be
            excluded in calculating the total impacts.
        allocate_by : str, sequence, or function to generate an sequence
            If provided as a str, can be "mass", "energy", or 'value' to allocate
            the impacts accordingly.
            If provided as a sequence (no need to normalize so that sum of the sequence is 1),
            will allocate impacts according to the sequence.
            If provided as a function,  will call the function to generate an
            sequence to allocate the impacts accordingly.
        
        .. note::
            
            Energy of the stream will be calcuated as the sum of HHVs of all components
            in the stream.
        
        '''
        if not (isinstance(streams, tuple) or isinstance(streams, list)
                or isinstance(streams, set)):
            streams = (streams,)
        impact_dct = self.get_total_impacts(exclude=streams)
        impact_vals = np.array([i for i in impact_dct.values()])
        allocated = {}
        if len(streams) == 1:
            return impact_dct
        if allocate_by == 'mass':
            ratios = np.array([i.F_mass for i in streams])
        elif allocate_by == 'energy':
            ratios = np.array([i.HHV for i in streams])
        elif allocate_by == 'value':
            ratios = np.array([i.F_mass*i.price for i in streams])
        elif iter(allocate_by):
            ratios = allocate_by
        elif callable(allocate_by):
            ratios = allocate_by()
        else:
            raise ValueError('allocate_by can only be "mass", "energy", "value", '
                             'a sequence, or a function to generate a sequence.')
        if ratios.sum() == 0:
            raise ValueError('Calculated allocation ratios are all zero, cannot allocate.')
        ratios = ratios/ratios.sum()
        for n, ws in enumerate(streams):
            if not ws in self.system.streams:
                raise ValueError(f'`WasteStream` {ws} not in the system.')
            allocated[ws.ID] = dict.fromkeys(impact_dct.keys(),
                                             (ratios[n]*impact_vals).sum())
        return allocated
        
    
    def get_unit_impacts(self, units, time=None, time_unit='hr',
                          exclude=None):
        '''Return total impacts with certain units, normalized to a certain time frame. '''
        if not (isinstance(units, tuple) or isinstance(units, list)
                or isinstance(units, set)):
            units = (units,)
        constr = self.get_construction_impacts(units, time, time_unit)
        trans = self.get_transportation_impacts(units, time, time_unit)
        ws_items = set(i for i in 
                       sum((tuple(unit.ins+unit.outs) for unit in units), ())
                       if i.impact_item)

        ws = self.get_stream_impacts(stream_items=ws_items, exclude=exclude,
                                     time=time, time_unit=time_unit)
        other = self.get_other_impacts()
        tot = constr.copy()
        for m in tot.keys():
            tot[m] += trans[m] + ws[m] + other[m]
        return tot
    
    def _append_cat_sum(self, cat_table, cat, tot):
        num = len(cat_table)
        cat_table.loc[num] = ''
        for i in self.indicators:
            cat_table[f'{i.ID} [{i.unit}]'][num] = tot[i.ID]
            cat_table[f'Category {i.ID} Ratio'][num] = 1
        if cat in ('construction', 'transportation'):        
            cat_table.rename(index={num: ('Sum', 'All')}, inplace=True)
            cat_table.index = \
                pd.MultiIndex.from_tuples(cat_table.index,
                                          names=[cat.capitalize(), 'SanUnit'])
        else:
            cat_table.rename(index={num: 'Sum'}, inplace=True)
        return cat_table
    
    def get_impact_table(self, category=None, time=None, time_unit='hr'):
        '''
        Return a :class:`pandas.DataFrame` table for the given impact category,
        normalized to a certain time frame.
        '''
        if not time:
            time = self.lifetime_hr
        else:
            time = auom(time_unit).convert(float(time), 'hr')
        
        if category in ('Construction', 'Other'):
            time = time/self.lifetime_hr
        
        cat = category.lower()
        tot = getattr(self, f'total_{cat}_impacts')
        if category in ('Construction', 'Transportation'):
            cat = category.lower()
            units = sorted(getattr(self, f'_{cat}_units'),
                              key=(lambda su: su.ID))
            items = sorted(set(i.item for i in getattr(self,  f'{cat}_inventory')),
                           key=(lambda item: item.ID))
            if len(items) == 0:
                return f'No {cat}-related impacts.'

            # Note that item_dct = dict.fromkeys([item.ID for item in items], []) won't work
            item_dct = dict.fromkeys([item.ID for item in items])
            for item_ID in item_dct.keys():
                item_dct[item_ID] = dict(SanUnit=[], Quantity=[])
            for su in units:
                for i in getattr(su, cat):
                    item_dct[i.item.ID]['SanUnit'].append(su.ID)
                    item_dct[i.item.ID]['Quantity'].append(i.quantity*time)
                    if cat == 'transportation':
                        item_dct[i.item.ID]['Quantity'][-1] /= i.interval
            dfs = []
            for item in items:
                dct = item_dct[item.ID]
                dct['SanUnit'].append('Total')
                dct['Quantity'] = np.array(dct['Quantity'])
                dct['Quantity'] = np.append(dct['Quantity'], dct['Quantity'].sum())
                dct['Item Ratio'] = dct['Quantity']/dct['Quantity'].sum()*2
                for i in self.indicators:
                    if i.ID in item.CFs:
                        dct[f'{i.ID} [{i.unit}]'] = impact = dct['Quantity']*item.CFs[i.ID]
                        dct[f'Category {i.ID} Ratio'] = impact/tot[i.ID]
                    else:
                        dct[f'{i.ID} [{i.unit}]'] = dct[f'Category {i.ID} Ratio'] = 0
                df = pd.DataFrame.from_dict(dct)
                index0 = f'{item.ID} [{item.functional_unit}]'
                df.set_index([pd.MultiIndex.from_arrays(
                    [(index0,)*len(dct['SanUnit'])], names=(category,)),
                    'SanUnit'],
                    inplace=True)
                dfs.append(df)

            table = pd.concat(dfs)
            return self._append_cat_sum(table, cat, tot)
        
        ind_head = sum(([f'{i.ID} [{i.unit}]',
                         f'Category {i.ID} Ratio'] for i in self.indicators), [])
        
        if category == 'Stream':
            headings = ['Stream', 'Mass [kg]', *ind_head]
            item_dct = dict.fromkeys(headings)
            for key in item_dct.keys():
                item_dct[key] = []
            for ws_item in self.stream_inventory:
                ws = ws_item.linked_stream
                item_dct['Stream'].append(ws.ID)
                mass = ws.F_mass * time
                item_dct['Mass [kg]'].append(mass)
                for ind in self.indicators:
                    if ind.ID in ws_item.CFs.keys():
                        impact = ws_item.CFs[ind.ID]*mass
                        item_dct[f'{ind.ID} [{ind.unit}]'].append(impact)
                        item_dct[f'Category {ind.ID} Ratio'].append(impact/tot[ind.ID])
                    else:
                        item_dct[f'{ind.ID} [{ind.unit}]'].append(0)
                        item_dct[f'Category {ind.ID} Ratio'].append(0)
            table = pd.DataFrame.from_dict(item_dct)
            table.set_index(['Stream'], inplace=True)
            return self._append_cat_sum(table, cat, tot)

        elif category == 'Other':
            headings = ['Other', 'Quantity', *ind_head]
            item_dct = dict.fromkeys(headings)
            for key in item_dct.keys():
                item_dct[key] = []
            for other_ID in self.other_items.keys():
                other = self.other_items[other_ID]['item']
                item_dct['Other'].append(f'{other_ID} [{other.functional_unit}]')
                quantity = self.other_items[other_ID]['quantity'] * time
                item_dct['Quantity'].append(quantity)
                for ind in self.indicators:
                    if ind.ID in other.CFs.keys():
                        impact = other.CFs[ind.ID]*quantity
                        item_dct[f'{ind.ID} [{ind.unit}]'].append(impact)
                        item_dct[f'Category {ind.ID} Ratio'].append(impact/tot[ind.ID])
                    else:
                        item_dct[f'{ind.ID} [{ind.unit}]'].append(0)
                        item_dct[f'Category {ind.ID} Ratio'].append(0)
            table = pd.DataFrame.from_dict(item_dct)
            table.set_index(['Other'], inplace=True)
            return self._append_cat_sum(table, cat, tot)
        
        else:
            raise ValueError(
                'category can only be "Construction", "Transportation", "Stream", or "Other", ' \
                f'not {category}.')

    def save_report(self, file=None, sheet_name='LCA',
                    time=None, time_unit='hr',
                    n_row=0, row_space=2):
        '''Save all LCA tables as an Excel file.'''
        if not file:
            file = f'{self.system.ID}_lca.xlsx'
        tables = [self.get_impact_table(cat, time, time_unit)
                  for cat in ('Construction', 'Transportation',
                              'Stream', 'Other')]
        with pd.ExcelWriter(file) as writer:
            for table in tables:
                table.to_excel(writer, sheet_name=sheet_name, startrow=n_row)
                n_row += table.shape[0] + row_space + len(table.columns.names) # extra lines for the heading

    @property
    def system(self):
        '''[biosteam.System] The system linked to this LCA.'''
        return self._system
    @system.setter
    def system(self, i):
        self._update_system(i)
    
    @property
    def lifetime(self):
        '''[float] Lifetime of the system, [yr].'''
        return self._lifetime
    @lifetime.setter
    def lifetime(self, lifetime, unit='yr'):
        self._update_lifetime(lifetime, unit)
        
    @property
    def lifetime_hr(self):
        '''[float] Lifetime of the system in hours, [hr].'''
        return self._lifetime*365*24*self.uptime_ratio
    
    @property
    def uptime_ratio(self):
        '''[float] Fraction of time that the system is operating.'''
        return self._uptime_ratio
    @uptime_ratio.setter
    def uptime_ratio(self, i):
        if 0 <= i <= 1:
            self._uptime_ratio = float(i)
        else:
            raise ValueError('uptime_ratio must be in [0,1].')
    
    @property
    def indicators(self):
        '''[set] All impact indicators associated with this LCA.'''
        if not self.construction_inventory:
            constr = set()
        else:
            constr = set(sum((i.indicators for i in self.construction_inventory
                              if i is not None), ()))
        if not self.transportation_inventory:
            trans = set()
        else:
            trans = set(sum((i.indicators for i in self.transportation_inventory
                             if i is not None), ()))
        if not self.stream_inventory:
            ws = set()
        else:
            ws = set(sum((i.indicators for i in self.stream_inventory
                          if i is not None), ()))
        if not self.other_items:
            other = set()
        else:
            other = set(sum((items[i].indicators for i in self.other_items.keys()), ()))
        tot = constr.union(trans, ws, other)
        if len(tot) == 0:
            raise ValueError('No `ImpactIndicators` have been added.')
        return tot
    
    @property
    def construction_units(self):
        '''[set] All units in the linked system with constrution activity.'''
        return self._construction_units
    
    @property
    def construction_inventory(self):
        '''[tuple] All construction activities.'''
        return sum((i.construction for i in self.construction_units), ())
    
    @property
    def total_construction_impacts(self):
        '''[dict] Total impacts associated with construction activities.'''
        return self.get_construction_impacts(self.construction_units)
    
    @property
    def transportation_units(self):
        '''[set] All units in the linked system with transportation activity.'''
        return self._transportation_units
    
    @property
    def transportation_inventory(self):
        '''[tuple] All transportation activities.'''
        return sum((i.transportation for i in self.transportation_units), ())
    
    @property
    def total_transportation_impacts(self):
        '''[dict] Total impacts associated with transportation activities.'''
        return self.get_transportation_impacts(self.transportation_units)
    
    @property
    def lca_streams(self):
        '''[set] All streams in the linked system with impacts.'''
        return self._lca_streams
    
    @property
    def stream_inventory(self):
        '''[tuple] All chemical inputs, fugitive gases, waste emissions, and products.'''
        return tuple(i.impact_item for i in self.lca_streams)
    
    @property
    def total_stream_impacts(self):
        '''[dict] Total impacts associated with `WasteStreams` (e.g., chemicals, emissions).'''
        return self.get_stream_impacts(stream_items=self.stream_inventory)
        
    @property
    def other_items (self):
        '''[dict] Other impact items (e.g., electricity) and their quantities.'''
        return self._other_items
    @other_items.setter
    def other_items(self, item, f_quantity, unit=''):
        self.add_other_item(item, f_quantity, unit)
        
    @property
    def total_other_impacts(self):
        '''[dict] Total impacts associated with other ImpactItems (e.g., electricity).'''
        return self.get_other_impacts()
    
    @property
    def total_impacts(self):
        '''[dict] Total impacts of the entire system (construction, transportation, and wastestream).'''
        return self.get_total_impacts()






