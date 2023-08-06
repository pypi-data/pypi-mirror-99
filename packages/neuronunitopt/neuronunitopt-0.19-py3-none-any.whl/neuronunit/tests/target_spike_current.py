"""F/I neuronunit tests, e.g. investigating firing rates and patterns as a
function of input current"""

import os
import multiprocessing

global cpucount
cpucount = multiprocessing.cpu_count()
from .base import np, pq, ncap, VmTest, scores, AMPL

ALLEN_DURATION = 2000 * pq.ms
ALLEN_DELAY = 1000 * pq.ms


import os
import quantities
import neuronunit

import quantities as pq
import numpy as np
import copy
import pdb
import time
import copy

from neuronunit.capabilities.spike_functions import (
    get_spike_waveforms,
    spikes2amplitudes,
    threshold_detection,
)

#
# When using differentiation based spike detection is used this is faster.


class SpikeCountSearch(VmTest):
    """
    A parallel Implementation of a Binary search algorithm,
    which finds a rheobase prediction.

    Strengths: this algorithm is faster than the serial class present in this file for model backends that are not able to
    implement numba jit optimisation.
    Failure to implement JIT happens to be typical of a signifcant number of backends
    """

    def _extra(self):
        self.verbose = 0

    required_capabilities = (ncap.ReceivesSquareCurrent, ncap.ProducesSpikes)
    description = (
        "A test of the rheobase, i.e. the minimum injected current "
        "needed to evoke at least one spike."
    )
    units = pq.pA
    ephysprop_name = "Rheobase"
    score_type = scores.ZScore

    def generate_prediction(self, model):
        def check_fix_range(model):
            """
            Inputs: lookup, A dictionary of previous current injection values
            used to search rheobase
            Outputs: A boolean to indicate if the correct rheobase current was found
            and a dictionary containing the range of values used.
            If rheobase was actually found then rather returning a boolean and a dictionary,
            instead logical True, and the rheobase current is returned.
            given a dictionary of rheobase search values, use that
            dictionary as input for a subsequent search.
            """

            steps = []
            model.rheobase = {}
            model.rheobase["value"] = None
            sub, supra = get_sub_supra(model.lookup)
            if (len(sub) + len(supra)) == 0:
                # This assertion would only be occur if there was a bug
                assert sub.max() <= supra.min()
            elif len(sub) and len(supra):
                # Termination criterion
                # print(cpucount)
                steps = np.linspace(sub.max(), supra.min(), cpucount + 1) * pq.pA
                steps = steps[1:-1] * pq.pA
            elif len(sub):
                steps = np.linspace(sub.max(), 2 * sub.max(), cpucount + 1) * pq.pA
                steps = steps[1:-1] * pq.pA
            elif len(supra):
                steps = np.linspace(supra.min() - 10, supra.min(), cpucount + 1) * pq.pA
                steps = steps[1:-1] * pq.pA

            model.current_steps = steps
            return model, sub, supra

        def get_sub_supra(lookup):
            sub, supra = [], []
            for current, n_spikes in lookup.items():
                if n_spikes < self.observation["value"]:
                    sub.append(current)
                elif n_spikes > self.observation["value"]:
                    supra.append(current)
                delta = n_spikes - self.observation["value"]
                # print(delta,'difference \n\n\n\nn')
            sub = np.array(sorted(list(set(sub))))
            supra = np.array(sorted(list(set(supra))))
            return sub, supra

        def check_current(model):
            """
            Inputs are an amplitude to test and a virtual model
            output is an virtual model with an updated dictionary.
            """
            model.boolean = False

            ampl = float(model.ampl)
            if ampl not in model.lookup or len(model.lookup) == 0:
                uc = {
                    "amplitude": ampl * pq.pA,
                    "duration": ALLEN_DURATION,
                    "delay": ALLEN_DELAY,
                    "padding": 342.85 * pq.ms,
                }

                vm = model.inject_square_current(**uc)
                n_spikes = model.get_spike_count()
                model.lookup[float(ampl)] = n_spikes

                target_spk_count = self.observation["value"]

                if n_spikes == target_spk_count:

                    model.lookup[float(ampl)] = n_spikes
                    model.rheobase = {}
                    model.rheobase["value"] = float(ampl) * pq.pA
                    model.target_spk_count = None
                    model.target_spk_count = model.rheobase["value"]
                    model.boolean = True
                    if self.verbose > 2:
                        print(
                            "gets here",
                            n_spikes,
                            target_spk_count,
                            n_spikes == target_spk_count,
                        )
                    return model

            return model

        def init_model(model):
            """
            Exploit memory of last model in genes.
            """
            if model.initiated == True:

                model = check_current(model)
                if model.boolean:

                    return model

                else:

                    if type(model.current_steps) is type(float):
                        model.current_steps = [
                            0.75 * model.current_steps,
                            1.25 * model.current_steps,
                        ]
                    elif type(model.current_steps) is type(list):
                        model.current_steps = [
                            float(s * 1.25) * pq.pA for s in model.current_steps
                        ]
                    model.initiated = (
                        True  # logically unnecessary but included for readibility
                    )
            if model.initiated == False:
                model.boolean = False
                # steps = np.linspace(-12,67,int(8))
                ###
                # These values are important for who knows what reason
                steps = np.linspace(0.0, 65, cpucount)
                ###
                steps_current = [float(s) * pq.pA for s in steps]
                model.current_steps = steps_current
                model.initiated = True
            return model

        def find_target_current(self, model):
            # This line should not be necessary:
            # a class, VeryReducedModel has been made to circumvent this.
            cnt = 0
            sub = np.array([0, 0])
            supra = np.array([0, 0])
            ##
            #
            ## Important number
            big = 50
            while model.boolean == False and cnt < big:

                # negeative spiker
                if len(sub):
                    if sub.max() < -1.0:
                        pass
                model_clones = [model for i in range(0, len(model.current_steps))]
                for i, s in enumerate(model.current_steps):
                    model_clones[i] = copy.deepcopy(model_clones[i])
                    model_clones[i].ampl = copy.deepcopy(model.current_steps[i])
                    model_clones[i].backend = copy.deepcopy(model.backend)

                model_clones = [d for d in model_clones if not np.isnan(d.ampl)]
                set_clones = set([float(d.ampl) for d in model_clones])
                model_clone = []
                for model, sc in zip(model_clones, set_clones):
                    model = copy.deepcopy(model)
                    model.ampl = float(sc) * pq.pA
                    model = check_current(model)
                    model_clone.append(model)

                for model in model_clone:
                    if model.boolean == True:
                        return model

                for d in model_clone:
                    model.lookup.update(d.lookup)
                model, sub, supra = check_fix_range(model)

                # sub, supra = get_sub_supra(model.lookup)
                if len(supra) and len(sub):
                    delta = float(supra.min()) - float(sub.max())
                    # tolerance = 0.0

                if self.verbose >= 2:
                    print(
                        "xx Try %d: SubMax = %s; SupraMin = %s"
                        % (
                            cnt,
                            sub.max() if len(sub) else None,
                            supra.min() if len(supra) else None,
                        )
                    )
                cnt += 1
                reversed = {v: k for k, v in model.lookup.items()}
            if cnt == big:
                if self.verbose >= 2:
                    print("counted out and thus wrong spike count")
            return model

        model = init_model(model)
        prediction = {}
        temp = find_target_current(self, model).rheobase

        if type(temp) is not type(None) and not type(dict):
            prediction["value"] = float(temp) * pq.pA
        elif type(temp) is not type(None) and type(dict):
            if temp["value"] is not None:
                prediction["value"] = float(temp["value"]) * pq.pA
            else:
                prediction = None
        else:
            prediction = None
        return prediction


class SpikeCountRangeSearch(VmTest):
    """
    A parallel Implementation of a Binary search algorithm,
    which finds a rheobase prediction.

    Strengths: this algorithm is faster than the serial class, present in this file for model backends that are not able to
    implement numba jit optimisation, which actually happens to be typical of a signifcant number of backends

    Weaknesses this serial class is significantly slower, for many backend implementations including raw NEURON
    NEURON via PyNN, and possibly GLIF.

    """

    def _extra(self):
        self.verbose = 0

    required_capabilities = (ncap.ReceivesSquareCurrent, ncap.ProducesSpikes)
    name = "Rheobase test"
    description = (
        "A test of the rheobase, i.e. the minimum injected current "
        "needed to evoke at least one spike."
    )
    units = pq.pA
    # tolerance  # Rheobase search tolerance in `self.units`.
    ephysprop_name = "Rheobase"
    # score_type = scores.ZScore

    def generate_prediction(self, model):
        def check_fix_range(model):
            """
            Inputs: lookup, A dictionary of previous current injection values
            used to search rheobase
            Outputs: A boolean to indicate if the correct rheobase current was found
            and a dictionary containing the range of values used.
            If rheobase was actually found then rather returning a boolean and a dictionary,
            instead logical True, and the rheobase current is returned.
            given a dictionary of rheobase search values, use that
            dictionary as input for a subsequent search.
            """

            steps = []
            model.rheobase = None
            sub, supra = get_sub_supra(model.lookup)

            import pdb

            pdb.set_trace()

            if (len(sub) + len(supra)) == 0:
                # This assertion would only be occur if there was a bug
                assert sub.max() <= supra.min()
            elif len(sub) and len(supra):
                # Termination criterion

                steps = np.linspace(sub.max(), supra.min(), cpucount + 1)  # * pq.pA
                steps = steps[1:-1] * pq.pA
            elif len(sub):
                steps = np.linspace(sub.max(), 2 * sub.max(), cpucount + 1)  # * pq.pA
                steps = steps[1:-1] * pq.pA
            elif len(supra):
                steps = np.linspace(
                    supra.min() - 100, supra.min(), cpucount + 1
                )  # * pq.pA
                steps = steps[1:-1] * pq.pA

            model.current_steps = steps
            return model

        def init_model(model):
            """
            Exploit memory of last model in genes.
            """
            # check for memory and exploit it.
            if model.initiated == True:

                model = check_current(model)
                if model.boolean:

                    return model

                else:
                    # Exploit memory of the genes to inform searchable range.
                    # if this model has lineage, assume it didn't mutate that far away from it's ancestor.
                    # using that assumption, on first pass, consult a very narrow range, of test current injection samples:
                    # only slightly displaced away from the ancestors rheobase value.

                    if type(model.current_steps) is type(float):
                        model.current_steps = [
                            0.75 * model.current_steps,
                            1.25 * model.current_steps,
                        ]
                    elif type(model.current_steps) is type(list):
                        model.current_steps = [s * 1.25 for s in model.current_steps]
                    model.initiated = (
                        True  # logically unnecessary but included for readibility
                    )
            if model.initiated == False:

                model.boolean = False

                steps = np.linspace(0, 85.0, int(8))

                steps_current = [i * pq.pA for i in steps]
                model.current_steps = steps_current
                model.initiated = True
            return model

        def find_target_current(self, model):
            cnt = 0
            sub = np.array([0, 0])
            supra = np.array([0, 0])

            big = 255

            while model.boolean == False and cnt < big:

                # negeative spiker
                if len(sub):
                    if sub.max() < -1.0:
                        pass
                        # use_diff = True # differentiate the wave to look for spikes

                # be = model.backend
                model_clones = [model for i in range(0, len(model.current_steps))]
                for i, s in enumerate(model.current_steps):
                    model_clones[i] = copy.copy(model_clones[i])
                    model_clones[i].ampl = copy.copy(model.current_steps[i])
                    model_clones[i].backend = copy.copy(model.backend)

                model_clones = [d for d in model_clones if not np.isnan(d.ampl)]
                set_clones = set([float(d.ampl) for d in model_clones])
                model_clone = []
                for model, sc in zip(model_clones, set_clones):
                    # model = copy.copy(model)
                    model.ampl = sc * pq.pA
                    model = check_current(model)
                    model_clone.append(model)

                for model in model_clone:
                    if model.boolean == True:
                        return model

                for d in model_clone:
                    model.lookup.update(d.lookup)
                model = check_fix_range(model)

                # sub, supra = get_sub_supra(model.lookup)
                if len(supra) and len(sub):
                    delta = float(supra.min()) - float(sub.max())

                    if str(supra.min()) == str(sub.max()):
                        if self.verbose >= 2:
                            print(
                                delta,
                                "a neuron, close to the edge! Multi spiking rheobase. # spikes: ",
                                len(supra),
                            )
                        if len(supra) < 300:
                            model.rheobase["value"] = float(supra.min())
                            model.boolean = True
                            model.lookup[float(supra.min())] = len(supra)
                        else:
                            if type(model.rheobase) is type(None):
                                model.rheobase = {}
                                model.rheobase["value"] = None
                                model.boolean = False
                                model.lookup[float(supra.min())] = len(supra)

                                return model

                if self.verbose >= 2:
                    print("not rheobase alg")
                    print(
                        "Try %d: SubMax = %s; SupraMin = %s"
                        % (
                            cnt,
                            sub.max() if len(sub) else None,
                            supra.min() if len(supra) else None,
                        )
                    )
                cnt += 1
            return model

        model = init_model(model)
        prediction = {}
        temp = find_target_current(self, model).rheobase
        if type(temp) is not type(None):
            if type(temp) is not type(dict()):
                prediction["value"] = float(temp) * pq.pA
            elif type(temp) is type(dict()):
                if type(temp["value"]) is not type(None):
                    prediction["value"] = float(temp["value"]) * pq.pA
                else:
                    prediction["value"] = None
            elif type(temp) is type(None):
                prediction["value"] = None
        else:
            prediction = None
        return prediction
