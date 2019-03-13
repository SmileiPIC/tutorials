Field initialization for a relativistic electron bunch
-----------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the the 
relativistic species field initialization with :program:`Smilei`. 

We also recommend to run the simulations of this tutorial with 4 MPI process 
(remember to set the number of OpenMP threads as explained in :doc:`basics_setup`).

The following features will be addressed:

* Initialization of the electromagnetic field of relativistic species
* Observation of plasma wakefield driven by a relativistic electron bunch


.. note::

  This tutorial is done in 2D which is not physically relevant.
  Proper simulation of this kind must be done in 3D.

.. note::

  This tutorial is done with an ideal relativistic electron bunch (zero emittance, zero energy spread).
  A more realistic simulation would have an electron bunch with a spread in the transverse and longitudinal momentum.
  This unrealistic set-up will trigger a sudden and exaggerate self-compression of the bunch by its own plasma wakefield
  during its propagation.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

A relativistic electron bunch enters a plasma. It propagates in
the plasma and creates a non linear plasma wave in its wake.


----


Preparing the case study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download `this input file <beam_driven_wake.py>`_ and open it with your
favorite editor.

First, note that the electron bunch driving the plasma wave is initalized through
a block ``Species``, where it takes the name ``bunch_electrons``. The plasma electrons
are instead initialized through a block ``Species`` where they take the name ``electrons``.
The electron bunch is defined through a custom density profile (gaussian in this case) and 
a mean velocity ``beta``. This is an ideal electron bunch, since it has no energy spread, 
no transverse momentum spread (or equivalently zero emittance). To have a more realistic electron bunch,
you could initialize the positions and momenta of each bunch particle through numpy arrays, as explained in the 
documentation online.

Note that the species ``bunch_electrons`` has a special flag ``relativistic_field_initialization = True``.
It means that its self-consistent electromagnetic fields will be computed at the time when
this ``Species`` starts to move, i.e. in this case ``t=0`` (the default value for species not frozen).
The procedure used in :program:`Smilei` for this initialization is detailed in the online documentation.

These electromagnetic fields will propagate with the bunch and will push away the plasma electrons
as an intense laser pulse would do through its ponderomotive force.
As in the laser case, this will trigger a plasma oscillation (see for example the tutorials :doc:`advanced_wakefield`, :doc:`advanced_wakefield_envelope`).

.. note::

  Since the perfectly matched layer boundary condition is still not available, 
  there will be some border effects due to the intense bunch electromagnetic fields arriving to the 
  boundaries of the simulation window. A possible solution in a more accurate simulation consists in 
  enlarging the transverse size of the window to let the fields decay at the border.


----


A subtlety: why ions are not present?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


From Maxwell's equations it is possible to demonstrate that 
(see `Smilei's website <http://www.maisondelasimulation.fr/smilei/relativistic_fields_initialization.html>`_ ), 
provided that the continuity equation :math:`\nabla\cdot\mathbf{J}=-\partial_t\rho` is satisfied, the quantities 
:math:`\nabla\cdot\mathbf{B}` and :math:`\nabla\cdot\mathbf{E}-\rho` will remain
constant for all the simulation. The continuity equation ensured by Esirkepov's method in :program:`Smilei`.
Therefore, the value of these quantities will be the same as it was at ``t=0``. 
At that instant, in the zones of the plasma where the bunch is not present, 
:math:`\mathbf{B}=0`, so its divergence is trivially zero.
There, also the initial field :math:`\mathbf{E}` is zero, so in that zone 
:math:`\nabla\cdot\mathbf{E}-\rho=-\rho_0` for all the simulation, 
where :math:`\rho` is the deposited charge density and :math:`\rho_0` is the density 
at the initial state (the charge density of the electron layer).
In other words,  :math:`\nabla\cdot\mathbf{E}=\rho-\rho_0` for all the simulation. 
Since at the initial state there consisted in a layer of electrons with density :math:`\rho_0`,
all the system will evolve as if there was also a layer of ions with density :math:`-\rho_0`,
without having a real ion ``Species``. 


These "implicit" ions will not move, but they will influence the field.
This is a good approximation in our case: normally in the characteristic timescales 
of the plasma oscillations driven by a relativistic electron bunch the ions act only 
as an immobile positively-charged species.


If we were interested in phenomena like ionization of partially ionized ions or 
the motion of the ions, we would have needed to explicitly define a ``Species`` for the ions.
In our case, we could have defined a ``Species`` for the ions, but we would have 
obtained the same results using a considerable amount of memory for a species whose 
motion is trivial. Therefore in this case we can rely on the Esirkepov method to ensure 
an "implicit" presence of ions neutralizing the electrons at ``t=0``.


In the zones where the electron bunch and its field are present, the electromagnetic field is computed, 
ensuring the correct divergences of the fields :math:`\mathbf{E}` and :math:`\mathbf{B}` 
according to the presence of the electron bunch. 
Therefore here no "implicit" ions will be present.



----


Relativistic field initialization 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the simulation and open the results with ``happi``:: 

  import happi
  S = happi.Open("/path/to/the/simulation")

To visualize the bunch density and electric field at the initial timestep 
(obtained through the ad hoc initialization procedure), use::

  S.Field.Field0("-Rho",timesteps=0.).plot(figure=1)
  S.Field.Field0("Ex",timesteps=0.).plot(figure=2)
  S.Field.Field0("Ey",timesteps=0.).plot(figure=3)

Note that the bunch is initially in vacuum. If a ``Species`` is initialized inside the plasma,
activating the initialization of its field creates non-physical forces.
The bunch will move in the positive ``x`` (/longitudinal) direction towards the plasma.
Note that the field ``Ex`` is much lower than the transverse field ``Ey`` as for a relativistic moving charge.
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

