# run-octave

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ferreirad08/run-octave/blob/main/LICENSE)

A package for running Octave functions and calling Scripts in the Python interpreter!

## Nota
* Install [GNU Octave](https://www.gnu.org/software/octave/index).

## Requirements
* `python 3`
* `scipy`

## Installation

Simply install run-octave package from [PyPI](https://pypi.org/project/run-octave/)

    pip install run-octave

## Examples
        
    from run_octave import RunOctave
    import numpy as np

    # Create the RunOctave object and explicitly add the path to octave-gui.exe
    #octave = RunOctave(octave_path='C:/Program Files/GNU Octave/Octave-6.2.0/mingw64/bin/octave-gui.exe')
    octave = RunOctave(octave_path='C:/Octave/Octave-5.2.0/mingw64/bin/octave-gui.exe')

    A = np.array([[ 2, 0, 1],
                  [-1, 1, 0],
                  [-1, 1, 0],
                  [-3, 3, 0]])

    # Start Testing
    m, n = octave.run(nargout=2, target='size', args=(A,))
    print(m, n)

    N = octave.run(nargout=1, target='vecnorm', args=(A, 2, 2))
    print(N)

    # Inserting expressions directly
    X = octave.run(nargout=1, target='ones(4, 3) * 255;')
    print(X)
