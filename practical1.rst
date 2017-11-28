Practical 1: Laser Propagation in a vacuum
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

First, remember to set the number of threads per processor to the number you intend:

.. code-block:: bash

  export OMP_NUM_THREADS=8

To run the simulation, typically, you will use the following command in a
job submission file, or in an interactive mode, or maybe directly on your terminal.

.. code-block:: bash

   cd /path/to/my/simulation
   mpirun -n 8 ./smilei laser_propagation_2d.py

Before going to the analysis of your simulation, check your ``log`` file.

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
   make happi

Start *ipython*:

.. code-block:: bash
    
    ipython

----

Get basic info on the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From *ipython*, import the happi module:

.. code-block:: python

   In [1]: import happi

Open the simulation that you have just run:

.. code-block:: python

   In [2]: S=happi.Open("/path/to/the/simulation")

.. warning::

  Use the correct path to the simulation folder.

See what is available from the simulation:

.. code-block:: python

   In [4]: S.namelist.  # then press <tab>

When pressing ``<tab>``, *ipython* display the content of the simulation.
You can explore all these items. They should all be exactly the same as the ones
that were defined earlier in the namelist ``laser_propagation_2d.py``.

----

Obtain the laser profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get the ``Laser`` block from the namelist:

.. code-block:: python
   
   In [5]: laser = S.namelist.Laser[0]
   
   In [6]: laser

Note that the ``laser`` is an object of type ``<Smilei Laser>``.

See what is available in this laser object:

.. code-block:: python

   In [7]: laser.  # then press <tab>
                   # This should display all info on the laser
   
   In [8]: laser.time_envelope

Note that this quantity is a python function: what function is it?
Some help is available `here <http://www.maisondelasimulation.fr/smilei/namelist.html#profiles>`_.

----

Plot the laser profile
^^^^^^^^^^^^^^^^^^^^^^

To plot the laser profile as a function of time, a list of times is necessary.
In the following, we use the package *numpy* to generate a list of times from 0 to
the end of the simulation, separated by the timestep.

.. code-block:: python

   In [9]: import numpy as np
   In [10]: tstop = S.namelist.Main.simulation_time # simulation end
   In [11]: tstep = S.namelist.Main.timestep        # simuation timestep
   In [12]: times = np.arange(0., tstop, tstep)

You may type ``times`` in order to see what is the list of times that we have created.

Now, we execute the laser time envelope function on each of this times that we just created.
We this obtain a list of values of the laser envelope corresponding to each time.

.. code-block:: python

   In [13]: laser_profile = [laser.time_envelope(t) for t in times]

Plot the profile using the usual *matplotlib* package:

.. code-block:: python

   In [14]: import matplotlib.pyplot as plt
   In [15]: %matplotlib
   In [16]: plt.plot( times, laser_profile )

----

Check laser using Scalar
^^^^^^^^^^^^^^^^^^^^^^^^^

Read the namelist again and spot the line where the ``Scalar`` diagnostic has been defined.
You may get more information on this diagnostic
`on this page <http://www.maisondelasimulation.fr/smilei/namelist.html#scalar-diagnostics>`_.

Obtain a list of ``Scalar`` diagnostics:

.. code-block:: python

   In [17]: S.Scalar. # then press <tab>

Open the ``Uelm`` scalar and plot:

.. code-block:: python

   In [18]: diag = S.Scalar('Uelm')
   In [19]: diag.plot()

This scalar represents the electromagnetic energy in the box. The plot we just obtained
should represent its evolution with time. Note that we used a different type of ``plot()``
than previously. This one corresponds to the utility from the ``happi`` package that
prepares plots specifically for `Smilei`
(`more info here <http://www.maisondelasimulation.fr/smilei/post-processing.html#plot-the-data-at-one-timestep>`_).


----

More ``Scalar`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check the evolution of the ``total energy`` in the simulation box:

.. code-block:: python

    In [20]: S.Scalar('Utot').plot()

Check the evolution of the ``energy balance`` in the simulation box:

.. code-block:: python

    In [21]: S.Scalar('Ubal').plot()


----

Plot laser using Field
^^^^^^^^^^^^^^^^^^^^^^

Read the namelist again and spot the line where the ``Field`` diagnostic has been defined.

Open the ``Ey`` field and plot:

.. code-block:: python

   In [22]: diag = S.Field.Field0("Ey")
   In [23]: diag.animate(vmin=-1, vmax=1, cmap="smileiD")

This new function ``animate()`` can animate the plot of any diagnostic when several
timesteps are available.

Now, open the field with an average, and compare to the previous profile.
The following calculates the laser amplitude envelope using ``"(2.*(Ex**2+Ey**2))**(0.5)"``.
Then, using the argument ``average``, it makes an average of this envelope for x
close to 0 and y around 200.

.. code-block:: python

   In [24]: S.Field.Field0("2*(Ex**2+Ey**2)**0.5", average={"x":[0,5],"y":[190,210]}).plot()

Overlay the previous plot of the laser profile and compare

.. code-block:: python

   In [25]: plt.plot( times, laser_profile )


----

Testing the CFL condition
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now change the `input file` and increase the time-step e.g. using :math:`\Delta t = 0.95\,\Delta x`.

Re-run :program:`Smilei` and check the total energy and/or energy balance.

What is going on?