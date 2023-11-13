Envelope model for laser wakefield acceleration
-----------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the laser
envelope model with :program:`Smilei`. Before starting with this tutorial, we
recommend to complete first the tutorial on :doc:`advanced_wakefield_AMcylindrical`. In that
Tutorial, Laser Wakefield Acceleration is simulated in a standard way, i.e. the
laser is defined through its electromagnetic fields defined on the grid.
We recommend also to complete the tutorial :doc:`advanced_wakefield_electron_beam`
to familiarize with the diagnostics involving the macro-particle quantities.

With 2 MPI processes and 20 OpenMP threads this simulation should run in a few minutes.
(remember to set the number of OpenMP threads as explained in :doc:`basics_setup`).

The following features will be addressed:

* Automatic conversion of the output to SI units (``pint`` Python module required)
* Laser envelope initialization "in the box"
* Initialization of the species interacting with the laser envelope
* Observation of relativistic self-focusing
* Automatic conversion of the output to SI units (``pint`` Python module required)
* Analysis of the grid fields when an envelope is present
* Use of the envelope ionization module.
* Use of the B-TIS3 interpolation scheme with a laser envelope

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma. It propagates in
the plasma and creates a non linear plasma wave in its wake.
The start of the plasma is made of a mixture of hydrogen and nitrogen, while the
rest of the plasma is made of pure hydrogen. The laser field is strong enough to 
ionize the hydrogen and the first 5 levels of the nitrogen much before the arrival 
of the laser peak field, thus the hydrogen will be assumed ionized and the nitrogen
ionized up to level 5. The field of the laser peak is intense enough to further 
ionize the nitrogen ions. Some of the newly released electrons are trapped and 
accelerated in the plasma wave behind the laser (hence the name laser wakefield 
acceleration with ionization injection).

The simulation is run with a `Laser Envelope model <https://smileipic.github.io/Smilei/Understand/laser_envelope.html>`_
for the laser pulse. This allows to simulate the laser-plasma interaction in an underdense plasma
without the need to resolve the high frequency oscillations of the laser pulse.
This way, we can use a coarser cell size along the laser propagation direction `x` and
a coarser timestep, obtaining considerable speed-ups for our simulations.
Thus, although the envelope represents a laser pulse, you won't see the laser oscillations at wavelength
:math:`\lambda_0` since we are using a laser envelope model.

Furthermore, the simulation of this tutorial is run in cylindrical geometry 
(only one azimuthal mode), which further speeds-up the simulations. 
The envelope model is available also in other geometries.

.. note::

  The simulation in this tutorial uses a few macro-particles per cell and a coarse mesh too keep the 
  computational time reasonable. Physically relevant simulations of the considered phenomena would 
  require more macro-particles and a finer mesh. Apart from the numerical artefacts whose 
  mitigation will be addressed in this tutorial, the noise in the grid quantities will be caused 
  also by the small number of macro-particles. 
  

----


Preparing the case study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download `this input file <laser_wake_envelope.py>`_ and open it with your
favorite editor.

First, note how we defined variables for physical constants and for conversions
from SI units to normalized units. Specifying a reference length, in this case
the laser wavelength, is important to treat ionization. This information is found
in the ``reference_angular_frequency_SI`` argument in the ``Main`` block.

The laser is initialized via the use of ``LaserEnvelope``
block. The laser envelope will be initialized in the box. The longitudinal
profile of the laser is called ``time_envelope`` in analogy with a standard
laser, but it does not represent a temporal variation during the simulation
as when the laser is injected from a window border, as in the tutorial in 
:doc:`advanced_wakefield_AMcylindrical`. 
To visualize it more easily, think of substituting the time ``t`` with the ``x`` coordinate. 
Thus, the center of the laser profile (i.e. its position at ``t=0``) must be chosen
inside the simulation domain. Note that the focus of the laser can have a longitudinal
position different from the laser center.

We have used the ``"explicit_reduced_dispersion"`` solver for the envelope equation.
For short propagation distances without strong self-focusing (see later in this tutorial)
you can use also the quicker ``"explicit"`` solver. 
However, when long propagation distances or quick envelope evolutions
occur in a plasma we recommend to use ``"explicit_reduced_dispersion"`` to have more accurate results.
In those situations the results using the two solvers can be considerably different.
The stability condition for ``"explicit_reduced_dispersion"`` is more strict, so it is 
possible that you will need a smaller integration timestep to use it.


**Action** Run the simulation and open the results::

  import happi
  S = happi.Open("/example/path/to/the/simulation")


----

Conversion to SI units
^^^^^^^^^^^^^^^^^^^^^^^^

We have specified the ``reference_angular_frequency_SI`` in the ``Main`` block
of our input namelist. Therefore, if you have built ``happi`` with the ``pint`` Python module, 
you should be able to automatically convert the normalized units of the outputs
towards SI units, as will be shown in the commands of this tutorial. 

To do this, while opening the diagnostic you will `specify the units in your plot <https://smileipic.github.io/Smilei/Use/post-processing.html#specifying-units>`_,
e.g. ``units = ["um","GV/m"]``. If ``happi`` was not built with the ``pint`` module 
or if you want to see the results in normalized units, just omit these units
and remember to adjust the ``vmin`` and ``vmax`` of your plot commands.

----

A subtlety: the envelope of the vector potential vs the envelope of the electric field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, let's study the laser propagation. Note the ``MovingWindow`` block and
that the window starts moving since the very first iteration of the simulation.
This allows the simulation domain to constantly shift toward the `x` direction
in order to follow the laser propagation.

Plot the values on the propagation axis of the fields called ``Env_A_abs`` and ``Env_E_abs``,
with the same scale. For this, use the diagnostic ``Fields`` (if the timestep is 
not provided, the last one is plotted by default):: 
  
  Env_A=S.Probe.Probe0("Env_A_abs", label="Env_A")
  Env_E=S.Probe.Probe0("Env_E_abs", label="Env_E")
  happi.multiSlide(Env_A,Env_E)

Here we have used the ``happi`` command ``multiSlide``, that it is analogous to
the command ``multiPlot``, but allows to slide between multiple timesteps.
Note that we have not converted these outputs to SI units, since in laser wakefield 
acceleration the peak normalized field (often called ``a0``) of the laser pulse can give important information
on the wave excitation regime (nonlinear for ``a0 > 1.`` for example, linear for ``a0 << 1.``).

Do you see some differences when the simulation advances?
The complex envelope field used for calculations is the envelope of the vector potential 
:math:`\tilde{A}`. In the diagnostics, you can plot its absolute value through ``Env_A_abs``.
Instead, the field ``Env_E_abs`` is the absolute value of the envelope of the electric field :math:`\tilde{E}`, 
the latter defined to allow comparisons with the field of a standard laser: 
:math:`\tilde{E}=-(\partial_t-ik_0c)\tilde{A}` (see `Smilei's website <https://smileipic.github.io/Smilei/Understand/laser_envelope.html>`_ for the derivation). 
Remember that as explained in the documentation, when the laser
temporal variations are quick, the difference between the two fields will be
sensitive. Both the fields are complex quantities, the `abs` means that their
absolute value is plotted. These quick temporal evolutions can occur during the 
propagation in plasmas.

You can see how the two fields evolve differently in this nonlinear case extracting
the data at all timesteps and computing the peak of the field at each timestep::

  import numpy as np
  import matplotlib.pyplot as plt
  
  dt        = S.namelist.dt
  timesteps = S.Probe.Probe0("Env_E_abs").getAvailableTimesteps()
  
  Env_A_abs = S.Probe.Probe0("Env_A_abs").getData()
  Env_A_abs = np.asarray(Env_A_abs)
  Env_A_abs = np.amax(Env_A_abs,axis=1)
  plt.plot(timesteps*dt,Env_A_abs,label="|Env_A|")
  
  Env_E_abs = S.Probe.Probe0("Env_E_abs").getData()
  Env_E_abs = np.asarray(Env_E_abs)
  Env_E_abs = np.amax(Env_E_abs,axis=1)
  plt.plot(timesteps*dt,Env_E_abs,label="|Env_E|")
  
  plt.ylabel("field peak [normalized units]")
  plt.xlabel("t [normalized units]")
  plt.legend()

In the namelist we have specified a peak value for the field equal to ``a0=1.8``,
and that is the peak value that the laser field in ``Env_E_abs`` would reach in vacuum at the focal plane.
From the previous plot you can see that the laser reaches higher values. 
This is due to relativistic self-focusing that occurs in plasmas when the laser
power exceeds the power threshold for the occurrence of this phenomenon.
The interaction of the plasma on the laser pulse propagation is quantified by the
field ``Env_Chi``, which appears in the `envelope equation <https://smileipic.github.io/Smilei/Understand/laser_envelope.html#the-envelope-equation>`_.

**Action** Visualize in 2D the envelope fields on the plane `xy` through the other ``Probes``
defined in the namelist, e.g.::

  S.Probe.Probe1("Env_E_abs").slide()

----


Wakefield excitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's observe the wakefield formation in the trail of the laser
envelope. Remember that the pusher scheme to use when a laser envelope model is present is
either ``pusher="ponderomotive_boris"`` or ``pusher="ponderomotive_borisBTIS3"``. 

**Action** Check that the defined ``Species`` has a compatible ``pusher`` scheme.

Through the diagnostic ``Probe`` and the option ``animate`` or ``slide``, you can follow
the envelope propagation and plasma evolution during the simulation. As before, you can plot the
absolute value of the envelope ``Env_E_abs``. 

You can also follow the formation of the plasma wave, plotting the electron density ``Rho``. 
To see it more clearly, we recommend the use of the option ``vmax`` in the
``slide()`` or ``plot()`` function, for example::

 S.Probe.Probe1("-Rho",units=["um","pC/cm^3"]).slide(figure=2, vmin=0.,vmax=1.5e12)

Note the formation of a bubble behind the laser, whose borders are full of
electrons and whose interior is emptied (or almost emptied in some regimes) of electrons.
 
The longitudinal electric field on axis, very important for electron
Laser Wakefield Acceleration, can be plotted with the ``Probe`` defined on the propagation axis, 
choosing the field ``Ex`` in your diagnostic::

  S.Probe.Probe0("Ex",units=["um","GV/m"]).slide(figure=3)

Through the function ``multiSlide``, follow the evolution of the envelope and the of
electron density on the axis::

  envelope_E = S.Probe.Probe0("20*Env_E_abs",units=["um"],label="20*Env_E_abs")
  Ex         = S.Probe.Probe0("Ex",label="Ex",units=["um","GV/m"])
  happi.multiSlide(Ex,envelope_E)
  
Note that we have multiplied the laser normalized electric field by 10 in the last command
to have a more readable scale in the plot.

The evolution of both the envelope and the electron density can be studied in 2D at the same time
through the `transparent` argument of the `multiSlide` function. We'll make transparent
all the values of `Env_E_abs` below 1.::

  Rho        = S.Probe.Probe1("-Rho",units=["um","pC/cm^3"],cmap="Blues_r",vmin=0.,vmax=1.5e12)
  Env_E      = S.Probe.Probe1("Env_E_abs",units=["um"],cmap="hot",vmin=0.8,transparent="under")
  happi.multiSlide(Rho,Env_E,xmin=0)

This way you should see the laser pulse envelope and the plasma wave in the electron density.


----

Envelope ionization module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As explained in the tutorial for :doc:`advanced_field_ionization`, to correctly model
tunnel ionization it is essential to specify a reference frequency, which is already 
done in the ``Main`` block of this tutorial's namelist.

Afterwards, you have to specify a ``Species`` that will be ionized, in this case ``"nitrogen5plus"``,
whose ``charge`` state at the start of the simulation is lower than its ``atomic_number``.
Note also that you can keep this ``Species`` frozen and at the same time able to be
ionized. This will avoid spending time in moving macro-particles that do not move too much,
as the nitrogen ions of this laser wakefield simulation set-up.

The new electrons created from the tunnel ionization of this ``Species`` will be 
stored in another ``Species``, specified in ``ionization_electrons`` of ``"nitrogen5plus"``.
In our case this ``Species`` at the start of the simulation has zero macro-particles.
We could have chosen an already populated species of electrons like ``bckgelectron``,
but if you want to keep them separated like in this case it can be useful for diagnostics 
(although it can take more simulation time, due to cache efficiency).

To ionize ``"nitrogen5plus"``, a ``ionization_model`` must be selected in its ``Species``
block. Since we are using a laser envelope model, we must use the ``"tunnel_envelope_averaged"`` model.
Physically tunnel ionization occurs at the peaks of the laser field, but these peaks 
are not part of an envelope model, by definition. 
How can we model tunnel ionization with a laser envelope model then?
The model ``"tunnel_envelope_averaged"`` uses an ADK ionization rate averaged over the
laser oscillations, and a similar averaging is taken into account when the newly created 
electrons are initialized, to correctly recreate their transverse momentum dispersion 
and the drift in their `x` direction from tunnel ionization occurring in relativistic regimes.
More details on this model can be found `here <http://dx.doi.org/10.1103/PhysRevE.102.033204>`_.

**Action** Visualize the density of the electrons created through ionization::

  S.Probe.Probe1("-Rho_electronfromion",units=["um","pC/cm^3"]).slide(figure=2, vmin=0.,vmax=1.5e12)

Run two new simulations, changing the fraction of the nitrogen dopant in the gas mixture,
stored in the variable ``dopant_N_concentration=0.10`` (i.e. ten percent of nitrogen).
Try a value 1.5 times larger and 1.5 times smaller. How does the ``Rho_electronfromion``
change?

**Action** Using the same techniques you have used in the tutorial :doc:`advanced_wakefield_electron_beam`,
try to plot the energy spectrum of the electrons created through ionization.

----

Reducing the effects of Numerical Cherenkov Radiation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As already discussed in this tutorial :doc:`advanced_wakefield_AMcylindrical`,
the use of finite difference solvers for Maxwell's equations introduces a numerical
dispersion, that interacting with relativistic macro-particles will generate 
a numerical artefact called Numerical Cherenkov Radiation. 
In that tutorial two methods are shown to cope with this artefact, one of which is
the B-TIS3 interpolation scheme described in 
`P.-L. Bourgeois and X. Davoine, Journal of Plasma Physics 89 (2023) <https://doi.org/10.1017/S0022377823000223>`_, 
that does not remove the Numerical Cherenkov Radiation, but considerably reduces 
its effects on the macro-particles, with minimal increase of the simulation time.
Now we will see how to use this feature with a laser envelope model.
The tricky part with an envelope model is that this feature works well only when 
the normalized timestep (or ``dt``) is close to the normalized cell length along `x` (or ``dx``), which is
not always compatible with the stability of the envelope solver, expecially 
the ``"explicit_reduced_dispersion"``. Try have at least ``dt>0.9*dx`` to use 
the B-TIS3, but check that the solver results (i.e. the envelope fields) do not
increase exponentially due to a too high ``dt``.

**Action**: Run a new simulation, changing the variable ``use_BTIS3_interpolation`` 
before the ``Main`` block to ``True``. Note how this changes the ``pusher`` 
to ``"ponderomotive_borisBTIS3"`` and adds some fields to the ``Probes`` in the namelist. 
Check how the electron beam shape changes::
  
  S.Probe.Probe1("-Rho",units=["um","pC/cm^3"]).slide(figure=2, vmin=0.,vmax=1.5e12)
  
Afterwards, check this combination of ``Probes``, proportional to the force acting 
on the macro-particles along the `y` direction::
  
  S.Probe.Probe1("Ey-c*BzBTIS3",units=["um","GV/m"]).slide(figure=3,vmin=-20,vmax=20,cmap="seismic")
  
What difference do you observe if you compare it with the equivalent combination 
in the simulation without the B-TIS3 scheme (using ``Bz`` instead of ``BzBTIS3``)?


