Parallel computing
=================================

On a personal computer, there may be one or several computing units (*cores*).
They all share the same memory (the RAM). However, on a supercomputer,
the memory is not shared between all the cores: the memory is split in several
*nodes*.
Each node contains several cores, which can all access the same
data simultaneously. The cores belonging to two different nodes
cannot use the same data directly; they must exchange chunks
of data that are communicated through a network.

In Smilei, this communication between nodes is achieved using the
Message Passing Interface (MPI). Within each node, the management 
of cores (sharing the same memory) is handled by the OpenMP protocol.

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
one given memory space. As the communication of data between processes
is done with the *MPI* library, they are sometimes called *MPI processes*.
Note that it is possible to assign several processes to one
node. In this case, the memory of this node is sub-divided.

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
Each of these patches is a rectangular portion of the plasma.

.. warning::

  In many PIC codes, there is 1 patch for 1 MPI process. This is different in
  Smilei where there should be **many** patches for each MPI process, typically 16
  to thousands.

----

One process may handle several cores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One MPI process must compute the many patches it owns. 
Fortunately, it has access to several *cores* to do that.
Cores compute patches *in parallel* until all patches are done.

The operations that are run sequentially, in a single core, are called a *thread*.
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

Run the simulation with 12 processes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a first test, we will use 12 processes, and 1 core per process:

.. code-block:: bash

  export OMP_NUM_THREADS=1
  mpirun -np 12 smilei beam_2d.py

Make sure that, in the output log, it specifies the correct number of
processes and threads.

Let us now use ``happi`` to analyse the simulation.
Open an ``ipython`` prompt, then run::

  import happi
  S = happi.Open("/path/to/beam_2d/")

You can have a quick understanding of what happens in the simulation using::

  S.ParticleBinning(0).animate()

A ball of plasma is moving through the box.

We are now going to use the ``Performances`` diagnostic.
The list of available quantities can be obtained with::

  S.Performances()

Let us try::

  S.Perfomances(map="hindex").plot()

You should obtain a map of the simulation box with one different color for
each memory region (i.e. each MPI process). There are 12 regions, as we requested
initially. You can see that these regions do not have necessarily the same shape.

Now plot the number of particles in each region::

  S.Performances(map="number_of_particles").animate(cmap="smilei_r", vmin=0)

Clearly, at every given time, only one region contains all the particles.
This is a typical situation where almost all processes have nothing to do
and wait for a single process to finish its computation.


----

Balancing the load between processes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Smilei has an automated load-balancing feature that can move patches from one
process to another in order to ensure they all have a similar load. Activate it
in the input file using::

    LoadBalancing(
        every = 100
    )

Then run the simulation again with 12 processes.

How are the regions modified? Can you observe differences in the computation time?


----

Balancing the load inside one process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, instead of splitting the simulation between 12 processes, let us
use only 1 process, but put as many threads as possible by your machine
in this process. We will suppose that the machine has 12 threads per process.
In this case, run the simulation with:

.. code-block:: bash

  export OMP_NUM_THREADS=12
  mpirun -np 1 smilei beam_2d.py

There is now, obvioulsy, only one region. How is the computation speed affected ?

Between processes, threads, and the number of patches, there are many ways the
simulation performances can be modified. There is no general rule for finding
the optimal configuration, so many tests are recommended.
