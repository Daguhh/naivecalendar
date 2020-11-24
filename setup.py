
#!/usr/bin/env python3

from setuptools import setup

setup(
    name='NaiveCalendar',
    version='0.0.1',
    url='https://framagit.org/Daguhh/naivecalendar/',
    author = 'Daguhh',
    author_email = 'code.daguhh@zaclys.net',
    maintainer= 'Daguhh',
    maintainer_email = 'code.daguhh@zaclys.net',
    keywords = 'A calendar with rofi and python3',
    license='MIT No Attribution (MIT-0)',
    packages=['naivecalendar'],
    scripts=['naivecalendar/naivecalendar.py'],
    entry_points={
        'console_scripts': [
          'naivecalendar = naivecalendar:main',
        ],
    }
)

