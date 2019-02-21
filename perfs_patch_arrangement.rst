Patch arrangement
=================================

For some case such as very local plasmas, the dynamic load balancing could reach limits :
 * it needs computational load to balance
 * it fits dynamic problems

For weak particles dynamic it could be preferable to masterize the patch distribution over MPI.
Using the `Hilbert curve <https://smileipic.github.io/Smilei/parallelization.html#load-balancing-between-mpi-regionsrunsimulation>`_
could not be intuitive, a linearized per direction distribution is proposed.

----

Configuration
^^^^^^^^^^^^^^^^^^^^^^

Starting case :  
  `radiation_pressure_acc_hilbert.py <radiation_pressure_acc_hilbert.py>`_

.. Linearized case :  
..  `radiation_pressure_acc_linearized.py <radiation_pressure_acc_linearized.py>`_

To highlight the phenomenon and to simplify the environment we propose to run MPI only simulations here.

----

Using appropriate patches arrangement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run in the default configuration :

.. code-block:: bash

  export OMP_NUM_THREADS=1  
  mpirun -np 16 smilei radiation_pressure_acc_hilbert.py

Observe timers and probes diagnostics.

.. note::
   Probes diagnostics are defined here, not fields diagnostics which do not works with some alternative ``patch_arrangement``.

Activate the dynamical load balancing to absorb synchronizations overhead

.. code-block:: python

  LoadBalancing(
      every = 20
  )

A look at the plasma shape shows that at the simulation initialization,
the plasma is located in an one patch large strip in the Y axis. Then it is propagating along the X axis. 
We propose here to enforce the distribution of patches over MPI along the Y axis to really provide computational load 
to many MPI process.

.. code-block:: python

  Main(
      patch_arrangement = "linearized_YX",
  )

Note that managing this along the X axis should be horrible in terms of CPU hours wasted !
Do not run the full simulation in this configuration.
  
.. code-block:: python

  Main(
      patch_arrangement = "linearized_XY",
  )

.. figure:: _extra/arrangement.png

  Each numbered square represents a patch in an 8 x 8 patches configuration distributed over 16 MPI processes.
  In this test case, the plasma is located in the 2nd column of the box. It explains why MPI domain are so small
  in this region.


----


Tuning the patch arrangement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Up to here, the 8 x 8 number of patches used limits the splitting in Y. Only 8 compute units are working.
Unfortunatly the patch size, 75 x 125 cells, do not permit to split more in Y.

We propose here to slightly increase the spatial resolution in Y, to get a number of cells in Y divisible per 16. 

.. code-block:: python

  current_ncells_Y = Lsim[1] / (l0/resx)
  target_ncells_Y = 1024.
  target_cell_length_Y = (l0/resx*current_ncells_Y)/target_ncells_Y

  Main(
      cell_length = [l0/resx,target_cell_length_Y],
  )

Re-run the ``linearized_YX`` configuration to note the related overhead of the new resolution.
Increasing the spatial resolution increase the particles resolution, you can have a look at the number of particles created.

You can now run the simulation with the 8 x 16 patches configuration :

.. code-block:: python

  Main(
      number_of_patches = [ 8, 16 ],
  )

To be fair, we can re-run this configuration with the ``hilbertian`` mode (it's the default value of ``patch_arrangement``)
with 8 x 16 patches. Indeed, in this mode, when the number of patches is not the same along all directions,
the square pattern is reproduced many times in the larger direction (Y here). This will benefits here. 

.. note::
   The paramater ``number_of_patches`` is no more forced to be a power of 2 with ``linearized`` configuration.
   We use here 16 patches in Y because, we run 16 MPI processes on a node of 16 cores.
   
