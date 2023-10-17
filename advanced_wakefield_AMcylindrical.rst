Azimuthal-mode-decomposition cylindrical geometry 
------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the cylindrical geometry 
with azimuthal Fourier decomposition in :program:`Smilei`.
The chosen physical configuration is a case of laser wakefield acceleration.
This set-up will allow us to address advanced features that are available
also in other geometries.
The following topics will be addressed:

* Understand the concept of azimuthal mode decomposition
* Set up a simulation in this geometry
* The analysis of the grid fields in AM cylindrical geometry
* Observation of the effect of Perfectly Matched Layers (feature available also in other geometries)
* Reduce the effects of the Numerical Cherenkov Radiation (with features available also in other geometries).

With 8 MPI processes and 10 OpenMP threads per MPI process, the simulation should need a few minutes.


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An high intensity laser pulse, linearly polarized in the ``y`` direction, enters an under dense plasma. 
It propagates in the plasma in the positive ``x`` direction and creates a non linear plasma wave in its wake.
The plasma density has a sharp density transition at its start, which triggers
the injection of an electron beam in the plasma wave. The plasma wave longitudinal
electric fields accelerate the electron beam.

The moving window in the namelist has been set to contain the laser and the first wake period in the simulation window.


.. note::

  You will see that the plasma does not fill all the simulation window. 
  This is because we want to include the laser electromagnetic field in the window, but the plasma particles creating the plasma oscillations
  are only those radially near to the laser pulse. Plasma particles at greater radial distances would not contribute to the relevant physics, but they would 
  require additional computational time. Thus we can omit them to perform the simulation more quickly without losing relevant phenomena.

----


A subtlety: why ions are not present?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Maxwell's equations and the continuity equation :math:`\nabla\cdot\mathbf{J}=-\partial_t\rho` 
(which is true also for the single species) imply that :math:`\nabla\cdot\mathbf{E}-\rho` remains 
constant throughout the simulation
(see `this <https://smileipic.github.io/Smilei/Understand/relativistic_fields_initialization.html>`_).
This can be written :math:`\nabla\cdot\mathbf{E}-\rho_e-\rho_i=\nabla\cdot\mathbf{E_0}-\rho_{e0}-\rho_{i0}`.
If we consider ions immobile, then this becomes :math:`\nabla\cdot\mathbf{E}-\rho_e=\nabla\cdot\mathbf{E_0}-\rho_{e0}`, 
because the ion continuity equation implies that if :math:`\mathbf{J}_{i}=0` then :math:`\rho_i=\rho_{i0}`.
Note that ions do not appear anymore so that they can be discarded from the simulation.
Assuming also :math:`\rho_{e0}+\rho_{i0}=0` and the initial field :math:`\mathbf{E_0}` being divergence free,
we have :math:`\nabla\cdot\mathbf{E}=\rho_e+\rho_{i0}` at all times.
The system will evolve as if there were ions, without having a real ion ``Species``. 
This is a good approximation in our case: plasma oscillations driven by a short 
laser pulse with the intensity used in this tutorial
do not substantially move the ions. Indeed, the ion mass is at least 2000 times 
greater than the mass of an electron, so the characteristic timescales of the 
ion motion are much greater than those of the electron motion. Discarding ions 
represents an important gain of computational time.
If we were interested in phenomena like ionization or ion motion,
we would have needed to explicitly define an ion ``Species``.

----



Azimuthal-mode-decomposition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some physical situations like the one of this tutorial, the phenomena of interest have a cylindrical geometry or are very near to be cylindrically symmetric.

The electromagnetic fields can then be decomposed in Fourier azimuthal modes (where the azimuthal angle is defined with respect to the propagation axis of the laser). 
Each mode is defined on a 2D grid, where the two dimensions are the longitudinal and radial ones.

In this case, Maxwell's Equations can evolve independently the 2D azimuthal modes, and to save time we can retain only a certain number of azimuthal modes, 
without losing the relevant physics. In the case simulated in this tutorial, using only two azimuthal modes allows to catch the relevant physics.
The particles, on the other hand, move in the 3D space, pushed by the 3D Cartesian fields reconstructed from the electromagnetic azimuthal modes. 
With this powerful technique, 3D features can be simulated at the cost of approximately N 2D simulations, where N is the number of modes we keep in the simulation.

More details on the Azimuthal modes decomposition can be found `here <https://smileipic.github.io/Smilei/Understand/azimuthal_modes_decomposition.html>`_.

Simulation setup
^^^^^^^^^^^^^^^^^^^^^^^^

An input file to simulate laser wake excitation in this geometry will be very similar to a namelist in 2D geometry, with some important differences.
Check them in the input file:

* The selected geometry is ``AMcylindrical``

* The grid resolution is given by a longitudinal and radial resolution, since the azimuthal modes are defined on a 2D grid 

* The number of azimuthal modes simulated is set in ``number_of_AM``. In this case only two of them are necessary to reproduce the relevant physics phenomena

* The laser can be defined through the ``LaserGaussianAM`` block

* When you define a plasma density profile, it will be defined with two coordinates ``(x,r)``

* Still in the plasma density profile definition, remember that ``r=0`` corresponds to the lower boundary of the grid, i.e. the laser propagation axis

* The ``Probes`` origin and corners are defined with three coordinates, since they will interpolate the fields in the 3D space as if they were macro-particles in a 3D simulation.

----


Step by step tutorial
^^^^^^^^^^^^^^^^^^^^^^^^

Download  `this input file <laser_wake_AM.py>`_ , open it with your favorite editor and run the simulation.
Then, open the results::

  import happi
  S = happi.Open("/example/path/to/the/simulation") 

.. rubric:: 1. Field diagnostic

Now let's have a look at the grid fields, for example the electron density::

  S.Field.Field0("-Rho",theta = 0.).plot(figure=1, vmin = 0., vmax = 0.01)

In the previous command we have specified a certain angle ``theta = 0`` (i.e. the demi-plane including the positive ``y`` coordinates).
With the ``Field`` diagnostic, you can virtually specify any angle ``theta``. 
See the reference frame `here <https://smileipic.github.io/Smilei/Understand/azimuthal_modes_decomposition.html>`_ for the definition of this angle.

At the cost of approximately N 2D simulations (N is the number of azimuthal modes, two in this case), you can obtain the fields in all the 3D space, like in a 3D simulation.
Note that in the ``Field`` diagnostic you will see only half of the plane, as the ``Field`` diagnostics shows the fields on the grid, defined on a half-plane in this geometry.

By default, the last command we used will plot the last timestep available. You can also slide along the available timesteps::
  
  S.Field.Field0("-Rho",timesteps=6000.,theta=0.).slide(figure=1, vmin = 0., vmax = 0.01)

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

.. rubric:: 2. Probe 1D

A quantity of interest e.g. for plasma acceleration is the longitudinal electric field on the laser propagation axis. 
For this purpose, we have defined the first ``Probe`` in the namelist. 
Check its ``origin`` and ``corners`` to understand where they are defined. 
To be more precise, we have defined it parallel to the axis, but at a small distance from it.
You can try to define another 1D ``Probe`` at the end of the namelist, but you will see that the fields there are very noisy. 

The ``Probes`` interpolate the cartesian components of the fields from the grid, not the cylindrical ones.
Thus, to follow the evolution of the longitudinal electric field you can use::

  S.Probe.Probe0("Ex").animate(figure=2)

Note that we haven't specified the mode. The ``Probes`` reconstruct the fields including all the modes.

.. rubric:: 3. Probe 2D

In the namelist, a 2D ``Probe`` is defined on the plane parallel to the polarization direction of the laser.
For how we have defined it, you won't see only half plane as in the ``Field`` diagnostic, but both the negative and positive ``y`` points.

Let's give a look to the evolution of the plasma density::

  S.Probe.Probe1("-Rho").slide(figure=3,vmin=0.,vmax=0.01)

To see the evolution of the longitudinal electric field and the electric field in the ``y`` direction, you can use::

  S.Probe.Probe1("Ex").slide(figure=4)
  S.Probe.Probe1("Ey").slide(figure=5)

Note that the ``Fields`` contained the cylindrical components of the fields, but the ``Probes`` diagnostics
contain the Cartesian reconstruction of the fields, thus with Cartesian components.

----


Perfectly Matched Layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Imperfect boundary conditions may cause unphysical effects when the laser's intense
electromagnetic fields arrive at the boundaries of the simulation window.
A larger box (transversally) could help fields decay near the boundaries.
However this can easily increase the simulation time beyond an acceptable level, 
and only to avoid reflections, adding to the domain some physical regions where 
no phenomenon of interest happens. 

Therefore, to avoid this inefficient approach, this namelist uses improved 
boundary conditions called `Perfectly Matched Layers <https://smileipic.github.io/Smilei/Understand/PML.html>`_, 
which add some cells to the simulation borders filled with a fictious medium 
where the fields are damped and not reflected back inside the physical simulation window. 
Note that these additional cells are not visible to the user.

The Perfectly Matched Layers are activated in the ``Main`` block through::

  EM_boundary_conditions = [
      ["PML","PML"],
      ["PML","PML"],
  ],

  number_of_pml_cells = [[20,20],[20,20]],  
  
**Action**: How do the results change if you decrease the number of PML cells
from 20 to 5? Are the fields more or less noisy? You may need to saturate the 
colormap to see differences.
Check the field with ::
  S.Probe.Probe1("Ey").slide(vmin=-0.001,vmax=0.001,cmap="seismic",figure=4)
  
We recommend to launch this simulation in a different directory to be able to
compare the two simulations. You should find some differences especially at 
the window borders.

**Action**: What happens if instead of the ``"PML"`` boundary conditions you use 
the more classic following conditions?::

  EM_boundary_conditions  =  [["silver-muller","silver-muller"],["buneman","buneman"],]

We recommend to launch this simulation in a different directory to be able to
compare the two simulations. As in the previous exercise, check the fields at the border.
Small differences given by the presence (or not) of reflections at the borders
can have visible effects on the accelerated electron beam dynamics.
For example, check the shape of the electron beam by visualizing the electron 
density::

  S.Probe.Probe1("-Rho").slide(vmin=0,vmax=0.005,figure=9)

How large should the simulation window be to avoid reflections without a Perfectly
Matched Layers? How much does the simulation time change with a larger window without
Perfectly Matched Layers?

----


Coping with the Numerical Cherenkov Radiation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The finite difference solver used in the simulation (``maxwell_solver="Yee"`` 
is used by default) introduces a numerical dispersion in the wave propagation.
For example, the laser and plasma fields propagating in the `x` direction as in 
the simulation of this tutorial are slowed down and this effect is stronger when 
the timestep is set increasingly smaller compared to the cell length along `x`.
To reduce the dispersion ideally the normalized timestep should be as near as 
possible to the normalized cell length along `x`.

The interaction of relativistic macro-particles with these numerically slowed waves
generates a purely numerical artifact called Numerical Cherenkov Radiation, which
manifests as a high frequency electromagnetic fields around relativistic macro-particles
as (e.g. in accelerated electron beam in laser wakefield acceleration). These spurious
fields have visible effects on the simulated dynamics of the accelerated beams
and can easily propagate in the simulation window. Therefore, in order to have 
more physically relevant results, some technique must be used to cope with this effect.
Unfortunately there is no universal solution that can remove the effects of the Numerical
Cherenkov Radiation in all physical set-ups that can be simulated and without 
considerably increasing the simulation time, thus the user
must find the technique that yields the desired accuracy-performance compromise
depending on their case of interest.

In this tutorial we will test the use of a low-pass filter on the currents and 
a force interpolation technique that can reduce the effects of the Numerical Cherenkov
Radiation on the macro-particles.

One of the simplest techniques to reduce the Numerical Cherenkov Radiation is to 
filter the currents with a binomial filter.
Try to launch a new simulation using the same namelist, but decommenting the block::

  CurrentFilter(
     model  = "binomial",
     passes = [2],
  )

**Action**: compare the results of the two simulations, with an without filter.
For example, you can use the ``Probes`` to check a combination of ``Probes`` proportional
to the force acting on the macro-particles in the `y` direction::

  S.Probe.Probe1("Ey-c*Bz").slide(vmin=-0.02,vmax=0.02,cmap="seismic")
  
Without the filter, you will see the high frequency oscillations of the numerical
Cherenkov Radiation, that have a visible effect also on the shape of the
accelerated electron beam inside the plasma waves. You can check this with::

  S.Probe.Probe1("-Rho").slide(vmin=0,vmax=0.005,figure=9)
  
The electron beam simulated with the filter should be transversely smaller.
This happens because the filter reduces the growth of the spurious radiation, 
whose effects include the heating the electron beams.
Using a low pass filter is not an ideal solution, since it can damp high frequencies 
that are physical and adds time dedicated to communications, especially when
the number of filter passes is increased to further reduce the numerical artifact.

A second solution, that we recommend, is the use of a force interpolation technique 
called B-TIS3 described in 
`P.-L. Bourgeois and X. Davoine, Journal of Plasma Physics 89 (2023) <https://doi.org/10.1017/S0022377823000223>`_, 
that does not remove the Numerical Cherenkov Radiation, but considerably reduces 
its effects on the macro-particles, with minimal increase of the simulation time.

**Action**: Run a new simulation (without filter), changing the variable ``use_BTIS3_interpolation`` 
before the ``Main`` block to ``True``. Note how this changes the ``pusher`` 
and adds some fields to the ``Probes`` in the namelist. 
Activating the B-TIS3 interpolates the magnetic fields 
in a way that is more physically accurate for fields moving close to the speed 
of light in the positive `x` direction, and when the normalized timestep is close
to the normalized cell size along `x` (which is typical of laser wakefield simulations).
Check how the electron beam shape changes as you have done before with the filter
and then check this combination of ``Probes``::

  S.Probe.Probe1("Ey-c*Bz").slide(vmin=-0.02,vmax=0.02,cmap="seismic")
  
The differences are small compared to the simulation with B-TIS3 and you will 
still see the Numerical Cherenkov Radiation in the grid. However, in this simulations
the macro-particles are not pushed on the `y` direction with these fields, 
but by a combination of fields that uses the B-TIS3 fields when necessary. 
The force along `y` acting on the macro-particles in this case is proportional to::
  
  S.Probe.Probe1("Ey-c*BzBTIS3").slide(vmin=-0.02,vmax=0.02,cmap="seismic")

Here you should see visible differences, especially near the electron beam.

**Action**: After you will have learned how to analyse the ``TrackParticles`` 
diagnostic in the next tutorials, compare the final electron beam
parameters with and without the techniques that we have explored to reduce 
the effects of the Numerical Cherenkov Radiation.
