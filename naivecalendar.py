#!/usr/bin/env python3
"""
A simple calendar made with rofi and python3.
Cycle through month and create linked note to days.

rofi theme by adi1090x : https://github.com/adi1090x/polybar-themes
"""

__author__ = "Daguhh"
__license__ = "MIT"
__status__ = "Dev"


import datetime
import calendar
from itertools import chain
import subprocess
import glob, os
import re

import sys


# Don't touch those one!
COL_NB = 7
ROW_NB = 8
HOME = os.getenv("HOME")

# Do what you want!
EDITOR = "kate"
NOTES_PATH = f"{HOME}/.naivecalendar_notes"


def main():
    """
    Display a calendar with rofi
    Calendar is interactive :
        - switch between month
        - open {EDITOR} and create a note for selected day
    """

    if not os.path.exists(NOTES_PATH):
        os.mkdir(NOTES_PATH)

    d = calendar.datetime.date.today()

    while True:

        cal = get_calendar_from_date(d)

        actual_month = d.strftime("%b %Y")
        notes_inds = get_month_notes_ind(d)
        today_ind = cal2rofi_ind(d.day, d)
        rofi = gen_rofi_conf(actual_month, notes_inds, today_ind)

        out = show_rofi_calendar(rofi, cal)

        if out == "<" or out == "p":
            d = add_months(d, -1)
        elif out == ">" or out == "n":
            d = add_months(d, 1)
        elif out == " ":
            print("Vous glissez entre les mois, vous perdez la notion du temps.")
        elif out in "LMJVSD":
            print("Ceci n'est pas un jour! R.Magritte.")
        elif {*out}.issubset({*"0123456789"}):
            #print(f"Vous avez selectionné le {out}/{d.month}/{d.year}")
            cmd = f"{EDITOR} {NOTES_PATH}/{d.year}-{d.month}-{out}.txt"
            subprocess.check_output(cmd, shell=True)
        elif out == "notes":
            notes_heads = get_month_notes_heads(d)
            rep = show_rofi(notes_heads, "liste des notes")
            print(rep)
        elif out == "help":
            display_help()
        else:
            print(out)


def intercept_rofi_kill(func):

    def wrapper(*args):
        try :
            out = func(*args)
        except subprocess.CalledProcessError as e:
            print('Bye')
            sys.exit()
        return out

    return wrapper

def display_help():

    txt = """This is an interactive calendar
here some tips:
- click or press enter on arrow to cycle through month
- type "p" or "n" to cycle through month
- interact with day number to add a note
- type "notes" to show all month's notes titles
- type "help" to display this help again
"""

    show_rofi(txt, "help:")


def get_month_notes_heads(date):
    """Return a list of file's first line"""

    note_lst = get_month_notes(date)

    heads = [get_note_head(n) for n in note_lst]

    return "".join(heads)


def get_note_head(note_path):
    """Return first line of a text file"""

    with open(note_path, "r") as f:
        head = f.read()
    return head


def rofi2cal_ind(ind):
    """ Convert coordinate from rofi to day number """
    pass


def cal2rofi_ind(ind, date):
    """Convert calendar date into coordinates for rofi"""
    # correct day offset
    ind = int(ind) - 1 # make month start at 0
    start, _ = calendar.monthrange(date.year, date.month)
    ind = ind + COL_NB + start

    # calendar coordinate
    row, col = ind // COL_NB, ind % COL_NB

    # rofi coordinate
    new_ind = col * ROW_NB + row

    return new_ind


def get_month_notes(date):
    """
    Return index of days that have an attached
    note in $HOME/.naivecalendar_notes/
    """

    # get note of the month list
    file_prefix = f"{date.year}-{date.month}-"
    note_lst = glob.glob(f"{NOTES_PATH}/{file_prefix}*")

    return note_lst


def get_month_notes_ind(date):
    """Return rofi-formatted index of days with attached note"""

    # get file list
    note_lst = get_month_notes(date)
    # get note day
    ind = [re.search(r"([^-]*)\.txt", f).group(1) for f in note_lst]
    # transform into rofi index
    ind = [cal2rofi_ind(int(i), date) for i in ind]
    # format into rofi command
    ind = ",".join([str(i) for i in ind])

    return ind

@intercept_rofi_kill
def show_rofi_calendar(rofi, cal):

    cmd = subprocess.Popen(f"echo '{cal}'", shell=True, stdout=subprocess.PIPE)
    out = (
        subprocess.check_output(rofi, stdin=cmd.stdout, shell=True)
        .decode("utf-8")
        .replace("\n", "")
    )
    return out

@intercept_rofi_kill
def show_rofi(txt_body, txt_head):
    """Launch a rofi window

    :param txt_body: text to Display
    :param txt_head: text to display in rofi prompt
    :type txt_body: str
    :type txt_head: str
    """

    cmd = subprocess.Popen(f'echo "{txt_body}"', shell=True, stdout=subprocess.PIPE)
    selection = (
        subprocess.check_output(
            f'rofi -dmenu -p "{txt_head}"', stdin=cmd.stdout, shell=True
        )
        .decode("utf-8")
        .replace("\n", "")
    )

    return selection


def weekly_transpose(cal):
    """transpose (math) a line by line list into column by column list

    for example, with an hypothetic 3 days week:

    :Example:

    >>> my_list = [1,2,3,4,5,6]
    >>> weekly_transpose(my_list)
    [1,4,2,5,3,6]

    """

    # split calendar into week
    iter_week = range(len(cal) // COL_NB)
    cal = [cal[i * COL_NB : (i + 1) * COL_NB] for i in iter_week]

    # transpose calendar
    iter_day = range(len(cal[0]))
    cal = [[row[i] for row in cal] for i in iter_day]

    # pack it into a lisr
    cal = list(chain(*cal))

    return cal


def add_months(sourcedate, months):
    """ go trough years by summing month"""

    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def get_calendar_from_date(date):
    """
    Return a montly calendar given {date}
    Calendar is a list formated to be shown by rofi (i.e. column bu column)
    """

    start_day, month_length = calendar.monthrange(date.year, date.month)

    # init calendar with 5 blank week
    cal = [" "] * 6 * COL_NB

    # fill with day numbers
    cal[start_day : month_length + start_day] = range(1, month_length + 1)

    # add head : day name, tail : switch month
    cal = list(
        chain(["L", "M", "M", "J", "V", "S", "D"], cal, ["<", "", "", "", "", "", ">"])
    )

    # Format calendar for rofi (column by column)
    cal = weekly_transpose(cal)

    cal = "\n".join((str(c) for c in cal))

    return cal


def gen_rofi_conf(text, urgent, day_ind):
    """
    Create a rofi command
    theme by adi1090x : https://github.com/adi1090x/polybar-themes
    """

    rofi = f"""

        # Custom Rofi Script

        BORDER="#1F1F1F"
        SEPARATOR="#1F1F1F"
        FOREGROUND="#FFFFFF"
        BACKGROUND="#1F1F1F"
        BACKGROUND_ALT="#252525"
        HIGHLIGHT_BACKGROUND="#8e24aa"
        HIGHLIGHT_FOREGROUND="#1F1F1F"

        BLACK="#000000"
        WHITE="#ffffff"
        RED="#e53935"
        GREEN="#43a047"
        YELLOW="#fdd835"
        BLUE="#1e88e5"
        MAGENTA="#00897b"
        CYAN="#00acc1"
        PINK="#d81b60"

        rofi -dmenu -p "{text}" \
        -show calendrier \
        -hide-scrollbar true \
        -bw 0 \
        -a 0,8,16,24,32,40,48 \
        -u {urgent} \
        -selected-row {day_ind} \
        -lines {ROW_NB} \
        -line-padding 5 \
        -padding 10 \
        -width 25 \
        -xoffset 320 -yoffset 25 \
        -location 2 \
        -columns {COL_NB}\
        -color-enabled true \
        -color-window "$BACKGROUND,$BORDER,$SEPARATOR" \
        -color-normal "$BACKGROUND_ALT,$FOREGROUND,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" \
        -color-active "$BACKGROUND,$BLUE,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" \
        -color-urgent "$BACKGROUND,$YELLOW,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" """

    return rofi


if __name__ == "__main__":
    main()
