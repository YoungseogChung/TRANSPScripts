"""
Assuming that there are stored results, this script will do the whole flow
of fetching the results onto local machine, running DCON, and then converting
dcon results into a ndarray.
"""

import subprocess

from evals_to_py import extract_evals

DONE = 'Done'

def get_result_evals(dcon_dir, gfile_path, dcon_out_path, num_intervals=20,
                     num_threads=15):
    # TODO: Right now fetch_results.sh is hardcoded, but later this will need
    # arguments so we are getting the correct result.
    subprocess.check_call(['./fetch_results.sh', gfile_path])
    subprocess.check_call(['./run_dcon.sh', dcon_dir, gfile_path,
                           dcon_out_path, str(num_intervals), str(num_threads)])
    return extract_evals(dcon_out_path)

if __name__ == '__main__':
    dcon_dir = '/home/ian/stride/dcon'
    gfile_path = '/home/ian/Documents/research/sim_output/gfiles/tmp/state1633030101_0x1.geq'
    dcon_out_path = '/home/ian/Documents/research/sim_output/dcon_out/tmp/tst_out.out'
    print get_result_evals(dcon_dir, gfile_path, dcon_out_path)
