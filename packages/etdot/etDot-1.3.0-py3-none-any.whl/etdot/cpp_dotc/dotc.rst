This file documents a python module built from C++ code with pybind11.
You should document the Python interfaces, *NOT* the C++ interfaces.

Module etdot.dotc
*********************************************************************

Module :py:mod:`dotc` built from C++ code in :file:`cpp_dotc/dotc.cpp`.

.. function:: add(x,y,z)
   :module: etdot.dotc
   
   Compute the sum of *x* and *y* and store the result in *z* (overwrite).

   :param x: 1D Numpy array with ``dtype=numpy.float64`` (input)
   :param y: 1D Numpy array with ``dtype=numpy.float64`` (input)
   :param z: 1D Numpy array with ``dtype=numpy.float64`` (output)
   