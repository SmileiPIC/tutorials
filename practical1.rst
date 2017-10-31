Practical 1: Laser Propagation in a vacuum
================================================================================

Goal of the tutorial
--------------------

The goal of this tutorial is to run your first simulation with :program:`Smilei`.
The following points will be addressed:

* How to prepare an input file: toto the ``Main`` block, a ``Laser`` block, and turn on some diagnostics (in particular ``Scalars``, ``Fields`` and ``Probes``),
* How to check your input file using the ``test mode``, and how to spot ``ERROR`` and ``WARNING`` messages.
* How to access your simulation results and use the :program:`happi` Python Package for post-processing (in particular using the ``plot``, ``animate`` and ``saveAs`` tools),
* get familiar with the `Courant-Friedrich-Lewy` (CFL) condition.

Physical configuration
----------------------

A Gaussian (in both space and time) laser pulse enters in the simulation box from the ``xmin`` side, 
and propagates through the box.

Content of the tutorial
-----------------------

This tutorial consist in a single directory :program:`Practical1` containing:
 
* `laser_propagation.py`: the input file for the simulation.

Setup the tutorial
------------------

* Copy the content of this tutorial in your `$SCRATCHDIR`, and go to this new folder:

.. code-block:: bash

    cp -r Smilei/HandsOn/Practical1 $SCRATCHDIR
    cd $SCRATCHDIR/Practical1

* Copy the executable files in the new folder:

.. code-block:: bash

    cp -r ~/Smilei/smilei .
    cp -r ~/Smilei/smilei_test .


Checking your input file in test mode
-------------------------------------

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`SMILEI` in test mode:

.. code-block:: bash

    ./smilei_test laser_propagation.py


This ``test_mode`` does the same initialization as the normal mode but does not enter the PIC loop. 
It provides you with a ``log`` (what appears on your screen).
What does this ``log`` tells you? Do you spot any ``ERROR`` message?

If you did spot an ``ERROR``, can you correct it? If so, correct it, and try again!

Once you have no more ``ERROR`` message. Do you get ``WARNING`` messages?



Running the simulation
----------------------

Once your simulation `input file` is correct, you can `submit your first job`.
As a first step, you will do this in :ref:`interactive mode`, that is directly running:

.. code-block:: bash

   llinteractif 2 clallmds+ 3
   [interactive] mpirun -np 16 ./smilei laser_propagation.py

Before going to the analysis of your simulation, check your ``log`` file.

* What did change compared to the `test mode`?
* Did your run complete correctly?
* Check what output files have been generated: what are they?



Preparing the post-processing tool
----------------------------------

Let's now turn to analysing the output of your run with the :program:`happi` Python post-processing package.
To do so, open a new terminal window & login again (via ssh) to your machine.

Then, install the python module happi

.. code-block:: bash
   
   cd Smilei
   make happi
   cd ..

Start ipython

.. code-block:: bash
    
    ipython

Get basic info on the simulation
--------------------------------

Import the happi module:

.. code-block:: python

   In [1]: import happi
    
Open the simulation:

.. code-block:: python

   In [2]: S=happi.Open("/gpfsdata/training[01-30]/Practical1/")
   
.. warning::

  Use the correct path to the simulation folder.
  You can run ``echo $SCRATCHDIR`` to obtain the full path to your scratchdir.

See what is available from the simulation:

.. code-block:: python

   In [4]: S.namelist.  # then press <tab>


Obtain the laser profile
------------------------

Get the Laser block from the namelist:

.. code-block:: python
   
   In [5]: laser = S.namelist.Laser[0]
   
   In [6]: laser

Note that the ``laser`` is an object of type ``<Smilei Laser>``.

See what is available in this laser object:

.. code-block:: python

   In [7]: laser.  # then press <tab>
   
   In [8]: laser.time_envelope

Note that this quantity is a python function: what function is it?
Some help is available `here <http://www.maisondelasimulation.fr/smilei/namelist.html#profiles>`_.

Plot the laser profile
----------------------

To plot the laser profile as a function of time, a list of times is necessary.
In the following, we use the package *numpy* to generate a list of times from 0 to
the end of the simulation, separated by the timestep.

.. code-block:: python

   In [9]: import numpy as np, matplotlib.pyplot as plt
   In [10]: tstop = S.namelist.Main.simulation_time
   In [11]: tstep = S.namelist.Main.timestep
   In [12]: times = np.arange(0., tstop, tstep)

Plot the profile using the usual *matplotlib* package:

.. code-block:: python

   In [13]: laser_profile = [laser.time_envelope(t) for t in times]
   In [14]: plt.plot( times, laser_profile )

Check laser using Scalar
------------------------

Obtain a list of Scalar diagnostics:

.. code-block:: python

   In [15]: S.Scalar. # then press <tab>

Open the Uelm scalar and plot:

.. code-block:: python

   In [16]: diag = S.Scalar.Uelm()
   In [17]: diag.plot()


More ``Scalar`` diagnostics
---------------------------

Check the evolution of the ``total energy`` in the simulation box:

.. code-block:: python

    In [18]: S.Scalar('Utot').plot()

Check the evolution of the ``energy balance`` in the simulation box:

.. code-block:: python

    In [18]: S.Scalar('Ubal').plot()


Plot laser using Field
---------------------------

Open the Ey field and plot:

.. code-block:: python

   In [18]: diag = S.Field.Field0("Ey")
   In [19]: diag.animate(vmin=-1, vmax=1, cmap="smileiD")

Open the field with an average, and compare to the previous profile.
The following calculates the laser amplitude envelope using ``"(2.*(Ex**2+Ey**2))**(0.5)"``.
Then, using the argument ``average``, it makes an average of this envelope for x
close to 0 and y around 105.

.. code-block:: python

   In [20]: S.Field.Field0("(2.*(Ex**2+Ey**2))**(0.5)", average={"x":[0,5],"y":[100,110]}).plot()

Overlay the previous plot of the laser profile and compare

.. code-block:: python

   In [21]: plt.plot( times, laser_profile )


Testing the CFL condition
---------------------------

Now change the `input file` and increase the time-step e.g. using: ... to be continued