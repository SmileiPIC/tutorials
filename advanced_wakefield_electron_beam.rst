Field initialization for a relativistic electron bunch
-----------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the the 
relativistic-species field initialization with :program:`Smilei`. 

With 20 MPI processes and 4 OpenMP threads the simulation of this tutorial should take a few minutes
(remember to set the number of OpenMP threads as explained in :doc:`basics_setup`).
The relativistic Poisson solver is parallelized through MPI but not with OpenMP, so a large number
of MPI processes is necessary to reduce the time spent in field initialization.

The following features will be addressed:

* Initialization of a `Species` through a `numpy` array
* Initialization of the electromagnetic field with relativistic species
* Observation of the plasma wakefield driven by a relativistic electron bunch


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

A relativistic electron bunch enters a plasma in a `AMcylindrical` geometry. It propagates in
the plasma and creates a non linear plasma wave in its wake.

.. note::

  This tutorial is done in `AMcylindrical` (see also the related tutorial).

Initializing our bunch through a plasma density and a Maxwell-Jüttner momentum distribution 
would not allow us to set a certain emittance for the bunch 
(this parameter is related to the transverse phase space distribution of the bunch particles). 
Also, initializing a converging/diverging bunch or a particle distribution obtained from a beam
transport code would not be possible with this kind of initialization.

To manage these situations, an initialization of a `Species` with a `numpy` array is more suitable.
The `Species` called `electron_bunch` in our input file the input file `beam_driven_wake.py <beam_driven_wake.py>`_
will receive two numpy arrays, `array_position` and `array_momentum` in the `position_initialization` and `momentum_initialization`
arguments.
Our bunch has `npart` particles, thus the shapes of these arrays will be `(4,npart)` 
and `(3,npart)` respectively. The `array_position` contains the coordinates of our bunch particles.
Remember that the origin of the axes is set on the propagation axis in `AMcylindrical` geometry,
so the transverse coordinates may be positive or negative. Each of the first three rows represents the `x`,`y`,`z`
coordinates of the particles, while each column represents a particle.
The last row represents the weight given to each particle, related to the macro-particle charge.
Similarly, the `array_momentum` contains the particles momenta `px`,`py`,`pz`.
With this initialization the density profile of the `Species` will be computed from the position of the
particles, and not from a profile given in the `Species` block as in other tutorials.

In our case, we generate the particles and momenta distribution of the electron bunch
assuming a gaussian distribution in the momentum space, with custom average energy, emittance, rms sizes, etc.
The bunch is assumed as waist (i.e. not converging, nor diverging), but manipulating the `numpy` arrays of the 
bunch particles it is easy to generate a more realistic electron bunch.

More details on the initialization through numpy arrays or from a file can be 
found `here <https://smileipic.github.io/Smilei/particle_initialization.html>`_.


----


Preparing the case study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download the input file `beam_driven_wake.py <beam_driven_wake.py>`_ and open it with your
favorite editor.

The plasma electrons are initialized in a block ``Species`` named ``electrons``.
The electron bunch driving the plasma wave is initalized in
a block ``Species`` named ``bunch_electrons``.

The flag ``relativistic_field_initialization = True`` in the ``bunch_electrons`` `Species`
means that its self-consistent electromagnetic fields will be computed at the time when
this ``Species`` starts to move, in this case at ``t=0`` because ``time_frozen=0``.
The procedure used in :program:`Smilei` for this initialization is detailed
`here <https://smileipic.github.io/Smilei/relativistic_fields_initialization.html>`_.

These electromagnetic fields will propagate with the bunch and push away the plasma electrons
(just like an intense laser pulse would do with its ponderomotive force)
triggering a plasma oscillation.

.. note::

  Imperfect boundary conditions may cause unphysical effects when the bunch's intense
  electromagnetic fields arrive at the boundaries of the simulation window.
  A larger box (transversally) could help fields decay near the boundaries.
  Perfecly absorbing boundary conditions for the electromagnetic fields are currently under development.

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

  S.Probe.Probe1("-Rho",timesteps=0.).plot(figure=1)
  S.Probe.Probe1("Ex",timesteps=0.).plot(figure=2)
  S.Probe.Probe1("Ey",timesteps=0.).plot(figure=3)

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

  S.Probe.Probe0("-Rho",).slide(figure=1)
  S.Probe.Probe1("-Rho",).slide(figure=2)

The evolution of the longitudinal electric field on axis, very important for acceleration of another particle bunch,
can be visualized through::

  S.Probe.Probe0("Ex").slide(figure=4)
  S.Probe.Probe1("Ex").slide(figure=4)

The wave form has a shape between a sinusoidal wave and a sawtooth wave, 
since the set-up is in the so-called weakly nonlinear regime. 

Try to change the total bunch charge ``Q_bunch`` and rerun the simulation, for example multiplying it by a factor
``0.1`` (a linear regime), ``1.5`` (a nonlinear regime). What happens to the ``Ex`` waveform?

The plasma electrons pushed away from the bunch path will be attracted back to their original positions
by the immobile ions and start to oscillate.

Particle Binning diagnostic 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's study in detail the evolution of the electron bunch.
To start, the energy spectrum can be found using the first `ParticleBinning` diagnostic defined in the namelist::

  S.ParticleBinning(0).slide()

Note how the bunch energy spread is increasing and the average energy is decreasing as it drives the plasma waves in its propagation.

The longitudinal phase space can be seen through the second `ParticleBinning` diagnostic of the namelist::

  S.ParticleBinning(1).slide()

Note how the bunch tail is losing its energy. That zone of the bunch is where the decelerating electric field
is generated.

The third and three `ParticleBinning` diagnostics can show you the bunch distribution in transverse phase space
(`y` and `z` planes respectively). Note how the transverse coordinates can be negative in cylindrical geometry.

----

Acceleration of a witness bunch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you know everything necessary to simulate beam-driven plasma acceleration: try to define
a smaller electron bunch, with the same energy of the driver bunch, smaller charge and small enough to fit 
in the plasma wave and injected in the accelerating phase of the plasma wave (i.e. negative `Ex`).

Use the `numpy` initialization method as you have done for the bunch driving the waves. 
Study the evolution of the energy spectrum of this witness bunch and check that its average energy is increasing.

 