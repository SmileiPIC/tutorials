Parallel computing
=================================

As supercomputers (as well as local clusters or personal computers)
become larger, we can explore new domains of plasma physics
with expensive, 3D, high-resolution models.

However, optimizing parallel algorithms on these new machines
becomes increasingly difficult, because hardware architectures
become increasingly complex as their computational power grows:

* supercomputers are composed of *nodes* which communicate through a dedicated network : see *distributed memory* parallelism below
* nodes are composed of many *computing units* (for instance, *cores*) which must be synchronized : see *shared memory* parallelism below
* cores access more and more advanced instructions sets, such as *SIMD* (Single Instruction Multiple Data) instructions

In Smilei, these three points are respectivly adressed with
MPI, OpenMP and vectorization using ``#pragma omp simd`` on Intel architecture.

Being efficient at each level of parallelism requires to understand constraints on 
the memory intimately related to them. This tutorial focuses on distributed and
shared memory paradigms in Smilei.

.. rubric:: Distributed memory
            
To enable parallel simulations over several nodes which all have their own memory, we first have to perform a domain decomposition:
the simulation's data (particles and fields) is decomposed into small pieces, called `Patch`, and evenly distributed between the memories.

Then, an **MPI process** is associated to each `Patch`. 
A single process is usually associated to several `Patch`.
Each process is also associated to computational ressources, a fraction of the supercomputer, which may have several processing units (cores) but has a single memory.
The **MPI process** executes all the computation necessary to handle the patches he has been given using the ressources he has access to.

In order to combat computational load imbalance, inherent to many particle-in-cell simulations,
the domain decomposition in :program:`Smilei` creates many more `Patch` than processes.
The main idea is to provide a variable number of `Patch` to each MPI process in order to balance the computational
load carried by each process (details about `parallelism <https://smileipic.github.io/Smilei/parallelization.html#decomposition-of-the-box>`_).

.. rubric:: Shared memory

This specific domain decomposition is also well adapted to the application of **OpenMP threads** parallelism over this collection of `Patch` per process.
Indeed, the MPI process is able to spawn as many **openMP threads** as he has cores.
These threads will be affected to successive `Patch` and will be able to efficiently deal with them in parallel.
This is an effective way to balance the load since as soon as a thread is done with a given `Patch`, it can start executing the next one withtout having to
synchronize with another thread that could have been slower and would have induced idle time.
This method also guarantees that threads are always treating different `Patch` and thus avoid fine grain memory concurrency between them during the current deposition.

.. rubric:: Summary
The domain should be divided into many `Patch` for each MPI process for two reasons :

* to distribute the computational load and feed all threads associated to each process
* to be able to manage the load imbalance
  
An attention must be paid to the limit of this approach.
An excessively refined decomposition with too many and too small patches is going to produce a large overhead due to synchronization (MPI and OpenMP).

The goal of this tutorial is to understand how to setup a simulation to get good performances,
the following features will be addressed :

* Decomposition of the simulation box into patches
* Choice of the number of MPI *processes* and OpenMP *threads*
* Smilei's *load balancing* feature
* Performance analysis with the ``DiagPerformances``

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

We introduce this tutorial talking about supercomputers but we will run here single node simulations.
It could seems out of context but the idea is to illustrate how works the code parallelism and its limits.

----


Splitting the box
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a first test, we will use a single core to focus on the box splitting :

.. code-block:: bash

  export OMP_NUM_THREADS=1
  mpirun -np 1 smilei beam_2d.py

The input file suggests to use 32x32 patches :

.. code-block:: python

  Main(
       number_of_patches = [ 32, 32 ],
  )

Run the simulation for various number of patches,
and compare the computation time :

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

.. rubric:: Details about timers
   
The ``Sync`` timers concern exchange between patches owned by **a single MPI processes and/or by many**.
In this case, these timers could contain waiting times due to load imbalance inherent to PIC simulations.

Whatever the case, ``Particles`` and  ``Maxwell`` do not contain MPI waiting time,
they only accumulate pure computation time.

``Load balancing``, ``Mov window`` or ``Diagnostics`` (which can be seen like a disk synchronization)
are global operations which require communications, they can contain waiting time.

For many MPI processes simulation, these times are averaged on all processes. 
Some detailed timing elements, such as minimum or maximum times on all processes
are provided in the file ``profil.txt`` and a full report can be obtained using the ``DiagPerformances``.


----

Introduce Smilei’s parallelism
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

A ball of plasma (30 cells radius) is moving through the box (256x256 cells) :

* With 8 x 8 patches, the size of a patch is 32 x 32 cells.
  The plasma, which represents the main time cost,
  occupies only a few patches of the simulation.
  This means many threads are doing nothing.
* With 16 x 16 patches, the size of a patch is 16 x 16 cells,
  an order of magnitude is earned regarding the number of patches loaded with particles.
  Verify the speedup.
* With 32 x 32 patches, the size of a patch is 8 x 8 cells,
  even more patches are loaded with particles, but with a synchronization overhead.
  
Check the behavior of these three configurations running 16 threads.

For this test, in the best case configuration,
an additionnal speed-up of 2 is obtained.
This is modest, but accelerating computations requires to split the particle load.
With a such local plasma, it is hard to achieve.

----

Imbalance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You applied some load balancing using OpenMP threading.
Indeed, the threads will keep working patch after patch in parallel on all the available patches
until all patches are done.
This is called *dynamic scheduling*.

The *static scheduling*, instead, assigns an exclusive pool of patches
to each thread. In this situation, threads will only work on their own pool,
even if it is an empty region. This obviously prevents load balancing between threads.
It is used on grids computing function of Smilei which is naturraly balanced.

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

Imbalance and distributed memory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the 16 x 16 patches simulation but with a MPI only configuration :

.. code-block:: bash

  source ${SMILEI_ROOT}/scripts/set_omp_env.sh 1
  mpirun -np 16 smilei beam_2d.py

This is technically similar to the ``static`` scheduling of the previous section :
the pool of patches is explicitly distributed over MPI processes starting the simulation.
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
compare it to the time saved regarding the simulation without dynamic load balancing.

.. warning::

  ``Sync`` timers are impacted by the imbalance of the
  algorithm part which precedes it :
  
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

To get familiar with Smilei's domain decomposition, distribued and shared memory parallelism,
we don't consider the NUMA (non uniform memory access) aspect of most of nodes which composed supercomputers.
Indeed, a node is generally composed of some processors which owns itself many cores. The cores of each node
has a privileged access to the memory associated to it processor.

As it has been described in the begining of this page supercomputers should be adressed with both paradigm :

* MPI to go through nodes **and** processors for many processors nodes to handle memory affinity.
* OpenMP to feed threads, minimize imbalance and to manage more efficiently diagnostics at large scale

The following example uses 2 MPI processes with 8 threads each :

.. code-block:: bash

  source ${SMILEI_ROOT}/scripts/set_omp_env.sh 8
  mpirun -np 2 smilei beam_2d.py


Between processes, threads, and the number of patches, there are many ways the
simulation performances can be modified. There is no general rule for finding
the optimal configuration, so we recommend trying several options.



