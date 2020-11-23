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
   python3 -m pip install -r requirements.txt
   make html


.. _LeRobert: https://dictionnaire.lerobert.com/definition/naif
