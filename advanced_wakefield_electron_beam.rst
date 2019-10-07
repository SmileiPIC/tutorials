Field initialization for a relativistic electron bunch
-----------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the the 
relativistic-species field initialization with :program:`Smilei`. 

We recommend to run the simulations of this tutorial with 4 MPI processes
(remember to set the number of OpenMP threads as explained in :doc:`basics_setup`).

The following features will be addressed:

* Initialization of the electromagnetic field with relativistic species
* Observation of the plasma wakefield driven by a relativistic electron bunch


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

A relativistic electron bunch enters a plasma in a 2D geometry. It propagates in
the plasma and creates a non linear plasma wave in its wake.

.. note::

  This tutorial is done in 2D which is not physically relevant.
  Proper simulation of this kind must be done in 3D 
  or in cylindrical geometry with azimuthal mode decomposition (see the related tutorial).

.. note::

  This tutorial is done with an ideal relativistic electron bunch (zero emittance, zero energy spread).
  A more realistic simulation would have an electron bunch with a spread in the transverse and longitudinal momentum.
  This unrealistic set-up will trigger a sudden and exaggerated self-compression of the bunch by its own plasma wakefield
  during its propagation.


----


Preparing the case study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download the input file `beam_driven_wake.py <beam_driven_wake.py>`_ and open it with your
favorite editor.

The plasma electrons are initialized in a block ``Species`` named ``electrons``.
The electron bunch driving the plasma wave is initalized in
a block ``Species`` named ``bunch_electrons``.
It has a custom density profile (gaussian in this case) and 
a mean velocity ``beta``. This is an ideal electron bunch, since it has no energy spread, 
no transverse momentum spread (or equivalently zero emittance).

.. note::

  To have a more realistic electron bunch,
  you could initialize the positions and momenta of each particle with numpy arrays,
  as explained `here <http://www.maisondelasimulation.fr/smilei/namelist.html#position_initialization>`_.

The special flag ``relativistic_field_initialization = True``
means that its self-consistent electromagnetic fields will be computed at the time when
this ``Species`` starts to move, in this case at ``t=0`` because ``time_frozen=0``.
The procedure used in :program:`Smilei` for this initialization is detailed
`here <http://www.maisondelasimulation.fr/smilei/relativistic_fields_initialization.html>`_.

These electromagnetic fields will propagate with the bunch and push away the plasma electrons
(just like an intense laser pulse would do with its ponderomotive force)
triggering a plasma oscillation.

.. note::

  Imperfect boundary condition cause unphysical effects when the bunch's intense
  electromagnetic fields arrive at the boundaries of the simulation window.
  A larger box (transversally) could help fields decay near the boundaries.

.. note::

  The moving window in the namelist has been set to contain the electron bunch and the first wake period in the simulation window.

.. note::

  You will see that the plasma does not fill all the simulation window. 
  This is because we want to include the electron bunch field in the window, but the plasma particles creating the plasma oscillations
  are only those radially near to the electron beam. Plasma particles at greater radial distances would not contribute to the relevant physics, but they would 
  require additional computational time. Thus we can omit them to perform the simulation more quickly without losing relevant phenomena.

----


A subtlety: why ions are not present?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Maxwell's equations and the continuity equation :math:`\nabla\cdot\mathbf{J}=-\partial_t\rho` 
(which is true also for the single species) imply that :math:`\nabla\cdot\mathbf{E}-\rho` remains 
constant throughout the simulation
(see `this <http://www.maisondelasimulation.fr/smilei/relativistic_fields_initialization.html>`_).
This can be written :math:`\nabla\cdot\mathbf{E}-\rho_e-\rho_i=\nabla\cdot\mathbf{E_0}-\rho_{e0}-\rho_{i0}`.
If we consider ions immobile, then this becomes :math:`\nabla\cdot\mathbf{E}-\rho_e=\nabla\cdot\mathbf{E_0}-\rho_{e0}`, 
because the ion continuity equation implies that if :math:`\mathbf{J}_{i}=0` then :math:`\rho_i=\rho_{i0}`.
Note that ions do not appear anymore so that they can be discarded from the simulation.
Assuming also :math:`\rho_{e0}+\rho_{i0}=0` and the initial field :math:`\mathbf{E_0}` being divergence free,
we have :math:`\nabla\cdot\mathbf{E}=\rho_e+\rho_{i0}` at all times.
The system will evolve as if there were ions, without having a real ion ``Species``. 

This is a good approximation in our case: plasma oscillations driven by a relativistic
electron bunch do not substantially move the ions. Indeed, the ion mass is at least 2000 times greater than the mass of an electron, so the characteristic timescales of the ion motion are much greater than those of the electron motion. Discarding ions represents an important gain of
computational time.
If we were interested in phenomena like ionization or ion motion,
we would have needed to explicitly define an ion ``Species``.


----


Relativistic field initialization 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the simulation and open the results with ``happi``:: 

  import happi
  S = happi.Open("/path/to/the/simulation")

To visualize the initial bunch density and electric field, use::

  S.Field.Field0("-Rho",timesteps=0.).plot(figure=1)
  S.Field.Field0("Ex",timesteps=0.).plot(figure=2)
  S.Field.Field0("Ey",timesteps=0.).plot(figure=3)

Note that the bunch is initially in vacuum. If a ``Species`` is initialized inside the plasma,
activating the initialization of its field creates non-physical forces.

The bunch will move in the positive ``x`` (longitudinal) direction towards the plasma.
The field ``Ex`` is much lower than the transverse field ``Ey`` as for a relativistic moving charge.
The field ``Ey`` is the field that pushes the plasma electrons away from the bunch's path and triggers the plasma oscillations
in the bunch wake.


----


Nonlinear, beam-driven plasma oscillations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The plasma electrons pushed away from the bunch path will be attracted back to their original positions
by the immobile ions and start to oscillate.

Visualize the nonlinear plasma wave forming in the wake of the electron bunch::

  S.Field.Field0("-Rho",).animate(figure=1)

The evolution of the longitudinal electric field on axis, very important for acceleration of another particle bunch,
can be visualized through::

  S.Probe.Probe0("Ex").animate(figure=4)

The wave form has a shape between a sinusoidal wave and a sawtooth wave, 
since the set-up is in the so-called weakly nonlinear regime. 

Try to change the normalized peak density of the bunch ``alpha`` and rerun the simulation, for example with the values
``0.001`` (a linear regime), ``1.5`` (a nonlinear regime). What happens to the ``Ex`` waveform?

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The plasma electrons pushed away from the bunch path will be attracted back to their original positions
by the immobile ions and start to oscillate.

Visualize the nonlinear plasma wave forming in the wake of the electron bunch::

  S.Field.Field0("-Rho",).animate(figure=1)

The evolution of the longitudinal electric field on axis, very important for acceleration of another particle bunch,
can be visualized through::

  S.Probe.Probe0("Ex").animate(figure=4)

The wave form has a shape between a sinusoidal wave and a sawtooth wave, 
since the set-up is in the so-called weakly nonlinear regime. 

Try to change the normalized peak density of the bunch ``alpha`` and rerun the simulation, for example with the values
``0.001`` (a linear regime), ``1.5`` (a nonlinear regime). What happens to the ``Ex`` waveform?

