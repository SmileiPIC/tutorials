Laser Wakefield Acceleration with Laser Envelope (in 2D)
---------------------------------------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the laser
envelope model with :program:`Smilei`. Before starting with this tutorial, we
recommend to complete first the tutorial on :doc:`advanced_wakefield`. In that
Tutorial, Laser Wakefield Acceleration is simulated in a standard way, i.e. the
laser is defined through its electromagnetic fields defined on the grid.

We also recommend to run the simulations of this tutorial with 1 MPI processes 
(remember to set the number of OpenMP thread as explained in :doc:`basics_setup`).

The following features will be addressed:

* Laser envelope initialization "in the box"
* Initialization of the species interacting with the laser envelope
* Observation of relativistic self-focusing
* Analysis of the grid fields when an envelope is present

.. note::

  This tutorial is done in 2D which is not physically relevant.
  Proper simulation of this kind must be done in 3D.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma. It propagates in
the plasma and creates a non linear plasma wave in its wake.

Preparing the case study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download `this input file <laser_wake_envelope.py>`_ and open it with your
favorite editor.

First, note that the laser is initialized via the use of ``LaserEnvelope``
block. The laser envelope will be initialized in the box. The longitudinal
profile of the laser is called ``time_envelope`` in analogy with a standard
laser, but it does not represent a temporal variation. To visualize it more
easily, think of substituting the time ``t`` with the ``x`` coordinate. Thus,
the center of the laser profile (i.e. its position at ``t=0``) must be chosen
inside the simulation domain. Note that the focus of the laser can have a longitudinal
position different from the laser center.

.. note::

  Reflective boundary conditions are chosen in all directions for the laser
  envelope, since for the moment absorbing boundary conditions are not available.

The particles ``Species`` interacting with the envelope need a flag
``ponderomotive_dynamics=True`` (normally ``False`` by default). The pusher
scheme that takes into account the envelope effect on the particles is called
``pusher="ponderomotive_boris"``. Check that the defined ``Species`` has the
right ``ponderomotive_dynamics`` flag and the right ``pusher`` scheme.

After these checks, run the simulation and import the results::

  import happi
  S = happi.Open("/path/to/the/simulation")

A subtlety: the envelope of the vector potential vs the envelope of the electric field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, let's study the laser propagation. Note the ``MovingWindow`` block and
that the window starts moving since the very first iteration of the simulation.
This allows the simulation domain to constantly shift toward the `x` direction
in order to follow the laser propagation.

Plot the values on the grid of the fields called ``Env_A_abs`` and ``Env_E_abs``,
with the same scale. For this, use the diagnostic ``Fields`` (if the timestep is 
not provided, the last one is plotted by default):: 
  
  S.Field.Field0("Env_A_abs").plot(figure=1, vmin = 0., vmax = 2.7)

and

  S.Field.Field0("Env_E_abs").plot(figure=2, vmin = 0., vmax = 2.7)

Do you see some differences?
The complex envelope field used for calculations is the envelope of the vector potential 
:math:`\tilde{A}`. In the diagnostics, you can plot its absolute value through ``Env_A_abs``.
The field ``Env_E_abs`` is the absolute value of the envelope of the electric field :math:`\tilde{E}`, 
the latter defined to allow comparisons with the field of a standard laser: 
:math:`\tilde{E}=-(\partial_t-ik_0c\tilde{A})`. 
Remember that as explained in the documentation, when the laser
temporal variations are quick, the difference between the two fields will be
sensitive. Both the fields are complex quantities, the `abs` means that their
absolute value is plotted.

You can see how the two fields evolve differently in this nonliner case through then
diagnostic ``Scalar``.
Through this diagnostic, you can plot the evolution of ``Env_E_absMax`` over time::

  S.Scalar("Env_E_absMax").plot(figure=1)

The ``Max`` after the name of the field means that the maximum of that field on 
the grid at each timestep will be plotted. You can see that after a brief diffraction 
in vacuum, the value of ``Env_E_absMax`` is increasing over time due to relativistic 
self-focusing and then starts to decrease again due to laser diffraction. 

To plot the evolution of the maximum of the absolute value of the envelope 
(of the vector potential) on the grid, you can use::

  S.Scalar("Env_A_absMax").plot(figure=2)

To plot them in the same figure, you can use the command ``multiPlot`` of ``happi``::

  env_E = S.Scalar("Env_E_absMax")
  env_A = S.Scalar("Env_A_absMax")
  happi.multiPlot(env_E,env_A)

You can see through their maximum value that initially the two fields are equal in vacuum. 
Then, when the self-focusing starts, the temporal variations of the envelope are not negligible 
and the two fields start to differ.

Wakefield excitation
^^^^^^^^^^^^^^^^^^^^^^^^

Now we are interested in the wakefield formation in the trail of the laser
envelope.

Through the diagnostic ``Fields`` and the option ``animate``, you can follow
the envelope propagation during the simulation. As before, you can plot the
absolute value of the envelope ``Env_E_abs``. Although the envelope represents
a laser pulse, you won't see the laser oscillations at wavelength
:math:`\lambda_0`. In the language of signal processing, with this model the
laser is represented through the complex envelope of the vector potential
component in the polarization direction. Indeed, the aim of the envelope model
is to simulate laser-plasma interaction without needing to resolve these high
frequency oscillations. This way, larger longitudinal grid sizes ``dx`` and
timesteps ``dt`` can be used, to considerably reduce the simulation time.

Through the diagnostic ``Fields`` and the option ``animate``, you can follow
the formation of the wakefield, plotting the electron density ``Rho``. To see
it more clearly, we recommend the use of the option ``vmax`` in the
``animate()`` or ``plot()`` function, for example::

 S.Field.Field0("-Rho").animate(figure=2, vmax=0.01)

Note the formation of a bubble behind the laser, whose borders are full of
electrons and whose interior is emptied of electrons. A diagnostic of type
``Probe`` is defined to see the values of some grid fields on the propagation
axis. The longitudinal electric field on axis, very important for electron
Laser Wakefield Acceleration, can be plotted in this way, choosing the field
``Ex`` in your diagnostic::

  S.Probe.Probe0("Ex").plot(figure=3)

Through the function ``animate``, follow the evolution of the envelope and the
electron density on the axis. 

Parametric study of self-focusing and wakefield excitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's try to change the laser and plasma parameters to see how self the 
self-focusing and the wake excitation change.

Try to repeat the simulation with different values of `a0` (the envelope initial peak value) 
and `n0` (the plasma plateau density). What changes in the process of
self-focusing? Try the values :math:`0.01`, :math:`0.1`, :math:`2.` for `a0`
and :math:`0.003`, :math:`0.005` for `n0`. Use the ``Scalar`` diagnostics to study the 
evolution of ``Env_E_absMax``.

Set the values of `a0` and `n0` to their original value (:math:`2.4`
and :math:`0.002` respectively) and rerun the simulation. Now try to relaunch 
the simulation with different values of `a0` (like :math:`0.01`, :math:`0.1`, 
:math:`2.`). What happens to the waveform of ``Ex`` on the propagation axis? 
And how changes the electron density on the 2D grid? Use the ``Probe`` and ``Field`` 
diagnostics to study the changes in ``Ex`` and ``Rho``.
