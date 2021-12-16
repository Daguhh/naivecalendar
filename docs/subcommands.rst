Subcommands
===========

Subcommands permit the user to modify theme in mass. 

add-event
^^^^^^^^^

.. include:: ../tools/naivecalendar-add-event
   :start-line: 4
   :end-line: 17

---------------------------------

update-themes
^^^^^^^^^^^^^

.. include:: ../tools/naivecalendar-update-themes
   :start-line: 34
   :end-line: 53

configure
^^^^^^^^^

.. include:: ../tools/naivecalendar-configure
   :start-line: 4
   :end-line: 13

Examples
^^^^^^^^

**Start with a copy of installation's themes:**

.. code:: bash

    naivecalendar configure --clone THEMES

::

    THEMES cloned into ~/.config/naivecalendar/
    Bye

**Edit actual config** (open an editor):

.. code:: bash 

    naivecalendar configure --edit THEMES

**Change a parameter in all themes:**

.. code:: bash

    naivecalendar update-themes --parameter USER_LOCALE --value es_ES.utf8

:: 

    setting parameter USER_LOCALE to es_ES.utf8
    27 files Updated:
    blackboard carbon_gold classic_dark classic_dark_compact classic_dark_extended classic_dark_variant classic_light classic_light_compact classic_light_extended classic_light_variant ...
    Bye!

**Change a parameter on choosen themes:**

.. code:: bash

    naivecalendar update-themes --parameter PROMT_DATE_FORMAT --value "%d-%m-%Y" --filter ".*compact" 

::

    setting parameter PROMT_DATE_FORMAT to %d-%m-%Y \n
    4 files Updated:
    classic_dark_compact classic_light_compact retro_blue_compact user_compact
    Bye!

**Change multiples parameters** (open text editor):

.. code:: bash

    naivecalendar update-themes --all-parameters --editor kate

::

    Start updating files............................................................................................................
    Updated parameters:
                  USER_LOCALE           DAY_ABBR_LENGHT            FIRST_DAY_WEEK

    In themes :
                   blackboard               carbon_gold              classic_dark      classic_dark_compact
        classic_dark_extended      classic_dark_variant             classic_light     classic_light_compact
        ...
    Bye!


**Add new event:**

.. code:: bash

    naivecalendar add-event --new Notes1 --value .my_notes/note-%d-%m-%y.txt



