=============
NaïveCalendar
=============

    **naïf, naïve n. adj**.

    `1.` *LITTERAIRE* Qui est naturel, sans artifice, spontané. Art naïf, art populaire, folklorique. —  Un peintre naïf.

    `2.` *COURANT* Qui est plein de confiance et de simplicité par ignorance, par inexpérience. ➙ candide, ingénu, simple. —  Qui exprime des choses simples que tout le monde sait. Remarque naïve. ➙ simpliste.

    LeRobert_

.. image:: https://img.shields.io/badge/Source-git-success
    :target: https://framagit.org/Daguhh/naivecalendar

.. image:: https://img.shields.io/badge/Download-script-yellow
   :target: https://framagit.org/Daguhh/naivecalendar/-/raw/master/naivecalendar.py?inline=false

A popup calendar with rofi_ and python3_:

* Cycle through calendar month by month
* Create notes linked to days. *Days with notes will appear colored*

.. image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/naivecalendar_screenshot.png 
    :width: 200 px
    :align: center

Dependancies
-----------

* python3_
* rofi_

Usage
-----

Run: 

.. code::

    chmod +x naivecalendar.py
    ./naivecalendar.py 

For more detail about commands, run the script, then, in the command prompt, type: 

.. code::

   help

Documentation
-------------

Build the doc
^^^^^^^^^^^^^

.. code::

   cd docs/
   python3 -m pip install -r requirements.txt
   make html


.. _LeRobert: https://dictionnaire.lerobert.com/definition/naif
.. _rofi: https://github.com/davatorium/rofi
.. _python3: https://www.python.org/
