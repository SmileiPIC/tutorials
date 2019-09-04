Azimuthal-mode-decomposition cylindrical geometry
------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the cylindrical geometry 
with azimuthal Fourier decomposition in :program:`Smilei`.
The following topics will be addressed:

* Understand the concept of azimuthal mode decomposition
* Set up a simulation in this geometry
* The analysis of the grid fields in AM cylindrical geometry

The simulation used for this tutorial is relatively heavy so make sure to submit the job on 160 cores at least.


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma. 
The laser is linearly polarized in the ``y`` direction.
It propagates in the plasma in the positive ``x`` direction and creates a non linear plasma wave in its wake.
The moving window in the namelist has been set to contain the laser and the first wake period in the simulation window.


.. note::

  You will see that the plasma does not fill all the simulation window. 
  This is because we want to include the laser electromagnetic field in the window, but the plasma particles creating the plasma oscillations
  are only those radially near to the laser pulse. Plasma particles at greater radial distances would not contribute to the relevant physics, but they would 
  require additional computational time. Thus we can omit them to perform the simulation more quickly without losing relevant phenomena.

----

Azimuthal-mode-decomposition
^^^^^^^^^^^^^^^^^^^^^^^^

In some physical situations like the one of this tutorial, the phenomena of interest have a cylindrical geometry or are very near to be cylindrically symmetric.

The electromagnetic fields can then be decomposed in Fourier azimuthal modes (where the azimuthal angle is defined with respect to the propagation axis of the laser). 
Each mode is defined on a 2D grid, where the two dimensions are the longitudinal and radial ones.

In this case, Maxwell's Equations can evolve independently the 2D azimuthal modes, and to save time we can retain only a certain number of azimuthal modes, 
without losing the relevant physics. In the case simulated in this tutorial, using only two azimuthal modes allows to catch the relevant physics.
The particles, on the other hand, move in the 3D space, pushed by the 3D fields reconstructed from the electromagnetic azimuthal modes. 
With this powerful technique, 3D features can be simulated at the cost of approximately N 2D simulations, where N is the number of modes we keep in the simulation.


Simulation setup
^^^^^^^^^^^^^^^^^^^^^^^^

An input file to simulate laser wake excitation in this geometry will be very similar to a namelist in 2D geometry, with some important differences.
Check them in the input file:

* The selected geometry is ``AMcylindrical``

* The grid resolution is given by a longitudinal and radial resolution, since the azimuthal modes are defined on a 2D grid 

* The number of azimuthal modes simulated is set in ``number_of_AM``. In this case only two of them are necessary to catch the relevant physics

* The laser can be defined through the ``LaserGaussianAM`` block

* When you define a plasma density profile, it will be defined with two coordinates ``(x,r)``

* Still in the plasma density profile definition, remember that ``r=0`` corresponds to the lower boundary of the grid, i.e. the laser propagation axis

* The ``Probes`` origin and corners are defined with three coordinates, since they will interpolate the fields in the 3D space as in a 3D simulation.

----


Step by step tutorial
^^^^^^^^^^^^^^^^^^^^^^^^

Download  `this input file <laser_wake_AM.py>`_ and open it with your favorite editor and run the simulation.
Then, open the results::

  import happi
  S = happi.Open("/path/to/the/simulation") 

.. rubric:: 1. Field diagnostic

Now let's have a look at the grid fields, for example the electron density::

  S.Field.Field0("-Rho",theta = 0.).plot(figure=1, vmin = 0., vmax = 0.01)

In the previous command we have specified a certain angle ``theta = 0`` (i.e. the demi-plane including the positive ``y`` coordinates).
With the ``Field`` diagnostic, you can virtually specify any angle ``theta``. 
This means that at the cost of approximately N 2D simulations (N is the number of azimuthal modes, two in this case), you can obtain the fields in all the 3D space, like in a 3D simulation.
Note that you will see only half of the plane, as the ``Field`` diagnostics shows the fields on the grid, which is defined on a half-plane.

By default, the last command we used will plot the last timestep available. You can also plot a specific timestep::
  
  S.Field.Field0("-Rho",timesteps=6000.,theta=0.).plot(figure=1, vmin = 0., vmax = 0.01)

In the last command no azimuthal mode was specified. By default, if no mode is specified the reconstruction with all the modes is performed.

To plot a specific mode (in this case the mode ``0``), you can use::

  S.Field.Field0("-Rho",theta=0.,modes=0).plot(figure=1, vmin = 0., vmax = 0.01)

The main azimuthal mode of the plasma wave in the wake of the laser is the mode 0. The mode 0 has a complete cylindrical symmetry.

The azimuthal mode of the laser is the mode ``1``. 
To see the transverse field of the laser, we can plot the mode ``1`` of 
the transverse electric field (i.e. ``Er``)::

  S.Field.Field0("Er",theta=0.,modes=1).plot(figure=2)

On ``theta=0`` it will correspond ``Ey`` with our choice of laser polarization.

You can plot the reconstruction of the whole longitudinal electric 
field (laser and wake fields, modes ``1`` and ``0`` respectively) through::

  S.Field.Field0("El",theta=0.).plot(figure=4)

You can also follow the evolution of any grid quantity (for example here the electron density) through the command ``animate()``::

  S.Field.Field0("-Rho",theta=0.,modes=0).animate(figure=1, vmin = 0., vmax = 0.01)

.. rubric:: 2. 1D Probe

A quantity of interest e.g. for plasma acceleration is the longitudinal electric field on the laser propagation axis. 
For this purpose, we have defined the first ``Probe`` in the namelist. 
Check its ``origin`` and ``corners`` to understand where they are defined. 
To be more precise, we have defined it parallel to the axis, but at a small distance from it.
You can try to define another 1D ``Probe`` at the end of the namelist, but you will see that the fields there are very noisy. 

The ``Probes`` interpolate the cartesian components of the fields from the grid, not the cylindrical ones.
Thus, to follow the evolution of the longitudinal electric field you can use::

  S.Probe.Probe0("Ex").animate(figure=2)

Note that we haven't specified the mode. The ``Probes`` reconstruct the fields including all the modes.


  