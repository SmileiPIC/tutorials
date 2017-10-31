Tutorial
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


Prepare and open an input file in a new directory

.. code-block:: bash

   [poincare] $ cd ~
   [poincare] $ mkdir mysimulation
   [poincare] $ cd mysimulation
   [poincare] $ cp ????/????/LaserPropagation.py .
   [poincare] $ gedit LaserPropagation.py &


Try the test mode
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   [poincare] $ ~/Smilei/smilei_test LaserPropagation.py


Run a simulation
^^^^^^^^^^^^^^^^

Set minimal OpenMP runtime environment :

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
   
   [interactive] mpirun -np 4 -ppn 2 ~/Smilei/smilei LaserPropagation.py
   ...
   [interactive] ls


Prepare the post-processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open a new terminal window & login to poincare

.. code-block:: bash

    $ ssh poincare –X
    [poincare] $ 
    
Install the python module happi

.. code-block:: bash
   
   [poincare] $ cd Smilei
   [poincare] $ make happi
   [poincare] $ cd ..

Start ipython

.. code-block:: bash
    
    [poincare] $ ipython

Get basic info on the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Import the happi module:

.. code-block:: python

   In [1]: import happi
    
Open the simulation:

.. code-block:: python

   In [2]: S=happi.Open("mysimulation")
   
See what is available:

.. code-block:: python

   In [4]: S.namelist.<tab>

Obtain the laser profile
^^^^^^^^^^^^^^^^^^^^^^^^

Get the Laser block from the namelist:

.. code-block:: python
   
   In [5]: laser = S.namelist.Laser[0]
   
   In [6]: laser

See what is available from the Laser block:

.. code-block:: python

   In [7]: laser.<tab>
   
   In [8]: laser.time_envelope

Plot the laser profile
^^^^^^^^^^^^^^^^^^^^^^^

Obtain a list of times:

.. code-block:: python

   In [9]: import numpy as np, matplotlib.pyplot as plt
   In [10]: tstop = S.namelist.Main.simulation_time
   In [11]: tstep = S.namelist.Main.timestep
   In [12]: times = np.arange(0., tstop, tstep)

Plot the profile:

.. code-block:: python

   In [13]: laser_profile = [laser.time_envelope(t) for t in times]
   In [14]: plt.plot( times, laser_profile )

Check laser using Scalar
^^^^^^^^^^^^^^^^^^^^^^^^

Obtain a list of Scalar diagnostics:

.. code-block:: python

   In [15]: S.Scalar.<tab>

Open the Uelm scalar and plot:

.. code-block:: python

   In [16]: diag = S.Scalar.Uelm()
   In [17]: diag.plot()

Plot laser using Field
^^^^^^^^^^^^^^^^^^^^^^^^

Open the Ey field and plot:

.. code-block:: python

   In [18]: diag = S.Field.Field0("Ey")
   In [19]: diag.animate(vmin=-1, vmax=1, cmap="smileiD")

Open the field with an average, and compare to the previous profile:

.. code-block:: python

   In [20]: S.Field.Field0("(2.*(Ex**2+Ey**2))**(0.5)", average={"x":[0,5],"y":[100,110]}).plot()
   In [21]: plt.plot( times, laser_profile )


