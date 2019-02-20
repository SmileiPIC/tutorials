Patch arrangement
=================================

For some case such as very local plasmas, the dynamic load balancing could reach limits :
 * it needs computational load to balance
 * it fits dynamic problems

For weak particles dynamic it could be preferable to masterize the patch distribution over MPI.
Using the `Hilbert curve <https://smileipic.github.io/Smilei/parallelization.html#load-balancing-between-mpi-regionsrunsimulation>`_
could not be intuitive, a linearized per direcction distribution is proposed.

----

Configuration
^^^^^^^^^^^^^^^^^^^^^^

Starting case :  
  `radiation_pressure_acc_hilbert.py <radiation_pressure_acc_hilbert.py>`_

Linearized case :  
  `radiation_pressure_acc_linearized.py <radiation_pressure_acc_linearized.py>`_

To highlight the phenomenon and to simplify the environment we propose to run MPI only simulations here.

----

Using appropriate patches arrangement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run in the default configuration :

.. code-block:: bash

  export OMP_NUM_THREADS=1  
  mpirun -np 16 smilei radiation_pressure_acc_hilbert.py

Observe timers and probes diagnostics.

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


----


Tuning the patch arrangement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Looking at the plasma shape → More patch along Y ?

Adjusted number of cells among Y : 1000 to 1024 (easier to divide on 16 cores)

Continue to run with the 8 x 8 patches configuration

Continue to run with the 8 x 16 patches configuration

Back on hilbert arrangement with 8 x 16 patches (36% time saved regarding DLB)
