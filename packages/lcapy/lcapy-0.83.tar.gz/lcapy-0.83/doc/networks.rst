.. _networks:

========
Networks
========

Lcapy supports one-port and two-port networks. 



One-port networks
=================

One-port networks are creating by combining one-port components in
series or parallel, for example, here's an example of resistors in
series

   >>> from lcapy import R
   >>> R1 = R(10)
   >>> R2 = R(5)
   >>> Rtot = R1 + R2
   >>> Rtot
   R(10) + R(5)

Here `R(10)` creates a 10 ohm resistor and this is assigned to the
variable `R1`.  Similarly, `R(5)` creates a 5 ohm resistor and this is
assigned to the variable `R2`.  `Rtot` is the name of the network
formed by connecting `R1` and `R2` in series.  

   >>> Rtot.draw()

.. image:: examples/networks/rseries.png
   :width: 4cm


Network components
------------------           

- `C` capacitor

- `CPE` constant phase element
  
- `Damper` mechanical damper

- `FeriteBead` ferrite bead (lossy inductor)

- `G` conductance  

- `I` arbitrary current source

- `i` arbitrary time-domain current source        

- `Iac` ac current source (default angular frequency :math:`\omega_0`)
  
- `Idc` dc current source

- `Inoise` noise current source            
  
- `Istep` step current source

- `L` inductor  

- `Mass` mass

- `O` open-circuit

- `R` resistor

- `Spring` spring

- `sV` s-domain voltage source

- `sI` s-domain current source

- `V` arbitrary voltage source

- `v` arbitrary time-domain voltage source    

- `Vac` ac voltage source (default angular frequency :math:`\omega_0`)
  
- `Vdc` dc voltage source

- `Vnoise` noise voltage source        
  
- `Vstep` step voltage source    

- `Xtal` crystal
  
- `W` wire

- `Y` generalized admittance

- `Z` generalized impedance      

  
.. _network_attributes:
           
Network attributes
------------------

Each network oneport has a number of attributes, including:

- `Voc` transform-domain open-circuit voltage

- `Isc` transform-domain short-circuit current

- `I` transform-domain current through network terminals (zero by definition)

- `voc` t-domain open-circuit voltage

- `isc` t-domain short-circuit current

- `isc` t-domain current through network terminals (zero by definition)

- `B` susceptance

- `G` conductance    
  
- `R` resistance

- `X` reactance
  
- `Y` admittance

- `Z` impedance

- `Ys` s-domain generalized admittance    

- `Zs` s-domain generalized impedance

- `y` t-domain impulse response of admittance

- `z` t-domain impulse response of impedance

- `is_dc` DC network

- `is_ac` AC network

- `is_ivp` initial value problem

- `is_causal` causal response


Here's an example:

   >>> from lcapy import R, V
   >>> n = V(20) + R(10)
   >>> n.Voc
   20
   ──
    s 
   >>> n.voc
   20
   >>> n.Isc
   2
   ─
   s
   >>> n.isc
   2
   >>> n.Z
   10
   >>> n.Y
   1/10

.. image:: examples/networks/VRseries.png
   :width: 4cm


.. _network_methods:
           
Network methods
---------------

- `circuit()` create a Circuit object from the network.

- `describe()` print a message describing how network is solved.

- `draw()` draw the schematic.

- `netlist()` create an equivalent netlist.


Network functions
-----------------

- `series()` connect one-port components in series.  This is similar to `Ser()` but is robust to `None` components and single components in series.

- `parallel()` connect one-port components in parallel.  This is similar to `Par()` but is robust to `None` components and single components in parallel.

- `ladder()` connect one-port components as a one-port ladder network.  This is an alternating sequence of series and parallel connections.   For example,

   >>> ladder(R(1), C(2), R(3))
   R(1) + (C(1) | R(3))

   >>> ladder(None, C(2), R(3), C(3))
   C(2) | (R(3) + C(3))
  
  

Network simplification
----------------------

A network can be simplified (if possible) using the `simplify` method.
For example, here's an example of a parallel combination of resistors.
Note that the parallel operator is `|` instead of the usual `||`.

   >>> from lcapy import *
   >>> Rtot = R(10) | R(5)
   >>> Rtot
   R(10) | R(5)
   >>> Rtot.simplify()
   R(10/3)

The result can be performed symbolically, for example,

   >>> from lcapy import *
   >>> Rtot = R('R_1') | R('R_2')
   >>> Rtot
   R(R_1) | R(R_2)
   >>> Rtot.simplify()
   R(R_1*R_2/(R_1 + R_2))
   >>> Rtot.simplify()
   R(R₁) | R(R₂)

Here's another example using inductors in series

   >>> from lcapy import *
   >>> L1 = L(10)
   >>> L2 = L(5)
   >>> Ltot = L1 + L2
   >>> Ltot
   L(10) + L(5)
   >>> Ltot.simplify()
   L(15)

Finally, here's an example of a parallel combination of capacitors

   >>> from lcapy import *
   >>> Ctot = C(10) | C(5)
   >>> Ctot
   C(10) | C(5)
   >>> Ctot.simplify()
   C(15)


Norton and Thevenin transformations
-----------------------------------

A Norton or Thevenin equivalent network can be created using the
`norton` or `thevenin` methods.  For example,

   >>> from lcapy import Vdc, R
   >>> a = Vdc(1) + R(2)
   >>> a.norton()
   G(1/2) | Idc(1/2)


Network schematics
==================

Networks are drawn with the `draw()` method.  Here's an example:

   >>> from lcapy import R, C, L
   >>> ((R(1) + L(2)) | C(3)).draw()

Here's the result:

.. image:: examples/networks/pickup.png
   :width: 5cm

By default, one port networks are drawn with a horizontal layout.
This can be changed to a vertical layout or as a ladder layout using the
`form` argument to the `draw()` method.

Here's an example of a vertical layout,

   >>> from lcapy import R, C, L
   >>> ((R(1) + L(2)) | C(3)).draw(form='vertical')

.. image:: examples/networks/pickupv.png
   :width: 2.2cm

Here's an example of a network drawn with ladder layout,

   >>> from lcapy import R, C
   >>> n = C('C1') | (R('R1') + (C('C2') | (R('R2') + (C('C3') | (R('R3') + C('C4'))))))
   >>> n.draw(form='ladder')


.. image:: examples/networks/ladderRC3.png
   :width: 6cm
           

The s-domain model can be drawn using:

   >>> from lcapy import R, C, L
   >>> ((R(1) + L(2)) | C(3)).s_model().draw()

This produces:

.. image:: examples/networks/pickup-s.png
   :width: 5cm

Internally, Lcapy converts the network to a netlist and then draws the
netlist.  The netlist can be found using the netlist method, for example,

   >>> from lcapy import R, C, L
   >>> print(((R(1) + L(2)) | C(3)).netlist())

yields::

   W 1 2; right=0.5
   W 2 4; up=0.4
   W 3 5; up=0.4
   R1 4 6 1; right
   W 6 7; right=0.5
   L1 7 5 2; right
   W 2 8; down=0.4
   W 3 9; down=0.4
   C1 8 9 3; right
   W 3 0; right=0.5


To create a schematic with multiple components in parallel, use `Par`.
For example,

.. literalinclude:: examples/networks/par3.py


.. image:: examples/networks/par3.png
   :width: 3cm


Network synthesis
=================

Networks can be created using network synthesis techniques given an impedance or admittance expression,
for example,

    >>> Z = impedance(4*s**2 + 3 * s + 1 / 6) / (s**2 + 2 * s / 3)
    >>> Z.network()
    ((C(1) + R(2)) | C(3)) + R(4)
    >>> Z.network().Z(s).canonical()
    
    :math:`\frac{4 s^{2} + 3 s + \frac{1}{6}}{s^{2} + \frac{2 s}{3}}`

For more details, see :ref:`network-synthesis`.

           
Random networks
===============

Networks can be randomly generated with the `random_network` function.  This is useful for automated exam question generation.   Here's an example:

   >>> from lcapy import random_network
   >>> net = random_network(num_resistors=4, num_capacitors=0, num_inductors=0, num_voltage_sources=2, kind='dc')

This example generates a DC network with four resistors, two-voltage sources, and no capacitors or inductors.   The `kind` argument can be `ac`, `dc`, or `transient`.   The number of parallel connections can be specified with the `num_parallel` argument.

           

Network analysis examples
=========================


Series R-C network
------------------


.. literalinclude:: examples/networks/series-RC1-Z.py


.. image:: examples/networks/series-RC1-Z.png
   :width: 15cm


.. literalinclude:: examples/networks/series-VRC1-isc.py

.. image:: examples/networks/series-VRC1-isc.png
   :width: 15cm



Series R-L network
------------------


.. literalinclude:: examples/networks/series-RL1-Z.py


.. image:: examples/networks/series-RL1-Z.png
   :width: 15cm


.. literalinclude:: examples/networks/series-VRL1-isc.py

.. image:: examples/networks/series-VRL1-isc.png
   :width: 15cm


Series R-L-C network
--------------------


.. literalinclude:: examples/networks/series-RLC3-Z.py


.. image:: examples/networks/series-RLC3-Z.png
   :width: 15cm


.. literalinclude:: examples/networks/series-VRLC1-isc.py

.. image:: examples/networks/series-VRLC1-isc.png
   :width: 15cm




Parallel R-L-C network
----------------------


.. literalinclude:: examples/networks/parallel-RLC3-Z.py


.. image:: examples/networks/parallel-RLC3-Z.png
   :width: 15cm


.. literalinclude:: examples/networks/parallel-IRLC1-voc.py

.. image:: examples/networks/parallel-IRLC1-voc.png
   :width: 15cm



Two-port network parameters
===========================

Lcapy describes two-port networks in the Laplace domain using A, B, G,
H, S, T, Y, and Z matrices.  These are defined in the following sections.
Note, for some network configurations some of these matrices can be
singular.


.. image:: examples/schematics/twoport1.png
   :width: 12cm


Each matrix has methods for converting to the other parameterisations, for example,

>>> A = AMatrix.generic()

.. math::

    \left[\begin{matrix}A_{11} & A_{12}\\A_{21} & A_{22}\end{matrix}\right]

>>> A.Zparams    

.. math::
   
    \left[\begin{matrix}\frac{A_{11}}{A_{21}} & \frac{A_{11} A_{22} - A_{12} A_{21}}{A_{21}}\\\frac{1}{A_{21}} & \frac{A_{22}}{A_{21}}\end{matrix}\right]

The elements can be accessed by name, for example:

>>> A.S11

.. math::

   \frac{A_{12} - A_{21} Z_{0}^{2} + Z_{0} \left(A_{11} - A_{22}\right)}{A_{12} + A_{21} Z_{0}^{2} + Z_{0} \left(A_{11} + A_{22}\right)}

Note, in this example, the A-parameters are converted to S-parameters.


Each parameterisation has the following attributes:

`is_bilateral`: True if the two-port is bilateral

`is_buffered`: True if the two-port is buffered, i.e., any load on the output has no affect on the input

`is_reciprocal`: True if the  two-port is reciprocal

`is_series`: True if the two-port is a series network

`is_shunt`: True if the two-port is a shunt network

`is_symmetrical`: True if the two-port is symmetrical


.. _A-parameters:

A-parameters (ABCD)
-------------------

.. math::

    \left[\begin{matrix}V_{1}\\I_{1}\end{matrix}\right] = \left[\begin{matrix}A_{11} & A_{12}\\A_{21} & A_{22}\end{matrix}\right] \left[\begin{matrix}V_{2}\\- I_{2}\end{matrix}\right]

The A matrix is the inverse of the B matrix.            


.. _B-parameters:

B-parameters (inverse ABCD)
---------------------------

.. math::

    \left[\begin{matrix}V_{2}\\I_{2}\end{matrix}\right] = \left[\begin{matrix}B_{11} & B_{12}\\B_{21} & B_{22}\end{matrix}\right] \left[\begin{matrix}V_{1}\\- I_{1}\end{matrix}\right]

The B matrix is the inverse of the A matrix.    


.. _G-parameters:

G-parameters (inverse hybrid)
-----------------------------

.. math::

    \left[\begin{matrix}I_{1}\\V_{2}\end{matrix}\right] = \left[\begin{matrix}G_{11} & G_{12}\\G_{21} & G_{22}\end{matrix}\right] \left[\begin{matrix}V_{1}\\I_{2}\end{matrix}\right]

The G matrix is the inverse of the H matrix.        


.. _H-parameters:

H-parameters (hybrid)
---------------------

.. math::

    \left[\begin{matrix}V_{1}\\I_{2}\end{matrix}\right] = \left[\begin{matrix}H_{11} & H_{12}\\H_{21} & H_{22}\end{matrix}\right] \left[\begin{matrix}I_{1}\\V_{2}\end{matrix}\right]
   
The H matrix is the inverse of the G matrix.    


.. _S-parameters:

S-parameters (scattering)
-------------------------

.. math::
   
    \left[\begin{matrix}b_{1}\\b_{2}\end{matrix}\right] = \left[\begin{matrix}S_{11} & S_{12}\\S_{21} & S_{22}\end{matrix}\right] \left[\begin{matrix}a_{1}\\a_{2}\end{matrix}\right]


.. _T-parameters:

T-parameters (scattering transfer)
----------------------------------

.. math::
   
    \left[\begin{matrix}b_{1}\\a_{1}\end{matrix}\right] = \left[\begin{matrix}T_{11} & T_{12}\\T_{21} & T_{22}\end{matrix}\right] \left[\begin{matrix}a_{2}\\b_{2}\end{matrix}\right]


.. _Y-parameters:

Y-parameters (admittance)
-------------------------

.. math::    

    \left[\begin{matrix}I_{1}\\I_{2}\end{matrix}\right] = \left[\begin{matrix}Y_{11} & Y_{12}\\Y_{21} & Y_{22}\end{matrix}\right] \left[\begin{matrix}V_{1}\\V_{2}\end{matrix}\right]

The Y matrix is the inverse of the Z matrix.           


.. _Z-parameters:

Z-parameters (impedance)
------------------------

.. math::

   \left[\begin{matrix}V_{1}\\V_{2}\end{matrix}\right] = \left[\begin{matrix}Z_{11} & Z_{12}\\Z_{21} & Z_{22}\end{matrix}\right] \left[\begin{matrix}I_{1}\\I_{2}\end{matrix}\right]

The Z matrix is the inverse of the Y matrix.       
