import io
import copy
import math
import pdb

from numba import jit
import numpy as np
import quantities as qt
from quantities import mV, ms, s
import matplotlib.pyplot as plt
from sciunit.utils import redirect_stdout
import pyNN
pyNN.neuron_log = io.StringIO()
with redirect_stdout(pyNN.neuron_log):
    from pyNN.neuron import HH_cond_exp
    from pyNN.neuron import EIF_cond_exp_isfa_ista
    from pyNN.neuron import Izhikevich
    from pyNN import neuron
    from pyNN.neuron import simulator as sim
    from pyNN.neuron import setup as setup
    from pyNN.neuron import DCSource

from .base import *


# Potassium ion-channel rate functions
class HHpyNNBackend(Backend):

    def load_model(self):
        neuron = None
        self.hhcell = neuron.create(EIF_cond_exp_isfa_ista())
        neuron.setup(timestep=self.dt, min_delay=1.0)


    def init_backend(self, attrs = None, cell_name= 'HH_cond_exp',
                     current_src_name = 'hannah', DTC = None, dt=0.01):
        backend = 'HHpyNN'
        self.current_src_name = current_src_name
        self.cell_name = cell_name
        self.adexp = True
        self.dt = dt

        #def init_backend(self, attrs=None, simulator='neuron', DTC = None):
        #self.Izhikevich = Izhikevich
        #self.Population = Population
        self.DCSource = DCSource
        self.setup = setup
        self.model_path = None
        self.related_data = {}
        self.lookup = {}
        self.attrs = {}
        self.neuron = neuron
        self.model._backend.use_memory_cache = False
        self.model.unpicklable += ['h','ns','_backend']

        if type(DTC) is not type(None):
            if type(DTC.attrs) is not type(None):

                self.set_attrs(**DTC.attrs)
                assert len(self.model.attrs.keys()) > 0

            if hasattr(DTC,'current_src_name'):
                self._current_src_name = DTC.current_src_name

            if hasattr(DTC,'cell_name'):
                self.cell_name = DTC.cell_name
        #if DTC is not None:
        #    self.set_attrs(**DTC.attrs)
        super(HHpyNNBackend, self).init_backend()#*args, **kwargs)

    def get_membrane_potential(self):
        """Must return a neo.core.AnalogSignal.
        And must destroy the hoc vectors that comprise it.
        """

        data = self.hhcell.get_data().segments[0]
        volts = data.filter(name="v")[0]


        vm = AnalogSignal(volts,
             units = mV,
             sampling_period = self.dt *ms)

        return vm

    def _backend_run(self):
        '''
        pyNN lazy array demands a minimum population size of 3. Why is that.
        '''
        results = {}
        DURATION = 1000.0



        if self.celltype == 'HH_cond_exp':
            self.hhcell.record('spikes','v')
        else:
            self.neuron.record_v(self.hhcell, "Results/HH_cond_exp_%s.v" % str(neuron))
            #self.neuron.record_gsyn(self.hhcell, "Results/HH_cond_exp_%s.gsyn" % str(neuron))
        self.neuron.run(DURATION)
        data = self.hhcell.get_data().segments[0]
        volts = data.filter(name="v")[0]#/10.0

        vm = AnalogSignal(volts,
                     units = mV,
                     sampling_period = self.dt *ms)
        results['vm'] = vm
        results['t'] = vm.times # self.times
        results['run_number'] = results.get('run_number',0) + 1
        return results

    def load_model(self):
        neuron = None
        if self.adexp:
        	self.hhcell = neuron.create(EIF_cond_exp_isfa_ista())
        elif self.HH:
        	self.hhcell = neuron.create(HH_cond_exp())
        elif self.Iz:
            self.hhcell = neuron.create(EIF_cond_exp_isfa_ista())
        neuron.setup(timestep=self.dt, min_delay=1.0)




    def set_attrs(self, **attrs):
        self.init_backend()
        self.model.attrs.update(attrs)
        assert type(self.model.attrs) is not type(None)
        self.hhcell[0].set_parameters(**attrs)
        return self


    def inject_square_current(self, current):
        attrs = copy.copy(self.model.attrs)
        self.init_backend()
        self.set_attrs(**attrs)
        c = copy.copy(current)
        if 'injected_square_current' in c.keys():
            c = current['injected_square_current']

        stop = float(c['delay'])+float(c['duration'])
        duration = float(c['duration'])
        start = float(c['delay'])
        amplitude = float(c['amplitude'])
        electrode = self.neuron.DCSource(start=start, stop=stop, amplitude=amplitude)

        electrode.inject_into(self.hhcell)
        self.results = self._local_run()
        self.vm = self.results['vm']
