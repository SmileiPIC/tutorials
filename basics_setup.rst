Setup 
-----

In these tutorials, we assume you are running on a UNIX machine that has access to internet
and can run simulation jobs on several cores. Ideally, it would run on 16 to 32 cores.
If you are, instead, using a home computer or workstation, we recommend you scale the
simulations down in order to reduce their execution time.

We recommend getting some `basic understanding of parallel computing
<http://www.maisondelasimulation.fr/smilei/parallelization.html>`_ and some basic knowledge
on UNIX commands.

You should first open a `terminal` or a `console`, then ``cd`` to the directory of your
choice.

----

Obtain Smilei
^^^^^^^^^^^^^

Use ``git`` to download the code into a ``Smilei`` directory:

.. code-block:: bash

  git clone --depth=1 https://github.com/SmileiPIC/Smilei.git
  cd Smilei

----

Compile the documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

In the main ``Smilei`` folder, use the `sphinx` python package to compile
the documentation (`get sphinx here <http://www.sphinx-doc.org/en/stable/install.html>`_).

.. code-block:: bash

  make doc
  firefox build/html/index.html &

Replace ``firefox`` by your favorite web browser.


----

Prepare the environment
^^^^^^^^^^^^^^^^^^^^^^^

The environment should be ready to accomodate for Smilei's installation.
Check `this page <http://www.maisondelasimulation.fr/smilei/installation.html>`_
for details.

In short, you need:

* a `C++11` compiler
* a compatible `MPI` library (``MPI_THREAD_MULTIPLE`` support is strongly recommended)
* a compatible `HDF5` library
* `python 2.7+`

We recommend that your `C++` compiler supports `OpenMP` for efficient
multi-threading. For best performances, the following environment variables should
be set, for instance in your ``.bash_profile`` or
``.bashrc`` configuration files.

.. code-block:: bash

   export OMP_NUM_THREADS=8
   export OMP_SCHEDULE=dynamic
   export OMP_PROC_BIND=true

The number ``8`` indicates the number of threads per process. For most systems, 
the ideal number is equal to the number of cores contained in one `node` or `socket`.
For example, if your machine has 12 cores that share the same memory, use
``OMP_NUM_THREADS=12``.

----

Compile Smilei
^^^^^^^^^^^^^^

Once all dependencies are installed, go to the ``Smilei`` directory and compile:

.. code-block:: bash
   
  make -j 8

The option ``-j 8`` provides 8 threads for compilation (faster).
When the compilation has succeeded, two executables are created: ``smilei``
and ``smilei_test``.

.. _runsimulation:

----

Run a simulation on your machine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step for any simulation is to create a new directory to
contain all the simulation inputs and outputs. Otherwise, the many
generated files would pollute your current directory.

.. code-block:: bash

  # Make a new folder and go inside
  mkdir mysimulation
  cd mysimulation

  # Copy necessary executables to the new folder
  cp /path/to/Smilei/smilei .
  cp /path/to/Smilei/smilei_test .

  # Copy the input file as well
  cp /path/to/my_input.py .

When running `Smilei` on your own computer, the first possibility
is to run directly the code in the current terminal:

.. code-block:: bash

  ./smilei my_input.py

If you want to use several computing units, you can use the relevant
``MPI`` executable on your machine. For example, with ``mpirun``:

.. code-block:: bash

  # Run the simulation on 4 processes
  mpirun -n 4 smilei my_input.py

To facilitate this process, a script ``smilei.sh`` is already available.
See `help here <http://www.maisondelasimulation.fr/smilei/run.html#using-the-provided-script>`_.

In this example, the simulation will use 4 processes, but remember that the option above
``OMP_NUM_THREADS=8`` will set 8 threads in each process, so a total of 24 threads.
As a consequence, this example is ideal for 4 nodes containing each 8 cores.
This parallel computing is studied in :doc:`this tutorial<perfs_parallel_computing>`.


----

Run a simulation on a cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most supercomputers provide two different options to run a simulation. Both are relevant
to this tutorial. You may choose either.

1. **Run in interactive mode:** you may request a few nodes of the machine for a given amount
   of time. You will have access interactively to the processes, so that the commands above
   can be directly written in the command line to run the simulation.
    
2. **Prepare a submission file** to submit a "job". You machine administrator should provide
   you with a typical job submission file. It defines the number of nodes and cores that
   you want to reserve. The command lines above have to be included in this file.


----

Tips
^^^^

* Launch a parallel interactive session:
  
  One hour with 2 nodes, 8 processors per node, on the ``default`` queue:

  * | with the *torque* (PBS) scheduler:
    | ``qsub -I -l walltime=01:00:00,nodes=2:ppn=8 -q default``
  
  * | with the *slurm* scheduler:
    | ``srun -p default -I -N 2 -c 8 --pty -t 0-01:00``
      
  * with `intel's LoadLeveler <https://www.ibm.com/support/knowledgecenter/SSFJTW_5.1.0/com.ibm.cluster.loadl.v5r1.load500.doc/am2cr_llrun.htm>`_
  

* Download a file from this webpage to your machine

  .. code-block:: bash
    
    curl -O http://URL/of/the/file
  
  
  
