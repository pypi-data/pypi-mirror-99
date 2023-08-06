from quantities import mV, ms, s, V
import sciunit
from neo import AnalogSignal
import neuronunit.capabilities as cap
import numpy as np
from neuronunit.models.backends import parse_glif
from neuronunit.models.backends.base import Backend
import quantities as qt
import quantities as pq

from quantities import mV, ms, s
import pickle
import copy
import re


import allensdk.core.json_utilities as json_utilities
from allensdk.model.glif.glif_neuron import GlifNeuron
from allensdk.api.queries.cell_types_api import CellTypesApi
# from neuronunit.models.reduced import ReducedModel

try:
    from allensdk.api.queries.glif_api import GlifApi
    from allensdk.core.cell_types_cache import CellTypesCache
    import allensdk.core.json_utilities as json_utilities
    import sciunit
except:
    import os
    os.system('pip install allensdk')
    from allensdk.api.queries.glif_api import GlifApi
    from allensdk.core.cell_types_cache import CellTypesCache
    import allensdk.core.json_utilities as json_utilities

    os.system('pip install git+https://github.com/scidash/sciunit@dev')



class GLIFBackend(Backend):
    def init_backend(self, attrs = None, cell_name = 'alice', current_src_name = 'hannah', DTC = None):
        backend = 'GLIF'
        super(GLIFBackend,self).init_backend()

        self.model._backend.use_memory_cache = False
        self.current_src_name = current_src_name
        self.cell_name = cell_name
        self.vM = None
        self.allen_id = None
        self.attrs = attrs
        self.nc = None

        self.temp_attrs = None


        if self.allen_id == None:
            try:
                self.nc = pickle.load(open(str('allen_id.p'),'rb'))
            except:
                self.allen_id = 566302806
                glif_api = GlifApi()

                self.nc = glif_api.get_neuron_configs([self.allen_id])[self.allen_id]
                pickle.dump(copy.copy(self.nc),open(str('allen_id.p'),'wb'))


        else:

            try:
                self.nc = pickle.load(open(str('allen_id.p'),'rb'))
            except:
                glif_api = GlifApi()
                self.allen_id = allen_id
                self.glif = glif_api.get_neuronal_models_by_id([allen_id])[0]
                self.nc = glif_api.get_neuron_configs([self.allen_id])[self.allen_id]
                pickle.dump(self.nc,open(str('allen_id.p'),'wb'))


        self.glif = GlifNeuron.from_dict(self.nc)


        if type(attrs) is not type(None):
            self.set_attrs(**attrs)
            self.sim_attrs = attrs

        if type(DTC) is not type(None):
            if type(DTC.attrs) is not type(None):

                self.set_attrs(**DTC.attrs)


            if hasattr(DTC,'current_src_name'):
                self._current_src_name = DTC.current_src_name

            if hasattr(DTC,'cell_name'):
                self.cell_name = DTC.cell_name

        #print(self.internal_params)
    def as_lems_model(self, backend=None):
        glif_package = []
        glif_package.append(self.metad)
        glif_package.append(self.nc)
        glif_package.append(self.get_sweeps)
        lems_file_path = parse_glif.generate_lems(glif_package)
        return ReducedModel(lems_file_path, backend=backend)

    def get_sweeps(self,specimen_id = None):
        if specimen_id == None:
            self.sweeps = ctc.get_ephys_sweeps(self.glif[self.allen_id], \
            file_name='%d_ephys_sweeps.json' % self.allen_id)

    def get_sweep(self, n,specimen_id = None):
        if specimen_id == None:
            self.sweeps = ctc.get_ephys_sweeps(self.glif[self.allen_id], \
            file_name='%d_ephys_sweeps.json' % self.allen_id)
        sweep_info = self.sweeps[n]
        sweep_number = sweep_info['sweep_number']
        sweep = ds.get_sweep(sweep_number)
        return sweep

    def get_stimulus(self, n):
        sweep = self.get_sweep(n)
        return sweep['stimulus']

    def apply_stimulus(self, n):
        self.stimulus = self.get_stimulus(n)

    def get_spike_train(self):
        #vms = self.get_membrane_potential()
        #from neuronunit.capabilities.spike_functions import get_spike_train
        #import numpy as np
        spike_times = self.results['interpolated_spike_times']
        return np.array(spike_times)

    def get_membrane_potential(self):
        """Must return a neo.core.AnalogSignal.
        And must destroy the hoc vectors that comprise it.
        """
        threshold = self.results['threshold']
        interpolated_spike_times = self.results['interpolated_spike_times']

        interpolated_spike_thresholds = self.results['interpolated_spike_threshold']
        grid_spike_indices = self.results['spike_time_steps']
        grid_spike_times = self.results['grid_spike_times']
        after_spike_currents = self.results['AScurrents']

        vm = self.results['voltage']
        if len(self.results['interpolated_spike_voltage']) > 0:
            isv = self.results['interpolated_spike_voltage'].tolist()[0]
            vm = list(map(lambda x: isv if np.isnan(x) else x, vm))
        dt =  self.glif.dt
        self.vM = AnalogSignal(vm,units = mV,sampling_period =  dt * ms)
        return vms

    def _local_run(self):
        #self.results = np.array(self.glif.run(self.stim))
        results = {}
        results['vm'] = self.vM
        results['t'] = self.vM.times
        results['run_number'] = results.get('run_number',0) + 1
        return results

        return self.results


    def set_attrs(self, **attrs):
        self.model.attrs.update(attrs)
        #self.nc.update(attrs)
        for k,v in attrs.items():
            self.nc[k] = v
        self.glif = GlifNeuron.from_dict(self.nc)
        return self.glif


    def set_stop_time(self, stop_time = 650*pq.ms):
        """Sets the simulation duration
        stopTimeMs: duration in milliseconds
        """
        self.tstop = float(stop_time.rescale(pq.ms))

    def inject_square_current(self, current):
        if 'injected_square_current' in current.keys():
            c = current['injected_square_current']
        else:
            c = current
        stop = float(c['delay'])+float(c['duration'])
        start = float(c['delay'])
        duration = float(c['duration'])
        amplitude = float(c['amplitude'])/1000.0
        self.glif.dt = 0.001
        dt =  self.glif.dt
        self.stim = [ 0.0 ] * int(start) + [ amplitude ] * int(duration) + [ 0.0 ] * int(stop)
        #self.glif.init_voltage = -0.0065
        self.results = self.glif.run(self.stim)
        vm = self.results['voltage']
        if len(self.results['interpolated_spike_voltage']) > 0:
            isv = self.results['interpolated_spike_voltage'].tolist()[0]
            vm = list(map(lambda x: isv if np.isnan(x) else x, vm))

        vms = AnalogSignal(vm,units = V,sampling_period =  dt * s)
        self.vM = vms
        return vms
