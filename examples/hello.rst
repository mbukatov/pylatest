=====================
 Hello World example
=====================

This is just simple demonstration of custom rst directive.

.. hello:: pylatest

And now something completelly different:

.. action:: 1

    Vor dem Gesetz steht ein Türhüter.
    Zu diesem Türhüter kommt ein Mann vom Lande
    und bittet um Eintritt in das Gesetz.

Table Line Directive Test
-------------------------

This is just another Hello World grade example.

.. foobar:: 1

    This is *the very first* thing to do: run `uname -a` command.

.. foobar:: 2

    And now this is 2nd. Try this::

        $ git st
        ## master
         M pylatest/directives.py
         M pylatest/transforms.py

.. foobar:: 4

    The end (id determines placement in an output document).

.. foobar:: 3

    `Es ist möglich,` sagt *der Türhüter*, `jetzt aber nicht.`
