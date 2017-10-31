Advanced Practical 4: Binary collisions and impact ionization
-------------------------------------------------------------

Smilei includes binary collisions between various species, which can also generate
ionization when one of the species is ions and the other one electrons.
`Smilei's website <http://www.maisondelasimulation.fr/smilei/collisions.html>`_
already gives a description of the approach, and provides results from various benchmarks.

The list of benchmarks, located in the ``benchmarks/collisions/`` folder is briefly
described below. You may run any of these benchmarks depending on your interests.

Beam relaxation
^^^^^^^^^^^^^^^

An electron beam encounters a thermal ion population; *e-i* collisions slow the beam down
and make it spread. Various electron velocities and ion charges are considered. For each
case, the ratios of weights between electrons and ions is varied.

.. rubric:: 1.  initial velocity = 0.05, ion charge = 1

| ``beam_relaxation1.py``
| ``beam_relaxation2.py``
| ``beam_relaxation3.py``
| Analysis and plotting provided in ``beam_relaxation123.py``

.. rubric:: 2.  initial velocity = 0.01, ion charge = 1

| ``beam_relaxation4.py``
| ``beam_relaxation5.py``
| ``beam_relaxation6.py``
| Analysis and plotting provided in ``beam_relaxation456.py``

.. rubric:: 3.  initial velocity = 0.01, ion charge = 3

| ``beam_relaxation7.py``
| ``beam_relaxation8.py``
| ``beam_relaxation9.py``
| Analysis and plotting provided in ``beam_relaxation789.py``


Thermalization
^^^^^^^^^^^^^^

Thermal electrons start with a different temperature from that of ions.
The thermalization due to *e-i* collisions is monitored for three different weight ratios.

| ``thermalisation_ei1.py``
| ``thermalisation_ei2.py``
| ``thermalisation_ei3.py``
| Analysis and plotting provided in ``thermalisation_ei123.py``


Temperature isotropization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Non-isotropic thermal electrons are isotropized with *e-e* collisions.

| ``temperature_isotropization1.py``
| Analysis and plotting provided in ``temperature_isotropization.py``


Maxwellianization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An electron population starting with a rectangular velocity distribution becomes
maxwellian due to *e-e* collisions.

| ``Maxwellianization1.py``
| Analysis and plotting provided in ``Maxwellianization.py``


Stopping power
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *e-e* slowing rate of test electrons passing through an electron plasma is monitored
*vs.* time and compared to a theoretical stopping power.

| ``Stopping_power1.py`` : projectiles from 10 to 30 keV
| ``Stopping_power2.py`` : projectiles from 100 to 300 keV
| ``Stopping_power3.py`` : projectiles from 1 to 10 MeV
| Analysis and plotting provided in ``Stopping_power123.py``


Conductivity
^^^^^^^^^^^^

An electric field applied to solid-density Cu generates an electron current. The maximum
electron velocity, due to *e-i* collisions, relates to the conductivity, which is
compared to theoretical values.

.. warning::
  
  This benchmark requires review

| ``conductivity1.py`` : temperature from 1 to 10 eV
| ``conductivity2.py`` : temperature from 20 to 100 eV
| ``conductivity3.py`` : temperature from 300 to 1000 eV
| Analysis and plotting provided in ``conductivity.py``


Ionization rate
^^^^^^^^^^^^^^^

Drifting electrons in a cold Al plasma cause *e-i* impact ionization at a rate compared
to theoretical values. The three inputs below correspond to various weight ratios
between electrons and ions.

| ``ionization_rate1.py``
| ``ionization_rate2.py``
| ``ionization_rate3.py``
| Analysis and plotting provided in ``ionization_rate.py``


Inelastic stopping power
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ionizing *e-i* slowing rate of test electrons passing through an Al plasma
is monitored *vs.* time and compared to a theoretical stopping power.

| ``ionization_stopping_power1.py`` : measurement for electrons at various energies

| ``ionization_stopping_power2.py`` : 
| ``ionization_stopping_power3.py`` : three examples to show the stopping dynamics
| ``ionization_stopping_power4.py`` : 

| Analysis and plotting provided in ``ionization_stopping_power.py``


Multiple ionization
^^^^^^^^^^^^^^^^^^^

The capability to ionize several times in one timestep is illustrated for five different
materials. For each material, two cases are provided: the first is well resolved, while
the second has a low time resolution requiring multiple ionization.

| ``ionization_multipleC1.py``
| ``ionization_multipleC2.py``
| ``ionization_multipleAl1.py``
| ``ionization_multipleAl2.py``
| ``ionization_multipleZn1.py``
| ``ionization_multipleZn2.py``
| ``ionization_multipleSn1.py``
| ``ionization_multipleSn2.py``
| ``ionization_multipleAu1.py``
| ``ionization_multipleAu2.py``
| Analysis and plotting provided in ``ionization_multiple.py``


Effect of neglecting recombination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As recombination is not accounted for, we can expect excess ionization to occur
indefinitely without being balanced to equilibrium. For picosecond laser interaction,
we illustrate here that the recombination rate can be neglected, thus providing
reasonable ionization state *vs.* temperature, in various materials.

| ``ionization_equilibriumH.py``
| ``ionization_equilibriumAl.py``
| ``ionization_equilibriumZn.py``
| ``ionization_equilibriumAu.py``
| Analysis and plotting provided in ``ionization_equilibrium.py``


