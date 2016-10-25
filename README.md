interpgain
=======

[CASA](http://casa.nrao.edu/) task to linearly interpolate and optionally extrapolate missing gain calibration solutions.

Latest version: 1.1 ([download here](https://github.com/chrishales/interpgain/releases/latest))

Tested with: CASA Version 4.7.0

interpgain is released under a BSD 3-Clause License (open source, commercially useable); refer to LICENSE for details.

Feedback regarding interpgain is always welcome.

A before and after example is shown below for phase solutions on a single spectral window, feed, and antenna. Both interpolation and extrapolation was applied.

<img src="before.png" width="400" title="before"> <img src="after.png" width="400" title="interp+extrap">

Installation
======

Download the latest version of the source files from [here](https://github.com/chrishales/interpgain/releases/latest).

Place the source files into a directory containing your measurement set. Without changing directories, open CASA and type
```
os.system('buildmytasks')
```
then exit CASA. A number of files should have been produced, including ```mytasks.py```. Reopen CASA and type
```
execfile('mytasks.py')
```
To see the parameter listing, type
```
inp interpgain
```
For more details on how interpgain works, type
```
help interpgain
```
Now set some parameters and press go!

For a more permanent installation, place the source files into a dedicated interpgain code directory and perform the steps above. Then go to the hidden directory ```.casa``` which resides in your home directory and create a file called ```init.py```. In this file, put the line
```
execfile('/<path_to_interpgain_directory>/mytasks.py')
```
interpgain will now be available when you open a fresh terminal and start CASA within any directory.

Acknowledging use of interpgain
======

interpgain is provided in the hope that it (or elements of its code) will be useful for your work. If you find that it is, I would appreciate your acknowledgement by citing [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.163002.svg)](https://doi.org/10.5281/zenodo.163002) as follows (note the [AAS guidelines for citing software](http://journals.aas.org/policy/software.html)):
```
Hales, C. A. 2016, interpgain, v1.1, doi:10.5281/zenodo.163002, as developed on GitHub
```
