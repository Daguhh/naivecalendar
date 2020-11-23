=============
NaïveCalendar
=============

Un popup calendrier avec rofi et python3 :

* Parcourez le calendrier de mois en mois
* Créez et éditez des notes liés à chaque date du calendrier. *Une date possédant une note apparait colorée*

.. image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/naivecalendar_screenshot.png 
    :width: 200 px
    :align: center

Dépendances
-----------

* python3
* rofi

Usage
-----

Lancer le programme:

.. code::

    chmod +x naivecalendar.py
    ./naivecalendar.py 

Pour le détail des commandes, dans le prompt rofi, tapez:

.. code::

   help

Documentation
-------------

Build the doc
^^^^^^^^^^^^^

.. code::

   cd docs/
   pip install -r requirements.txt
   make html

