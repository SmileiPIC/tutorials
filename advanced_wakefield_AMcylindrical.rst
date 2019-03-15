Azimuthal-mode-decomposition cylindrical geometry
------------------------------------------------------

The goal of this tutorial is to give an introduction to the use of the cylindrical geometry 
with azimuthal Fourier decomposition in :program:`Smilei`.
The following feature will be addressed:

* The analysis of the grid fields in AM cylindrical geometry

The simulation used for this tutorial is relatively heavy so make sure to submit the job on 160 cores at least.


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma. 
The laser is linearly polarized in the ``y`` direction.
It propagates in the plasma and creates a non linear plasma wave in its wake.
Electrons from the plasma are eventually trapped in this wave and accelerated to high energies.


.. note::

  You will see that the plasma does not fill all the simulation window. 
  This is because we want to include the laser electromagnetic field in the window, but the plasma particles creating the plasma oscillations
  are only those radially near to the laser pulse. Plasma particles at greater radial distances would not contribute to the relevant physics, but they would 
  require additional computational time. Thus we can omit them to perform the simulation more quickly without losing relevant phenomena.

----


Step by step tutorial
^^^^^^^^^^^^^^^^^^^^^^^^

Download  `this input file <laser_wake_AM.py>`_ and open it with your favorite editor and run the simulation.
Then, open the results::

  import happi
  S = happi.Open("/path/to/the/simulation") 

Now let's have a look at the grid fields, for example the electron density::

  S.Field.Field0("-Rho",theta = 0.).plot(figure=1, vmin = 0., vmax = 0.01)

In the previous command we have specified a certain angle ``theta = 0.`` (i.e. the demi-plane including the positive ``y`` coordinates).

By default, this command will plot the last timestep available. You can also plot a specific timestep::
  
  S.Field.Field0("-Rho",timesteps=6000.,theta=0.).plot(figure=1, vmin = 0., vmax = 0.01)

In the last command no azimuthal mode was specified. By default, if no mode is specified the reconstruction with all the modes is performed.
In this simulation (see namelist), only two modes are present.
To plot a specific mode (in this case the mode ``0``), you can use::

  S.Field.Field0("-Rho",theta=0.,modes=0).plot(figure=1, vmin = 0., vmax = 0.01)

The main azimuthal mode of the plasma wave in the wake of the laser is the mode 0.
This time we specified that mode in the plot command.

The azimuthal mode of the laser is the mode ``1``. 
To see the transverse field of the laser, we can plot the mode ``1`` of 
the transverse electric field (i.e. ``Er``)::

  S.Field.Field0("Er",theta=0.,modes=1).plot(figure=2)

On ``theta=0.`` it will correspond ``Ey`` with our choice of laser polarization.

You can plot the reconstruction of the whole longitudinal electric 
field (laser and wake fields, modes ``1`` and ``0`` respectively) through::

  S.Field.Field0("El",theta=0.).plot(figure=4)

You can also follow the evolution of any grid quantity (for example here the electron density) through the command ``animate()``::

  S.Field.Field0("-Rho",theta=0.,modes=0).animate(figure=1, vmin = 0., vmax = 0.01)

.. note::

  The moving window in the namelist has been set to contain the laser and the first wake period in the simulation window.