Setup 
--------

Obtain Smilei
^^^^^^^^^^^^^

.. code-block:: bash

   $ git clone --depth=1 git@github.com:SmileiPIC/Smilei.git
   $ cd Smilei

Compile the documentation
   
.. code-block:: bash

   $ make doc
   $ firefox build/html/index.html &
                 


Prepare the environment on Poincare
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Upload Smilei on Poincare

.. code-block:: bash
   
   $ scp -r . poincare:~/
   $ ssh poincare –X
   [poincare] $ 

Description of Poincare
^^^^^^^^^^^^^^^^^^^^^^^

https://groupes.renater.fr/wiki/poincare/public/description_de_poincare

Node :

* Compute : 2 Xeon Sandy Bridge of 8 cores
* Memory : 32 Go

Software environment :

* compiler : Intel
* MPI : IntelMPI (``MPI_THREAD_MULTIPLE``)
* HDF5 : compiled using IntelMPI
* GNU : C++11 compatible
* Anaconda : rich Python distribution for post-processing 

Look at the environment

.. code-block:: bash
   
   [poincare] $ cat .bash_profile
   [poincare] $ module list


Compile Smilei
^^^^^^^^^^^^^^

.. code-block:: bash
   
   [poincare] $ cd Smilei
   [poincare] $ make –j 8


.. _interactivemode:

How to run a simulation
^^^^^^^^^^^^^^^^^^^^^^^

Set a minimal OpenMP runtime environment :

.. code-block:: bash

   [poincare] $ cat scripts/set_omp_env.sh
   #!/bin/bash

   export OMP_NUM_THREADS=$1
   export OMP_SCHEDULE=dynamic
   export OMP_PROC_BIND=true

   [poincare] $ . scripts/set_omp_env.sh 4

Start an interactive session for computation
   
.. code-block:: bash

   [poincare]  $ llinteractive 2 clallmds+ 3
   
   [interactive] mpirun -np 4 -ppn 2 ~/Smilei/smilei mysimulation.py
   ...
   [interactive] ls


