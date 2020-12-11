#!/usr/bin/env python3
"""
A simple calendar made with rofi and python3.

Cycle through month and create linked note to days.

rofi theme by adi1090x : https://github.com/adi1090x/polybar-themes
"""

__author__ = "Daguhh"
__license__ = "MIT-0"
__status__ = "Dev"


import glob, os
import sys
import subprocess
import shutil
import re
import datetime
import calendar
import locale
from itertools import chain
from functools import wraps
import argparse
import configparser
import time

##################################################
############# User parameters ####################
##################################################

# Locate
USER_LOCALE = "" # keep empty to get system locale, use 'locale -a" on your system to list locales

# Week parameters
DAY_ABBR_LENGHT = 3 # day name lenght
FIRST_DAY_WEEK = 1 # 0 : sunday, 1 : monday...
SYM_WEEK_DAYS = [] # day names list, if empty, locale names will be set

# Notes conf
NOTES_RELATIVE_PATH = ".naivecalendar_notes" # path to save notes (retative to $HOME)
NOTES_DATE_FORMAT = "%Y-%m-%d" # strftime format, contains at least %d and month (%b, %m...)  + year (%Y...) identifier

# Rofi/Calendar shape
COL_NB = 7  # 7 days
WEEK_NB = 6  # number of "complete" weeks, a month can extend up to 6 weeks
ROW_NB = 1 + WEEK_NB + 1  # 1 day header + 6 weeks + 1 control menu

# Calendar symbols and shorcuts
SYM_NEXT_MONTH = [">", "+", "n"]  # 1st symbol : displayed, others : shortcuts
SYM_NEXT_YEAR = [">>", "++", "nn"]
SYM_PREV_MONTH = ["<", "-", "p"]
SYM_PREV_YEAR = ["<<", "--", "pp"]
SYM_DAYS_NUM = [str(n) for n in range(1, 32)]
SYM_NOTES = ["notes"]
SYM_HELP = ["help"]

# Other display parameters
PROMT_DATE_FORMAT = "%b %Y"
IS_TODAY_HEAD_MSG = True # toogle day num and name header display

##################################################
######### End User parameters ####################
##################################################


# create path to notes
HOME = os.getenv("HOME")
NOTES_PATH = f"{HOME}/{NOTES_RELATIVE_PATH}"

CACHE_PATH = f"{HOME}/.cache/naivecalendar"
DATE_CACHE = f"{CACHE_PATH}/date_cache.ini"
PP_CACHE = f"{CACHE_PATH}/pretty_print_cache.txt"


##################################################
############ Script ##############################
##################################################


def main():
    """
    Display a calendar with rofi
    Calendar is interactive :

    - switch between month
    - open {EDITOR} and create a note for selected day
    """
    args, rofi_output = get_arguments()

    # Get locale week days, override WEEKS_DAYS variable to personalize day names
    if not args.locale:
        locale.setlocale(locale.LC_ALL, USER_LOCALE)
    else:
        locale.setlocale(locale.LC_ALL, args.locale)
    global SYM_WEEK_DAYS
    if not SYM_WEEK_DAYS:
        get_loc_day = lambda d, l: locale.nl_langinfo(locale.DAY_1 + d)[:l].title()
        week_order = chain(range(FIRST_DAY_WEEK, 7), range(0, FIRST_DAY_WEEK))
        SYM_WEEK_DAYS = [get_loc_day(x, DAY_ABBR_LENGHT) for x in week_order]

    # create note path n test rofi intall
    first_time_init()

    # read previous date or show actual month on first loop
    d = Date()
    if rofi_output or args.read_cache:
        d.read_cache()
    else:
        d.today()

    # react to rofi date change output
    out = rofi_output
    if out in SYM_PREV_YEAR:
        d.year -= 1
    elif out in SYM_PREV_MONTH:
        d.month -= 1
    elif out in SYM_NEXT_MONTH:
        d.month += 1
    elif out in SYM_NEXT_YEAR:
        d.year += 1

    # generate new datas
    date = d.date
    cal = get_calendar_from_date(date)
    date_prompt = date.strftime(PROMT_DATE_FORMAT).title()
    notes_inds = get_month_notes_ind(date)
    today_ind = cal2rofi_ind(date.day, date.month, date.year)

    # send datas
    # A_,d_,B_,Y_ = [date.strftime(x) for x in ['%A', '%d', '%B', '%Y']]
    print(f"\0prompt\x1f{date_prompt}\n")
    print(f"\0urgent\x1f{notes_inds}\n")
    if not rofi_output:
        print(f"\0active\x1f{today_ind}\n")
        if IS_TODAY_HEAD_MSG:
            day_numb = f"""<span size="xx-large" >{date.strftime('%d')}</span>"""
            day_name = f"""<span rise="12000" size="small">{date.strftime('%A')}</span>"""
            print(f"\0message\x1f{day_numb} {day_name}\n")
    #else:
    #    msg = """<span size="xx-small">A</span>"""
    #    print(f"""\0message\x1f\n""")

    print(f"\0active\x1fa 0,8,16,24,32,40,48\n")
    print(cal)

    # write new date in buffer
    d.write_cache()

    # react to rofi output
    if out in SYM_DAYS_NUM:
        if args.print:
            print_selection(out, d.date, args.format)
        else:
            open_note(out, d.date, args.editor)
    elif out in SYM_NOTES:
        show_notes(d.date)
    elif out in SYM_HELP:
        display_help()
    elif out == " " or out in SYM_WEEK_DAYS:
        joke(out)
    else:
        pass
        # print('No output',file=sys.stderr)


def get_calendar_from_date(date):
    r"""Return a montly calendar given date

    Calendar is a string formated to be shown by rofi (i.e. column bu column)::

                 L  M  M  J  V  S  D
                                   1
                 2  3  4  5  6  7  8
      date  ->   9 10 11 12 13 14 15   ->   'L\n \n2\n9\n16\n23\n30\n<\nM\n \n3\n10\n17\n24\n...'
                16 17 18 19 20 21 22
                23 24 25 26 27 28 29
                30

    Parameters
    ----------
    date : datetime.date
        Any day of the month to display

    Returns
    -------
    str
        A str that contain chained columns of a calendar in a rofi format

    """

    start_day, month_length = calendar.monthrange(date.year, date.month)

    # init calendar with WEEK_NB blank week
    cal = [" "] * WEEK_NB * COL_NB

    # fill with day numbers
    cal[start_day : month_length + start_day] = [
        str(n) for n in range(1, month_length + 1)
    ]

    # create menu bar
    cal_menu = [" "] * COL_NB
    cal_menu[:2] = [SYM_PREV_YEAR[0], SYM_PREV_MONTH[0]]
    cal_menu[-2:] = [SYM_NEXT_MONTH[0], SYM_NEXT_YEAR[0]]

    # chain calendar elements
    cal = list(chain(SYM_WEEK_DAYS, cal, cal_menu))

    # Format calendar for rofi (column by column)
    cal = list_transpose(cal)

    # format data to be read by rofi (linebreak separated elements)
    cal = list2rofi(cal)

    return cal


def rofi_transpose(rofi_datas, column_number=COL_NB):
    """
    Transpose (math) a row by row rofi-list into column by column rofi-list
    given column number

    Parameters
    ----------
    lst : str
        row by row elements
    col_nb : int
        number of column to display

    Returns
    -------
    str
        A rofi-list, column by column elements

    Examples
    --------

    >>> by_row = "1\\n2\\n3\\n4\\n5\\n6"
    >>> rofi_transpose(by_row, 3)
    "1\\n4\\n2\\n5\\n3\\n6"

    """

    byrow_datas = rofi2list(rofi_datas)
    bycol_datas = list_transpose(byrow_datas, column_number)

    return list2rofi(bycol_datas)


def list_transpose(lst, col_nb=COL_NB):
    """
    Transpose (math) a row by row list into column by column list
    given column number

    Parameters
    ----------
    lst : list
        row by row elements
    col_nb : int
        number of column to display

    Returns
    -------
    list
        A list that represent column by column elements

    Examples
    --------
    >>> my_list = [1,2,3,4,5,6]
    >>> list_transpose(my_list, col_nb=3)
    [1,4,2,5,3,6]

    """

    # split into row
    iter_col = range(len(lst) // col_nb)
    row_list = [lst[i * col_nb : (i + 1) * col_nb] for i in iter_col]

    # transpose : take 1st element for each row, then 2nd...
    iter_row = range(len(row_list[0]))
    col_list = [[row[i] for row in row_list] for i in iter_row]

    # chain columns
    lst = list(chain(*col_list))

    return lst


def list2rofi(datas):
    """
    Convert python list into a list formatted for rofi

    Parameters
    ----------
    datas : list
        elements stored in a list

    Returns
    -------
    str
        elements separated by line-breaks

    Examples
    --------

    >>> my_list = [1,2,3,4,5,6]
    >>> list2rofi(my_list]
    "1\\n2\\n3\\n4\\n5\\n6"
    """

    return "\n".join(datas)


def rofi2list(datas):
    """
    Convert list formatted for rofi into python list object

    Parameters
    ----------
    datas : str
        a string with element separeted by line-breaks

    Returns
    -------
    list
        elements of datas in a list

    Examples
    --------

    >>> rofi_list = "1\\n2\\n3\\n4\\n5\\n6"
    >>> rofi2list
    [1,2,3,4,5,6]
    """

    return datas.split("\n")


def get_month_notes_heads(date):
    """
    Return a list of file's first line of a specific month

    Parameters
    ----------
    date : datetime.date
        Any day of the month to display

    Returns
    -------
    str
        A rofi formatted list of month's notes first line
    """

    note_lst = get_month_notes(date)

    heads = [get_note_head(n) for n in note_lst]
    prompts = [n.split(".")[-2].split("/")[-1] for n in note_lst]

    return "\n".join([f"{p} : {h}" for p, h in zip(prompts, heads)])


def get_note_head(note_path):
    """
    Return first line of a text file

    Parameters
    ----------
    note_path : str
        A text file path

    Returns
    -------
    str
        First line of the text file
    """

    with open(note_path, "r") as f:
        head = f.read().split("\n")[0]
    return head


def rofi2cal_ind(ind):
    """ Convert coordinate from rofi to day number """
    pass


def cal2rofi_ind(day, month, year):
    """
    Convert calendar date into coordinates for rofi

    Parameters
    ----------
    day : int
        A day number (1-31)
    month : int
        A month number (1-12)
    year : int
        A year number

    Returns
    -------
    int
        A rofi index
    """
    # correct day offset
    day = int(day) - 1  # make month start at 0
    start, _ = calendar.monthrange(year, month)
    ind = day + COL_NB + start

    # calendar coordinate
    row, col = ind // COL_NB, ind % COL_NB

    # rofi coordinate
    new_ind = col * ROW_NB + row

    return new_ind


def get_month_notes(date):
    """
    Return notes files paths that are attached to date's month

    Parameters
    ----------
    date : datetime.date
        Any day of the month displayed

    Returns
    -------
    list
        list of files that belong to date.month
    """

    pattern = NOTES_DATE_FORMAT.replace('%d', '*')
    file_prefix = date.strftime(pattern) #f"{date.year}-{date.month}-"
    note_lst = glob.glob(f"{NOTES_PATH}/{file_prefix}*")

    return note_lst


def get_month_notes_ind(date):
    """
    Return rofi-formatted index of days with attached note

    Parameters
    ----------
    date : datetime.date
        Any day of the month displayed

    Returns
    -------
    str
        Column index list formatted for rofi
    """

    # get file list
    note_lst = get_month_notes(date)
    # get note day number
    pattern = re.sub('%d',r'([0-9]*)', NOTES_DATE_FORMAT)
    pattern = re.sub('%.','[a-zA-Z0-9]*', pattern)
    days = [re.match(pattern, f.split('/')[-1]).group(1) for f in note_lst]
    # transform into rofi index
    ind = [cal2rofi_ind(int(d), date.month, date.year) for d in days]
    # format into rofi command
    ind = ",".join([str(i) for i in ind])

    return ind


def open_n_reload_rofi(func):
    """ decorator to open and reload the rofi script at the same date"""

    script_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    @wraps(func)
    def wrapper(*args, **kwargs):

        subprocess.Popen(["pkill", "-9", "rofi"])
        out = func(*args)
        cmd = f"{script_path}/naivecalendar.sh -c"
        os.system(cmd)

        return out

    return wrapper


@open_n_reload_rofi
def show_notes(date):
    """open rofi popup with notes list of selected month"""

    notes_heads = get_month_notes_heads(date)
    text_popup("Notes", notes_heads)


@open_n_reload_rofi
def open_note(day, date, editor):
    """open note for the selected date"""

    note_name = datetime.date(date.year, date.month, int(day)).strftime(NOTES_DATE_FORMAT)
    note_path = f"{NOTES_PATH}/{note_name}.txt"
    cmd = f"touch {note_path} & {editor} {note_path}"
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    sdtout, sdterr = p.communicate()


def print_selection(day, date, f):
    """return select date to stdout given cmd line parameter '--format'"""

    d = int(day)
    m = date.month
    y = date.year

    pretty_date = datetime.date(y, m, d).strftime(f)
    with open(PP_CACHE, "w") as f:
        f.write(pretty_date + "\n")

    sys.exit(0)


def first_time_init():
    """Create config files and paths given script head variables"""

    if shutil.which("rofi") == None:
        print("please install rofi")
        sys.exit()

    if not os.path.exists(NOTES_PATH):
        os.mkdir(NOTES_PATH)
        display_help(head_txt="Welcome to naivecalendar")

    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)


class Date:
    """Class to store date
    Make easier reading and writing to date cache file
    """

    def __init__(self):

        self.today()
        self._cache = configparser.ConfigParser()
        self.year = Year(self)
        self.month = Month(self)

    def today(self):
        """Set and return today date"""
        self.date = datetime.date.today()
        return self.date

    def read_cache(self):
        """load cache ini file"""

        self._cache.read(DATE_CACHE)
        day = 1
        month = int(self._cache["buffer"]["month"])
        year = int(self._cache["buffer"]["year"])

        self.date = datetime.date(year, month, day)

    def write_cache(self):
        """write date to ini cache file"""

        date = self.date
        self._cache["buffer"] = {"year": date.year, "month": date.month}
        with open(DATE_CACHE, "w") as buff:
            self._cache.write(buff)


class Year:
    """Make computation on date years"""
    def __init__(self, outer):
        self.outer = outer

    def __repr__(self):
        return f"Year({self.outer.date.year})"

    def __add__(self, years):
        """
        Increment or decrement date by a number of years

        Parameters
        ----------
        sourcedate : datetime.date
            Date to Increment
        months : int
            number of years to add

        Returns
        -------
        datetime.date
            Incremented date
        """

        year = self.outer.date.year + years
        month = self.outer.date.month
        day = min(self.outer.date.day, calendar.monthrange(year, month)[1])
        self.outer.date = datetime.date(year, month, day)

    def __sub__(self, years):
        self.__add__(-years)


class Month:
    """Make computation on date months"""
    def __init__(self, outer):
        self.outer = outer

    def __repr__(self):
        return f"Month({self.outer.date.month})"

    def __add__(self, months):
        """
        Increment or decrement date by a number of month

        Parameters
        ----------
        sourcedate : datetime.date
            Date to Increment
        months : int
            number of month to add

        Returns
        -------
        datetime.date
            Incremented date
        """

        month = self.outer.date.month - 1 + months
        year = self.outer.date.year + month // 12
        month = month % 12 + 1
        day = min(self.outer.date.day, calendar.monthrange(year, month)[1])

        self.outer.date = datetime.date(year, month, day)
        # return datetime.date(year, month, day)

    def __sub__(self, months):
        self.__add__(-months)


def get_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description="""A simple popup calendar""")

    parser.add_argument(
        "-p",
        "--print",
        help="print date to stdout instead of opening a note",
        action="store_true",
    )

    parser.add_argument(
        "-f",
        "--format",
        help="""option '-p' output format (datetime.strftime format, defaut='%%Y-{%%m}-%%d')""",
        dest="format",
        default="%Y-%m-%d",
    )

    parser.add_argument(
        "-e",
        "--editor",
        help="""editor command to open notes""",
        dest="editor",
        default="xdg-open",
    )

    parser.add_argument(
        "-l",
        "--locale",
        help="""force system locale, for example '-l es_ES.utf8'""",
        dest="locale",
        default="",
    )

    parser.add_argument(
        "-c",
        "--read-cache",
        dest="read_cache",
        action="store_true",
    )

    args, unknown = parser.parse_known_args()
    unknown = unknown if len(unknown) == 0 else "".join(unknown)

    return args, unknown


def joke(sym):
    """Just display stupid jokes in french"""

    if sym == " ":
        print(
            "Vous glissez entre les mois, vous perdez la notion du temps.",
            file=sys.stderr,
        )
    elif sym in SYM_WEEK_DAYS:
        print("Ceci n'est pas un jour! R.Magritte.", file=sys.stderr)


def text_popup(head, body):
    """ Display a popup msg with tkinter

    Parameters
    ----------
    head :
        str : window title
    body :
        str : message to Display
    """

    import tkinter as tk
    import tkinter.scrolledtext as st

    win = tk.Tk()
    win.title(head)
    text_area = st.ScrolledText(win, width=50, height=12, font=("Noto Sans", 10))
    text_area.grid(column=0, pady=10, padx=10)
    text_area.insert(tk.INSERT, body)
    text_area.configure(state="disabled")
    win.mainloop()


@open_n_reload_rofi
def display_help(head_txt="help:"):
    """Show a rofi popup with help message"""

    txt = f"""This calendar is interactive. Here some tips:

 - Use mouse or keyboard to interact with the calendar.
 - Hit bottom arrows to cycle through months.
 - Hit a day to create a linked note.
(A day with attached note will appear yellow.)
 - Notes are stored in {HOME}/.naivecalendar_notes/
(For now you've to manually delete it)

There's somme shortcut too, type it in rofi prompt :

       -- : go to previous year
   n or - : go to previous month
   p or + : go to next month
 pp or ++ : go to next year
    notes : display notes of the month (first line)
     help : display this help

There's some command line option too, dislay it with :
    ./naivecalendar -h

That's all :

close window to continue...
"""

    text_popup("Help", txt)


if __name__ == "__main__":
    main()
