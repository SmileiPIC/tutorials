Advanced Tutorial 3: Electron Laser Wakefield Acceleration (in 2D)
------------------------------------------------------------------------------

The goal of this tutorial is to give an introduction to Laser Wakefield acceleration simulation with :program:`Smilei`.
The following features will be addressed:

* The moving window in order to follow the laser propagation.
* Laser initialization "in the box" accelerated by numpy.
* Particle binning diagnostic.
* Variations on Silver-Muller transverse boundary conditions.
* Dynamic load balancing.

Disclaimer: This tutorial is done in 2D which is not physically relevent. Proper simulation of this kind must be done in 3D.
Even in 2D, this case is a bit heavy with respect to the other tutorial and can not be run on a labtop.
We suggest using around a hundred cores to run this tutorial in a reasonable time.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma.
It propagates in the plasma and creates a non linear plasma wave in its wake.

Step by step tutorial
^^^^^^^^^^^^^^^^^^^^^^^^

Download  `this input file <laser_wake.py>`_ and open it with your favorite editor. 

First, notice that the laser is initialized via the use of ``external fields`` blocks. 
Each field component must de defined by one external field.
Defining the external fields as ``numpy.array`` makes their initialization much faster.


Absorbing Siler-Muller boundary conditions are chosen in all directions.
By default, the optimal absorption angle is set to be normal to all faces.
In other words, the laser will be optimally absorbed on the +X face.

The box is initally empty of plasma.

Action: Try to run the simulation and observe laser absorption on the +X face with the Probe diagnostic. Notice that a small fraction of the laser
is reflected back into the simulation domain. This is a numerical artefact induced by non perfect absorbing bounday conditions even though we are
in the optimal conditions.
Hint: In order to see more details, you can manually setup the color scale extrema in ``Happi`` by using the ``vmin`` and ``vmax`` optional arguments.

We are interested in looking at the laser propagation.
Notice the ``MovingWindow`` block.
This allows the simulation domain to constantly shifts toward the `x` direction in order to follow the laser propagation.

Action: Give a proper velocity and start time to the moving window in order to follow the laser pulse and observe it enter the plasma.
Hint: Remember that a variable can be given as a function of variables from other blocks. For instance, the grid length along x can be called as
``Main.grid_length[0]``.

There are strong reflections of the laser field on the transverse boundary. One can tune the Silver-Muller boundary conditions in order to fix this problem.

Action: Change the Silver-Muller absorption angle in order to smoothly handle the laser at the transverse boundary.
Refers to the documentation in order to fix a proper absorbing vector. 
Hint: The absorbing vector :math:`k_{abs}` must be as much aligned as possible with the wave vector of the pulse you need to absorb but
it must keep a non zero normal component.

Action: Increase simulation time up to 10 tens the box length in order to have electrons injected in the wakefield.

Action: Use the performance diag to observe imbalance.

Action: Use the dynamic load balancing to improve the code performances.

Action: Visualize the particle binning diagnostic and evaluate the accelerated beam energy.


