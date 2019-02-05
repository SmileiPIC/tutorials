Laser Wakefield Acceleration with Laser Envelope (in 2D)
---------------------------------------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the laser envelope model with :program:`Smilei`.
Before starting with this tutorial, we recommend to complete first the tutorial on Laser Wakefield Acceleration (without envelope).
In that Tutorial, Laser Wakefield Acceleration is simulated in a standard way, i.e. the laser is defined through its electromagnetic fields defined on the grid. 

The following features will be addressed:

* Laser envelope initialization "in the box"
* Initialization of the species interacting with the laser envelope
* Observe relativistic self-focusing through a DiagScalar on the envelope fields
* Analysis of the grid fields when an envelope is present

Disclaimer: This tutorial is done in 2D which is not physically relevant. Proper simulation of this kind must be done in 3D.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma.
It propagates in the plasma and creates a non linear plasma wave in its wake.

Step by step tutorial
^^^^^^^^^^^^^^^^^^^^^^^^

Download  `this input file <laser_wake_envelope.py>`_ and open it with your favorite editor. 

First, note that the laser is initialized via the use of ``LaserEnvelope`` block. 
The laser envelope will be initialized in the box. 
The longitudinal profile of the laser is called ``time_envelope`` in analogy with a standard laser, but it does not represent a temporal variation.
To visualize it more easily, think of substituting the time ``t`` with the ``x`` coordinate. 
Thus, the center of the laser profile (i.e. its position at ``t=0``) must be chosen inside the window. 
Note that the focus of the laser can have a longitudinal position different from the laser center. 

Reflective boundary conditions are chosen in all directions for the laser envelope, since for the moment absorbing boundary conditions are not available.

The particles ``Species`` interacting with the envelope need a flag ``ponderomotive_dynamics=True`` (normally ``False`` by default). 
The pusher scheme that takes into account the envelope effect on the particles is called ``pusher="ponderomotive_boris"``.
Check that the defined ``Species`` has the right ``ponderomotive_dynamics`` flag and the right ``pusher`` scheme.

After these checks, run the simulation and import the results:

``import happi ; S = happi.Open(".")``

First, let's study the laser propagation.
Note the ``MovingWindow`` block and that the window starts moving since the very first iteration of the simulation.
This allows the simulation domain to constantly shifts toward the `x` direction in order to follow the laser propagation.

To follow the laser propagation, the diagnostic ``Scalar`` can be used to plot the evolution of ``Env_E_abs`` over time:

``S.Scalar("Env_E_absMax").plot(figure=1)`` 

This field is the envelope of the electric field, and it is defined to allow comparisons with the field of a standard laser.
The envelope field used for calculations is the envelope of the vector potential ``A``. 
With the ``Scalar`` diagnostic, you can plot also the absolute value of the envelope field, ``Env_A_abs``.  
Remember that as explained in the documentation, when the laser temporal variations are quick, the difference between the two fields will be sensitive.
Both the fields are complex quantities, the `abs` means that their absolute value is plotted.

You can see that after a brief diffraction in vacuum, the value of ``Env_E_abs`` is increasing over time due to relativistic self-focusing and then starts to decrease again due to laser diffraction. 
Try to repeat the simulation with different values of `a0` (the envelope initial peak value) and `n0` (the plasma plateau density).
What changes in the process of self-focusing? Try the values :math:`0.01`, :math:`0.1`, :math:`2.` for `a0` and :math:`0.003`, :math:`0.005` for `n0`.

Now we are interested in the wakefield formation in the trail of the laser envelope. 
Set the values of `a0` and `n0` to their original value (:math:`2.4` and :math:`0.002` respectively) and rerun the simulation.

Through the diagnostic ``Fields`` and the option ``animate``, you can follow the envelope propagation during the simulation. 
As before, you can plot the absolute value of the envelope ``Env_E_abs``. 
Although the envelope represents a laser pulse, you won't see the laser oscillations at wavelength :math:`lambda_0`. 
In the language of signal processing, with this model the laser is represented through the complex envelope of the vector potential component in the polarization direction. 
Indeed, the aim of the envelope model is to simulate laser-plasma interaction without needing to resolve these high frequency oscillations.
This way, larger longitudinal grid sizes ``dx`` and timesteps ``dt`` can be used, to considerably reduce the simulation time.

Through the diagnostic ``Fields`` and the option ``animate``, you can follow the formation of the wakefield, plotting the electron density ``Rho``.
To see it more clearly, we recommend the use of the option ``vmax`` in the ``animate()`` or ``plot()`` function, for example:

``S.Field.Field0("-Rho").animate(figure=2, vmax=0.01)``

Note the formation of a bubble behind the laser, whose borders are full of electrons and whose interior is emptied of electrons.
A diagnostic of type ``Probe`` is defined to see the values of some grid fields on the propagation axis. 
The longitudinal electric field on axis, very important for electron Laser Wakefield Acceleration, can be plotted in this way, choosing the field ``Ex`` in your diagnostic:

``S.Probe.Probe0("Ex").plot(figure=3)``  

Through the function ``animate``, follow the evolution of the envelope and the electron density on the axis. 
Try to relaunch the simulation with different values of `a0` (like :math:`0.01`, :math:`0.1`, :math:`2.`). 
What happens to the waveform of ``Ex`` on the propagation axis? And how changes the electron density on the 2D grid?






