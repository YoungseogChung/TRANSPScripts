"""
Script to manage .out files.
"""
import sys
import numpy as np
from os import listdir

PLASMA_EVAL_COL_INDEX = 1
TOTAL_EVAL_HEADER = 'Total Energy Eigenvalues:'
TOTAL_EVAL_INDEX = 3

def extract_dir_evals(dir_path, out_path=None):
    """
    Extracts evecs where each column is a evec and evecs are sorted from left
    to right. One unfortunate thing is that there seem to be varying amounts
    of evals for some reason. If evals are missing fill in 0s at the bottom.
    """
    files = listdir(dir_path)
    files.sort()
    cols = []
    for col, f in enumerate(files):
        f_path = ''.join([dir_path, '/', f])
        cols.append(_evecs_to_vec(f_path))
    eval_mat = np.zeros((max([len(col) for col in cols]), len(files)))
    for col_ind, col in enumerate(cols):
        eval_mat[:len(col),col_ind] = col
    if out_path is not None:
        np.save(out_path, eval_mat)
    return eval_mat

def _evecs_to_vec(path):
    """
    Get the total energy total evecs and load into numpy vector.
    """
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    found_total_energy = False
    start_read = False
    evals = []
    for line in lines:
        if TOTAL_EVAL_HEADER in line:
            found_total_energy = True
        elif found_total_energy:
            nums = line.split()
            if len(nums) > 0  and nums[0] == '1':
                start_read = True
            if start_read:
                if len(nums) > 0:
                    evals.append(nums[TOTAL_EVAL_INDEX])
                else:
                    break
    if len(evals) == 0:
        raise ValueError('Invalid format of file, no evals found: %s' % path)
    return np.asarray(evals)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Incorrect number of command line args.')
    src_dir = sys.argv[1]
    out_path = sys.argv[2]
    print extract_dir_evals(src_dir, out_path)
