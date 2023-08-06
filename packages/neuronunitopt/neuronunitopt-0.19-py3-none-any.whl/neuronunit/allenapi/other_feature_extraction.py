def nuunit_allen_evaluation(dtc):
    if hasattr(dtc, "vtest"):
        values = [v for v in dtc.vtest.values()]
        for value in values:
            if str("injected_square_current") in value.keys():
                current = value["injected_square_current"]
                current["amplitude"] = dtc.rheobase * 3.0
                break
    else:
        try:
            observation_spike = {"range": dtc.tsr}
        except:
            dtc.tsr = [
                dtc.pre_obs["spike_count"]["mean"] - 2,
                dtc.pre_obs["spike_count"]["mean"] + 5,
            ]
            observation_spike = {"range": dtc.tsr}

        if not str("GLIF") in str(dtc.backend):
            scs = SpikeCountRangeSearch(observation_spike)
            model = new_model(dtc)
            assert model is not None
            target_current = scs.generate_prediction(model)

            dtc.ampl = None
            if target_current is not None:
                dtc.ampl = target_current["value"]
                dtc = prediction_current_and_features(dtc)
                dtc = filter_predictions(dtc)
                dtc.error_length = len(dtc.preds)
            if target_current is None:
                dtc.ampl = None
                dtc.preds = {}
                return dtc
        else:
            try:
                with open("waves.p", "wb") as f:
                    make_stim_waves = pickle.load(f)
            except:
                make_stim_waves = make_stim_waves_func()
            dtc = dtc_to_rheo(dtc)
            dtc.ampl = dtc.rheobase["value"] * 3.0
            dtc = prediction_current_and_features(dtc)
            dtc = filter_predictions(dtc)
            dtc.error_length = len(dtc.preds)
        return dtc


def nuunit_dm_evaluation(dtc):
    model = dtc.dtc_to_model()
    model.set_attrs(dtc.attrs)
    model.vm_soma = None
    model.vm_soma = dtc.vm_soma
    if type(dtc.rheobase) is type(dict()):
        rheobase = dtc.rheobase["value"]
    else:
        rheobase = dtc.rheobase
    model.druckmann2013_standard_current = None
    model.druckmann2013_standard_current = rheobase * 1.5
    model.vm30 = None
    model.vm30 = dtc.vm30
    if rheobase < 0.0 or np.max(dtc.vm30) < 0.0:  # or model.get_spike_count()<1:
        dtc.dm_test_features = None
        return dtc
    model.druckmann2013_strong_current = None
    model.druckmann2013_strong_current = rheobase * 3.0

    model.druckmann2013_input_resistance_currents = [
        -5.0 * pq.pA,
        -10.0 * pq.pA,
        -15.0 * pq.pA,
    ]  # ,copy.copy(current)
    from neuronunit.tests import dm_test_container  # import Interoperabe

    DMTNMLO = dm_test_container.DMTNMLO()
    DMTNMLO.test_setup(None, None, model=model)
    dm_test_features = DMTNMLO.runTest()
    dtc.AP1DelayMeanTest = None
    dtc.AP1DelayMeanTest = dm_test_features["AP1DelayMeanTest"]
    dtc.InputResistanceTest = dm_test_features["InputResistanceTest"]
    dtc.dm_test_features = None
    dtc.dm_test_features = dm_test_features
    return dtc


def input_resistance_dm_evaluation(dtc):
    model = dtc.dtc_to_model()
    model.set_attrs(dtc.attrs)
    try:
        values = [v for v in dtc.protocols.values()][0]

    except:
        values = [v for v in dtc.tests.values()][0]
    current = values["injected_square_current"]
    current["amplitude"] = dtc.rheobase * 1.5
    model.inject_square_current(current)
    vm15 = model.get_membrane_potential()
    model.vm_soma = None
    model.vm_soma = vm15
    model.druckmann2013_standard_current = None
    model.druckmann2013_standard_current = dtc.rheobase * 1.5
    current["amplitude"] = dtc.rheobase * 3.0

    vm30 = model.inject_square_current(current)
    vm30 = model.get_membrane_potential()
    if dtc.rheobase < 0.0 or np.max(vm30) < 0.0 or model.get_spike_count() < 1:
        dtc.dm_test_features = None
        return dtc
    model.vm30 = None
    model.vm30 = vm30
    model.druckmann2013_strong_current = None
    model.druckmann2013_strong_current = dtc.rheobase * 3.0

    model.druckmann2013_input_resistance_currents = [
        -5.0 * pq.pA,
        -10.0 * pq.pA,
        -15.0 * pq.pA,
    ]  # ,copy.copy(current)

    DMTNMLO = dm_test_container.DMTNMLO()
    DMTNMLO.test_setup(None, None, model=model)
    dm_test_features = DMTNMLO.runTest()
    dtc.AP1DelayMeanTest = None
    dtc.AP1DelayMeanTest = dm_test_features["AP1DelayMeanTest"]
    dtc.InputResistanceTest = dm_test_features["InputResistanceTest"]

    dtc.dm_test_features = None
    dtc.dm_test_features = dm_test_features
    return dtc


"""
def nuunit_dm_rheo_evaluation(dtc):
    model = dtc.dtc_to_model()
    model.set_attrs(dtc.attrs)
    try:
        values = [v for v in dtc.protocols.values()][0]
    except:
        values = [v for v in dtc.tests.values()][0]

    current = values['injected_square_current']
    current['amplitude'] = dtc.rheobase
    model.inject_square_current(current)
    vm15 = model.get_membrane_potential()
    model.vm_soma = None
    model.vm_soma = vm15
    model.druckmann2013_standard_current = None
    model.druckmann2013_standard_current = dtc.rheobase * 1.5
    current['amplitude'] = dtc.rheobase * 3.0
    vm30 = model.inject_square_current(current)
    vm30 = model.get_membrane_potential()
    if dtc.rheobase <0.0 or np.max(vm30)<0.0 or model.get_spike_count()<1:
        return dtc
    model.vm30 = None
    model.vm30 = vm30
    model.druckmann2013_strong_current = None
    model.druckmann2013_strong_current = dtc.rheobase * 3.0
    model.druckmann2013_input_resistance_currents =[ -5.0*pq.pA, -10.0*pq.pA, -15.0*pq.pA]#,copy.copy(current)
    DMTNMLO = dm_test_container.DMTNMLO()
    DMTNMLO.test_setup_subset(None,None,model= model)
    dm_test_features = DMTNMLO.runTest()
    dtc.dm_test_features = None
    dtc.dm_test_features = dm_test_features
    return dtc
#from allensdk.ephys.ephys_extractor import EphysSweepFeatureExtractor

"""


def retestobs(dtc):
    if type(dtc.tests) is not type(list()):
        dtc.tests = list(dtc.tests.values())
    for t in dtc.tests:
        t.observation["std"] = np.abs(t.observation["std"])
    return dtc


def rekeyeddm(dtc):
    standard = 0
    strong = 0
    easy_map = [
        {"AP12AmplitudeDropTest": standard},
        {"AP1SSAmplitudeChangeTest": standard},
        {"AP1AmplitudeTest": standard},
        {"AP1WidthHalfHeightTest": standard},
        {"AP1WidthPeakToTroughTest": standard},
        {"AP1RateOfChangePeakToTroughTest": standard},
        {"AP1AHPDepthTest": standard},
        {"AP2AmplitudeTest": standard},
        {"AP2WidthHalfHeightTest": standard},
        {"AP2WidthPeakToTroughTest": standard},
        {"AP2RateOfChangePeakToTroughTest": standard},
        {"AP2AHPDepthTest": standard},
        {"AP12AmplitudeChangePercentTest": standard},
        {"AP12HalfWidthChangePercentTest": standard},
        {"AP12RateOfChangePeakToTroughPercentChangeTest": standard},
        {"AP12AHPDepthPercentChangeTest": standard},
        {"InputResistanceTest": str("ir_currents")},
        {"AP1DelayMeanTest": standard},
        {"AP1DelaySDTest": standard},
        {"AP2DelayMeanTest": standard},
        {"AP2DelaySDTest": standard},
        {"Burst1ISIMeanTest": standard},
        {"Burst1ISISDTest": standard},
        {"InitialAccommodationMeanTest": standard},
        {"SSAccommodationMeanTest": standard},
        {"AccommodationRateToSSTest": standard},
        {"AccommodationAtSSMeanTest": standard},
        {"AccommodationRateMeanAtSSTest": standard},
        {"ISICVTest": standard},
        {"ISIMedianTest": standard},
        {"ISIBurstMeanChangeTest": standard},
        {"SpikeRateStrongStimTest": strong},
        {"AP1DelayMeanStrongStimTest": strong},
        {"AP1DelaySDStrongStimTest": strong},
        {"AP2DelayMeanStrongStimTest": strong},
        {"AP2DelaySDStrongStimTest": strong},
        {"Burst1ISIMeanStrongStimTest": strong},
        {"Burst1ISISDStrongStimTest": strong},
    ]
    dm_labels = [list(keys.keys())[0] for keys in easy_map]
    rekeyed = {}
    dmtf = dtc.dm_test_features
    keep_columns = {}
    for l in easy_map:
        for k in l.keys():
            if str(k) + str("_3.0x") in dmtf.keys():
                keep_columns.append(str(k) + str("_3.0x"))
            elif str(k) + str("_1.5x") in df.columns:
                keep_columns.append(str(k) + str("_1.5x"))
    return dtc


import scipy
from multiprocessing import Process, Pipe
import multiprocessing

# https://stackoverflow.com/questions/3288595/multiprocessing-how-to-use-pool-map-on-a-function-defined-in-a-class


def evaluate_allen(dtc):
    # assign worst case errors, and then over write them with situation informed errors as they become available.
    fitness = [1.0 for i in range(0, len(dtc.ascores))]
    if dtc.ascores[str(t)] is None:
        fitness[int_] = 1.0
    else:
        fitness[int_] = dtc.ascores[str(t)]
    return tuple(
        fitness,
    )


def evaluate(dtc, allen=None):
    # assign worst case errors, and then over write them with situation informed errors as they become available.
    if not hasattr(dtc, str("SA")):
        return []
    else:
        if allen is not None:
            not_allen = [t for t in dtc.tests if not hasattr(t, "allen")]
            fitness = []
            dtc.tests = not_allen
            fitness = [v for v in dtc.SA.values]
            return augment_with_three_step(dtc, fitness)
        if allen is None:
            fitness = (v for v in dtc.SA.values)
            return fitness


from sciunit.scores import ZScore, RatioScore


def augment_with_three_step(dtc, fitness):
    temp_tests = copy.copy(dtc.tests)
    allen = [t for t in temp_tests if hasattr(t, "allen")]
    dtc = multi_spiking_feature_extraction(dtc)
    features = dtc.preds
    dtc.tests = temp_tests
    for t in allen:
        t.score_type = ZScore
    for t, (k, v) in zip(allen, features.items()):
        if t.name == k:
            t.set_prediction(v)
    for t in allen:
        if type(t.prediction["mean"]) is type(dict()):
            x = t.prediction["mean"]["mean"]
        else:
            x = t.prediction["mean"]
        try:
            result = np.abs(
                np.log(np.abs(x - t.observation["mean"]) / t.observation["std"])
            )
        except:
            try:
                model = dtc.dtc_to_model()
                result = t.judge(model)
            except:
                result = 1000.0
        fitness.append(result)
    for i, f in enumerate(fitness):
        if np.isnan(f) or np.isinf(f):
            fitness[i] = 1000.0
    return (f for f in fitness)


from dask import compute, delayed


def get_dm(dtcpop, pop=None):
    if PARALLEL_CONFIDENT:
        NPART = min(npartitions, len(dtcpop))
        dtcbag = [delayed(nuunit_dm_evaluation(d)) for d in dtcpop]
        dtcpop = compute(*dtcbag)

    else:
        dtcpop = list(map(nuunit_dm_evaluation, dtcpop))
    if type(pop) is not type(None):
        dtcpop, pop = score_attr(dtcpop, pop)
    return dtcpop, pop


def fun(f, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        q_out.put((i, f(x)))


def parmap(f, X, nprocs=multiprocessing.cpu_count()):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()

    proc = [
        multiprocessing.Process(target=fun, args=(f, q_in, q_out))
        for _ in range(nprocs)
    ]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


def pebble_parmap(f, X, nprocs=multiprocessing.cpu_count()):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()

    proc = [
        multiprocessing.Process(target=fun, args=(f, q_in, q_out))
        for _ in range(nprocs)
    ]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


def z_val(sig_level=0.05, two_tailed=True):
    """Returns the z value for a given significance level"""
    z_dist = scs.norm()
    if two_tailed:
        sig_level = sig_level / 2
        area = 1 - sig_level
    else:
        area = 1 - sig_level

    z = z_dist.ppf(area)

    return z
