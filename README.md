# TRANSPScripts
Useful scripts for running TRANSP simulations and processing the output.

## batch_dcon.sh

This is a very basic script used for batch runs of DCON. It takes a target directory consisting of gfiles and will 
write the output to another specified directory.
You must move the batch_dcon.sh file to [appropriate_path]/stride-master/dcon/ before running it.

#### Usage
```
./batch_dcon.sh <gfile_directory> <output_directory> <num_intervals> <num_threads>
```

The number of intervals and number of threads used in the tutorial is 20 and 15, respectively.

## evals_to_py.py

This script takes DCON output and formats the information in it as numpy ndarrays. As of now, when called it is called
it takes a directory of output, sorts the file names (make sure sorted file names correspond to time step, and creates
a matrix where each column corresponds to one of the files.

#### Usage
To get the "total" column in the "Total Energy" eigenvalue column
```
evals_to_py.py <path_to_dcon_output_dir> <path_to_output_file_name.npy_file> 
```
Note that it has been observed that there are varying number of eigenvalues in these files. As a result, there may be
0s at the end of some columns in the matrix if the file doesn't have as many eigenvalues.

To get the values in the row for beta...
```
evals_to_py.py <path_to_dcon_output_dir> <path_to_output_.npy_file> --beta
```
