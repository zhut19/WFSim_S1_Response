import straxen, strax, wfsim
print(strax.__file__, 'v', strax.__version__)
print(straxen.__file__, 'v', straxen.__version__)
print(wfsim.__file__, 'v', wfsim.__version__)

import sys, os, getpass
import numpy as np
import json

pwd, user = os.getcwd(), getpass.getuser()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        rn = int(sys.argv[1])
    else:
        sys.exit(1)

    strax.Mailbox.DEFAULT_TIMEOUT=10000
    config=dict(fax_file=f'{pwd}/instructions/test_rnd_%d.csv'%rn,
                run_number=rn,
                exclude_dpe_in_truth=True, # False if dpe treated as one photon
                output_name=f'/dali/lgrandi/{user}/sim/pax_data')

    pax_sim = wfsim.PaxEventSimulator(config)
    pax_sim.compute()