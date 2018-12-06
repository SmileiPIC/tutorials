Tutorial 1: Laser Propagation in vacuum
------------------------------------------

The goal of this tutorial is to run your first simulation with :program:`Smilei`.
The following points will be addressed:

* How to prepare an input file
* How to check your input file using the ``test mode``
* How to access your simulation results
* Get familiar with the `Courant-Friedrich-Lewy` (CFL) condition.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

Download the input file `laser_propagation_2d.py <laser_propagation_2d.py>`_.
Note that this file is written in the *python* language.

Read through this file and try to understand the contents of the ``Main(...)`` and
``LaserGaussian2D(...)`` blocks. You can obtain details on the meaning of all keywords
in this `documentation page <https://smileipic.github.io/Smilei/namelist.html>`_.
Note that all units are normalized according to
`these conventions <https://smileipic.github.io/Smilei/units.html>`_.

A Gaussian (in both space and time) laser pulse enters in the simulation box from
the ``xmin`` side and propagates through the box.

----

Setup the tutorial
^^^^^^^^^^^^^^^^^^

As explained in the :ref:`setup page <runsimulation>`, you should make a new directory
to run your simulation. This directory should contain the input file that you just downloaded
and the executables ``smilei`` and ``smilei_test``.


----

Checking your input file in test mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`Smilei` in test mode:

.. code-block:: bash

    ./smilei_test laser_propagation_2d.py


This *test mode* does the same initialization as the normal mode but does not enter the PIC loop. 
It provides you with a *log* (what appears on your screen).
What does this *log* tells you? Do you spot any ``ERROR`` message?

If you did spot an ``ERROR``, can you correct it? If so, correct it, and try again!

Once you have no more ``ERROR`` message. Do you get ``WARNING`` messages?



----

Running the simulation
^^^^^^^^^^^^^^^^^^^^^^

Once your simulation `input file` is correct, you can
:ref:`run the simulation <runsimulation>`.

.. code-block:: bash

  ./smilei laser_propagation_2d.py

Before going to the analysis of your simulation, check the ``log``.

* What did change compared to the `test mode`?
* Did your run complete correctly?
* Check what output files have been generated: what are they?



----

Preparing the post-processing tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's now turn to analysing the output of your run with the python post-processing
package :program:`happi`.
To do so, **open a new terminal window**, then install :program:`happi`:

.. code-block:: bash
   
   cd /path/to/Smilei
   make happi       # this is needed only once on a given computer

Start *ipython*:

.. code-block:: bash
    
    ipython

----

Get basic info on the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From *ipython*, import the happi module:

.. code-block:: python

   import happi

Open the simulation that you have just run:

.. code-block:: python

   S=happi.Open("/path/to/the/simulation")

.. warning::

  Use the correct path to the simulation folder.

See what is available from the simulation:

.. code-block:: python

   S.namelist.  # then press <tab>

When pressing ``<tab>``, *ipython* display the content of the simulation.
You can explore all these items. They should all be exactly the same as the ones
that were defined earlier in the namelist ``laser_propagation_2d.py``.

----

Check laser using ``Scalar``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Read the namelist again and spot the line where the ``Scalar`` diagnostic has been defined.
You may get more information on this diagnostic
`on this page <http://www.maisondelasimulation.fr/smilei/namelist.html#scalar-diagnostics>`_.

Obtain a list of ``Scalar`` diagnostics:

.. code-block:: python

   S.Scalar()

Open the ``Uelm`` scalar and plot:

.. code-block:: python

   diag = S.Scalar('Uelm')
   diag.plot()

This scalar represents the electromagnetic energy in the box. The plot we just obtained
should represent its evolution with time.

----

More ``Scalar`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check the evolution of the ``total energy`` in the simulation box:

.. code-block:: python

    S.Scalar('Utot').plot()

Check the evolution of the ``energy balance`` in the simulation box:

.. code-block:: python

    S.Scalar('Ubal').plot()


----

Plot laser using ``Field``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Read the namelist again and spot the line where the ``Field`` diagnostic has been defined.

Open the ``Ey`` field and plot:

.. code-block:: python

   diag = S.Field(0, "Ey")
   diag.animate(vmin=-1, vmax=1, cmap="smileiD")

This new function ``animate()`` can animate the plot of any diagnostic when several
timesteps are available.

Now, open the field with an average, and compare to the previous profile.
The following calculates the laser amplitude envelope using ``"Ey**2+Ez**2"``.
Then, using the argument ``average``, it makes an average of this envelope for x
close to 0 and y at 100.

.. code-block:: python

   S.Field(0, "Ey**2+Ez**2", average={"x":[0,7],"y":100}).plot()


----

Compare the laser profile with the theory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are going to overlay the previous plot of the laser profile with
the theoretical laser profile.

Get the ``Laser`` block from the namelist:

.. code-block:: python
   
   laser = S.namelist.Laser[0]
   
   laser

Note that the ``laser`` is an object of type ``<Smilei Laser>``.

See what is available in this laser object:

.. code-block:: python

   laser.  # then press <tab>
           # This should display all info on the laser
   
   laser.time_envelope

Note that this quantity is a python function: what function is it?
Some help is available `here <http://www.maisondelasimulation.fr/smilei/namelist.html#profiles>`_.

To plot the laser profile as a function of time, a list of times is necessary.
In the following, we use the package *numpy* to generate a list of times from 0 to
the end of the simulation, separated by the timestep.

.. code-block:: python

   from numpy import array, arange
   tstop = S.namelist.Main.simulation_time # simulation final time
   tstep = S.namelist.Main.timestep        # simulation timestep
   times = np.arange(0., tstop, tstep)

You may type ``times`` in order to see what is the list of times that we have created.

Now, we execute the ``laser.time_envelope`` function on each of the times that we just created.
We obtain a list of values of the laser envelope corresponding to each time.

.. code-block:: python

   laser_profile = array([laser.time_envelope(t) for t in times])

Plot the profile using the *matplotlib* package:

.. code-block:: python

   %pylab
   plot( times+5, laser_profile**2 / 2 )

----

Testing the CFL condition
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now change the `input file` and increase the time-step e.g. using :math:`\Delta t = 0.95\,\Delta x`.

Re-run :program:`Smilei` and check the total energy and/or energy balance.

What is going on?
