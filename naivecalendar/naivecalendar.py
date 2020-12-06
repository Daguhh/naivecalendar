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


############# Parameters #########################

# day name lenght (enlarge calendar for larger values)
DAY_ABBR_LENGHT = 3
FIRST_DAY_WEEK = 1  # 0 : sunday, 1 : monday...

# path to save notes (retative to $HOME)
NOTES_RELATIVE_PATH = ".naivecalendar_notes"

# rofi shape parameters
# CAL_WIDTH = 320
# CAL_X_OFFSET = 320
# CAL_Y_OFFSET = 25
# CAL_LINE_PADDING = 5
# CAL_PADDING = 10
# CAL_LOCATION = 2

# rofi grid shape to contain calendar
COL_NB = 7  # 7 days
WEEK_NB = 6  # number of "complete" weeks, a month can extend up to 6 weeks
ROW_NB = 1 + WEEK_NB + 1  # 1 day header + 6 weeks + 1 control menu

# Symbols displayed in the calendar
SYM_NEXT_MONTH = [">", "+", "n"]  # first symbol is displayed, others are just shortcuts
SYM_NEXT_YEAR = [">>", "++", "nn"]
SYM_PREV_MONTH = ["<", "-", "p"]
SYM_PREV_YEAR = ["<<", "--", "pp"]
SYM_DAYS_NUM = [str(n) for n in range(1, 32)]
SYM_NOTES = ["notes"]
SYM_HELP = ["help"]

# Rofi prompt date format:
PROMT_DATE_FORMAT = "%b %Y"
# NOTES_DATE_FORMAT = "%Y-%m-%d"

# Get locale week days, override WEEKS_DAYS variable to personalize day names
locale.setlocale(locale.LC_ALL, "")
get_loc_day = lambda d, l: locale.nl_langinfo(locale.DAY_1 + d)[:l].title()
week_order = chain(range(FIRST_DAY_WEEK, 7), range(0, FIRST_DAY_WEEK))
SYM_WEEK_DAYS = [get_loc_day(x, DAY_ABBR_LENGHT) for x in week_order]

# create path to notes
HOME = os.getenv("HOME")
NOTES_PATH = f"{HOME}/{NOTES_RELATIVE_PATH}"

CACHE_PATH = f"{HOME}/.cache/naivecalendar"
DATE_CACHE = f"{CACHE_PATH}/date_cache.ini"
PP_CACHE = f"{CACHE_PATH}/pretty_print_cache.txt"


############ Script ##############################


def main():
    """
    Display a calendar with rofi
    Calendar is interactive :

    - switch between month
    - open {EDITOR} and create a note for selected day
    """
    args, rofi_output = get_arguments()

    # create note path n test rofi intall
    first_time_init()

    # read previous date or show actual month on first loop
    buffer = DateBuffer()
    if rofi_output:
        d = buffer.read()
    else:
        d = calendar.datetime.date.today()

    # react to rofi output
    out = rofi_output
    if out in SYM_PREV_YEAR:
        d = add_year(d, -1)
    elif out in SYM_PREV_MONTH:
        d = add_months(d, -1)
    elif out in SYM_NEXT_MONTH:
        d = add_months(d, 1)
    elif out in SYM_NEXT_YEAR:
        d = add_year(d, 1)
    elif out in SYM_DAYS_NUM:
        if args.print:
            print_selection(out, d, args.format)
        else:
            open_note(out, d, args.editor)
    elif out in SYM_NOTES:
        show_notes(d)
    elif out in SYM_HELP:
        display_help()
    elif out == " " or out in SYM_WEEK_DAYS:
        joke(out)
    else:
        pass
        # print('No output',file=sys.stderr)

    # send new data to rofi
    cal = get_calendar_from_date(d)
    date_prompt = d.strftime(PROMT_DATE_FORMAT).title()
    notes_inds = get_month_notes_ind(d)
    today_ind = cal2rofi_ind(d.day, d.month, d.year)

    print(f"\0prompt\x1f{date_prompt}\n")
    print(f"\0urgent\x1f{notes_inds}\n")
    if not rofi_output:
        print(f"\0active\x1f{today_ind}\n")
    print(f"\0active\x1fa 0,8,16,24,32,40,48\n")
    print(cal)

    # write new date in buffer
    buffer.write(d)


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

    >>> by_row = "1\n2\n3\n4\n5\n6"
    >>> rofi_transpose(by_row, 3)
    r"1\n4\n2\n5\n3\n6"

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
    # print(lst, file=sys.stderr)

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
    "1\n2\n3\n4\n5\n6"
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

    >>> rofi_list = "1\n2\n3\n4\n5\n6"
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
        print("--------------", file=sys.stderr)
        print(head, file=sys.stderr)
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

    # get note of the month list
    file_prefix = f"{date.year}-{date.month}-"
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
    days = [re.search(r"([^-]*)\.txt", f).group(1) for f in note_lst]
    # transform into rofi index
    ind = [cal2rofi_ind(int(d), date.month, date.year) for d in days]
    # format into rofi command
    ind = ",".join([str(i) for i in ind])

    return ind


def add_year(sourcedate, years):
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

    year = sourcedate.year + years
    day = min(sourcedate.day, calendar.monthrange(year, sourcedate.month)[1])
    return datetime.date(year, sourcedate.month, day)


def add_months(sourcedate, months):
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

    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])

    return datetime.date(year, month, day)


def open_n_reload_rofi(func):
    """ decorator to open and reload the rofi script """

    script_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    @wraps(func)
    def wrapper(*args):

        subprocess.Popen(["pkill", "-9", "rofi"])
        out = func(*args)
        cmd = f"{script_path}/naivecalendar.sh"
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

    note_path = f"{NOTES_PATH}/{date.year}-{date.month}-{day}.txt"
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

# def intercept_rofi_error(func):
#    """A decorator to capture sdtout after rofi being killed"""
#
#    @wraps(func)
#    def wrapper(*args):
#        try:
#            out = func(*args)
#        except subprocess.CalledProcessError as e:
#            print("Bye")
#            sys.exit()
#        return out
#
#    return wrapper
#
# @intercept_rofi_error
# def show_rofi_calendar(rofi, cal):
#    """Launch a rofi window
#
#    Parameters
#    ----------
#    rofi : str
#        Rofi command to be run in a shell
#    cal : str
#        A column by column calendar list formatted for rofi
#
#    Returns
#    -------
#    str
#        Rofi selected cell content
#    """
#
#    cmd = subprocess.Popen(f"echo '{cal}'", shell=True, stdout=subprocess.PIPE)
#    out = (
#        subprocess.check_output(rofi, stdin=cmd.stdout, shell=True)
#        .decode("utf-8")
#        .replace("\n", "")
#    )
#    return out
#
# @intercept_rofi_error
# def show_rofi(txt_body, txt_head):
#    """Launch a rofi window
#
#    Parameters
#    ----------
#    txt_body : str
#        Text to display in rofi window
#    txt_head : str
#        Text to display in rofi prompt
#
#    Returns
#    -------
#    str
#        Rofi selected cell content
#    """
#
#    cmd = subprocess.Popen(f'echo "{txt_body}"', shell=True, stdout=subprocess.PIPE)
#    selection = (
#        subprocess.check_output(
#            f'rofi -dmenu -p "{txt_head}"', stdin=cmd.stdout, shell=True
#        )
#        .decode("utf-8")
#        .replace("\n", "")
#    )
#
#    return selection

#def reload_rofi():
#
#    path = os.path.abspath(os.path.dirname(sys.argv[0]))
#    cmd = f"{path}/naivecalendar_cmd.sh"
#    os.system(cmd)
#    #subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def first_time_init():

    if shutil.which("rofi") == None:
        print("please install rofi")
        sys.exit()

    if not os.path.exists(NOTES_PATH):
        os.mkdir(NOTES_PATH)
        display_help(head_txt="Welcome to naivecalendar")

    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)


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
        help="""option '-p' output format (datetime.strftime format, defaut='%%Y-%%m-%%d')""",
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

    # messagebox.showinfo('Help', txt)
    text_popup("Help", txt)
    #subprocess.Popen("./naivecalendar_cmd.sh", shell=True)
    # show_rofi(txt, head_txt)


# def gen_rofi_conf(text, urgent):
#    """Create a rofi command
#    theme by adi1090x : https://github.com/adi1090x/polybar-themes
#    """
#
#    rofi = f"""
#
#        BORDER="#1F1F1F"
#        SEPARATOR="#1F1F1F"
#        FOREGROUND="#FFFFFF"
#        BACKGROUND="#1F1F1F"
#        BACKGROUND_ALT="#252525"
#        HIGHLIGHT_BACKGROUND="#8e24aa"
#        HIGHLIGHT_FOREGROUND="#1F1F1F"
#
#        BLACK="#000000"
#        WHITE="#ffffff"
#        RED="#e53935"
#        GREEN="#43a047"
#        YELLOW="#fdd835"
#        BLUE="#1e88e5"
#        MAGENTA="#00897b"
#        CYAN="#00acc1"
#        PINK="#d81b60"
#
#        rofi -dmenu -p "{text}" \
#        -show calendrier \
#        -hide-scrollbar true \
#        -bw 0 \
#        -a 0,8,16,24,32,40,48 \
#        -u {urgent} \
#        -lines {ROW_NB} \
#        -line-padding {CAL_LINE_PADDING} \
#        -padding {CAL_PADDING} \
#        -width {CAL_WIDTH} \
#        -xoffset {CAL_X_OFFSET} -yoffset {CAL_Y_OFFSET} \
#        -location {CAL_LOCATION} \
#        -columns {COL_NB}\
#        -color-enabled true \
#        -color-window "$BACKGROUND,$BORDER,$SEPARATOR" \
#        -color-normal "$BACKGROUND_ALT,$FOREGROUND,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" \
#        -color-active "$BACKGROUND,$BLUE,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" \
#        -color-urgent "$BACKGROUND,$YELLOW,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" """
#
#    return rofi


class DateBuffer:
    """ Class to store date """

    def __init__(self):

        self.buffer = configparser.ConfigParser()

    def iSconfig(self):
        pass

    def read(self):

        self.buffer.read(DATE_CACHE)
        month = int(self.buffer["buffer"]["month"])
        year = int(self.buffer["buffer"]["year"])

        return calendar.datetime.date(year, month, 1)

    def write(self, date):

        self.buffer["buffer"] = {"year": date.year, "month": date.month}
        with open(DATE_CACHE, "w") as buff:
            self.buffer.write(buff)

def text_popup(head, body):
    """ Display a popup msg with tkinter """

    import tkinter as tk
    import tkinter.scrolledtext as st

    win = tk.Tk()
    win.title(head)
    text_area = st.ScrolledText(win, width=50, height=12, font=("Noto Sans", 10))
    text_area.grid(column=0, pady=10, padx=10)
    text_area.insert(tk.INSERT, body)
    text_area.configure(state="disabled")
    win.mainloop()


if __name__ == "__main__":
    main()
