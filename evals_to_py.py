"""
Script to manage .out files.
"""
import sys
import numpy as np
from os import listdir
import argparse

PLASMA_EVAL_COL_INDEX = 1
TOTAL_EVAL_HEADER = 'Total Energy Eigenvalues:'
TOTAL_EVAL_INDEX = 3

BETA = 'beta'

def extract_dir_info(dir_path, out_path=None, betas=False):
    """
    Extracts evecs (or beta vals) where each column is a evec and evecs
    are sorted from left to right. One unfortunate thing is that there seem
    to be varying amounts of evals for some reason. If evals are missing
    fill in 0s at the bottom.
    """
    files = listdir(dir_path)
    files.sort()
    cols = []
    extract_vec = _betas_to_vec if betas else _evecs_to_vec
    for col, f in enumerate(files):
        f_path = ''.join([dir_path, '/', f])
        cols.append(extract_vec(f_path))
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

def _betas_to_vec(path):
    """
    Extract the beta values in the output and return as a vector.
    """
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    beta_line_ind = 0
    for line in lines:
        beta_line_ind += 1
        headers = line.split()
        if len(headers) > 0 and BETA in headers[0]:
            beta_line_ind += 1
            break
    if beta_line_ind == len(lines):
        raise ValueError('Could not find beta header in file: %s' % path)
    return np.asarray([float(n) for n in lines[beta_line_ind].split()])

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Script for extracting DCON output info')
    parser.add_argument('src_dir', type=str,
                        help='Path to directory of DCON output')
    parser.add_argument('dest_path', type=str,
                        help='Path of .npy file to write result to.')
    parser.add_argument('--beta', action='store_true',
                        help='Extract beta values')
    args = parser.parse_args()
    print extract_dir_info(args.src_dir, args.dest_path, betas=args.beta)
