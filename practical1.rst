Practical 1: Laser Propagation in a vacuum
================================================================================

Presentation
--------------------------------------------------------------------------------

Goal of the tutorial
^^^^^^^^^^^^^^^^^^^^

The goal of this tutorial is to run your first simulation with :program:`Smilei`.
The following points will be addressed:

* How to prepare an input file: toto the ``Main`` block, a ``Laser`` block, and turn on some diagnostics (in particular ``Scalars``, ``Fields`` and ``Probes``),
* How to check your input file using the ``test mode``, and how to spot ``ERROR`` and ``WARNING`` messages.
* How to access your simulation results and use the :program:`Happi` Python Package for post-processing (in particular using the ``plot``, ``animate`` and ``saveAs`` tools),
* get familiar with the `Courant-Friedrich-Lewy` (CFL) condition.

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

A Gaussian (in both space and time) laser pulse enters in the simulation box from the ``xmin`` side, 
and propagates through the box.

Content of the tutorial
^^^^^^^^^^^^^^^^^^^^^^^
This tutorial consist in a single directory :program:`Practical1` containing:
 
* `laser_propagation.py`: the input file for the simulation.

Setup the tutorial
^^^^^^^^^^^^^^^^^^

* Connect on `Poincare` via `ssh` using the `-X` option:

.. code-block:: bash

    ssh -X poincare

* Copy the content of this tutorial in the `$SCRATCHDIR` of `Poincare`:

.. code-block:: bash

    cp -r Smilei/HandsOn/Practical1 $SCRATCHDIR/.

* Copy the executable files in the new folder:

.. code-block:: bash

    cp -r Smilei/smilei $SCRATCHDIR/Practical1/.
    cp -r Smilei/smilei_test $SCRATCHDIR/Practical1/.

* Go the tutorial directory:

.. code-block:: bash

    cd $SCRATCHDIR/Practical1



Checking your input file in test mode
-------------------------------------

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`SMILEI` in test mode:

.. code-block:: bash

    ./smilei_test 2 2 laser_propagation.py


This ``test_mode`` does the same initialization as the normal mode but does not enter the PIC loop. 
It provides you with a ``log`` (what appears on your screen).
What does this ``log`` tells you? Do you spot any ``ERROR`` message?

If you did spot an ``ERROR``, can you correct it? If so, correct it, and try again!

Once you have no more ``ERROR`` message. Do you get ``WARNING`` messages?



Running the simulation
----------------------

Once your simulation `input file` is correct, you can `submit your first job`.
As a first step, you will do this in `interactive mode`, that is directly running:

.. code-block:: bash

    ./smilei 2 2 laser_propagation.py

Before going to the analysis of your simulation, check your ``log`` file.

* What did change compared to the `test mode`?
* Did your run complete correctly?


Analysing the simulation
------------------------

Preparing the post-processing tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, check what output files have been generated: what are they?

Let's now turn to analysing the output of your run with :program:`Happi` Python post-processing package.
To do so, open an ``ipython`` session:

.. code-block:: bash

    ipython

In the python session:

* import the :program:`Happi` package:

.. code-block:: python

    import happi

* open your simulation:

.. code-block:: python

    S = happi.Open('/gpfsdata/training[01-30]/Practical1/')

.. warning::

    Use your correct `training` identification number!

Having a look at the ``Scalar`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* check the evolution of the ``total energy`` in the simulation box:

.. code-block:: python

    S.Scalar('Utot').plot()

* check the evolution of the ``energy balance`` in the simulation box:

.. code-block:: python

    S.Scalar('Ubal').plot()

Having a look at the ``Field`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* use the ``animate`` function to show you the temporal evolution of the fields:

.. code-block:: python

    S.Field(0,'Ey').animate(vmin=-1,vmax=1,cmap='RdBu')
 
Testing the CFL condition
^^^^^^^^^^^^^^^^^^^^^^^^^

Now change the `input file` and increase the time-step e.g. using :math:`\Delta t = 0.95\,\Delta x`.

Re-run :program:`Smilei` and check the total energy and/or energy balance.

What is going on?