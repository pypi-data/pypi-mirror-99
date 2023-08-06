==========
Pitchtools
==========

This module provides a set of functions to work with musical pitch. It enables
to convert between frequenies, midinotes and notenames

Examples
========

Convert some note names to frequencies

.. code-block:: python

    from pitchtools import *
    ebscale = "4Eb 4F 4G 4Ab 4Bb 5C 5D".split()
    for note in ebscale:
        # Convert to frequency with default a4=442 Hz
        freq = n2f(note)
        midinote = f2m(freq)
        print(f"{note} = {freq} Hz (midinote = {midinote})")

    
The same but with a different reference frequency


.. code-block:: python


    from pitchtools import *
    ebscale = "4Eb 4F 4G 4Ab 4Bb 5C 5D".split()
    cnv = Converter(a4=435)
    for note in ebscale:
        # Convert to frequency with default a4=442 Hz
        freq = cnv.n2f(note)
        midinote = cnv.[Of2m(freq)
        print(f"{note} = {freq} Hz (midinote = {midinote})")


Microtones
~~~~~~~~~~

.. code-block:: python

    >>> from pitchtools import *
    >>> n2m("4C+")
    60.5
    >>> n2m("4Db-10")
    60.9
    >>> m2n(61.2)
    4C#+20


**Microtonal notation**


+---------+---------+
| Midinote| Notename|
|         |         |
+=========+=========+
| 60.25   | 4C+25 / |
|         | 4C>     |
+---------+---------+
| 60.45   | 4C+45   |
+---------+---------+
| 60.5    | 4C      |
+---------+---------+
| 60.75   | 4Db-25  |
+---------+---------+
| 61.5    | 4D-     |
+---------+---------+
| 61.80   | 4D-20   |
+---------+---------+
| 63      | 4D#     |
+---------+---------+
| 63.5    | 4D#+    |
+---------+---------+
| 63.7    | 4E-30   |
+---------+---------+
