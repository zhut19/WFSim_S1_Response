import hax, pax
from pax import core
from hax.runs import is_mc
import pandas as pd
import pickle, io, sys, os
from pax.plugins.io import Pickle

import numpy as np
import zlib
from pax import configuration


print('PAX', pax.__version__)
print('HAX', hax.__version__)


class RenameUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = module
        if module == "wfsim.pax_datastructure.datastructure":
            renamed_module = "pax.datastructure"

        return super(RenameUnpickler, self).find_class(renamed_module, name)


def renamed_load(file_obj):
    return RenameUnpickler(file_obj).load()


def renamed_loads(pickled_bytes):
    file_obj = io.BytesIO(pickled_bytes)
    return renamed_load(file_obj)


m = sys.modules['pax.plugins.io.Pickle']
m.pickle.loads = renamed_loads


def get_run_number(run_id):
        return int(run_id)

m = sys.modules['hax.runs']
m.get_run_number = get_run_number


def init_core(run_number):
    user = getpass.getuser()
    core_processor = core.Processor(
        config_names=['_base', 'XENON1T'],
        just_testing=False,
        config_dict={
            'pax':{
                'input_name' : '/dali/lgrandi/%s/sim/pax_data/XENON1T_MC_%s'%(user, run_number),
                'output_name': '/dali/lgrandi/%s/sim/pax_data/processed/%s'%(user, run_number),
                'look_for_config_in_runs_db': False},
            'MC':{
                'mc_generated_data': True,
                'mc_sr_parameters': "sr1",
                'mc_run_number': run_number,}
        })
    return core_processor


dtype = [
('event_number', 'i8'),
('event_start', 'i8'),
('run_number', 'i8'),
('s1', 'f8'),
('s1_area_fraction_top', 'f8'),
('s1_range_50p_area', 'f8'),
('s1_rise_time', 'f8'),
('s1_center_time', 'f8'),
('s1_n_hits', 'f8'),
('s1_tight_coincidence', 'i4'),
('time', 'i8'),
('endtime', 'i8'),
]


def extract_data(result, event, index):
    cnt = 0
    
    for p in event.s1s():
        result[index]['event_number'] = event.event_number
        result[index]['event_start'] = event.start_time
        result[index]['s1'] = p.area
        result[index]['s1_area_fraction_top'] = p.area_fraction_top
        result[index]['s1_range_50p_area'] = p.range_50p_area
        result[index]['s1_rise_time'] = -p.area_decile_from_midpoint[1]
        result[index]['s1_center_time'] = p.center_time
        result[index]['s1_n_hits'] = p.n_hits
        result[index]['time'] = p.left * 10 + event.start_time
        result[index]['endtime'] = p.right * 10 + event.start_time
        result[index]['s1_tight_coincidence'] = p.tight_coincidence

        index += 1
        cnt += 1
        if cnt == 10:
            break
    
    return index

if __name__ == '__main__':
    if len(sys.argv) == 2:
        name = sys.argv[1]
    else:
        sys.exit(1)


    processor = init_core(name)
    result = np.zeros(processor.number_of_events * 10, dtype=np.dtype(dtype))
    index = 0
    for event in processor.get_events():

        for j, plugin in enumerate(processor.action_plugins[:-6]):
            if 'PosRec' in plugin.name: continue
            event = plugin.process_event(event)

        index = extract_data(result, event, index)
    result['run_number'] = int(name)

    with open('/dali/lgrandi/zhut/minitrees/pax_s1b_tb/%s_HitPerPE'%name, 'wb') as f:
        result = zlib.compress(result, 4)
        f.write(result)
