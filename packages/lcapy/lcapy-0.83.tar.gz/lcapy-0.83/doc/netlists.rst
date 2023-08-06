.. _netlist:
.. _netlists:

========
Netlists
========

Lcapy circuits are described using a netlist of interconnected components (see :ref:`component-specification`).  Each line of a netlist describes a component using a Spice-like syntax.


Circuits
========

A circuit (or network) can be created by loading a netlist from a file or by
dynamically adding nets.  For example,

   >>> cct = Circuit('circuit.sch')

or

   >>> cct = Circuit()
   >>> cct.add('R1 1 2')
   >>> cct.add('L1 2 3')

or
   
   >>> cct = Circuit()
   >>> cct.add("""
   >>> R1 1 2
   >>> L1 2 3
   >>> """)

or
   
   >>> cct = Circuit("""
   >>> R1 1 2
   >>> L1 2 3
   >>> """)

This last version requires more than one net otherwise it is interpreted as a filename.   
   

A Node object is obtained from a Circuit object using indexing notation, for example:

   >>> cct[2]

A Component object is obtained from a Circuit object using member notation, for example:

   >>> cct.R1


.. _component-specification:

Component specification
-----------------------

Each line in a netlist describes a single component, with the 
general form:

    `component-name positive-node negative-node arg1 [arg2 etc.]`

If no args are specified then the component value is assigned a
symbolic name specified by `component-name`. 

Arguments containing delimiters (space, tab, comma, left bracket,
right bracket) can be escaped with brackets or double quotes.  For
example:

   `V1 1 0 {cos(5 * t)}`

The component type is specified by the first letter(s) of the
`component-name`.  For example, the following line defines a voltage
source called V1 connected btween nodes 1 and 0::

   V1 1 0

Here's another example defining a resistor R between nodes 1 and 2::

   R 1 2
  

Here's a list of the known components that can be used for circuit
simulation (additional components can be drawn, see
:ref:`schematic-components`):
   
- Arbitrary voltage source:

   `Vname Np Nm Vexpr`

   For example,

   `V1 1 0`  This is equivalent to `V1 1 0 {v1(t)}`

   `V1 1 0 10`  This is a DC source of 10 V
  
   `V1 1 0 {2 * cos(5 * t)}` This is an AC source
  
   `V1 1 0 {2 * cos(5 * t) * u(t)}`  This is a transient source

   `V1 1 0 {10 / s}` This is a transient source defined in the s-domain

   `V1 1 0 {s * 0 + 10}`  This is a transient source defined in the s-domain, equivalent to `V1 1 0 s 10`

- DC voltage source of voltage V:

   `Vname Np Nm dc V`

- AC voltage source of complex voltage amplitude V and phase p (radians) with default angular frequency :math:`\omega_0`

   `Vname Np Nm ac V p`

- AC voltage source of complex voltage amplitude V and phase p (radians) with angular frequency :math:`w`

   `Vname Np Nm ac V p w`  

- Step voltage source of amplitude V

   `Vname Np Nm step V`

- s-domain voltage source of complex amplitude V

   `Vname Np Nm s V`  
   
- Arbitrary current source:

   `Iname Np Nm Iexpr`

   `I1 1 0`  This is equivalent to `I1 1 0 {i1(t)}`

   `I1 1 0 10`  This is a DC source of 10 A
  
   `I1 1 0 {2 * cos(5 * t)}` This is an AC source
  
   `I1 1 0 {2 * cos(5 * t) * u(t)}`  This is a transient source

   `I1 1 0 {10 / s}` This is a transient source defined in the s-domain

   `I1 1 0 {s * 0 + 10}`  This is a transient source defined in the s-domain, equivalent to `I1 1 0 s 10`

- DC current source of current I:

   `Iname Np Nm dc I`

- AC current source of complex current amplitude I and phase p (radians) with default angular frequency :math:`\omega_0`

   `Iname Np Nm ac I p`

- AC current source of complex current amplitude I and phase p (radians) with angular frequency :math:`w`

   `Iname Np Nm ac I p w`

- Step current source of amplitude I

   `Iname Np Nm step I`

- s-domain current source of complex current I

   `Iname Np Nm s I`

- Resistor of resistance R:

   `Rname Np Nm R`

- Conductor of conductance G:

   `Gname Np Nm G`

- Inductor of inductance L:

   `Lname Np Nm L`

   `Lname Np Nm L i0`

   Here `i0` is the initial current through the inductor.  If this is specified then the circuit is solved as an initial value problem.

- Capacitor of capacitance C:

   `Cname Np Nm C`

   `Cname Np Nm C v0`

   Here `v0` is the initial voltage across the capacitor.  If this is specified then the circuit is solved as an initial value problem.

- Wire:

   `Wname Np Nm`

   Note, if name is not specified, a unique name is chosen.

- Open circuit:

   `Oname Np Nm`

   Note, if name is not specified, a unique name is chosen.

- Port:

   `Pname Np Nm`

   This acts like an open-circuit; it is useful for schematics.

- Voltage-controlled voltage source (VCVS) of voltage gain E with controlling nodes Nip and Nim:

   `Ename Np Nm Nip Nim E`

- Opamp of differential gain Ad and common-mode gain Ac (default 0) with controlling nodes Nip and Nim.   The common-mode voltage is with respect to node Nm:

   `Ename Np Nm opamp Nip Nim Ad Ac`    

- Current-controlled current source (CCVS) of current gain F.  The control current is defined as the current flowing through the voltage source Vcontrol.

   `Fname Np Nm Vcontrol F`
   
- Voltage-controlled current source (VCCS) of transadmittance G with controlling nodes Nip and Nim:

   `Gname Np Nm Nip Nim G`

- Current-controlled voltage source (VCCS) of transimpedance H.  The control current is defined as the current flowing through the voltage source Vcontrol.

   `Hname Np Nm Vcontrol H`   

- Ideal transformer of turns ratio a:

   `TFname Np Nm Nip Nim a`

- Ideal gyrator of gyration resistance R:

   `GYname Np Nm Nip Nim R`  

- Mechanical spring:

   `kname Np Nm k`

   `kname Np Nm k u0` Here `u0` is the initial speed.  If this is specified then the circuit is solved as an initial value problem.


- Mechanical mass:

   `mname Np Nm m`

   `mname Np Nm m f0` Here `f0` is the initial force.  If this is specified then the circuit is solved as an initial value problem.


- Mechanical damper:

   `rname Np Nm r`
   
   
Np denotes the positive node; Np denotes the negative node.  For
two-port devices, Nip denotes the positive input node and Nim denotes
the negative input node.  Note, positive current flows from
`positive-node` to `negative-node`.  Node names can be numeric or
symbolic.  The ground node is designated `0`.

If the value is not explicitly specified, the component name is used.
For example,

   `C1 1 0` is equivalent to `C1 1 0 C1`


Circuit attributes
------------------

A circuit is comprised of a collection of Nodes and a collection of
circuit elements (Components).  For example,

   >>> cct = Circuit("""
   ... V1 1 0 {u(t)}
   ... R1 1 2
   ... L1 2 0""")
   >>> cct
   V1 1 0 {u(t)}
   R1 1 2
   L1 2 0

   >>> cct.R1
   R1 1 2

   

Circuit methods
---------------

`admittance(Np, Nm)` returns the driving-point admittance between nodes `Np` and `Nm`.

`impedance(Np, Nm)` returns the driving-point impedance between nodes `Np` and `Nm`.

The above methods can be called with a component name, for example,

   >>> a.admittance('L1')

This calculates the driving-point admittance that would be measured across the nodes of `L1`.

`in_parallel()` returns a list of sets of component names that are connected in parallel.

`in_series()` returns a list of sets of component names that are connected in series.

`subs(subs_dict)` substitutes arguments in the Circuit use a dictionary of symbols `subs_dict`.  For example,

   >>> cct = Circuit("""
   ... V1 1 0 Vs}
   ... R1 1 2
   ... L1 2 0""")
   >>> cct2 = cct.subs({'R1': 2, 'L1': 3})
   >>> cct2
   V1 1 0 Vs
   R1 1 2 2
   L1 2 0 3

`transfer(N1p, N1m, N2p, N2m)` returns the s-domain transfer function
`V2(s) / V1(s)`, between the ports defined by nodes `N1p`, `N1m`,
`N2p`, and `N2m` where `V1 = V[N1p] - V[N1m]` and `V2 = V[N2p] -
V[N2m]`.

`Aparams(N1p, N1m, N2p, N2m)` returns the two-port A-parameters matrix for the
two-port defined by nodes `N1p`, `N1m`, `N2p`, and `N2m`, where `I1`
is the current flowing into `N1p` and out of `N1m`, `I2` is the
current flowing into `N2p` and out of `N2m`, `V1 = V[N1p] - V[N1m]`,
and `V2 = V[N2p] - V[N2m]`.   See :ref:`A-parameters`.

`Bparams(N1p, N1m, N2p, N2m)` returns the two-port B-parameters matrix.  See
:ref:`B-parameters`.

`Gparams(N1p, N1m, N2p, N2m)` returns the two-port G-parameters matrix.  See
:ref:`G-parameters`.

`Hparams(N1p, N1m, N2p, N2m)` returns the two-port H-parameters matrix.  See
:ref:`H-parameters`.

`Sparams(N1p, N1m, N2p, N2m)` returns the two-port S-parameters matrix.  See
:ref:`S-parameters`.

`Tparams(N1p, N1m, N2p, N2m)` returns the two-port T-parameters matrix.  See
:ref:`T-parameters`.

`Yparams(N1p, N1m, N2p, N2m)` returns the two-port Y-parameters matrix.  See
:ref:`Y-parameters`.

`Zparams(N1p, N1m, N2p, N2m)` returns the two-port Z-parameters matrix.  See
:ref:`Z-parameters`.

`Yparamsn(N1p, N1m, N2p, N2m, ...)` returns the n-port Y-parameters matrix.  See
:ref:`Y-parameters`.

`Zparamsn(N1p, N1m, N2p, N2m, ...)` returns the n-port Z-parameters matrix.  See
:ref:`Z-parameters`.     
   

Nodes
=====

A node object is obtained using indexing notation.  For example,

   >>> n1 = cct[1]
   >>> n2 = cct['2']


Node attributes
---------------

Nodes have many attributes including: `name`, `v`, `V`, `dpY`, and `dpZ`.

`v` is the time-domain voltage (with respect to the ground node 0).
`V` is a superposition of the node voltage in the different transform
domains.

For example,
   
   >>> cct[2].v
    -R₁⋅t              
    ──────             
      L₁               
   e      ⋅Heaviside(t)


`dpY` and `dpZ` return the driving-point admittance and impedance for the node with respect to ground, for example,

   >>> cct[2].dpZ
    R₁⋅s 
   ──────
       R₁
   s + ──
       L₁

Circuit components
==================

A Component object is obtained from a Circuit object using member notation.  For example,

   >>> cpt = cct.R1


Component attributes
--------------------

Each Component object has a number of attributes, including:

- `V` transform-domain voltage across component (use `V(t)` to get the time-domain voltage or `V(s)` to get the Laplace domain voltage)
  
- `I` transform-domain current through component (use `I(t)` to get the time-domain current or `I(s)` to get the Laplace domain current)

- `v` time-domain voltage across component
  
- `i` time-domain current through component

Lcapy uses the passive sign convention.  Thus for a passive device (R,
L, C), current flows into the positive node, and for a source (V, I),
current flows out of the positive node.

Note, the above attributes are influenced by other components in the
circuit.  The following attributes assume that the component is not in
circuit:
  
- `Voc` transform-domain open-circuit voltage; it is zero for passive
  components and infinite for current sources

- `Isc` transform-domain short-circuit current (the current flowing
  through the component when it is short-circuited); it is zero for
  passive components and infinite for voltage sources

- `voc` t-domain open-circuit voltage; it is zero for passive
  components and infinite for current sources

- `isc` t-domain short-circuit current (the current flowing through
  the component when it is short-circuited); it is zero for passive
  components and infinite for voltage sources

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

- `is_ivp` initial value problem (at least one capacitor or inductor has an explicit initial condition)

- `is_causal` causal response

  
`v` is the time-domain voltage difference across the component, for example:

   >>> cct.R1.v   
    -R₁⋅t              
    ──────             
      L₁               
   e      ⋅Heaviside(t)   
   
`i` is the time-domain current through the component, for example:

   >>> cct.R1.i   
   ⎛      -R₁⋅t ⎞             
   ⎜      ──────⎟             
   ⎜        L₁  ⎟             
   ⎜1    e      ⎟             
   ⎜── - ───────⎟⋅Heaviside(t)
   ⎝R₁      R₁  ⎠             

The `V` and `I` attributes provide the voltage and current as a
superposition in the transform domains, for example,

   >>> cct.V1.V
   ⎧   1⎫
   ⎨s: ─⎬
   ⎩   s⎭

The `Y` and `Z` attributes provide the generalized s-domain admittance and impedance of the component, for example,

   >>> cct.L1.Z(s)
   L₁⋅s

   >>> cct.R1.Z(s)
   R₁

The generalized s-domain driving point admittance and impedance can be found using `dpY` and `dpZ`, for example,

   >>> cct.L1.dpZ(s)
    R₁⋅s 
   ──────
       R₁
   s + ──
       L₁

Note, this is the total impedance across `L1`, not just the impedance of the component as given by `cct.L1.Z(s)`.
       

Oneports
========

A Oneport object is defined by a pair of nodes or by a component name.
There are three circuit methods that will create a Oneport object from
a Circuit object:

- `thevenin(Np, Nm)`  This creates a series combination of a voltage source and an impedance.

- `norton(Np, Nm)`  This creates a parallel combination of a current source and an impedance.

- `oneport(Np, Nm)` This creates either a Norton model, Thevenin model, source, or impedance as appropriate.

A Oneport object is a Network object so shares the same attributes and
methods, see :ref:`network_attributes` and :ref:`network_methods`.
   

Here's an example of creating and using a Oneport object:

   >>> cct = Circuit("""
   >>> R1 3 2
   >>> L 2 1
   >>> C 1 0
   >>> R2 3 0""")
   >>> o = cct.oneport('R1')

Alternatively, a Oneport object can be created using a pair of nodes:

   >>> o = cct.oneport(3, 2)

A third way is from a node object and another node name, for example,

   >>> o = a[3].oneport(2)   

Here's an example,

   >>> cct = Circuit("""
   >>> R1 3 2
   >>> L 2 1
   >>> C 1 0
   >>> R2 3 0""")
   >>> cct.oneport('R1').Z(omega)
           ⎛   2   ⅉ⋅R₂⋅ω    1 ⎞ 
    C⋅L⋅R₁⋅⎜- ω  + ────── + ───⎟ 
           ⎝         L      C⋅L⎠ 
   ──────────────────────────────
          2                      
   - C⋅L⋅ω  + ⅉ⋅C⋅ω⋅(R₁ + R₂) + 1
   >>> cct.oneport('R1').Z(s)
           ⎛ 2   R₂⋅s    1 ⎞ 
    C⋅L⋅R₁⋅⎜s  + ──── + ───⎟ 
           ⎝      L     C⋅L⎠ 
   ──────────────────────────
        2                    
   C⋅L⋅s  + C⋅s⋅(R₁ + R₂) + 1


Netlist evaluation
==================

The circuit node voltages are determined using Modified Nodal Analysis
(MNA).  This is performed lazily as required with the results cached.

When a circuit has multiple independent sources, the circuit is
decomposed into a number of sub-circuits; one for each source type.
Again, this is performed lazily as required.  Each sub-circuit is
evaluated independently and the results are summed using the principle
of superposition.  For example, consider the circuit

   >>> cct = Circuit("""
   ... V1 1 0 {1 + u(t)}
   ... R1 1 2
   ... L1 2 0""")

In this example, V1 can be considered the superposition of a DC source
and a transient source.  The approach Lcapy uses to solve the circuit
can be found using the `describe` method:

   >>> cct.describe()
   This is solved using superposition.
   DC analysis is used for source V1.
   Laplace analysis is used for source V1.

For the curious, the sub-circuits can be found with the `subcircuits` attribute:

   >>> cct.subcircuits
   {'dc': V1 1 0 dc {1}
          R1 1 2
          L1 2 0 L_1,
   's': V1 1 0 {Heaviside(t)}
        R1 1 2
        L1 2 0 L_1
   }

Here the first sub-circuit is solved using DC analysis and the second
sub-circuit is solved using Laplace analysis in the s-domain.

The properties of each sub-circuit can be found with the `analysis` attribute:

   >>> cct.sub['dc'].analyse()
   {'ac': False,
   'causal': False,
   'control_sources': [],
   'dc': True,
   'dependent_sources': [],
   'has_s': False,
   'has_ic': False,
   'independent_sources': ['V1'],
   'ivp': False,
   'time_domain': False,
   'zeroic': True}

   
Simplification
==============

Netlists have simplification methods : `simplify_series()`,
`simplify_parallel()`, and `simplify()`, The latter is a generic
method; it repeatedly calls `simplify_series()` and
`simplify_parallel()` until no changes can be made.  The number of
iterations is controlled by the `passes` argument.

Each of the netlist simplification methods have an `explain` argument,
If this is `True`, the simplification steps are printed.  There is
also a `modiy` argument.  If this is `False`, the modifications are
not performed.


Netlist analysis examples
=========================


V-R-C circuit (1)
-----------------

This example plots the transient voltage across a capacitor in a series R-L circuit:

.. image:: examples/netlists/circuit-VRC1.png
   :width: 10cm

.. literalinclude:: examples/netlists/circuit-VRC1-vc.py

.. image:: examples/netlists/circuit-VRC1-vc.png
   :width: 15cm


V-R-C circuit (2)
-----------------

This example is the same as the previous example but it uses an
alternative method of plotting.

.. literalinclude:: examples/netlists/circuit-VRC2-vc.py

.. image:: examples/netlists/circuit-VRC2-vc.png
   :width: 15cm


V-R-L-C circuit (1)
-------------------

This example plots the transient voltage across a resistor in a series R-L-C circuit:

.. image:: examples/netlists/circuit-VRLC1.png
   :width: 10cm

.. literalinclude:: examples/netlists/circuit-VRLC1-vr.py

.. image:: examples/netlists/circuit-VRLC1-vr.png
   :width: 15cm



V-R-L-C circuit (2)
-------------------

This is the same as the previous example but with a different resistor value giving an underdamped response:

.. image:: examples/netlists/circuit-VRLC2.png
   :width: 10cm
           
.. literalinclude:: examples/netlists/circuit-VRLC2-vr.py

.. image:: examples/netlists/circuit-VRLC2-vr.png
   :width: 15cm


Mechanical netlists
===================

Linear mechanical networks comprising masses, springs, and dampers can
be simulated.  The mechanical analogue II (impedance analogue) is
employed where voltage is equivalent to force and current is
equivalent to speed.  Thus a mass is analogous to an inductor, a
spring is analogous to a capacitor, and a damper is analogous to a
resistor.

For example,
   >>> a = Circuit("""
   k 1 2; right
   r 2 3; right
   m 3 4; right""")
   >>> Z = a.impedance(1, 4)
   >>> Z(s).partfrac() 
              1 
   m⋅s + r + ───
             k⋅s

With this analogue d'Alemberts law is equivalent to Kirchhoff's voltage law.  Thus every loop in the electrical circuit is analogous to a point in the mechanical system.   This also means that series combinations transform to parallel combinations and vice-versa.


Interrogation
=============

Netlist attributes
------------------

`components` dictionary of components

`nodes` dictionary of nodes

`subcircuits` dictionary of sub-circuits (for ac, dc, transient, etc.)

`is_ac` all independent sources are ac

`is_causal`  all independent sources are causal

`is_dc` all independent sources are dc

`is_time_domain` netlist can be analysed in time domain

`is_superposition` netlist must be analysed as a superposition

`ivp` initial value problem

`has_ic` initial conditions are specified

`has_ac` an independent source has an ac component

`has_dc` an independent source has a dc component

`has_s_transient` an independent source has a transient component defined in s-domain

`has_transient` an independent source has a transient component

`control_sources` list of voltage sources used to specify control current for CCVS and CCCS components

`dependent_sources` list of dependent sources

`ics` list of components with explicit initial conditions

`independent_sources` list of independent sources

`reactances` list of capacitors and inductors

`sources` list of sources



Netlist methods
---------------

`describe()` print message describing how netlist is solved

`kill()` kills specified independent sources (voltage sources
  become short-circuits and current sources become open-circuits)

`kill_except()` kills all but the specified independent sources

`s_model()` converts sources to the s-domain and represents
  reactive components as impedances

`state_space_model()` creates a state-space model by replacing inductors
  with current sources and capacitors with voltage sources

`r_mode()` creates a resistive equivalent model using companion
  circuits (this is used for time-stepping simulation)

`noise_model()` replaces resistors with a series combination of a
  resistor and a noise voltage source
  
`subs()` substitutes symbolic component values


Component attributes
--------------------

`connected` list of components connected to the component

`is_ac` source is only ac

`is_causal`  source or component is causal

`is_capacitor` component is a capacitor

`is_current_source` component is a current source

`is_dependent_source` source is dependent

`is_dc` source is only dc

`is_inductor` component is an inductor

`is_independent_source` source is independent

`is_noisy` source only has a noisy component

`is_resistor` component is a resistor

`is_reactance` component is a capacitor or inductor

`is_source` component is a source

`is_voltage_source` component is a voltage source

`has_ic` initial conditions are specified

`has_ac` source has an ac component

`has_dc` source has a dc component

`has_noisy` source has a noisy component

`has_s_transient` source has a transient component defined in s-domain

`has_t_transient` source has a transient component defined in time domain

`has_transient` source has a transient component

`nodes` list of nodes

`nodenames` list of node names


Component methods
-----------------

`norton()` Create Norton oneport object viewed from nodes of the component

`thevenin()` Create Thevenin oneport object viewed from nodes of the component

`oneport()` Create Thevenin or Noton oneport object as appropriate when viewed from nodes of the component

`transfer(cpt)` Create transfer function for the voltage across `cpt`
divided by the voltage across the component

`connected()` Return list of components connected to this component

`is_connected(cpt)` True if connected to specified `cpt`


Node attributes
---------------

`connected` list of components connected to node


Node methods
------------

`is_connected(node)` True if connected to specified node


.. image:: examples/netlists/graph1.png
   :width: 8cm
           

