=============
NaïveCalendar
=============

    **naïf, naïve n. adj**.

    `1.` *LITTERAIRE* Qui est naturel, sans artifice, spontané. Art naïf, art populaire, folklorique. —  Un peintre naïf.

    `2.` *COURANT* Qui est plein de confiance et de simplicité par ignorance, par inexpérience. ➙ candide, ingénu, simple. —  Qui exprime des choses simples que tout le monde sait. Remarque naïve. ➙ simpliste.

    LeRobert_


Un popup calendrier avec rofi_ et python3_ :

* Parcourez le calendrier de mois en mois
* Créez et éditez des notes liés à chaque date du calendrier. *Une date possédant une note apparait colorée*

|classic dark| |square dark nord| |round_light nord| |classic light compact| 


.. _dependancies:

Dépendances
-----------

* python3_
* rofi_

Installation
^^^^^^^^^^^^

Le naivecalendar utilise deux fichiers:

- naivecalendar.py : envoie la liste des entrées d'un calendrier vers la sortie standard
- naivecalendar.sh : lance rofi en mode script en interaction avec le fichier précedent.

Plus, deux fichiers de configuration:

- /themes/<theme>.rasi : fichier de configuration rofi (forme et couleurs)
- /themes/<theme>.cfg : un fichier .ini qui défini le contenu du calendrier

Copiez simplement les fichiers dans le même dossier (en respectant l'arborescece)

finallement, lancez avec::

    ./naivecalendar.sh 

Utilisation
-----------

Basique
^^^^^^^

Executez le script, puis:

- Interagisez avec la souris ou le clavier
- Utlisez les flêches pour parcourir le calendrier
- Cliquez sur un date ou créer une note liée
  (Un jour avec une note attachée apparaitra colorée)
- Les notes sont enregistrée dans {HOME}/.naivecalendar_notes/
  (Vous devez les supprimer manuellement)

Raccourcis
^^^^^^^^^^

Les raccourcis sont à entrer dans l'invite de commande rofi.
*Sym* est le symbole affiché à l'écran. *Sym*, *Touche* et *Alt-Key* peuvent être utilisés pour executer une action.

====  =====  =======  ========  ========================================
Sym    Keys                     Action
----  ------------------------  ----------------------------------------
  ..     ..       ..        ..  ..
====  =====  =======  ========  ========================================
 ◀◀      <<       pp       --   année précédente
  ◀       <        p      `-`   mois précédent
  ▶       >        n      `+`   mois suivant
 ▶▶      >>       nn       ++   année suivante
 ..   notes       ..       ..   montrer les notes du mois courant
 ..    help       ..       ..   afficher l'aide
 ..   theme       ..       ..   changer de theme
====  =====  =======  ========  ========================================

Dans un script
^^^^^^^^^^^^^^

Vous pouvez utiliser le naivecalendar dans un script pour demander interactivement une date. Plus d'informations sur l'utilisation en ligne de commande:

.. code:: bash

   ./naivecalendar.sh -h

Personnalisation
^^^^^^^^^^^^^^^^

Editer les paramètres dans les fichiers suivant:

- contenu du calendrier : ./*themes*/**<theme>.cfg**
- apparence du calendrier : ./*themes*/**<theme>.rasi** 


.. warning::

   modifier le contenu du calendrier peut demander la modification conjointe de l'apparence de ce dernier.

Themes
------

Des `themes sont disponibles <https://framagit.org/Daguhh/naivecalendar/-/blob/master/naivecalendar/themes/themes.rst>`_, vous pouvez les appliquer en tapant *theme* dans l'init de rofi ou les charger temporairement en précisnat l'arugment *--theme*. Vous pouvez créer vos propres fichiers de thème (`rasi <https://github.com/davatorium/rofi/blob/next/doc/rofi-theme.5.markdown>`_), placez les dans le dossier *./themes/* 

Files
-----

Voici un brêve description des fichiers demandés/générés par le calendrier

=================================   ==============================================
Fonction                            Fichier
=================================   ==============================================
commande rofi                       ./naivecalendar.sh
script appellé par rofi             ./naivecalendar.py
fichiers de thème rofi              ./themes/\*.rasi
configuration du contenu            ./themes/\*.cfg 
chemin d'enregistrement des notes   ~/.naivecalendar_notes/
dossier des fichiers de cache       ~/.cache/naivecalendar/
sauvegarde la date                  ~/.cache/naivecalendar/date_cache.ini
sauve la date avec l'option -p      ~/.cache/naivecalendar/pretty_print_cache.txt
sauvegarde le theme choisi          ~/.cache/naivecalendar/theme_cache.txt
=================================   ==============================================

Documentation
-------------

Construisez la documentation 

.. code::

   cd docs/
   python3 -m pip install -r requirements.txt
   make html


.. _LeRobert: https://dictionnaire.lerobert.com/definition/naif
.. _rofi: https://github.com/davatorium/rofi
.. _python3: https://www.python.org/

.. |python_stable_badge| image:: https://img.shields.io/badge/Download-py-yellow?logo=data:image/png;base64,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&style=plastic
    :target: https://framagit.org/Daguhh/naivecalendar/-/raw/master/naivecalendar/naivecalendar.py?inline=false

.. |python_dev_badge| image:: https://img.shields.io/badge/Download-sh-grey?logo=data:image/png;base64,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&style=plastic
    :target: https://framagit.org/Daguhh/naivecalendar/-/raw/master/naivecalendar/naivecalendar.sh?inline=false

.. |git_badge| image:: https://img.shields.io/badge/Source-git-red?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABpFBMVEUAAADwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDP////R9jl6AAAAinRSTlMAAANVzvz5wEICYOrfTGHt4k1d7vBn7wUUAWLCOdM49fFAPzdctQ2B+DYLqXlL91Qk41PkgjDo1QRu8qwd/souDPtRfK7SM2ONdpDQMhmI9lbpB5PeQc2zCSm8pKe/ssPGNUXmThghwVm7SAoWT8Va89HU+ozhdEblt2wg4F8rnmX9Stu5h6jn3MffBpBlAAAAAWJLR0SL8m9H4AAAAAd0SU1FB+QLGg4tBCSsxiIAAAJwSURBVFjDpdTpXxJBGMDxfQjQVVHMEqkszeToULqMNCq7bwLJisouKkoty+47O6znr24ZZnFgd2efnZ2XOL/vx515djXNeUFgXTAUbmsH0JQW6B2daKyuiJoAencPshXtVRHWejVB7FWE5t67ALC+D9GHANC9Af0JgY39ygLEBuLgQwB90+YtoC6w8x/cqizw+1MWGvfPhb5tQyEvgjA/TIgNbx/ZMRomC03zVxPYSCSSKaLQMr+D6fpW2LmL9hSt84+7+U7YM0YRLH1onO+DzF7CXVh6DO1rAPvdb9PaIx4wH+HghOs82PV4KMOB7OFJF8G2R5w6wu/BTXDoMXf0GED8uPFuygWnHnH6hDGNJ0dALjj3DAicOn1GKkj6OjCFQZkg602gLsTOnjt/4WKoVdA7nPsGgMFLUF+Xr+RFIQLa1QISAPY/sAcuzogbSte0WSQBeP0Gn6qbUXFHWZsmArd0DhRHxR15LUUEZswXQ78t7khpd4jAXJEDibvijntae4kGTNznX7gHQ8KGhxUNIlESgHOPDAHg8RPh753VuPFTb5QE5J4+G5hfWHwu9i/itVGUCCKAuPSy7VXe0kuFZqBlmb1MkAFrvURYXnQExN5RmHy9YLw/1TeuvYMQfptlh/zuvWtvL3xI8ENOuve2wkdz/NP97r2NsFwxb+nTZ0JvFXJfTOBrgdJbhW9Zfgbff5B6i9Czwr66kJkl9hbh5/i88TlPl8m9RVj69Tv5Z9VDL383Kb1coPQygdY7C9TeSaD39oKX3k7w1luFgse+Jqx0+enZh6jkpxcFtZ4Jf2v9alWtrwnD5bHwv4ou6/8Djb7EGx2gqrEAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMTEtMjZUMTM6NDU6MDQrMDE6MDADclLHAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTExLTI2VDEzOjQ1OjA0KzAxOjAwci/qewAAAABJRU5ErkJggg==&style=plastic
    :target: https://framagit.org/Daguhh/naivecalendar

.. |classic dark| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/classic_dark.png
    :height: 130 px

.. |square dark nord| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/square_dark_nord.png
    :height: 130 px

.. |round_light nord| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/round_light_nord.png
    :height: 130 px

.. |classic light compact| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/classic_light_compact.png
    :height: 130 px
