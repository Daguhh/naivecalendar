=============
NaïveCalendar
=============

:author: Daguhh
:version: 0.7.0

|readme_fr| |git_badge| |doc sphinx| |deb package|

    **naïf, naïve n. adj**.

    `1.` *LITTERAIRE* Qui est naturel, sans artifice, spontané. Art naïf, art populaire, folklorique. —  Un peintre naïf.

    `2.` *COURANT* Qui est plein de confiance et de simplicité par ignorance, par inexpérience. ➙ candide, ingénu, simple. —  Qui exprime des choses simples que tout le monde sait. Remarque naïve. ➙ simpliste.

    LeRobert_


Un popup calendrier avec rofi_ et python3_ :

|classic dark| |square dark nord| |round_light nord| |classic light compact| 

Fonctionnalités
---------------

* Parcourez le calendrier de mois en mois
* Support de la langue locale ou forcer une langue
* Créez et éditez des notes liés à chaque date du calendrier. *Une date possédant une note apparait colorée*
* Créez plusieurs types de notes (c-à-d plusieurs dossier), créez des évenements récurrents, basculez entre elles.
* Personnalisez les thèmes, contenus, symboles, raccourcis avec de simples fichiers textes
* Changez de thème à la volée
* Intrégrez le à vos scripts et rendez les iinteracifs : ouvrir à une date particulière, demander une date, copier une date dans le presse papier.

.. _contents:

-----------------------------------------------------------------------------

.. _installation:

Dépendances
-----------

Requirements
^^^^^^^^^^^^

* python3_ (stdlib)
* rofi_

Recommends
^^^^^^^^^^

* xclip (option "copier dans le presse papier)
* sensible-utils (sous-command "update" : choix de l'éditeur)

Suggests
^^^^^^^^

* fontawesome (icons)

Installation
------------

Manuelle
^^^^^^^^

Le naivecalendar utilise deux fichiers:

- naivecalendar.py : envoie la liste des entrées d'un calendrier vers la sortie standard
- naivecalendar.sh : lance rofi en mode script en interaction avec le fichier précedent.

Plus, deux fichiers de configuration:

- /themes/<theme>.rasi : fichier de configuration rofi (forme et couleurs)
- /themes/<theme>.cfg : un fichier .ini qui défini le contenu du calendrier

Copiez simplement les fichiers dans le même dossier (en respectant l'arborescece)

finallement, lancez avec::

    ./naivecalendar.sh 

Paquet (debian)
^^^^^^^^^^^^^^^^

.. code:: bash

    apt install ./naivecalendar_x.y.z_all.deb

Lancez avec:

.. code:: bash

    naivecalendar

---------------------------------------------------------------------------------

.. _usage:

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
La liste ci-dessous est à titre indicative et peut varier selon les themes. 
L'entièreté des symboles peut être modifée via les fichiers de configurations.
*Sym* est le symbole affiché à l'écran. *Sym* et *Keys* peuvent être utilisés pour executer une action.

====  =======  =======  ========  ========================================
Sym     Keys                      Action
----  --------------------------  ----------------------------------------
  ..     ..       ..        ..    ..
====  =======  =======  ========  ========================================
 ◀◀        <<       pp       --   année précédente
  ◀         <        p      `-`   mois précédent
  ▶         >        n      `+`   mois suivant
 ▶▶        >>       nn       ++   année suivante
       event       ee       ..   montre les évenements du mois courant
      switch       ss       ..   change le type d'evénement affiché
        help       hh       ..   montre l'aide
       theme       tt       ..   montre le selecteur de thème
  ☰      menu       mm       ..   montre le menu
====  =======  =======  ========  ========================================

Evenements
^^^^^^^^^^

Les événements sont de simples fichiers (textes) créés par le calendrier à l'interaction avec un jour (clic/touche entée)
Les noms de fichiers de ces evenenements doivent contenir des directives au format `strftime <https://strftime.org/>`_ (%d, %m ...). ::

    note_%Y-%m-%d.txt

Ne pas donner de directive identifiant un jour et un mois permet par exemple de rendre récurrent l'évenement (parfait pour les anniversaires!).::

    birthday_on_%d-%m.txt

Vous pouvez créer plusieurs types d'événements (qui ne sont que différents dossiers). Définir un nouveau type d'événement nécessite simplement la création d'un nouvelle entrée dans la section [EVENTS] des fichiers de configuration.::

    [EVENTS]

    Notes = .naivecalendar_events/MyNotes/note_%Y-%m-%d.txt
    Birthday = .naivecalendar_events/Birthdays/birthday_on_%d-%m.txt

Les notes quant à elles supportent un léger format pour être correctement affichées lors de l'action "montrer les événements du mois" :

- montrer section : si vous crééz des sections (format : [section]), toute ligne contenant cette directive sera affichées::

    [9H30] rdv with truc <---- will be displayed
    Some text
    Some text again
    [14H30] rdv with muche <----- will be displayed
    Some text again again

- montrer entête : si la note ne contient pas de [section], la première ligne sera affichée::

    # Note Title  <---- only first line is displayed
    Some text
    Some text again...

Dans le menu "montrer les événements du mois", si vous interagissez avec le nom du fichier, l'editeur rouvrira la note, autrement, cliquer sur une autre ligne vous rammenaera au calendrier::

    notes_2021-01-05 : <---- reopen editor
    [9H30] rdv with truc   <--- do nothing : back to calendar
    [14H30] rdv with muche



Options
^^^^^^^

Des options sont disponibles en ligne de commande et peuvent être utiles lors de l'integration dans un script ou pour écraser temporairement certains paramètres. 
Les sous-commandes **update** et **add-event** peuvent vous permettre d'éditeren une fois un paramètre sur tous les thèmes de l'utilisateur.

.. code::

    usage: naivecalendar [-h] [-V] [-v] [-p] [-x] [-f FORMAT] [-e EDITOR] [-l LOCALE] [-c] [-t THEME] [-d DATE]

    A simple popup calendar

    subcommands:
        update      Update a calendar parameter for all user themes at once
        add-event   Add, modify, delete event in all user themes config at once

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -v, --verbose         direct rofi command  errors to stdout
      -p, --print           print date to stdout instead of opening a event
      -x, --clipboard       copy date to clipboard
      -f FORMAT, --format FORMAT
                            option '-p' or '-x' output format (datetime.strftime format, defaut='%Y-%m-%d')
      -e EDITOR, --editor EDITOR
                            editor command to open events
      -l LOCALE, --locale LOCALE
                            force system locale, for example '-l es_ES.utf8'
      -c, --read-cache      force calendar to read old date from cache
      -t THEME, --theme THEME
                            set calendar theme, default=classic_dark (theme file name without extention)
      -d DATE, --date DATE  display calendar at the given month, format='%m-%Y'

-----------------------------------------------------------------------------

.. _customize:

Personnalisation
^^^^^^^^^^^^^^^^

Editer les paramètres dans les fichiers suivant:

- contenu du calendrier : ./*themes*/**<theme>.cfg**
- apparence du calendrier : ./*themes*/**<theme>.rasi** 

.. warning::

   modifier le contenu du calendrier peut demander la modification conjointe de l'apparence de ce dernier.


Des `themes sont disponibles <https://framagit.org/Daguhh/naivecalendar/-/blob/master/naivecalendar/themes/themes.rst>`_, vous pouvez les appliquer en tapant *theme* dans l'init de rofi ou les charger temporairement en précisnat l'arugment *--theme*. Vous pouvez créer vos propres fichiers de thème (`rasi <https://github.com/davatorium/rofi/blob/next/doc/rofi-theme.5.markdown>`_), placez les dans le dossier *./themes/* 

Vous pouvez commencer avec une copie des thèmes "officiels"::

    cp -r /usr/share/naivecalendar/themes/* ~/.config/naivecalendar/themes/

.. note::

    Si vous créez un thème du même nom qu'existant dans le dossier /usr/share/naivecalendar/themes/, seul celui-ci sera prit en compte.

Puis, modifiez les thèmes, un par un avec votre éditeur favoris, ou, en masse à l'aide des sous commandes du naivecalendar (utilisez la complétion) ::

    naivecalendar <subcommand> -h

-----------------------------------------------------------------------------

Files
-----

Voici une brêve description des fichiers demandés/générés par le calendrier

================================   ===================================================================
Fonction                           Fichier
================================   ===================================================================
..
------------------------------------------------------------------------------------------------------
commande rofi                      /usr/share/naivecalendar/**naivecalendar.sh**
script appellé par rofi            /usr/share/naivecalendar/**naivecalendar.py**
fichiers de thèmes rofi            /usr/share/naivecalendar/**themes/\*.rasi**
configuration du contenu           /usr/share/naivecalendar/**themes/\*.cfg**
--------------------------------   -------------------------------------------------------------------
..
------------------------------------------------------------------------------------------------------
thèmes de l'utilisateur            ~/.config/naivecalendar/**themes/\*.rasi**
conf du contenu de l'utilisateur   ~/.config/naivecalendar/**themes/\*.cfg**
--------------------------------   -------------------------------------------------------------------
..
------------------------------------------------------------------------------------------------------
dossier des evenements (defaut)    ~/.naivecalendar_events/<event type>/**<user date format>.txt**
--------------------------------   -------------------------------------------------------------------
..
------------------------------------------------------------------------------------------------------
fichier cache : date               ~/.cache/naivecalendar/**date_cache.ini**
date au format -f|-format          ~/.cache/naivecalendar/**pretty_print_cache.txt**
sauvegarde le thème                ~/.cache/naivecalendar/**theme_cache.txt**
sauvegarder le type d'évenement    ~/.cache/naivecalendar/**event_cache.txt**
log de la dernière commande rofi   ~/.cache/naivecalendar/**rofi_log.txt** 
================================   ===================================================================

---------------------------------------------------------------------------------

Construction du paquet debian
-----------------------------

.. code::

    sudo apt install devscripts
    cd naivecalendar-x.y.z/
    debuild -us -uc

.. note::

   Personnalisez vos thèmes avant construction, l'intrégralité du dossier "themes" sera inclut dans votre paquet.

Documentation
-------------

Construisez la documentation 

.. code::

   cd docs/
   python3 -m pip install -r requirements.txt
   make html


.. _start-link:

.. _LeRobert: https://dictionnaire.lerobert.com/definition/naif
.. _rofi: https://github.com/davatorium/rofi
.. _python3: https://www.python.org/

.. |git_badge| image:: https://img.shields.io/badge/Source-git-red?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABpFBMVEUAAADwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDPwUDP////R9jl6AAAAinRSTlMAAANVzvz5wEICYOrfTGHt4k1d7vBn7wUUAWLCOdM49fFAPzdctQ2B+DYLqXlL91Qk41PkgjDo1QRu8qwd/souDPtRfK7SM2ONdpDQMhmI9lbpB5PeQc2zCSm8pKe/ssPGNUXmThghwVm7SAoWT8Va89HU+ozhdEblt2wg4F8rnmX9Stu5h6jn3MffBpBlAAAAAWJLR0SL8m9H4AAAAAd0SU1FB+QLGg4tBCSsxiIAAAJwSURBVFjDpdTpXxJBGMDxfQjQVVHMEqkszeToULqMNCq7bwLJisouKkoty+47O6znr24ZZnFgd2efnZ2XOL/vx515djXNeUFgXTAUbmsH0JQW6B2daKyuiJoAencPshXtVRHWejVB7FWE5t67ALC+D9GHANC9Af0JgY39ygLEBuLgQwB90+YtoC6w8x/cqizw+1MWGvfPhb5tQyEvgjA/TIgNbx/ZMRomC03zVxPYSCSSKaLQMr+D6fpW2LmL9hSt84+7+U7YM0YRLH1onO+DzF7CXVh6DO1rAPvdb9PaIx4wH+HghOs82PV4KMOB7OFJF8G2R5w6wu/BTXDoMXf0GED8uPFuygWnHnH6hDGNJ0dALjj3DAicOn1GKkj6OjCFQZkg602gLsTOnjt/4WKoVdA7nPsGgMFLUF+Xr+RFIQLa1QISAPY/sAcuzogbSte0WSQBeP0Gn6qbUXFHWZsmArd0DhRHxR15LUUEZswXQ78t7khpd4jAXJEDibvijntae4kGTNznX7gHQ8KGhxUNIlESgHOPDAHg8RPh753VuPFTb5QE5J4+G5hfWHwu9i/itVGUCCKAuPSy7VXe0kuFZqBlmb1MkAFrvURYXnQExN5RmHy9YLw/1TeuvYMQfptlh/zuvWtvL3xI8ENOuve2wkdz/NP97r2NsFwxb+nTZ0JvFXJfTOBrgdJbhW9Zfgbff5B6i9Czwr66kJkl9hbh5/i88TlPl8m9RVj69Tv5Z9VDL383Kb1coPQygdY7C9TeSaD39oKX3k7w1luFgse+Jqx0+enZh6jkpxcFtZ4Jf2v9alWtrwnD5bHwv4ou6/8Djb7EGx2gqrEAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMTEtMjZUMTM6NDU6MDQrMDE6MDADclLHAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTExLTI2VDEzOjQ1OjA0KzAxOjAwci/qewAAAABJRU5ErkJggg==&style=flat-square
    :target: https://framagit.org/Daguhh/naivecalendar

.. |readme_fr| image:: https://img.shields.io/badge/Readme-fr-blue?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAgBAMAAACm+uYvAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAG1BMVEUAHpYAHJUfOqPf4/L////85ObwP0/tIjTuJDb4vwGgAAAAAWJLR0QEj2jZUQAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAAd0SU1FB+QMCxQNM0KhjcMAAAAbSURBVCjPY2CAACETFzBwTe+AAIZRiVGJUQkAzmzIQZyPCzQAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMTItMTFUMjA6MTI6NTIrMDA6MDDP69WKAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTEyLTExVDIwOjEyOjUyKzAwOjAwvrZtNgAAAABJRU5ErkJggg==&style=flat-square
   :target: https://framagit.org/Daguhh/naivecalendar/-/blob/master/README_fr.rst

.. |classic dark| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/classic_dark.png
    :height: 130 px

.. |square dark nord| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/square_dark_nord.png
    :height: 130 px

.. |round_light nord| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/round_light_nord.png
    :height: 130 px

.. |classic light compact| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/classic_light_compact.png
    :height: 130 px

.. |doc sphinx| image:: https://framagit.org/Daguhh/naivecalendar/badges/master/pipeline.svg?key_text=Sphinx+doc&key_width=70
    :target: http://daguhh.frama.io/naivecalendar

.. |deb package| image:: https://img.shields.io/badge/deb\ package-0.6.2-blue?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAAB3RJTUUH5QESDCExmXZ6iAAACYpJREFUaN7tmUlsnVcVx3/nft8b/DyP8ZA4DknbpKRzQpGyqIQQUqWqqlgAy+6K2CKqLlgiMayQKtZ0jdQNUoWQUFskCi3QNiQtOGnixBmcOInd2Hn2G77vnsPifm9w4uE5LQiknOj65X3Dufd/zv8M9z54IA/kgTyQB/IFRDa7+P6bPweRvJntwYgA+8/MtI0YAjiEqojcANKvf/vVndW+95ufoN67KM79yEXu+yISYbsEICAISKbeLKjYrRkEZ2oVVf+6T9NfuSjSE9/58YZH4rvf0TTFzA5h/gelUmk6ilybUToX5+KWeQxU0w4U3P2A4L2nfKf8Q1P9vZqdvWee9i9vv/Ea3qf4NPmWiEw7J5jRHGwYtvUAEIdIhEgE4rLl7fTv7ikM5xxO2O/T5Fvep7z9xmtbe0B9ik/q3S6OX4ziCO91lz4Pk4o4xElG4wDWp4rZ7vUBRFGEavqiJumvRdzalgB8mmCmT0ZxdNy5CO/9rnjTeFQEnGVxAJgJ3u8EwDa/JCAuQrDjPk2eFHHvtT/SpNBbr7+CCGiavuCieMAMfKp473ccaTbar5kFD5hJBsDj0+2G3ju8Zp4D56IBTdMXRIS3Xn/lXg+oT6iW63uiXO75KM4H629joM0dE646F6yOuSatvFdMPfcrLs5j5p+vlld+KU4WN3jgzZ99D5+m+LR+QiQ6Ii5uWiZtDL9xeJ9uMjJrekUtpHJDUKMDD2w+0uxTXIyIO+LT+gmfprz50++2PCDi8Ek9FudeivPFfHA9gGSpXDIytni9pQiIi4niAhLFWUxEOJdHLd2+oFn4Ez5CLhIaiUGIC6V8dW31JU1qvxUXpU0Apb5hTHUsinPP9o+Oky+UkCjGuQgXxWG4uHmtUaC2WouLYoq9I6EWEGpAT/9AoNCGl+7SYB5Vj6nHNMW0/bun1NMFps+mSX3MuWihCaDY3Y+q5nKFfLGnt0QcZ6EhipCAJGACKa3qytYJyqIcYj0I+aDG6lh9GfXJjly3rI40krATwyIgAid5Sr0DxXqtnnPOtShkrbfBFDPfrEe7FyMyC1aTFDND0wSf1vFpbbeq2pwlqNcmwMatAMAUNUPN8Krgd9t5NefADMrLK8zPnaSyXqNeqdLd183goNDdWySKQ29o1raMDo2l6lEN63RZTYnDDcNUMVVUFZHdAxCB8so65z6dY+7MFSpVQzWw3EVCJAl7JocZGh1gcmaCodGBJuJOna0aiqGporRTyMINVUV9A8A2aje4NnwsXLzOyb98ws3FZdSMQj5PsVQkn48BYX0t5dzsPMxepOfkWY4+c5iHHz+Ic25XAAKIQPUWAA0UCiA8op27FRGunL/K++98RLm8Tj4XMzoywOEnDjEyMUycixGBylqVK3MLnDl9njur6/z9T6fwqefwUw9tSAybWylYymceUFOcShuFzDL6WKDQNjHQ7HcIxamyVuXjP5+mfGeN3t5uHn36YQ4cniZfzG94IVfI8+hQL0NjA3zwzkesrKxx6m//on+4j/HpsWZwbrN+1GuT7rohC2VuadBoqxiwtv8JwrX5RS7PXWV5aYXxqVGePvEYg2MDSNbHN/VkTRkGY3tHeez4ET5492OqlRoXZucZmRjqKO5CTcgopO0Uspb1GwB2Ci1To16rMX/uKoPDfRx/7gl6B3tRVbDAipXPy1y9cI2kVqdvsJfx/eMUuvJMzOxhZGyQxYVb1Cs10iTNstNOAAJ9TBVcAOzCDQseyEB49cFdWwxTo1KucObkOWq1OjMP7aW7vxuf+mauvnV9mQ//eJJapcrg6ADeexYuLDQXOzIx1FxQtVJDG0lENUuXreHVtwI4i1dV2+gBU2sq2VEExAmpKt09XYzv34P6VvFLk5QzH3/G9ENTTD+yL9DDjCRJg4dVKJYKmBn9I/3kC3F4vyMP2AYPxA06hMhW1G/W8m6WETxpmtLb302hq9V+iwhLi8ukacrEzJ7mwoQQhEvXlhjdO7qhqiJ0tPtreMBMQduCWO/2wI7xJE0q5Qs5yFwaNh7CernS/N7wqIlwZ6Xc3OvWqjXQ0HH6djDbAmhQyRB3Vx0IMeA2B7BZSlOPmRLFUWaA1s04H1FeXaOyVqGrp0hSS0iSlOXrywyMDVBdq7Awv0ippxjoo74zAL6VLdmsDoi2YmA7dSLhHRCqlSo+9VkxMsyEeqVOeaXMhdlLPPLUQcqra5Rvl5k8OIGpcf7Ti5RX1jh0dIbBscGMPp14QJtx0LBxAOA9qiYuyiJ9S9O3rCwC+UKOO7fL1Gt14nwOCBuPXDGmq1Tg3Ok5knrC3oMT9A33sXj5BhdnL7NernDkmUNMHhhHRFDt7PCg0Qv51ItrD+L+3i5m567HE2MDouqRDrSJCL2D3cyfvc3yjduMTA417w2ODnDsG09y/vRF5s9c4tLZy0RxRK6QY2Ckn0eeOkjfUC+mtmO9CWYMhVNV8V5lcWk1PvKV8QabQ1C9+vI3Hzt2dP/vuvt6psS57bSFF51w48pN/vruKbq7izzz3OP0DvZs6DXUK7dvrrC8+DlmMHlgD6W+UjOt7kTVe6ZWY+1O+eqHn8w//4s3/nBaRBp7YolffvFrXd6rqGqGakez0D/cx+BwL7cWb7OytErPQHfI0W0yONbP4Fh/U11ohe9PLHTLcvPzO10iEgNp41glt7pWLaqqU1WkfbOxjbjYse/QJEs3Vrhy4RqjU0NEcfQlHGVvNBQAEgB4Vbe6Vi0CuXYAcbWa5L1mHhDbUk+7CDA6OcTUzBgLFxdZuLjI1MGJjlLi5ih36L/MUFWpVpM8WfzG2TqiJPW55obGdRLGNJu2g0enWS9XOPuPOXL5mOFGQFvbg1+GM8xQ9SSpzwERIA0PiKqKqYqqZ8Oh9T1z37uYXCHHkWOHmP3oPKffn+XQ4zPsmR4ljqPOvNEpADVMTVQ1O6hqHS2aCGamFtrh3U9a6Mpz5NghLn+2wIV/XuLWwjIHvrqPrp4ibrustt2C774QCplJ4Lg1ABjg48gljXaa+9jUA0Q5x8yRvYxODnHr2jJXz18jX8gxMjVMqa/rCzPJst8fokgSwAPW8ECaz0U1w/R+TyXapdTXxXTfFOrDqXMUOew+fmvYDIBhWshFNcIxW5NC6dLK+s1qtX4aM7GA7gtLwwwJX04YC0TVWnLq1u31mw0AjTkc0P/s0X1T48M9/aa7Oa3574ggiEOuL5VXPvjk8lVghWZPGoDkgRJ3/W72PygKrAN1woltG8hQ3f4fADRZ+W+ct7vQfGUeCQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0xOFQxMjoyODo1NCswMDowMDKkURkAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMThUMTI6Mjg6NTQrMDA6MDBD+emlAAAAAElFTkSuQmCC&style=flat-square
    :target: https://acloud.zaclys.com/index.php/s/YjLLMHWpRPPFfZp/download
