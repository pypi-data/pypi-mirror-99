This file documents a python module built from Fortran code with f2py.
You should document the Python interfaces, *NOT* the Fortran interfaces.

Module etdot.dotf
*********************************************************************

Module :py:mod:`dotf` built from fortran code in :file:`f90_dotf/dotf.f90`.

.. function:: add(x,y,z)
   :module: etdot.dotf

   Compute the sum of *x* and *y* and store the result in *z* (overwrite).

   :param x: 1D Numpy array with ``dtype=numpy.float64`` (input)
   :param y: 1D Numpy array with ``dtype=numpy.float64`` (input)
   :param z: 1D Numpy array with ``dtype=numpy.float64`` (output)
