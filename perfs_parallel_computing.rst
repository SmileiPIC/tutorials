Parallel computing
=================================

On a personal computer, there may be one or several computing units (*cores*).
They all share the same memory (the RAM). However, on a supercomputer,
the memory is not shared between all the cores: the memory is split in several
*nodes*.
Each node contains several cores, which can all access the same
data simultaneously. The cores belonging to two different nodes
cannot use the same memory directly; they must exchange chunks
of data that are communicated through a network.

In Smilei, this communication between nodes is achieved using the
Message Passing Interface (MPI). Within each node, the management 
of cores (sharing the same memory) can be handled by the OpenMP protocol or using MPI.

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

The computer memory is not all located in one place, but is split among
in many nodes. We call a *process* the set of operations that occur within
the piece of the simulation data associated to
one given memory space. As the communication of data between processes
is done with the *MPI* library, they are sometimes called *MPI processes*.
Note that it is possible to assign several processes to one
node. In this case, the memory of each process is managed independetly
even if it's located on the same place.

To specify the number of processes for a simulation, you must use the
correct MPI command on your machine. Usually, this command is ``mpirun``.
For instance, the following command runs Smilei with 8 processes:

.. code-block:: bash

  mpirun -np 8 smilei beam_2d.py

As the computer memory is split among many nodes, we must also divide
the box in *patches* to distribute the data. See, for instance,
in the input file ``beam_2d.py``, the line::

    number_of_patches = [ 32, 32 ],

It defines a splitting of the box in 32x32 patches.
Each of these patches is a rectangular portion of the simulation box.

.. _`warning about  patches for thread`:

.. warning::

  In Smilei there is not 1 large domain for 1 MPI process.
  The domain should be divided in **many** patches for each MPI process for two reasons :
  1) to distribute the compute load to feed all threads associated to each process, 2) to 
  be able to manage the load imbalance.

  Note that too many patches will cost a time overhead, the size of the patch must be think
  regarding the occupency and the evolution of the plasma in the box.

----

One process may handle several cores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One MPI process must compute the many patches it owns. 
In case of a multi-cores architecture coupled to the shared memory paradigm,
processes can access to several *cores* to do that.

In the most common model, for each core,
a *thread* is associated to compute patches *in parallel* until all patches are done.
These threads are managed with *OpenMP* to synchronize their advance.
Very importantly, there should be **as many threads as cores**. If you specify
less, then some cores will have no threads to run. If you specify more, then
some threads will keep waiting for the next available core.

To specify the number of threads per process, use the environment variable
``OMP_NUM_THREADS``. For instance, for 8 threads per process, you may run
the following command before running Smilei:

.. code-block:: bash

  export OMP_NUM_THREADS=8

----

First approach of number_of_patches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a first test, we will use a single core to be focus on the patch division :

.. code-block:: bash

  export OMP_NUM_THREADS=1
  mpirun -np 1 smilei beam_2d.py

The provided input file suggest to use 32 x 32 patches.
Compare the simulation times of this simulation to the same run with :
 * a single patch
 * 16 x 16 patches
 * and 8 x 8 patches

.. code-block:: python

  Main(
       number_of_patches = [ 1, 1 ],
  )

Look at times provided at the end of the simulation :
 * ``Time in time loop`` : the whole PIC loop
 * ``Particles``         : all particles operations except collisions 
 * ``Maxwell``           : Maxwell equations and the electromagnetic boundary conditions
 * ``Diagnostics``       : all ``Diag`` blocks defined in the namelist
 * ``Sync Particles``    : particles exchange between patches
 * ``Sync Fields``       : ``E``, ``B`` exchange between patches
 * ``Sync Densities``    : ``J`` exchange between patches

**The** ``Sync`` **timers concern exchange between patches owned by a single MPI processes or by many.**
In this  case, these timers could contain waiting times due to load imbalance inherent to PIC simulations.

Whatever the case, ``Particles`` and  ``Maxwell`` do not contain MPI waiting time,
they only accumulate pure computation time.

``Load balancing``, ``Mov window`` or ``Diagnostics`` (which can be seen like a disk synchronization)
are global operations which require communications, they can contain waiting time.

For many MPI processes simulation, these times are averaged on all processes. 
Some detailed timing elements, such as minimum or maximum times on all processes
are provided in a file ``profil.txt`` or in ``DiagPerformances``.
It is usefull to note the imbalance cost.


----

Introduce Smilei's parallelism
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this step, parallelism is introduced naively to handle ``number_of_patches`` with parallelism.
To do so, we'll first use only OpenMP threads on a single node on our local supercomputer with a single MPI processes.

         
Of course, we run it on the best patches configuration defined in the previous step : 8 x 8 patches.
The single patch simulation is maybe slightly faster but it does not exhibit any parallelism (see `warning about patches for thread`_).

.. code-block:: bash

  source ${SMILEI_ROOT}/scripts/set_omp_env.sh 16
  mpirun -np 1 smilei beam_2d.py

Make sure that, in the output log, it specifies the correct number of
processes and threads. 
Even though 16 compute resources are used, the speed-up is very poor.

Let us now use ``happi`` to analyse the simulation.
Open an ``ipython`` prompt, then run::

  import happi
  S = happi.Open("/path/to/beam_2d/")

You can have a quick understanding of what happens in the simulation using::

  S.ParticleBinning(0).animate()

A ball of plasma is moving through the box. 
The box size is described with a 256 x 256 cells grid
and the plasma ball is a 30 cells radius circle.
 * With the 8 x 8 patches configuration, the size of a patch is 32 x 32.
   The plasma, which represents the main time cost, concerns only few patches of the simulation, 16 threads are useless.
 * With the 16 x 16 patches configuration, the size of a patch is 16 x 16,
   an order of magnitude is earned regarding the number of patches loaded with particles, almost 1 per thread. 
 * With the 32 x 32 patches configuration, the size of a patch is 8 x 8,
   there is more than 3 loaded patches per thread, but with a synchronization overhead.

For this test, in the best case configuration, an additionnal speed-up of 2 is earned.
This is modest, but accelerating computations needs particles. With a such local plasma, it's hard to achieve.

.. note::
    That we are investigating new technics based on tasking over species and  clusers of particles to exhibit more shared memory  parallelism.

----

Imbalance 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Without knowing it, you applied load balancing using OpenMP threading.
Indeed, to achieve good performances using the shared memory parallelism, we apply a ``dynamic`` OpenMP scheduling using the script ``set_omp_env.sh``.

You can observe the difference with the ``static`` scheduling :

.. code-block:: bash

  export OMP_NUM_THREADS=16
  export OMP_SCHEDULE=static
  mpirun -np 1 smilei beam_2d.py

With the ``dynamic`` scheduling, threads operate patches one by one in the patches pool while all patches are not treated.
It's interesting, because the cost of 2 patches regarding particles operation can vary a lot.

With the ``static`` scheduling, the pool is divided with the number of threads, then the first thread operate the first package and so on. 
If all loaded patches are in the same package, the parallelism is annihilated.

OpenMP offers intermediary solutions but regarding the granularity of the level of parallelism, we advice the ``dynamic`` scheduling.

----

Imbalance and distributed memory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the 16 x 16 patches simulation but with a MPI only configuration :

.. code-block:: bash

  source ${SMILEI_ROOT}/scripts/set_omp_env.sh 1
  mpirun -np 16 smilei beam_2d.py

You can observe that the time spent in the PIC loop is near to the 16 threads ``static`` scheduling time.

.. warning::

   You also may have noticed major differences in sub timers.
   This is explained by the Smilei's timers implementation which is managed per MPI process,
   so timers include OpenMP imbalance due to implicit OpenMP barrier of ``#pragma omp for``.

We are now going to use the ``Performances`` diagnostic.
The list of available quantities can be obtained with::

  S.Performances()

Let us try::

  S.Perfomances(map="hindex").plot()

You should obtain a map of the simulation box with one different color for
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

Then run the simulation again with 16 processes and have a look to the ``Load balancing`` timer. 
You can observe differences in the computation time and
compare it to the time saved regarding the simulation without dynamic load balancing.


.. warning::

  ``Sync`` timers are impacted by the imbalance of the algorithm part which precedes it :
  
   * ``Particles``
   * ``Sync Densities``
   * ``Maxwell``
   * ``Sync Particles``
   * ``Sync Fields``


Have look to the performance diagnostic and especially to the regions distribution.


----

Real life configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As it has been described in the begining of this page supercomputers should be adressed
with both paradigm.
 * MPI to go through nodes **and** processors for many socket nodes to handle memory affinity.
 * OpenMP to minimize imbalance and to manage more efficiently diagnostics at large scale

.. code-block:: bash

  export OMP_NUM_THREADS=8
  mpirun -np 2 smilei beam_2d.py

Between processes, threads, and the number of patches, there are many ways the
simulation performances can be modified. There is no general rule for finding
the optimal configuration, so many tests are recommended.

