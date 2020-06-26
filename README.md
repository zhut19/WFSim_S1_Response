# WFSim_S1_Response

A simple task of running WFSim to simulate S1s, process it with pax.

# How to run

Start one pax session and one strax session, we will be switching between the two.


Starting with the strax session ./pre_batch_test.ipynb, write instructions in csv files, run the test.

Switch into pax session (or any session outside container)
Continue with ./batch_job.ipynb, put run names into `loop_over`, they will be used as arguments for ./pax_wfsim_job.py and be submitted to dali

Once the simulation jobs are finished, process them with pax. The code to do it is in ./processdata/pre_batch_test.ipynb but as usual we want to submit them
with ./processdata/batch_job.ipynb, and run the GrowMTs.py (but no minitrees made in this analysis)

Switch back to strax session, for some convenient code written in strax
Run ./post_batch_analysis.ipynb for the real analysis.
