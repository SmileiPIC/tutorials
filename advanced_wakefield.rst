2D laser wakefield acceleration
-------------------------------------

The goal of this tutorial is to give an introduction to Laser Wakefield acceleration simulation with :program:`Smilei`.
The following features will be addressed:

* The moving window in order to follow the laser propagation.
* Variations on Silver-Muller transverse boundary conditions.
* Particle Binning diagnostic.
* Dynamic load balancing.

The simulation used for this tutorial is relatively heavy so make sure to submit the job on 160 cores at least.

Disclaimer: This tutorial is done in 2D which is not physically relevant. Proper simulation of this kind must be done in 3D 
or in cylindrical geometry with azimuthal mode decomposition (see the related tutorial).
Even in 2D, this case is a bit heavy with respect to the other tutorial and can not be run on a laptop.
We suggest using around a hundred cores to run this tutorial in a reasonable time.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma.
It propagates in the plasma and creates a non linear plasma wave in its wake.
Electrons from the plasma are eventually trapped in this wave and accelerated to high energies.

Step by step tutorial
^^^^^^^^^^^^^^^^^^^^^^^^

Download  `this input file <laser_wake.py>`_ and open it with your favorite editor. 
Keep open a page with the `documentation for the namelist <https://smileipic.github.io/Smilei/namelist.html>`_ to follow the tutorial's steps. 

.. rubric:: 1. Transverse reflections

Absorbing Silver-Muller boundary conditions are chosen for all faces.
By default, the optimal absorption angle is set to be normal to all faces.
In other words, the laser will be optimally absorbed on the +X face.

The box is initially empty of plasma.

To visualize e.g. the density ``-Rho`` and the laser ``Ey``, try::

  S.Probe.Probe1("-Rho").slide()
  S.Probe.Probe1("Ey").slide(figure=2)

**Action**: Try to run the simulation and observe laser absorption on the Ymin and Ymax faces with the Probe diagnostic. Notice that a fraction of the laser
is reflected back into the simulation domain. This is a numerical artefact induced by non perfect absorbing boundary conditions. 

**Hint**: In order to see more details, you can manually setup the color scale extrema in ``happi`` by using the ``vmin`` and ``vmax`` optional arguments.

.. rubric:: 2. Optimize absorbing boundary conditions

In order to reduce these reflexions, one can tune the Silver-Muller boundary conditions.

**Action**: Change the Silver-Muller absorption angle in order to smoothly handle the laser at the transverse boundary.
Refers to the documentation in order to fix a proper absorbing vector. 

**Hint**: The absorbing vector :math:`k_{abs}` must be as much aligned as possible with the wave vector of the pulse you need to absorb but
it must keep a non zero normal component.

.. rubric:: 3. Moving Window

Now that the laser propagates without interfering with the simulation too much, we are interested in looking at the laser propagation over several box lengths.
Notice the ``MovingWindow`` block in the `documentation for the namelist <https://smileipic.github.io/Smilei/namelist.html>`_.
This allows the simulation domain to constantly shifts toward the `x` direction in order to follow the laser propagation.

**Action**: Give a proper velocity and start time to the moving window in order to follow the laser pulse and observe it enter the plasma.
Remember that the window speed is normalized by `c` as usual. 
Increase the number of iterations from `3000` to `38000`.
This is a rather long simulation so make sure to use at least 160 cores.

**Hint**: Remember that a variable can be given as a function of variables from other blocks. For instance, the grid length along x can be called as
``Main.grid_length[0]``.

.. rubric:: 4. Particle binning

Some electrons have been trapped and accelerated in the wakefield of the laser. 
We can use the ``ParticleBinning`` diagnostic in order to visualize them in phase space::

  S.ParticleBinning(0).slide()

**Action**: Visualize the particle binning diagnostic and evaluate the accelerated beam energy.

**Hint**: In order to see more details, also here you can manually setup the color scale extrema in ``happi`` by using the ``vmin`` and ``vmax`` optional arguments.

**Hint**: Check the documentation in order to know the default normalization for energy.

.. rubric:: 5. Performances diagnostic

Do you feel like the load is correctly balanced? Check it via the ``Performance`` diagnostic!

**Action**: Use the ``Performance`` diagnostic to observe load imbalance.

**Hint**: Pick a specific quantity like "timer_particles" in order to highlight the imbalance. The :program:`timer_total` quantity is not relevant since it adds up all imbalances which compensate each other.

.. rubric:: 6. Optimize simulation

**Action**: Use the dynamic load balancing to improve the code performances, using the ``LoadBalancing`` block described in the namelist documentation.
Make sure to run this new simulation in a different directory in order to compare your performance diagnostics. Check that imbalance is reduced.

**Hint**: Does the gain in performance compensate the cost of the dynamic load balancing ? If not, you probably set a too frequent load balance.
Comments: In that case load imbalance mostly builds up only at the end of the simulation. This is why performance gain is not spectacular.



