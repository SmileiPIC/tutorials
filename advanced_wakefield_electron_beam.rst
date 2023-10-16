Field initialization for a relativistic electron bunch
-----------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the the 
relativistic-species field initialization with :program:`Smilei`. 

With 8 MPI processes and 5 OpenMP threads the simulation of this tutorial should take a few minutes
(remember to set the number of OpenMP threads as explained in :doc:`basics_setup`).
The relativistic Poisson solver is parallelized through MPI but not with OpenMP, 
sometimes for larger simulations a larger number of MPI processes is necessary 
to reduce the time spent in field initialization.

The following features will be addressed:

* Initialization of a `Species` through a `numpy` array
* Initialization of the electromagnetic field with relativistic species
* Observation of the plasma wakefield driven by a relativistic electron bunch
* Analysis of the bunch evolution with the ``DiagParticleBinning`` diagnostic
* Analysis of the bunch evolution with the ``TrackParticles`` diagnostic
* Observation of the effect of Perfectly Matched Layers.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

A relativistic electron bunch enters a plasma in a ``AMcylindrical`` geometry. It propagates in
the plasma and creates a non linear plasma wave in its wake.

.. note::

  This tutorial is done in ``AMcylindrical`` with one azimuthal mode, thus assuming perfect cylindrical geometry in the fields (see also the related tutorial).

Initializing our bunch through a plasma density and a Maxwell-Jüttner momentum distribution 
would not allow us to set a certain emittance for the bunch 
(this parameter is related to the transverse phase space distribution of the bunch particles). 
Also, initializing a converging/diverging bunch or a particle distribution obtained from a beam
transport code would not be possible with this kind of initialization.

To manage these situations, an initialization of a ``Species`` with a ``numpy`` array is more suitable.
The ``Species`` called ``electron_bunch`` in our input file the input file `advanced_beam_driven_wake.py <advanced_beam_driven_wake.py>`_
will receive two ``numpy`` arrays, ``array_position`` and `array_momentum` in the ``position_initialization`` and ``momentum_initialization``
arguments.

Our bunch has ``npart`` particles, thus the shapes of these arrays will be ``(4,npart)``
and ``(3,npart)`` respectively. The ``array_position`` contains the coordinates of our bunch particles.
Remember that the origin of the axes is set on the propagation axis in ``AMcylindrical`` geometry,
so the transverse coordinates may be positive or negative. Each of the first three rows represents the ``x``, ``y``, ``z``
coordinates of the particles, while each column represents a particle.
The last row represents the weight given to each particle, related to the macro-particle charge.
Similarly, the ``array_momentum`` contains the particles momenta ``px``, ``py``, ``pz``.
With this initialization the density profile of the ``Species`` will be computed from the position of the
particles, and not from a profile given in the ``Species`` block as in other tutorials.

In our case, we generate the particles and momenta distribution of the electron bunch
assuming a gaussian distribution in the momentum space, with custom average energy, emittance, rms sizes, etc.
The bunch is assumed as waist (i.e. not converging, nor diverging), but manipulating the ``numpy`` arrays of the 
bunch particles it is easy to generate a more realistic electron bunch.

More details on the initialization through numpy arrays or from a file can be 
found `here <https://smileipic.github.io/Smilei/Use/particle_initialization.html>`_.


----


Preparing the case study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download the input file `advanced_beam_driven_wake.py <advanced_beam_driven_wake.py>`_ and open it with your
favorite editor. Note how the physical quantities are defined.
First the physical constants for conversions and then used to convert the physical quantities 
of interest, e.g. the bunch size, from SI units to normalized units.

The plasma electrons are initialized in a block ``Species`` named ``plasmaelectrons``.
The electron bunch driving the plasma wave is initalized in
a block ``Species`` named ``electronbunch``.

The flag ``relativistic_field_initialization = True`` in the ``electronbunch`` `Species`
means that its self-consistent electromagnetic fields will be computed at the time when
this ``Species`` starts to move, in this case at ``t=0`` because ``time_frozen=0``.
The procedure used in :program:`Smilei` for this field initialization is detailed
`here <https://smileipic.github.io/Smilei/Understand/relativistic_fields_initialization.html>`_.

These electromagnetic fields will propagate with the bunch and push away the plasma electrons
(just like an intense laser pulse would do with its ponderomotive force)
triggering a plasma oscillation.


.. note::

  You will see that the plasma does not fill all the simulation window. 
  This is because we want to include the electron bunch field in the window, but the plasma particles creating the plasma oscillations
  are only those radially near to the electron beam. Plasma particles at greater radial distances would not contribute to the relevant physics, but they would 
  require additional computational time. Thus we can omit them to perform the simulation more quickly without losing relevant phenomena.

.. note::

  The moving window in the namelist has been set to contain the electron bunch and the first wake period in the simulation window.




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
  S = happi.Open("example/of/path/to/the/simulation")

To visualize the initial bunch density and transverse electric field on the ``xy`` plane, use::

  S.Probe.Probe1("-Rho",timesteps=0.).plot(figure=1)
  S.Probe.Probe1("Ey",timesteps=0.).plot(figure=2)

Note that the bunch is initially in vacuum. If a ``Species`` is initialized inside the plasma,
activating the initialization of its field creates non-physical forces.

The bunch will move in the positive ``x`` (longitudinal) direction towards the plasma.
The field ``Ex`` is much lower than the transverse field ``Ey`` as for a relativistic moving charge.
The field ``Ey`` is the field that pushes the plasma electrons away from the bunch's path and triggers the plasma oscillations
in the bunch wake.

**Action**: What happens to the fields if you increase the number of bunch particles ``npart``? 
Are the fields more or less noisy?

.. note::
  You will see from the simulation log that the iterative relativistic Poisson solver 
  does not converge in this simulation with the chosen maximum number of iterations 
  (``relativistic_poisson_max_iteration`` in the ``Main`` block).
  However, the field obtained from this initialization will be accurate enough to 
  see a plasma wave driven by the electron beam's field and learn from this tutorial. 
  A more accurate initialization would probably require more iterations, increasing
  the initialization time. There is no value for ``relativistic_poisson_max_iteration`` 
  or for the acceptable error ``relativistic_poisson_max_error`` suited
  for all physical problems. The user should find the values suited to their 
  case of interest through careful trial and error.


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
  S.Probe.Probe1("Ex").slide(figure=4,vmin=-0.4,vmax=0.4,cmap="seismic")

The wave form has a shape of a sawtooth wave, 
since the set-up is in the so-called nonlinear regime. 

Try to change the total bunch charge ``Q_bunch`` and rerun the simulation, for example multiplying it by a factor
``0.05`` (a linear regime), ``0.75`` (a weakly nonlinear regime). What happens to the ``Ex`` waveform?


**Action**: What happens to the fields if you increase the number of particles in the plasma? 
Are the fields more or less noisy?


----

Particle Binning diagnostic 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's study in detail the evolution of the electron bunch.
To start, the energy spectrum can be found using the first ``ParticleBinning`` diagnostic defined in the namelist::

  S.ParticleBinning(0).slide()

Note how the bunch energy spread is increasing and the average energy is decreasing as it drives the plasma waves in its propagation.

The longitudinal phase space can be seen through the second ``ParticleBinning`` diagnostic of the namelist::

  S.ParticleBinning(1).slide()

Note how the bunch tail is losing its energy. That zone of the bunch is where the decelerating electric field
is generated.

**Action**: Study the remaining ``ParticleBinning`` diagnostics, which contain the bunch distribution in transverse phase space
(``y`` and ``z`` phase space planes respectively). Note how the transverse coordinates can be negative in cylindrical geometry.


----

Track Particles diagnostic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note how we had to specify the limits of the axes of our ``ParticleBinning`` diagnostics.
This can be a considerable constraint when these boundaries are not known.
Furthermore, if we wanted to compute more complex quantities derived from the 
positions and momenta of the electron bunch, e.g. the energy spread of its longitudinal
slices, it would have not been easy to do with ``ParticleBinning`` diagnostics.
Finally, sometimes we want to export the final bunch distribution in the phase space,
i.e. the 3D positions and 3D momenta of all particles, e.g. to use them as input of 
a beam dynamics code to design a magnetic transport line, so we would need the coordinates
of each macro-particle. 

For these reasons, often in wakefield simulations it is preferrable to use the 
``TrackParticles`` diagnostic. This diagnostic allows to select a ``Species`` 
and optionally a filter (e.g. macro-particles above a certain energy). The diagnostic
can give the id numbers, position, momentum and weight of the macro-particles of
that ``Species`` satisfying the filter.

**Note** Specifying a filter can be essential to avoid exporting exceedingly large amount of 
data. For example, in a laser wakefield acceleration where the accelerated electron 
beam comes from the plasma itself, not specifying a filter would export the 
data of all the plasma species macro-particles. In this case, using a filter e.g.
select only the  macro-particles above a certain energy, would likely export the
macro-particles of interest for typical laser wakefield acceleration studies.

In this simulation's namelist, a ``TrackParticles`` block is specified 
to export the data of all the electron bunch macro-particles.
The bunch does not have many macro-particles, so we don't need to specify a filter.

You can extract the ``TrackParticles`` data of a given ``timestep`` with::

  # Read the DiagTrackParticles data
  import numpy as np
  chunk_size   = 60000
  species_name = "electronbunch"
  timestep     = 0.
  track = S.TrackParticles(species = species_name, chunksize=chunk_size, sort=False)
  for particle_chunk in track.iterParticles(timestep, chunksize=chunk_size):

      
    # positions
    x            = particle_chunk["x"] 
    y            = particle_chunk["y"]
    z            = particle_chunk["z"]
    
    # momenta
    px           = particle_chunk["px"]
    py           = particle_chunk["py"]
    pz           = particle_chunk["pz"]
    p            = np.sqrt((px**2+py**2+pz**2)) 
    
    # weights, proportional to che macro-particle charge
    w            = particle_chunk["w"]
  
    # energy
    E            = np.sqrt((1.+p**2))                           
      
    Nparticles   = np.size(w)                                 
    print(" ")
    print("Read "+str(Nparticles)+" macro-particles from the file")
    
    
This way, you will have some numpy arrays, with the coordinates, momenta etc of all 
the electron bunch macro-particles at the timestep ``timestep``.
In this case we exported the first timestep. You can find a list of the available 
timesteps with::
  timesteps = track.getAvailableTimesteps()
Each array has a size equal to the number of macro-particles.
The argument ``chunksize`` denotes the maximum number macro-particles per chunk
you are reading. Extracting data in chunks avoids reading all the macro-particles at once,
which can be useful with large amounts of data. In this case we just need to read one chunk.

Using these numpy arrays, you can easily compute derived quantities, e.g.
you can obtain the electron bunch charge by summing the weights of all the 
macro-particles (which can in principle vary between macro-particles) and using
the appropriate conversion factor::
  
  import scipy.constants
  total_weight = w.sum()
  weight_to_pC = S.namelist.e * S.namelist.ncrit 
  weight_to_pC = weight_to_pC * (S.namelist.c_over_omega0)**3 
  Q_pC         = total_weight * weight_to_pC * 10**(12)
  print(" ")
  print("Total bunch charge = "+str(Q_pC)+" pC")
  
**Action** Check that this is the bunch charge set in the input namelist.
  
**Action** Try to extract the evolution of the bunch parameters during the simulation.
Remember that you can extract the available timesteps and then loop the extraction 
of the macro-particle arrays over the timesteps.

**Action** plot the energy spectrum, i.e. the histogram of the macro-particles energies,
and check that the result is the same obtained with the ``ParticleBinning`` diagnostic.
Pay attention to the normalizations of the axes!

**Action** Adapting this `script <https://github.com/SmileiPIC/TP-M2-GI/blob/main/Postprocessing_Scripts/Follow_electron_bunch_evolution.py>`_,
study the evolution of the bunch parameters, e.g. its emittance, energy spread, etc.

----


Perfectly Matched Layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Imperfect boundary conditions may cause unphysical effects when the bunch's intense
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
from 20 to 5? Are the fields more or less noisy?

**Action**: What happens if instead of the ``"PML"`` boundary conditions you use 
the more classic following conditions?::

  EM_boundary_conditions  =  [["silver-muller","silver-muller"],["buneman","buneman"],]

How large should the simulation window be to avoid reflections without a Perfectly
Matched Layers?

----

Acceleration of a witness bunch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you know everything necessary to simulate beam-driven plasma acceleration: try to define
a second, smaller electron bunch, with the same energy of the driver bunch, smaller charge and small enough to fit 
in the plasma wave and injected in the accelerating phase of the plasma wave (i.e. negative ``Ex``).

Use the ``numpy`` array initialization method as you have done for the bunch driving the waves. 
Study the evolution of the energy spectrum of this witness bunch and check that its average energy is increasing.




 