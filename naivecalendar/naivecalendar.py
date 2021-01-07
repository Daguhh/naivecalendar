#!/usr/bin/env python3
"""
A simple calendar made with rofi and python3.

Cycle through month and create linked note to days.
"""

__author__ = "Daguhh"
__license__ = "MIT-0"
__status__ = "Dev"

import glob, os, sys, subprocess, shutil
import re, argparse, configparser
import datetime, calendar, locale
from itertools import chain
from functools import wraps

##################################################
############# User parameters ####################
##################################################

def to_list(cfg_list):
    return [word.strip() for word in cfg_list.split(',')]

config = configparser.ConfigParser(interpolation=None)
config.read("config.cfg")

# set Locate
cfg = config['LOCALE']
USER_LOCALE = cfg["USER_LOCALE"] #"" #: keep empty to get system locale, use 'locale -a' on your system to list locales

# Week parameters
cfg = config['DAY NAMES']
DAY_ABBR_LENGHT = int(cfg["DAY_ABBR_LENGHT"]) #: day name lenght
FIRST_DAY_WEEK = int(cfg["FIRST_DAY_WEEK"]) #: 0 = sunday, 1 = monday...
SYM_WEEK_DAYS = to_list(cfg["SYM_WEEK_DAYS"]) #: day names list, if empty, locale names will be set

# Notes conf
cfg = config['NOTES']
NOTES_RELATIVE_PATH = cfg["NOTES_RELATIVE_PATH"] # ".naivecalendar_notes" #: path to save notes (retative to $HOME)
NOTES_DATE_FORMAT = cfg["NOTES_DATE_FORMAT"] #"%Y-%m-%d" #: strftime format, contains at least %d and month (%b, %m...)  + year (%Y...) identifier

# Rofi/Calendar shape
cfg = config['SHAPE']
NB_COL = 7 #int(cfg['NB_COL'])#: 7 days for a week
NB_WEEK = 6 #int(cfg['NB_WEEK'])#: number of "complete" weeks, a month can extend up to 6 weeks
NB_ROW = 8 #int(cfg['NB_ROW'])#: 1 day header + 6 weeks + 1 control menu

ROW_WEEK_SYM = int(cfg['ROW_WEEK_SYM'])#: row number where to display day symbols
ROW_CAL_START = int(cfg['ROW_CAL_START'])#: row number where to display calendar first line
ROW_CONTROL_MENU = int(cfg['ROW_CONTROL_MENU'])#: row number where to display buttons

#: Calendar symbols and shorcuts
cfg = config['CONTROL']
SYM_NEXT_MONTH = to_list(cfg['SYM_NEXT_MONTH']) #: 1st symbol is displayed, others are simply shortcuts
SYM_NEXT_YEAR = to_list(cfg['SYM_NEXT_YEAR']) #: 1st symbol is displayed, others are simply shortcuts
SYM_PREV_MONTH = to_list(cfg['SYM_PREV_MONTH']) #: 1st symbol is displayed, others are simply shortcuts
SYM_PREV_YEAR = to_list(cfg['SYM_PREV_YEAR']) #: 1st symbol is displayed, others are simply shortcuts

cfg = config['DAYS']
SYM_DAYS_NUM_unformatted = to_list(cfg['SYM_DAYS_NUM']) #:

cfg = config['SHORTCUTS']
SYM_NOTES = to_list(cfg['SYM_NOTES']) #: shortcut to display notes popup
SYM_HELP = to_list(cfg['SYM_HELP']) #: shortcut to display help popup
SYM_THEME = to_list(cfg['SYM_THEME']) #: shortcut to display theme chooser popup

# Date header display (rofi prompt)
cfg = config['HEADER']
PROMT_DATE_FORMAT = cfg['PROMT_DATE_FORMAT']#: date format in rofi prompt

# Today header display
IS_TODAY_HEAD_MSG = config.getboolean('HEADER', 'IS_TODAY_HEAD_MSG')#: toogle day num and name header display
TODAY_HEAD_NUMB_SIZE = cfg['TODAY_HEAD_NUMB_SIZE']#: 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', see pango markup language spec
TODAY_HEAD_NUMB_RISE = int(cfg['TODAY_HEAD_NUMB_RISE'])#: The vertical displacement from the baseline, in ten thousandths of an em, see pango markup language spec
TODAY_HEAD_NAME_SIZE = cfg['TODAY_HEAD_NAME_SIZE']#: 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', see pango markup language spec
TODAY_HEAD_NAME_RISE = int(cfg['TODAY_HEAD_NAME_RISE'])#: The vertical displacement from the baseline, in ten thousandths of an em, see pango markup language spec

##################################################
######### End User parameters ####################
##################################################

# week days symbols : can be changed by locale
def set_locale_n_week_day_names(cmd_line_locale):

    global SYM_WEEK_DAYS

    if cmd_line_locale:
        locale.setlocale(locale.LC_ALL, cmd_line_locale)
    else:
        locale.setlocale(locale.LC_ALL, USER_LOCALE)

    if not SYM_WEEK_DAYS or len(SYM_WEEK_DAYS) == 1:
        day_align_format = '{:>' + str(DAY_ABBR_LENGHT if DAY_ABBR_LENGHT >=2 else 2) + '}'
        get_loc_day = lambda d, l: locale.nl_langinfo(locale.DAY_1 + d)[:l].title()
        week_order = chain(range(FIRST_DAY_WEEK, 7), range(0, FIRST_DAY_WEEK))
        SYM_WEEK_DAYS = [day_align_format.format(get_loc_day(x, DAY_ABBR_LENGHT)) for x in week_order]

# create path to notes
HOME = os.getenv("HOME")
DIRNAME = os.path.dirname(__file__)
NOTES_PATH = f"{HOME}/{NOTES_RELATIVE_PATH}"

CACHE_PATH = f"{HOME}/.cache/naivecalendar"
DATE_CACHE = f"{CACHE_PATH}/date_cache.ini"
PP_CACHE = f"{CACHE_PATH}/pretty_print_cache.txt"
THEME_CACHE = f"{CACHE_PATH}/theme_cache.txt"
THEME_PATH = f"{DIRNAME}/themes"

# right align symbols given day abbreviation header length by adding spaces
# example (_ represents spaces):
# Mon Thu ...
# __1 __2 ...
DAY_FORMAT = '{:>' + str(DAY_ABBR_LENGHT if DAY_ABBR_LENGHT>=2 else 2) + '}'
SYM_DAYS_NUM = [DAY_FORMAT.format(day_sym) for day_sym in SYM_DAYS_NUM_unformatted]
##################################################
################# Script #########################
##################################################

def main():
    """
    Display a calendar with rofi
    Calendar is interactive :

    - switch between month
    - open {EDITOR} and create a note for selected day
    """

    first_time_init() # create note path n test rofi intall

    args, rofi_output = get_arguments()
    is_first_loop = bool(rofi_output)
    out = rofi_output

    set_locale_n_week_day_names(args.locale)

    d = Date()
    if is_first_loop or args.is_force_read_cache:
        d.read_cache()
    else:
        d.today()

    print('---------------------', file=sys.stderr)
    print(out,file=sys.stderr)
    # react to rofi output : date change
    if out in SYM_PREV_YEAR:
        d.year -= 1
    elif out in SYM_PREV_MONTH:
        d.month -= 1
    elif out in SYM_NEXT_MONTH:
        d.month += 1
    elif out in SYM_NEXT_YEAR:
        d.year += 1
    elif out in SYM_DAYS_NUM_unformatted:
        if args.print:
            print_selection(out, d.date, args.format)
        else:
            open_note(out, d.date, args.editor)
    elif out == "" or out in SYM_WEEK_DAYS:
        joke(out)

    update_rofi(d.date, is_first_loop)

    d.write_cache()

    # react to rofi output (read cache file to reload rofi)
    if out in SYM_NOTES:
        show_notes(d.date)
    elif out in SYM_HELP:
        display_help()
    elif out in SYM_THEME:
        ask_theme()
    else:
        pass

def update_rofi(date, is_first_loop):
    """generate and send calendar data to stdout/rofi

    It use the rofi `custom script mode <https://github.com/davatorium/rofi/wiki/mode-Specs>`_ to communicate with rofi
    and `pango markup <https://developer.gnome.org/pygtk/stable/pango-markup-language.html>`_ for theming

    Parameters
    ----------
    date : datetime.date
        A day of the month to display
    is_first_loop : bool
        True on first loop, if true, update today highlights

    """

    # generate new datas
    cal = get_calendar_from_date(date)
    date_prompt = date.strftime(PROMT_DATE_FORMAT).title()
    notes_inds = get_month_notes_ind(date)
    today_ind = cal2rofi_ind(date.day, date.month, date.year)
    week_sym_row = get_row_rofi_inds(ROW_WEEK_SYM)
    control_sym_row =get_row_rofi_inds(ROW_CONTROL_MENU)

    # send datas to stdout
    print(f"\0prompt\x1f{date_prompt}\n")
    print(f"\0urgent\x1f{notes_inds}\n")
    if not is_first_loop:
        print(f"\0active\x1f{today_ind}\n")
        if IS_TODAY_HEAD_MSG:
            day_numb = f"""<span rise="{TODAY_HEAD_NUMB_RISE}" size="{TODAY_HEAD_NUMB_SIZE}">{date.strftime('%d')}</span>"""
            day_name = f"""<span rise="{TODAY_HEAD_NAME_RISE}" size="{TODAY_HEAD_NAME_SIZE}">{date.strftime('%A')}</span>"""
            print(f"\0message\x1f{day_numb} {day_name}\n")

    print(f"\0active\x1f{week_sym_row}\n")
    print(f"\0active\x1f{control_sym_row}\n")
    print(cal)


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

    # init calendar with NB_WEEK blank week
    cal = [" "] * NB_WEEK * NB_COL

    # index
    ind_first_day = (start_day - (FIRST_DAY_WEEK - 1)) % 7
    ind_last_day = ind_first_day + month_length

    # fill with day numbers
    cal[ind_first_day : ind_last_day] = SYM_DAYS_NUM[:month_length]

    # create menu bar
    cal_menu = [" "] * NB_COL
    cal_menu[:2] = [SYM_PREV_YEAR[0], SYM_PREV_MONTH[0]]
    cal_menu[-2:] = [SYM_NEXT_MONTH[0], SYM_NEXT_YEAR[0]]

    index = (ROW_WEEK_SYM, ROW_CAL_START, ROW_CONTROL_MENU)
    content = [SYM_WEEK_DAYS, cal, cal_menu]
    index, content = (list(x) for x in zip(*sorted(zip(index, content))))

    # chain calendar elements
    cal = list(chain(*content))

    # Format calendar for rofi (column by column)
    cal = list_transpose(cal)

    # format data to be read by rofi (linebreak separated elements)
    cal = list2rofi(cal)

    return cal


def rofi_transpose(rofi_datas, column_number=NB_COL):
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


def list_transpose(lst, col_nb=NB_COL):
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

def get_row_rofi_inds(row):

    return ",".join(str(i * NB_ROW + row) for i in range(NB_COL))

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
    cal_offset = NB_COL * ROW_CAL_START
    day = int(day) - 1  # make month start at 0
    start_day, _ = calendar.monthrange(year, month)
    ind_start_day = (start_day - (FIRST_DAY_WEEK - 1)) % 7

    ind_r = cal_offset + day + ind_start_day

    # calendar coordinate
    row, col = ind_r // NB_COL, ind_r % NB_COL

    # rofi coordinate
    ind_c = col * NB_ROW + row

    return ind_c


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
def open_note(day_sym, date, editor):
    """open note for the selected date"""

    day_ind = SYM_DAYS_NUM_unformatted.index(day_sym) + 1

    note_name = datetime.date(date.year, date.month, day_ind).strftime(NOTES_DATE_FORMAT)
    note_path = f"{NOTES_PATH}/{note_name}.txt"
    cmd = f"touch {note_path} & {editor} {note_path}"
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    sdtout, sdterr = p.communicate()

@open_n_reload_rofi
def ask_theme():
    themes = glob.glob(f'{THEME_PATH}/*.rasi')
    themes = (t.split('/')[-1].split('.')[0]for t in themes)
    #themes = '\n'.join((t.split('/')[-1] for t in themes))

    out = text_list_popup("select theme", themes)
    print(out, file=sys.stderr)


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
        dest="is_force_read_cache",
        action="store_true",
        help="""force calendar to read old date from cache"""
    )

    parser.add_argument(
        "-t",
        "--theme",
        help="""set calendar theme, default=classic_dark (theme file name without extention)""",
        dest="theme"
    )

    args, unknown = parser.parse_known_args()
    unknown = unknown if len(unknown) == 0 else "".join(unknown).strip(' ')

    return args, unknown


def joke(sym):
    """Just display stupid jokes in french"""

    if sym == "":
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

def text_list_popup(head, lst):

    import tkinter as tk
    from tkinter import Listbox

    win = tk.Tk()
    win.title(head)
    l = Listbox(win)
    l.insert(1,*lst)
    l.pack()

    win.bind('<Return>', lambda _:[set_theme_cache(l.get(l.curselection()[0])), win.destroy()])

    win.mainloop()

def set_theme_cache(selected):

    with open(THEME_CACHE, 'w') as f:
        f.write(selected)

def rofi_popup(txt_body, txt_head):
    """Launch a rofi window

    Parameters
    ----------
    txt_body : str
        Text to display in rofi window
    txt_head : str
        Text to display in rofi prompt

    Returns
    -------
    str
        Rofi selected cell content
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
    theme : show theme selector

There's some command line option too, dislay it with :
    ./naivecalendar -h

That's all :

close window to continue...
"""

    text_popup("Help", txt)


if __name__ == "__main__":
    main()
