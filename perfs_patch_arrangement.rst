Patch arrangement
=================================


Single node / Poincare (16 cores, 2 x 8 cores)
Test case : tst2d_02_radiation_pressure_acc.py

Run in MPI only to enforce the phenomenon at that scale

.. code-block:: python

  + particles_per_cell = 16,
  - Fields - Screen - Track
  + Probes (to validate linearized_YX) :
  DiagProbe(
      number = [600, 1000],
      origin = [0.*l0, 0.*l0],
      corners = [
      [6.*l0, 0.*l0],
      [0.*l0, 10.*l0]
      ],
  )

----

Using appropriate patches arrangement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run in the default configuration

Add the dynamic load balancing  (every = 20)  

Test the linearized_YX (16% time saved regarding DLB)  

Test the linearized_XY  


----


Tuning the patch arrangement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Looking at the plasma shape → More patch along Y ?

Adjusted number of cells among Y : 1000 to 1024 (easier to divide on 16 cores)

Continue to run with the 8 x 8 patches configuration

Continue to run with the 8 x 16 patches configuration

Back on hilbert arrangement with 8 x 16 patches (36% time saved regarding DLB)
