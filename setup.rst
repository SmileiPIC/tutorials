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

The following ``git`` command downloads the code into the ``Smilei`` directory, located
in the current working directory.

.. code-block:: bash

   $ git clone --depth=1 https://github.com/SmileiPIC/Smilei.git
   $ cd Smilei

Now that you are in the main ``Smilei`` folder, you may compile the documentation using
the `sphinx` python package. If you do not have `sphinx` installed with your `python`
environment, `check this out <http://www.sphinx-doc.org/en/stable/install.html>`_.
   
.. code-block:: bash

   $ make doc
   $ firefox build/html/index.html &

Change ``firefox`` to your favorite web browser.


----

Prepare the environment
^^^^^^^^^^^^^^^^^^^^^^^

The environment should be ready to accomodate for Smilei's installation. The dependencies
that are required for Smilei are listed in
`this page <http://www.maisondelasimulation.fr/smilei/installation.html>`_.

In short, you need a `C++11` compiler, a compatible `MPI` library, a compatible `HDF5`
library, and `python 2.7+`. We do not provide a full explanation on how to install these
on all systems, but the link above gives a few examples. 

We recommend that your `C++` compiler supports `OpenMP`, which allows for several threads
to operate in each process. This makes simulations potentially much faster.
Note that this requires the ``MPI_THREAD_MULTIPLE`` option
when the MPI library is compiled. In order to setup the `OpenMP` environment, we
recommend the following commands, that you may include in your ``.bash_profile`` or
``.bashrc`` configuration files (or the relevant one on your system).

.. code-block:: bash

   export OMP_NUM_THREADS=8
   export OMP_SCHEDULE=dynamic
   export OMP_PROC_BIND=true

The number ``8`` above indicates the number of threads per process. For most systems, 
the ideal number is equal to the number of cores contained in one `node` or `socket`.
For example, if your machine has 12 cores that share the same memory, we recommend using
``OMP_NUM_THREADS=12``.

----

Compile Smilei
^^^^^^^^^^^^^^

Once all dependencies are installed, go to the ``Smilei`` directory. You should be able
to run the following command to compile `Smilei`.

.. code-block:: bash
   
   $ make -j 8

The option ``-j 8`` simply indicates that the compilation with use 8 threads (faster).
When the compilation has succeeded, two executables are created: ``smilei``
and ``smilei_test``.

.. _runsimulation:

----

How to run a simulation
^^^^^^^^^^^^^^^^^^^^^^^

When running `Smilei` on your own computer, you may use the following commands:

.. code-block:: bash

  # Make a new folder and go inside
  mkdir mysimulation
  cd mysimulation
  # Copy necessary executables to the new folder
  cp /path/to/Smilei/smilei .
  cp /path/to/Smilei/smilei_test .
  # Copy the input file as well
  cp /path/to/my_input.py .
  # Run the simulation on 4 processes
  mpirun -n 4 smilei my_input.py

In this example, the simulation will use 4 processes, but remember that the option above
``OMP_NUM_THREADS=8`` will set 8 threads in each process, so a total of 24 threads.
As a consequence, this example is ideal for 4 nodes containing each 8 cores.

Most supercomputers provide two different options to run a simulation. Both are relevant
to this tutorial. You may choose either.

1. **Run in interactive mode:** you may request a few nodes of the machine for a given amount
   of time. You will have access interactively to the processes, so that the commands above
   can be directly written in the command line to run the simulation. Instead of copying
   the commands each time, **you may use the script** ``smilei.sh``
   **already available in** ``/path/to/Smilei/``.
   See `help here <http://www.maisondelasimulation.fr/smilei/run.html#using-the-provided-script>`_.
    
2. **Prepare a submission file** to submit a "job". You machine administrator should provide
   you with a typical job submission file. It defines the number of nodes and cores that
   you want to reserve. The command lines above have to be included in this file.


----

Tips
^^^^

* Launch a parallel interactive session:
  
  One hour with 2 nodes, 8 processors per node, on the ``default`` queue:

  * with the *torque* scheduler: 
  
    .. code-block:: bash
      
      qsub -I -l walltime=01:00:00,nodes=2:ppn=8 -q default
  
  * with the *slurm* scheduler:
    
    .. code-block:: bash
      
      srun -p default -I -N 2 -c 8 --pty -t 0-01:00 
   
    ``llinteractive 2 clallmds+ 3``

* Download a file from this webpage to your machine

  .. code-block:: bash
    
    curl -O http://URL/for/the/file
  
  
  
