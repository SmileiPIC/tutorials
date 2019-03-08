Electron Laser Wakefield Acceleration (in Azimuthal Modes cylindrical geometry)
------------------------------------------------------------------------------

The goal of this tutorial is to give an introduction to Laser Wakefield acceleration simulation with :program:`Smilei`.
The following feature will be addressed:

* The analysis of the grid fields in AM cylindrical geometry

The simulation used for this tutorial is relatively heavy so make sure to submit the job on 160 cores at least.


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^^^

An ultra high intensity laser enters an under dense plasma.
It propagates in the plasma and creates a non linear plasma wave in its wake.
Electrons from the plasma are eventually trapped in this wave and accelerated to high energies.

Step by step tutorial
^^^^^^^^^^^^^^^^^^^^^^^^

Download  `this input file <laser_wake_AM.py>`_ and open it with your favorite editor and run the simulation.
Then, open the results::

  import happi
  S = happi.Open("/path/to/the/simulation") 

Now let's have a look at the grid fields, for example the electron density::

  S.Field.Field0("-Rho",theta = 0.).plot(figure=1, vmin = 0., vmax = 0.03)

Note that we have specified a certain angle 'theta = 0.' (i.e. the demi-plane including the positive 'y' coordinates).

By default, this command will plot the last timestep available. You can also plot a specific timestep::
  
  S.Field.Field0("-Rho",timesteps=1000.,theta=0.).plot(figure=1, vmin = 0., vmax = 0.03)

Note that no azimuthal mode is specified. Thus, by default, the reconstruction of the modes is performed.
In this simulation (see namelist), only two modes are present.
To plot a specific mode (in this case the mode '0'), you can use::

  S.Field.Field0("-Rho",timesteps=1000.,theta=0.,modes=0).plot(figure=1, vmin = 0., vmax = 0.03)

The main azimuthal mode of the plasma wave in the wake of the laser is the mode 0.
The azimuthal mode of the laser is the mode '1'. 
To see its transverse field, we can plot the mode 1 of the transverse electric field (i.e. 'Er')::

  S.Field.Field0("Er",timesteps=1000.,theta=0.,modes=1).plot(figure=2)

The mode '0' will be instead the main mode of the electric field of the plasma wave::
  
  S.Field.Field0("Er",timesteps=1000.,theta=0.,modes=0).plot(figure=3)

Plot also the longitudinal electric field ('El') of the laser (mode '1') and of the wake (mode '0')::

  S.Field.Field0("El",timesteps=1000.,theta=0.,modes=1).plot(figure=4)
  S.Field.Field0("El",timesteps=1000.,theta=0.,modes=0).plot(figure=5)

Or, you can plot the sum of the two, performing the reconstruction of the modes::

  S.Field.Field0("El",timesteps=1000.,theta=0.).plot(figure=5)

You can follow the evolution of any grid quantity (for example here the electron density) through the command 'animate()'::

  S.Field.Field0("-Rho",timesteps=1000.,theta=0.,modes=0).animate(figure=1, vmin = 0., vmax = 0.03)