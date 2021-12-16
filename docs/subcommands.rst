Subcommands
===========

Subcommands permit the user to modify theme in mass. 

add-event
^^^^^^^^^

.. include:: ../tools/naivecalendar-add-event
   :start-line: 4
   :end-line: 17

---------------------------------

update
^^^^^^

.. include:: ../tools/naivecalendar-update
   :start-line: 34
   :end-line: 54

Examples
^^^^^^^^

Change a parameter in all themes:

.. code:: bash

    naivecalendar update --parameter USER_LOCALE --value es_ES.utf8

:: 

    setting parameter USER_LOCALE to es_ES.utf8
    27 files Updated:
    blackboard carbon_gold classic_dark classic_dark_compact classic_dark_extended classic_dark_variant classic_light classic_light_compact classic_light_extended classic_light_variant classic_material_red lead_pencil magnolia material_darker modern_blue modern_wedgewood paper-float pastel-blue retro_blue_compact round_light_nord slate square_nord user_classic user_compact user_extended user_sparse user_variant
    Bye!

Change a parameter on choosen themes:

.. code:: bash

    naivecalendar update --parameter PROMT_DATE_FORMAT --value "%d-%m-%Y" --filter ".*compact" 

::

    setting parameter PROMT_DATE_FORMAT to %d-%m-%Y \n
    4 files Updated:
    classic_dark_compact classic_light_compact retro_blue_compact user_compact
    Bye!

Change multiples parameters (open text editor):

.. code:: bash

    naivecalendar update --all-parameters --editor kate

::

    Start updating files............................................................................................................
    Updated parameters:
                  USER_LOCALE           DAY_ABBR_LENGHT            FIRST_DAY_WEEK

    In themes :
                   blackboard               carbon_gold              classic_dark      classic_dark_compact
        classic_dark_extended      classic_dark_variant             classic_light     classic_light_compact
       classic_light_extended     classic_light_variant      classic_material_red               lead_pencil
                     magnolia           material_darker               modern_blue          modern_wedgewood
                  paper-float               pastel-blue        retro_blue_compact          round_light_nord
                        slate               square_nord              user_classic              user_compact
                user_extended               user_sparse              user_variant
    Bye!


Add new events:

.. code:: bash

    naivecalendar add-event --new Notes1 --value .my_notes/note-%d-%m-%y.txt



