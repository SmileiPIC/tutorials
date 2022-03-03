Units
================================================

The goal of this tutorial is to familiarize with the use of physical units in ``Smilei``.

This tutorial will allow you to:

* get familiar with the units of the input namelist
* postprocess the results displaying units of your choice

This tutorial requires the installation of the `pint` Python package.

----

What units are used by the code?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usually, physics codes work with normalized units to simplify the equations and reduce the number
of multiplications.

For the electromagnetic PIC method, the system given by Maxwell's and Vlasov's equations
can be easily written in normalized `units <https://smileipic.github.io/Smilei/units.html>`_,
normalizing speeds by :math:`c`, masses by the electron mass :math:`m_e` and charges
by the unit charge :math:`e`.
However, there are is natural length or time normalization in this system of equations.
To complete the normalization, one must choose a reference length :math:`L_r`, or equivalently
a reference time :math:`T_r`, or equivalently a reference angular frequency :math:`\omega_r`.
In the following, we choose :math:`\omega_r` as our normalization quantity (:math:`L_r` and
:math:`T_r` are deduced from :math:`\omega_r`).

Importantly, it is not even necessary to choose a value for this last normalization.
Indeed, it automatically cancels out, so that the system of equations does not depend on
:math:`\omega_r`. This means that the result of the simulation is true for any value of
:math:`\omega_r`! That is why is it usually not necessary to set a value to :math:`\omega_r`
in the simulation input file.

In practice, we always know our problem in terms of real-world units, but in Smilei's
input file, all quantities must be normalized.

1. Choose :math:`\omega_r` as one important frequency of your problem (i.e. laser frequency,
   plasma frequency, ...)
2. Deduce other reference quantities such as :math:`L_r` and :math:`T_r` 
3. The parameters in the input file should be normalized accordingly

During post-processing, you will obtain results in terms of normalized quantities, 
but :program:`happi` gives you the possibility to convert to units of your choice.


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

Download the input file `radiation_pressure_2d.py <radiation_pressure_2d.py>`_.

In this simulation, a slab of pre-ionized overdense plasma of uniform density :math:`n_0`
is irradiated by a high-intensity laser pulse, triggering electron and ion expansion.

----

Check input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`Smilei` in test mode:

.. code-block:: bash

    ./smilei_test radiation_pressure_2d.py

Take some time to study the namelist, in particular how the physical parameters
have been defined. For the moment you can ignore the lines of code marked with ``Choice 2``
at the start of the namelist.

----

Normalized units in the input namelist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The blocks of the input namelist will accept only quantities in normalized units.
As mentioned before, choosing a reference length/time/angular frequency yields 
conversion factors for all physical units involved in a PIC simulation. 
For more details, see the `units <https://smileipic.github.io/Smilei/units.html>`_
page in the documentation.

Therefore, if you are accustomed to work with normalized units, you can directly 
put your physical set-up's parameters in the input namelist in normalized units.
We will call this ``Choice 1`` in the following and in the input namelist.
The use of SI units will be called ``Choice 2`` and will be explored in the last section 
of this tutorial.

The provided input file already has ``Choice 1`` implemented in the namelist 
(see the initial part of the file). As you can see reading the namelist,
most of the simulation parameters can be defined starting from the definition 
of the laser wavelength, which will be also our reference wavelength.
This can be seen in the ``LaserGaussian2D`` block, where the ``Laser`` 's angular frequency 
``omega`` in normalized units is 1, i.e. equal to our reference angular frequency.

With this choice of normalization:

* a length of :math:`2\pi` corresponds to a laser wavelength,
* a time interval :math:`2\pi` corresponds to an optical cycle of the laser,
* the reference density corresponds to the laser critical density :math:`n_c=\varepsilon_0 m_e \omega^2/e^2`.

.. note:: In other set-ups you may want to choose the reference length equal to the Debye length,
  or the plasma electron wave frequency, etc. In this case, if a ``Laser`` is present,
  remember to redefine the ``omega`` in the ``Laser`` block accordingly.

.. note:: Some reference quantities do not change with the choice of reference length/time,
  e.g. the electron charge will be :math:`-1`, the electron mass will be :math:`1`, since the 
  reference charge and mass in our normalized units are those of the electron. 
  Also, the reference energy and speed are :math:`m_ec^2` and `c`, independently of the choice for
  the reference length/time.

**Question**: if we wanted a laser with frequency equal to two times the reference frequency,
what would be the value of `omega` in the `Laser` block?

**Question**: for a reference length of :math:`L_r=0.8` µm what would be 
the reference density? See its definition `here <https://smileipic.github.io/Smilei/units.html>`_
(you may use the constants in the module ``scipy.constants``).
It is equal to :math:`L_r^{-3}`?

.. warning::

  As you have seen, in this namelist there is no need to specify a reference angular frequency 
  or a reference length in SI units. However, when using advanced physical operators like
  ionization, collisions, multiphoton Breit Wheeler pair generation, radiation emission 
  you will have to do it (see related tutorials and the ``Main`` block of their namelists).
  This happens because these operators represent an extension of the basic Vlasov-Maxwell system of
  PIC codes, and are not invariant under the described normalization.


----

Units in the postprocessing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's study the results, without specifying a conversion::

  import happi; S_normalized = happi.Open('/path/to/your/simulation')

If we plot the laser transverse field on the propagation axis, we can verify
that indeed a length of :math:`2\pi` corresponds to the laser wavelength::
  
  S_normalized.Probe.Probe0("Ey").slide()

Now, what if we wanted our results in physical units, e.g. SI units? While opening the output with happi,
we can specify a reference angular frequency in SI. In this case, we can choose it from 
the laser wavelength::

  import scipy.constants
  laser_wavelength_um = 0.8
  c                   = scipy.constants.c     # Lightspeed, m/s
  omega_r_SI          = 2*math.pi*c/(laser_wavelength_um*1e-6)
  S_SI = happi.Open('/path/to/your/simulation', reference_angular_frequency_SI=omega_r_SI)

This allows ``happi`` to make the necessary conversions for our scale of interest.
Then, we have to specify the units we want in our plot::

  S_SI.Probe.Probe0("Ey", units=['um','fs','GV/m']).slide(figure=2)

**Question**: Does the peak transverse field of the laser correspond to the one in normalized units
at the same timestep and in the namelist? Compute first the reference electric field as explained `here <https://smileipic.github.io/Smilei/units.html>`_
and check the conversion to GV/m.

**Action**: Similarly, try to plot the kinetic energy ``Ukin`` from the ``Scalar`` diagnostic
and the evolution of the electron density ``Rho_eon`` from the ``Field`` diagnostic
in normalized and physical units.  

**Note**: Other systems of units can be used, e.g. CGS, or different combinations of units, including ``inches``, ``feet``.
For more details, see `here <https://smileipic.github.io/Smilei/post-processing.html#specifying-units>`_.

----

SI units in the input namelist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer to work with physical units, e.g. SI units, the use of Python for the input namelist 
allows to easily convert our inputs in SI units to normalized inputs required by
the code. In the namelist there is a way to do it, marked with ``Choice 2`` 
and commented for the moment

**Action**: Comment the two lines marked with the comment ``Choice 1`` in the input namelist.
Uncomment the lines marked with ``Choice 2`` and take some time to read them.

As you can see, first we use the ``scipy.constants`` module to define some useful physical constants,
e.g. the speed of light. Then, we define the reference length, from which we derive some variables useful
for the conversions.
With these variables, it is easy to have the necessary quantities in normalized units and vice-versa::

  length_normalized_units = length_SI / L_r

**Question**: Near the ``Laser`` block, a variable ``E_r`` is defined, representing the reference
electric field. Using this variable, can you convert the normalized peak electric field of the laser ``a0``
to TV/m? Similarly, can you convert the plasma density ``n0`` to :math:`\textrm{cm}^{-3}`? Note that instead of
defining the density as in the namelist we could have just used::

  density_normalized_units = n0_SI / N_r