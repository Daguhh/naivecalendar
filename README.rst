=============
NaïveCalendar
=============

A popup calendar with rofi_ and python3_

|readme_fr| |git_badge| |doc sphinx| |deb package|

**naïf, naïve n. adj**.

    `1.` *LITTERAIRE* Qui est naturel, sans artifice, spontané. Art naïf, art populaire, folklorique. —  Un peintre naïf.

    `2.` *COURANT* Qui est plein de confiance et de simplicité par ignorance, par inexpérience. ➙ candide, ingénu, simple. —  Qui exprime des choses simples que tout le monde sait. Remarque naïve. ➙ simpliste.

    -- LeRobert_

|classic dark extended| |classic light extended|

`see all themes <https://framagit.org/Daguhh/naivecalendar/-/blob/master/docs/themes.rst>`_

Features
--------
 
* **Interactive** : Cycle through calendar months by months, years by years.
* **Locale support** : Automatic or force desired one
* **Events** : Create notes linked to days, create multiple notes types, switch between them, (link to other app?), display your caldav events
* **Customize** : change themes, content, symbols, shortcuts with text files, switch on the fly
* **Integrate** : use it in your scripts and make them more interactive: open on a particular date, request a date, copy-to-clipboard. 

.. admonition:: Author note

    This script/programm/app/whatever you call it, is a spare time and learning purpose project, nevertheless I hope you will find it useful. I intended this rofi_ diversion to be used with `my polybar/i3 installation <https://framagit.org/Daguhh/naivecalendar/-/wikis/home>`_. 
    
    Although it's seems working fine to me, there might be still some (ok, there are) bugs, so feel free to open an issue for any comment or consideration.

.. _contents:

.. contents:: Table of Contents
    :depth: 1

---------------------------------------------------------------------------------

.. _installation:

Dependancies
------------

Requirements
^^^^^^^^^^^^

* python3_ (stdlib)
* rofi_

Recommends
^^^^^^^^^^

* xclip (copy to clipboard option)
* sensible-utils (choose editor in update subcommand)
* python3-caldav (show caldav events in calendar (very light support))

Suggests
^^^^^^^^

* fontawesome (for icons)

Install
-------

Manually
^^^^^^^^

The naivecalendar use two files:

- **naivecalendar.py** : that print a list-formatted calendar entries to sdtout
- **naivecalendar.sh** : that run rofi in script mode with the previous file

Plus, a couple of theme files:

- **<theme>.rasi** : rofi configuration file (shape and colors)
- **common/<element>.rasi** : rasi theme file dependancies (combine shape, colors position...)  
- /themes/**<theme>.cfg** : an ini file that define calendar content

Simply copy those files (src folder content) in the same place (.ie : keep the tree as it is), remove as many theme as you want, but please keep at least *classic_dark_extended* default theme. 

Here is the simplest doable installation tree ::

    .
    ├── naivecalendar.py
    ├── naivecalendar.sh
    └── themes
        ├── classic_dark_extended.cfg
        ├── classic_dark_extended.rasi
        └── common
            ├── position.rasi
            ├── shape_base.rasi
            ├── shape_extended.rasi
            ├── theme_base.rasi
            └── theme_dark.rasi


Then, Launch with:: 

    ./naivecalendar.sh 

Package (debian)
^^^^^^^^^^^^^^^^

.. code:: bash

    apt install ./naivecalendar_x.y.z_all.deb

Launch with:

.. code:: bash

    naivecalendar

Makefile
^^^^^^^^

Edit **Makefile.config** to customize your installation, then run:

.. code:: bash

    make install

Get more info :

.. code:: bash

    make help

Launch with:

.. code:: bash

    naivecalendar

---------------------------------------------------------------------------------

.. _usage:

Usage
-----

Basic
^^^^^

Simply execute the script, then, Use mouse or keyboard to interact with the calendar:

- Hit arrows to cycle through months or years
- Hit a day to create a linked event. *(day change color as it has a linked event)*
- Hit menu button to switch theme, switch event type, show month events

Shortcuts
^^^^^^^^^

Shortcuts have to be entered in the rofi command prompt. 
Those are default shortcuts, it can vary along themes and can be modified in <theme>.cfg files.
*Sym* is the symbol displayed, you can type either *Sym* or *Keys* to execute an action

====  ======  =======  ========  ========================================
Sym     Keys                     Action
----  -------------------------  ----------------------------------------
  ..      ..       ..        ..  ..
====  ======  =======  ========  ========================================
 ◀◀       <<       pp       --   go to previous year
  ◀        <        p      `-`   go to previous month
  ▶        >        n      `+`   go to next month
 ▶▶       >>       nn       ++   go to next year
      event       ee       ..   display events of the month (first line)
     switch       ss       ..   switch event type (open another folder)
       help       hh       ..   display this help
      theme       tt       ..   display theme selector
  ☰     menu       mm       ..   display menu 
====  ======  =======  ========  ========================================


.. _Events:

Events
^^^^^^

Events are simply files (usally text files) created by the calendar when you interact with a day (click/return key)
On interaction, your default editor will open the event file. (see Customize/Events section for formatting advices)
On editor closing, calendar will reopen and the day with a linked note will appear colored.

A script in avaible in calendar menu to show event from online calendar - using caldav -, that's a very light support,
you can only show events on calendar (day, time, description, location), but you won't be able to sync or push new event to it.
(see `scripts/caldav2file.py <https://framagit.org/Daguhh/naivecalendar/-/blob/master/src/scripts/caldav2file.py>`_  file for details)

Options
^^^^^^^

Some command line options are avaible and can be useful if you want to integrate the naivecalendar in a script or temporarily override parameters.
Subcommands **update-themes** could be useful to update all theme config at once instead of doing it manually (use completion).


    **usage:** *naivecalendar* [-h] [-V] [-v] [-p] [-x] [-f FORMAT] [-e EDITOR] [-l LOCALE] [-c] [-t THEME] [-d DATE]

    A simple popup calendar

    **subcommands:**
      | update-themes       Update a calendar parameter for all user themes at once
      | add-event           Add or delete event
      | configure           Clone or open configuration files


    **optional arguments:**
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -v, --verbose         direct rofi command errors to stdout
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


.. _customize:

Customize
---------

To customize the calendar (without altering installation files), you can start with a copy of them in the user config folder:

Manually :

.. code:: bash

    # Themes
    cp -r /usr/share/naivecalendar/themes/* ~/.config/naivecalendar/themes/

    # Events
    cp -r /usr/share/naivecalendar/global/events.cfg  ~/.config/naivecalendar/global/events.cfg

    # Scripts
    cp -r /usr/share/naivecalendar/global/custom_actions.cfg  ~/.config/naivecalendar/global/custom_actions.cfg
    cp -r /usr/share/naivecalendar/scripts/*  ~/.config/naivecalendar/scripts/

With subcommand:

.. code:: bash

    naivecalendar configure --clone <config file>




Themes
^^^^^^

A theme consist of two files :

- `theme.cfg`_ : an ini file, configure calendar content
- `theme.rasi`_ : a rofi theme file, configure apperance (color, size, layout...)

.. warning::

   Number of rows in rofi (*.rasi*) should match content configuration (*.cfg*)! See more details in .cfg files.

Some `themes are avaibles <https://framagit.org/Daguhh/naivecalendar/-/blob/master/docs/themes.rst>`_, set them by typing *theme* in rofi prompt or temporarily load them with :code:`--theme` argument. To create your own theme, create a `rasi <https://github.com/davatorium/rofi/blob/next/doc/rofi-theme.5.markdown>`_ file and a cfg file in *~/.config/naivecalendar/themes*. 

You can start from a copy of "officials" themes, with :code:`configure` subcommand or manually:

.. code:: bash

    cp -r /usr/share/naivecalendar/themes/* ~/.config/naivecalendar/themes/

.. note::

    If it exist two themes with the same name in differents folders, the one in *$HOME/.config/...* will be prevalent over the others

Then modify themes one by one with your favourite editor or use naivecalendar subcommand to update multiples themes at once (cfg files only)

.. code:: bash

    naivecalendar update-themes -h

.. admonition:: Author

   Proposed themes are more examples than official. I intented this calendar to easily match all user configurations and to be easily configurable.
   There is no specific tool to update .rasi files, but they (almost all) share some ressources in *themes/common/*, commonly:

   - a color theme : **theme_<color_name>.rasi**
   - a position on the screen : **position.rasi**
   - a shape (contain number of row) : **shape_<kind>.rasi**

   So you can easily mix them to customize calendar aspect or modify independently colors and shapes.

Events
^^^^^^

Events files names should contain `strftime <https://strftime.org/>`_  directives (%d, %m ...) to appear in the calendar. 

.. code:: ini

    note_%Y-%m-%d.txt

Not giving it a year directive will make it occur every year (usefull for birthday isn't it?)

.. code:: ini

    birthday_on_%d-%m.txt

The calendar handle multiple events types (that are simply differents folders), you can define new event type by adding an entry in [EVENTS] section in *.config/naivecalendar/global/event.cfg*. Paths are relative to user's home.

.. code:: ini

    [EVENTS]

    Notes = .naivecalendar_events/MyNotes/note_%Y-%m-%d.txt
    Birthday = .naivecalendar_events/Birthdays/birthday_on_%d-%m.txt

Notes support a very light format to be parsed when displaying "events of the month" :

- show section : if you create sections (format : [section]) all lines containing a section will be displayed 
  
  .. code:: ini

    [9H30 -> 10H] short description <---- will be displayed
    Long 
    multilines
    description...
    [14H30] rdv with bidulle <----- will be displayed
    Some text again again

- show header : if the event/note don't contain section, only first line will be displayed
  
  .. code:: ini

    # Note Title  <---- only first line is displayed
    Some text
    Some text again...

if you interact with the event file name, it will open the note again, other rows will bring you back to calendar

.. code:: ini

    notes_2021-01-05 : <---- reopen editor
    [9H30 -> 10H] short description  <--- do nothing : back to calendar
    [14H30] rdv with bidulle


Custom actions
^^^^^^^^^^^^^^

User can also create is own custom action i.e. create a button that launch user's script.
To add a custom action please, put your script in *~/.config/naivecalendar/script/*, then,
edit *~/.config/naivecalendar/global/custom_actions.cfg* to configure the button/shortcut:

  .. code:: ini

    [Shortcut Name] <--- used as id for other conf file
    SYM = Icon, [shortcut_1, shortcut_2], long description   <--- Icon : displayed on calendar
    CMD = path/to/script <--- script or system command            long description : displayed in menu 


.. _files:

Files
-----

Here is a brief description of files needed/generated by the naivecalendar

================================   ================================================================
Function                           File
================================   ================================================================
**Minimal : required**
---------------------------------------------------------------------------------------------------
rofi command                       /usr/share/naivecalendar/**naivecalendar.sh**
script called by rofi              /usr/share/naivecalendar/**naivecalendar.py**
rofi theme files                   /usr/share/naivecalendar/**themes/\*.rasi**
calendar content configuration     /usr/share/naivecalendar/**themes/\*.cfg**
--------------------------------   ----------------------------------------------------------------
**Installation & optional**
---------------------------------------------------------------------------------------------------
system command                     /usr/bin/**naivecalendar**
theme config editor command        /usr/share/naivecalendar/tools/**naivecalendar-update-themes**
theme event editor command         /usr/share/naivecalendar/tools/**naivecalendar-add-event**
manage config files command        /usr/share/naivecalendar/tools/**naivecalendar-configure**
custom actions                     /usr/share/naivecalendar/**global/custom_actions.cfg**
scripts                            /usr/share/naivecalendar/**scripts/\*"**    
events conf                        /usr/share/naivecalendar/**global/events.cfg**   
--------------------------------   ----------------------------------------------------------------
**User themes : optional** (overide installation conf file)
---------------------------------------------------------------------------------------------------
user theme files                   ~/.config/naivecalendar/**themes/\*.rasi**
user content configuration         ~/.config/naivecalendar/**themes/\*.cfg**
user custom actions                ~/.config/naivecalendar/**global/custom_actions.cfg**
user events conf                   ~/.config/naivecalendar/**global/events.cfg**   
user scripts                       ~/.config/naivecalendar/**scripts/\*"**    
--------------------------------   ----------------------------------------------------------------
**Event : editable**
---------------------------------------------------------------------------------------------------
day notes path (default)           ~/.naivecalendar_events/<event type>/**<date format>.txt**
--------------------------------   ----------------------------------------------------------------
**Generated : cache**
---------------------------------------------------------------------------------------------------
remember date throught loops       ~/.cache/naivecalendar/**date_cache.ini**
pass date to bash when -p option   ~/.cache/naivecalendar/**pretty_print_cache.txt**
remember theme after quitting      ~/.cache/naivecalendar/**theme_cache.txt**
remember event type                ~/.cache/naivecalendar/**event_cache.txt**
last rofi command log file         ~/.cache/naivecalendar/**rofi_log.txt**
================================   ================================================================

Build
-----

.. _dev:

.. note::

    You can use the makefile with **make** command to build package and documentation.

Build debian package
^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    sudo apt install devscripts
    cd naivecalendar-x.y.z/
    debuild -us -uc

.. note::

   You can personnalize your themes before building, all themes folder content will be included in the package

Build the doc
^^^^^^^^^^^^^

.. code:: bash

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

.. |classic dark extended| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/classic_dark_extended.png
    :height: 200 px

.. |classic light extended| image:: https://framagit.org/Daguhh/naivecalendar/-/raw/master/docs/screenshots/classic_light_extended.png
    :height: 200 px

.. |doc sphinx| image:: https://framagit.org/Daguhh/naivecalendar/badges/master/pipeline.svg?key_text=Sphinx+doc&key_width=70
    :target: http://daguhh.frama.io/naivecalendar

.. |deb package| image:: https://img.shields.io/badge/deb\ package-2.0.1-blue?logo=data:image/png;base64,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&style=flat-square
    :target: https://acloud.zaclys.com/index.php/s/PBQoqRkMSdAw6Hr/download/naivecalendar_2.0.1_all.deb

