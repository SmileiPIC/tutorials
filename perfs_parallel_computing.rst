Parallel computing
=================================

On a personal computer, there may be several computing units (*cores*)
which all have access to the same memory (the RAM). This is called
*shared memory*.

On a supercomputer, there are too many cores to share all the memory.
Instead, cores are grouped into *nodes*: cores belonging to the same
node access the same memory ; cores belonging to different nodes
cannot use the same memory. This is called *distributed memory*.

To communicate information between distinct nodes,
they must exchange chunks of data through a network.
In Smilei, this communication is achieved using the
Message Passing Interface (MPI).

Within each node, the management of cores (sharing the same memory)
is usually handled by the OpenMP protocol. It is also possible to
fallback to MPI (in this case, the memory is artificially split).

The goal of this tutorial is to understand how to setup a simulation that
can ensure proper workload distribution between all the cores.
You will learn how to:

* Launch a simulation on several nodes 
* Choose the number of MPI *processes* and OpenMP *threads*
* Split the simulation in many *patches* to be distributed to the cores
* Use Smilei's *load balancing* feature
* Analyse these aspects with the ``DiagPerformances``

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

Download the input file `beam_2d.py <beam_2d.py>`_.
A small plasma ball is set with an initial velocity :math:`v_x=0.3`
and traverses the box.

----

Setup the tutorial
^^^^^^^^^^^^^^^^^^

As explained in the :ref:`setup page <runsimulation>`, you should make a new directory
to run your simulation. This directory should contain the input file that you just downloaded
and the executables ``smilei`` and ``smilei_test``.

----


The simulation box is split in *patches*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As explained above, the computer memory is not all located in one place,
but is split into nodes, or even artificially sub-split within each node.
We call a *process* the set of operations that uses one of these memory spaces.
As the communication of data between processes
is done with the *MPI* library, they are sometimes called *MPI processes*.

To specify the number of processes for a simulation, you must run Smilei
using the correct MPI command on your machine. Usually, this command is ``mpirun``.
For instance, the following command runs Smilei with 8 processes:

.. code-block:: bash

  mpirun -np 8 smilei beam_2d.py

In order to run the simulation on these 8 processes, we must also divide
the box in *patches* to distribute the data to them (at least 8 patches).
This is specified in the input file ``beam_2d.py``::

    number_of_patches = [ 32, 32 ],

This line defines a splitting of the box in 32x32 patches.
Each of these patches is a rectangular portion of the simulation box.

.. warning::

  Most PIC codes would split the box in 8 patches,
  so that there is 1 patch for each process.
  In Smilei, the box should be divided in **many** more patches, for two reasons:
  
  1. To distribute patches to all cores.
  2. To exchange patches between processes so that the computational load is balanced.
  
  These two points will be investigated in this tutorial.

----

One process may handle several cores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One MPI process must compute the many patches it owns.
Knowing that each MPI process is composed of several cores,
it must distribute patches to its cores so that they can work in parallel.

We call a *thread* the operations to be executed by each core.
The management of threads and their distribution to the cores is handled
by the OpenMP protocol.

.. note::

  It is possible to request less threads than cores,
  but this means some cores will do nothing.
  It is also possible to request more threads than cores,
  but this means some threads will keep waiting for the next available core.
  Overall, it is strongly recommended to have **as many threads as cores**.

To specify the number of threads per process, use the environment variable
``OMP_NUM_THREADS``. For instance, if your machine has 8 cores per MPI process,
we recommend the following command before running Smilei:

.. code-block:: bash

  export OMP_NUM_THREADS=8

----

Splitting the box
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a first test, we will use a single core in a single node
to focus on the box splitting:

.. code-block:: bash

  export OMP_NUM_THREADS=1
  mpirun -np 1 smilei beam_2d.py

The input file suggests to use 32x32 patches.
Run the simulation for various number of patches,
and compare the computation time:

* 32 x 32 patches
* 16 x 16 patches
* 8 x 8 patches
* a single patch

Computation times are provided at the end of the simulation:

* ``Time in time loop`` : the whole PIC loop
* ``Particles``         : all particles operations except collisions 
* ``Maxwell``           : Maxwell equations and the electromagnetic boundary conditions
* ``Diagnostics``       : all ``Diag`` blocks defined in the namelist
* ``Sync Particles``    : particle exchange between patches
* ``Sync Fields``       : ``E``, ``B`` exchange between patches
* ``Sync Densities``    : ``J`` exchange between patches

.. warning::

  The ``Sync``, ``Load balancing``, ``Mov window`` and ``Diagnostics`` timers
  may include *waiting* time. Indeed, processes must sometimes
  wait until others are ready to communicate.

These times are averaged on all processes. 
Some more detailed information is provided in the file ``profil.txt``,
and a full report can be obtained using the ``DiagPerformances``.


----

Using several threads in a single process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's make the first step to introduce parallel processing of all the patches.
We will use several OpenMP threads in a single MPI process.

Use the best patch configuration found in the previous step: 8x8 patches.
The single patch simulation is maybe slightly faster but it does not exhibit any parallelism.

Use the following commands to setup 1 process, and 16 threads per process.
You may need to adjust these settings according to your machine.

.. code-block:: bash

  source ${SMILEI_ROOT}/scripts/set_omp_env.sh 16
  mpirun -np 1 smilei beam_2d.py

Make sure that, in the output log, it specifies the correct number of
processes and threads. 
Even though 16 threads are used, the speed-up is very poor.

Let us now use ``happi`` to analyse the simulation.
Open an ``ipython`` prompt, then run::

  import happi
  S = happi.Open("/path/to/beam_2d/")

You can have a quick understanding of what happens in the simulation using::

  S.ParticleBinning(0).animate()

A ball of plasma (30 cells radius) is moving through the box (256x256 cells). 

* With 8 x 8 patches, the size of a patch is 32 x 32 cells.
  The plasma, which represents the main time cost,
  occupies only a few patches of the simulation.
  This means many threads are doing nothing.
* With 16 x 16 patches, the size of a patch is 16 x 16 cells,
  more patches are occupied. Verify the speedup.
* With 32 x 32 patches, the size of a patch is 8 x 8 cells,
  even more patches are occupied, but there is also a communication overhead.
  Check whether this was useful.

For this test, in the best case configuration,
an additionnal speed-up of 2 is obtained.
This is modest, but accelerating computations requires to split the particle load.
With a such local plasma, it is hard to achieve.

----

Thread scheduling 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Without knowing it, you applied some load balancing using OpenMP threading.
Indeed, the threads will keep working in parallel on all the available patches
until all patches are done.
This is called *dynamic scheduling*.

The default *static scheduling*, instead, assigns an exclusive pool of patches
to each thread. In this situation, threads will only work on their own pool,
even if it is an empty region. This obviously prevents load balancing between threads.

To choose the type of OpenMP scheduling, you can use the environment
variable ``OMP_SCHEDULE``, which was set to ``dynamic`` in the script
``set_omp_env.sh``.
You can observe the difference with the ``static`` scheduling:

.. code-block:: bash

  export OMP_NUM_THREADS=16
  export OMP_SCHEDULE=static
  mpirun -np 1 smilei beam_2d.py

OpenMP offers intermediary solutions but regarding the granularity of
the level of parallelism, we advice the ``dynamic`` scheduling.

----

Using several processes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the 16 x 16 patches simulation with several processes,
but only 1 thread per process:

.. code-block:: bash

  source ${SMILEI_ROOT}/scripts/set_omp_env.sh 1
  mpirun -np 16 smilei beam_2d.py

This is technically similar to the ``static`` scheduling of the previous section:
processes are assigned, in advance, to a pool of patches.
Compare the time spent in the PIC loop to that previous case.

.. warning::

   You also may have noticed major differences in sub timers.
   As these timers are managed per MPI process,
   they include waiting times due to thread imbalance.
   Specifically, they are caused by implicit OpenMP barriers
   in ``#pragma omp for`` loops.

We are now going to use the ``Performances`` diagnostic.
The list of available quantities can be obtained with::

  S.Performances()

Let us try::

  S.Perfomances(map="hindex").plot()

You should obtain a map of the simulation box with one distinct color for
each memory region (i.e. each MPI process). There are 16 regions, as we requested
initially. You can see that these regions do not have necessarily the same shape.

Now plot the number of particles in each region::

  S.Performances(map="number_of_particles").animate(cmap="smilei_r", vmin=0)

Clearly, at every given time, no more than only few regions contain particles.
This is a typical situation where almost all processes have nothing to do
and wait for a single process to finish its computation.


----

Balancing the load between processes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Smilei has an automated load-balancing feature that can move patches from one
process to another in order to ensure they all have a similar load. Activate it
in the input file using::

    LoadBalancing(
        every = 20
    )

Then run the simulation again with 16 processes and
have a look at the ``Load balancing`` timer. 
Observe differences in the computation time,
compared to the case without dynamic load balancing.

.. warning::

  ``Sync`` timers are impacted by the imbalance of the
  algorithm part which precedes it:
  
  * ``Particles``
  * ``Sync Densities``
  * ``Maxwell``
  * ``Sync Particles``
  * ``Sync Fields``


Use again the performances diagnostic to monitor the evolution of the
regions and their computational load.


----

Realistic configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With supercomputers, both MPI parallelization and OpenMP parallelization
must be used:

* MPI to communicate between large regions of the box
  and exchange patches in order to achieve global load balancing.
* OpenMP to handle patches locally and dynamically.


The following example uses 2 MPI processes with 8 threads each.

.. code-block:: bash

  export OMP_NUM_THREADS=8
  mpirun -np 2 smilei beam_2d.py

Between processes, threads, and the number of patches, there are many ways the
simulation performances can be modified. There is no general rule for finding
the optimal configuration, so we recommend trying several options.

