Practical 4: Field ionization
=============================

Goal of the tutorial
^^^^^^^^^^^^^^^^^^^^

The goal of this tutorial is 

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^



Content of the tutorial
^^^^^^^^^^^^^^^^^^^^^^^
This tutorial consist in a single directory :program:`Practical3` containing:
 
* `field_ionization_1d.py`: the input file for the simulation.


Setup the tutorial
^^^^^^^^^^^^^^^^^^

* Connect on `Poincare` via `ssh` using the `-X` option:

.. code-block:: bash

    ssh -X poincare

* Copy the content of this tutorial in the `$SCRATCHDIR` of `Poincare`:

.. code-block:: bash

    cp -r Smilei/HandsOn/Practical2 $SCRATCHDIR/.

* Copy the executable files in the new folder:

.. code-block:: bash

    cp -r Smilei/smilei $SCRATCHDIR/Practical3/.
    cp -r Smilei/smilei_test $SCRATCHDIR/Practical3/.

* Go the tutorial directory:

.. code-block:: bash

    cd $SCRATCHDIR/Practical3



Check input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`SMILEI` in test mode:

.. code-block:: bash

    ./smilei_test 2 2 thermal_plasma_1d.py

If your simulation `input file` is correct, you can `submit your first job`.
As a first step, you will do this in `interactive mode`, that is directly running:

.. code-block:: bash

    ./smilei 2 2 thermal_plasma_1d.py

Before going to the analysis of your simulation, check your ``log`` file!


Analysing the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^

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

    S = happi.Open('/gpfsdata/training[01-30]/Practical2/')

.. warning::

    Use your correct `training` identification number!

Having a look at the ``Scalar`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Having a look at the ``Field`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


 
Effect of spatial resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

