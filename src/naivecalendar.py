#!/usr/bin/env python3
"""
A simple calendar made with rofi and python3.

Cycle through month and create linked event to days.
"""

__author__ = "Daguhh"
__license__ = "MIT-0"
__status__ = "Dev"
__version__ = "0.3.5"

import glob, os, sys, subprocess, shutil, pathlib
import re, argparse, configparser
import datetime, calendar, locale
from itertools import chain
from functools import wraps
import time

######################
### Path constants ###
######################
HOME = os.getenv("HOME")
DIRNAME = os.path.dirname(__file__)
CACHE_PATH = f"{HOME}/.cache/naivecalendar"
DATE_CACHE = f"{CACHE_PATH}/date_cache.ini"
PP_CACHE = f"{CACHE_PATH}/pretty_print_cache.txt"
THEME_CACHE = f"{CACHE_PATH}/theme_cache.txt"
EVENT_CACHE = f"{CACHE_PATH}/event_cache.txt"
THEME_USER_PATH = f"{HOME}/.config/naivecalendar/themes"
THEME_PATHS = [THEME_USER_PATH, f"{DIRNAME}/themes"]

#######################################
### load a theme configuration file ###
#######################################
try: # cache file
    with open(THEME_CACHE, 'r') as theme_cache:
        theme = theme_cache.read()
        for path in THEME_PATHS:
            THEME_CONFIG_FILE = f"{path}/{theme}.cfg"
            if os.path.isfile(THEME_CONFIG_FILE):
                break
except FileNotFoundError: #  default if not initialized
    theme = "classic_dark"
    THEME_CONFIG_FILE = f"{THEME_PATHS[-1]}/{theme}.cfg"

try:
    with open(EVENT_CACHE, 'r') as event_cache:
        EVENTS_DEFAULT = event_cache.read()
except FileNotFoundError:
    EVENTS_DEFAULT = ''

############################
### Load user parameters ###
############################
def to_list(cfg_list):
    """convert string with comma separated elements into python list"""
    return [word.strip() for word in cfg_list.split(',')]

config = configparser.ConfigParser(interpolation=None)
config.read(THEME_CONFIG_FILE)

### set Locate ###
cfg = config['LOCALE']
#: keep empty to get system locale,
#: use 'locale -a' on your system to list locales
USER_LOCALE = cfg["USER_LOCALE"]

### Week parameters ###
cfg = config['DAY NAMES']
#: day name lenght
DAY_ABBR_LENGHT = int(cfg["DAY_ABBR_LENGHT"])
#: 0 = sunday, 1 = monday...
FIRST_DAY_WEEK = int(cfg["FIRST_DAY_WEEK"])
#: day names list, if empty, locale names will be set
SYM_WEEK_DAYS = to_list(cfg["SYM_WEEK_DAYS"])

### Notes conf ###
cfg = config['EVENTS']
#: events path should contains at least %d and month (%b, %m...)  + year (%Y...) (strftime format)
EVENTS_PATHS = {n:pathlib.Path.home()/pathlib.Path(cfg[n]) for n in cfg}
#: default date events folder to display
EVENTS_DEFAULT = EVENTS_DEFAULT if EVENTS_DEFAULT != '' else next(EVENTS_PATHS.keys().__iter__()) #cfg['DEFAULT'].lower()

### Rofi/Calendar shape ###
cfg = config['SHAPE']
#: 7 days for a week
NB_COL = 7
#: number of "complete" weeks, a month can extend up to 6 weeks
NB_WEEK = 6
#: 1 day header + 6 weeks + 1 control menu
NB_ROW = 8
#: row number where to display day symbols
ROW_WEEK_SYM = int(cfg['ROW_WEEK_SYM'])
#: row number where to display calendar first line
ROW_CAL_START = int(cfg['ROW_CAL_START'])
#: row number where to display buttons
ROW_CONTROL_MENU = int(cfg['ROW_CONTROL_MENU'])

### Calendar symbols and shortcuts ###
cfg = config['CONTROL']
#: 1st symbol is displayed, others are simply shortcuts
SYM_NEXT_MONTH = to_list(cfg['SYM_NEXT_MONTH'])
#: 1st symbol is displayed, others are simply shortcuts
SYM_NEXT_YEAR = to_list(cfg['SYM_NEXT_YEAR'])
#: 1st symbol is displayed, others are simply shortcuts
SYM_PREV_MONTH = to_list(cfg['SYM_PREV_MONTH'])
#: 1st symbol is displayed, others are simply shortcuts
SYM_PREV_YEAR = to_list(cfg['SYM_PREV_YEAR'])
#: 1st symbol is displayed, others are simply shortcuts
SYM_MENU = to_list(cfg['SYM_MENU'])

### Day numbers symbols
cfg = config['DAYS']
# symbols for day numbers
SYM_DAYS_NUM_unformatted = to_list(cfg['SYM_DAYS_NUM'])

### Shortcuts for popup windows ###
cfg = config['SHORTCUTS']
#: shortcut to display events popup
SYM_SHOW_EVENTS = to_list(cfg['SYM_SHOW_EVENTS'])
#: shortcut to display help popup
SYM_SHOW_HELP = to_list(cfg['SYM_SHOW_HELP'])
#: shortcut to display theme chooser popup
SYM_SWITCH_THEME = to_list(cfg['SYM_SWITCH_THEME'])
#: shortcut to display event chooser popup
SYM_SWITCH_EVENT = to_list(cfg['SYM_SWITCH_EVENT'])

### Today header display ###
cfg = config['HEADER']
#: date format in rofi prompt
PROMT_DATE_FORMAT = cfg['PROMT_DATE_FORMAT']
#: toogle day num and name header display
IS_TODAY_HEAD_MSG = config.getboolean('HEADER', 'IS_TODAY_HEAD_MSG')
#: Size of day number in the header. See pango markup language spec
TODAY_HEAD_NUMB_SIZE = cfg['TODAY_HEAD_NUMB_SIZE']
#: Vertical position of day number in header. See pango markup language spec
TODAY_HEAD_NUMB_RISE = int(cfg['TODAY_HEAD_NUMB_RISE'])
#: Size of day name in the header. See pango markup language spec
TODAY_HEAD_NAME_SIZE = cfg['TODAY_HEAD_NAME_SIZE']
#: Vertical position of day name in header. See pango markup language spec
TODAY_HEAD_NAME_RISE = int(cfg['TODAY_HEAD_NAME_RISE'])

############################################
### Configure paramters given users ones ###
############################################

# format to align all signs to right given size of day names
# example (_ represents spaces):
# Mon Thu ...
# __1 __2 ...
DAY_FORMAT = '{:>' + str(max(DAY_ABBR_LENGHT,2)) + '}'
# absolute path
#EVENTS_PATH = f"{HOME}/{EVENTS_RELATIVE_PATH}"
#: symbols for day numbers
SYM_DAYS_NUM = [DAY_FORMAT.format(day_sym) for day_sym in SYM_DAYS_NUM_unformatted]
# create menu bar
CAL_MENU = [" "] * NB_COL
CAL_MENU[:2] = [SYM_PREV_YEAR[0], SYM_PREV_MONTH[0]]
CAL_MENU[-4] = SYM_MENU[0] if SYM_MENU[0] != '' else '_'
CAL_MENU[-2:] = [SYM_NEXT_MONTH[0], SYM_NEXT_YEAR[0]]

#############
###Script ###
#############

def main():
    """Print calendar to stdout and react to rofi output"""

    # create event path n test rofi intall
    first_time_init()

    # get command line arguments and if exist : rofi output
    args, rofi_output = get_arguments()

    global SYM_WEEK_DAYS
    SYM_WEEK_DAYS = set_locale_n_week_day_names(args.locale)

    is_first_loop = not bool(rofi_output)
    out = rofi_output

    # get date given context
    d = get_date(is_first_loop, args.is_force_read_cache, args.date)
    # react to "date" event from rofi
    d = process_event_date(out, d, args)
    # send next datas to rofi
    update_rofi(d.date, is_first_loop)
    # save  date
    d.write_cache()
    # react to rofi output (read cache file to reload rofi)
    process_event_popup(out, d)


def get_date(is_first_loop, is_force_read_cache, arg_date):
    """get date given the context

    Parameters
    ----------
    is_first_loop : bool
        true on first calendar call
    is_force_read_cache : bool
        force date from cache
    arg_date : str
        date in '%m%Y' format

    Returns
    -------
    Date
       Date object that contain the date to display
    """

    d = Date()
    if not is_first_loop or is_force_read_cache:
        d.read_cache() # read previous date
    elif is_first_loop and arg_date:
        d.set_month(arg_date) # command line force date
    else: # at first loop if no force option
        d.today()

    return d


def process_event_date(out, d, args):
    """React to rofi output for "date" events"""

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
        elif args.clipboard:
            send2clipboard(out, d.date, args.format)
        else:
            open_event(out, d.date, args.editor)
    elif out == "" or out in SYM_WEEK_DAYS:
        joke(out)

    return d


def process_event_popup(out, d):
    """React when shortcut for popup is enter in rofi prompt"""

    if out in SYM_SHOW_EVENTS:
        show_events(d.date)
    elif out in SYM_SHOW_HELP:
        display_help()
    elif out in SYM_SWITCH_THEME:
        ask_theme()
    elif out in SYM_SWITCH_EVENT:
        ask_event_to_display()
    elif out in SYM_MENU:
        show_menu(d)


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
    events_inds = get_month_events_ind(date)
    today_ind = cal2rofi_ind(date.day, date.month, date.year)
    week_sym_row = get_row_rofi_inds(ROW_WEEK_SYM)
    control_sym_row =get_row_rofi_inds(ROW_CONTROL_MENU)

    # send datas to stdout
    print(f"\0prompt\x1f{date_prompt}\n")
    print(f"\0urgent\x1f{events_inds}\n")
    if is_first_loop:
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

    # fill with day numbers
    ind_first_day = (start_day - (FIRST_DAY_WEEK - 1)) % 7
    ind_last_day = ind_first_day + month_length
    cal[ind_first_day : ind_last_day] = SYM_DAYS_NUM[:month_length]

    # join calendar parts given user order
    index = (ROW_WEEK_SYM, ROW_CAL_START, ROW_CONTROL_MENU)
    content = [SYM_WEEK_DAYS, cal, CAL_MENU]
    index, content = (list(x) for x in zip(*sorted(zip(index, content))))

    # chain calendar elements
    cal = list(chain(*content))

    # Format calendar for rofi (column by column)
    cal = list_transpose(cal) # + ["theme", "help", "event", "switch"]

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


def get_month_events_heads(date):
    """
    Return a list of file's first line of a specific month

    Parameters
    ----------
    date : datetime.date
        Any day of the month to display

    Returns
    -------
    str
        A rofi formatted list of month's events first line
    """

    event_lst = get_month_events(date)

    heads = [get_event_head(n) for n in event_lst]
    prompts = [pathlib.Path(n).stem for n in event_lst]

    return "\n".join([f"{p} : {h}" for p, h in zip(prompts, heads)])


def get_event_head(event_path):
    """
    Return first line of a text file

    Parameters
    ----------
    event_path : str
        A text file path

    Returns
    -------
    str
        First line of the text file
    """

    with open(event_path, "r") as f:
        head = f.read().split("\n")[0]
    return head


def get_row_rofi_inds(row):
    """Get all rofi index of a row

    Parameters
    ----------
    row : int
        row number (start at 0)

    Returns
    -------
    str
        a ',' separate list of rofi indexes
    """

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


def get_month_events(date):
    """
    Return events files paths that are attached to date's month

    Parameters
    ----------
    date : datetime.date
        Any day of the month displayed

    Returns
    -------
    list
        list of files that belong to date.month
    """

    # folder of the actual watched events
    path = EVENTS_PATHS[EVENTS_DEFAULT]

    # make all elements that change during a month (d, h, m, s) match a regex
    # "%a-%d-%b-%m-%Y" --> "[a-zA-Z.]*-[0-9]*-%b-%m-%Y"
    file_pattern = re.sub('%-{0,1}[dwjhHIMSfzZ]', '[0-9]*', str(path))
    file_pattern = re.sub('%[aAp]', '[a-zA-Z.]*', file_pattern)

    # format all element that identify the month (year, month)
    # "[a-zA-Z.]*-[0-9]*-%b-%m-%Y" --> "[a-zA-Z.]*-[0-9]*-Jan.-01-2021"
    file_pattern = date.strftime(file_pattern) #f"{date.year}-{date.month}-"

    # return all elements that belong to current month (match previous regex)
    path = pathlib.Path(file_pattern)
    event_lst = list(pathlib.Path(path.parent).glob(path.name))

    return event_lst


def get_month_events_ind(date):
    """
    Return rofi-formatted index of days with attached event

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
    event_lst = get_month_events(date)
    # get event day number
    date_format = EVENTS_PATHS[EVENTS_DEFAULT].name
    # make capture group for day number (%d)
    pattern = re.sub('%d',r'([0-9]*)', date_format)
    # create pattern for %-d, %w, %a, %A
    pattern = re.sub('%-{0,1}[dwjhHIMSfzZ]',r'[0-9]*', pattern)
    pattern = re.sub('%[aAp]',r'[a-zA-Z.]*', pattern)
    # replace other (month and year) with real date
    pattern = date.strftime(pattern)
    # match the day (%d) capture group for each event in event_lst
    days = [re.match(pattern, f.name).group(1) for f in event_lst]
    # transform into rofi index
    inds = [cal2rofi_ind(int(d), date.month, date.year) for d in days]
    # format into rofi command
    inds = ",".join([str(i) for i in inds])

    return inds


def open_n_reload_rofi(func):
    """ decorator to open and reload the rofi script at the same date"""

    script_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    @wraps(func)
    def wrapper(*args, **kwargs):

        subprocess.Popen(["pkill", "-9", "rofi"])
        time.sleep(0.1)
        out = func(*args)
        cmd = f"{script_path}/naivecalendar.sh -c"
        os.system(cmd)

        return out

    return wrapper


@open_n_reload_rofi
def show_events(date):
    """open rofi popup with events list of selected month"""

    events_heads = get_month_events_heads(date)
    rofi_popup(EVENTS_DEFAULT, events_heads)

@open_n_reload_rofi
def show_menu(d):

    menu = '\n'.join([to_list(config['SHORTCUTS'][s])[1] for s in config['SHORTCUTS']])
    output = rofi_popup("menu", menu + '\nback to calendar')
    process_event_popup(output, d)

@open_n_reload_rofi
def open_event(day_sym, date, editor):
    """open event for the selected date"""

    day_ind = SYM_DAYS_NUM_unformatted.index(day_sym) + 1

    date_format = str(EVENTS_PATHS[EVENTS_DEFAULT])
    event_path = datetime.date(date.year, date.month, day_ind).strftime(date_format)
    #event_path = S_PATH}/{event_name}.txt"
    cmd = f"touch {event_path} & {editor} {event_path}"
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    sdtout, sdterr = p.communicate()


@open_n_reload_rofi
def ask_event_to_display():

    events = list(EVENTS_PATHS.keys())
    events = list2rofi(events)

    event = rofi_popup(f"select what to display (actual = {EVENTS_DEFAULT})", events)

    set_event_cache(event)


@open_n_reload_rofi
def ask_theme():
    """Search themes in paths and open a popup"""

    themes = list(chain(*[glob.glob(f'{path}/*.rasi') for path in THEME_PATHS]))
    themes = (t.split('/')[-1].split('.')[0]for t in themes)
    themes = list2rofi(themes)
    #themes = '\n'.join((t.split('/')[-1] for t in themes))

    theme = rofi_popup("select theme", themes)
    set_theme_cache(theme)

def print_selection(day, date, f):
    """return select date to stdout given cmd line parameter '--format'"""

    d = int(day)
    m = date.month
    y = date.year

    pretty_date = datetime.date(y, m, d).strftime(f)
    with open(PP_CACHE, "w") as f:
        f.write(pretty_date + "\n")

    sys.exit(0)


@open_n_reload_rofi
def send2clipboard(day, date, f):
    """return select date to stdout given cmd line parameter '--format'"""

    if shutil.which("xclip") == None:
        print("\nplease install xclip to use 'copy-to-clipboard' option (-x/--clipboard)\n", file=sys.stderr)
        sys.exit(0)

    d = int(day)
    m = date.month
    y = date.year

    pretty_date = datetime.date(y, m, d).strftime(f)
    p = subprocess.Popen(('echo', pretty_date), stdout=subprocess.PIPE)
    subprocess.check_output(('xclip', '-selection', 'clipboard'), stdin=p.stdout)

    sys.exit(0)


def first_time_init():
    """Create config files and paths given script head variables"""

    if shutil.which("rofi") == None:
        print("please install rofi")
        sys.exit()

    if not os.path.exists(THEME_USER_PATH):
        os.makedirs(THEME_USER_PATH)

    for events_path in EVENTS_PATHS.values():
        if not os.path.exists(events_path.parent):
            os.makedirs(events_path.parent)

    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)
        date = datetime.date.today()
        date_buff = configparser.ConfigParser()
        date_buff["buffer"] = {"year": date.year, "month": date.month}
        with open(DATE_CACHE, 'w') as date_cache:
            date_buff.write(date_cache)
        display_help(head_txt="Welcome to naivecalendar")


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

    def set_month(self, month):
        """Set and return date of the given Month

        Parameters
        ----------
        month : str
            month to set in '%m-%Y' format

        Returns
        -------
        datetime.date
            a day of the month
        """

        m, y = [int(x) for x in month.split('-')]
        self.date = datetime.date(y,m,1)

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

    parser = argparse.ArgumentParser(
        prog="naivecalendar",
        description="A simple popup calendar"
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version="%(prog)s " + __version__
    )

    cmd_group = parser.add_mutually_exclusive_group()

    cmd_group.add_argument(
        "-p",
        "--print",
        help="print date to stdout instead of opening a event",
        action="store_true",
    )

    cmd_group.add_argument(
        "-x",
        "--clipboard",
        help="copy date to clipboard",
        action="store_true",
    )

    parser.add_argument(
        "-f",
        "--format",
        help="""option '-p' or '-x' output format (datetime.strftime format, defaut='%%Y-%%m-%%d')""",
        dest="format",
        default="%Y-%m-%d",
    )

    parser.add_argument(
        "-e",
        "--editor",
        help="""editor command to open events""",
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

    parser.add_argument(
        "-d",
        "--date",
        help="""display calendar at the given month, format='%%m-%%Y'""",
        dest="date",
        default=False
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


def set_theme_cache(selected):
    """Write theme name to cache file"""

    with open(THEME_CACHE, 'w') as f:
        f.write(selected)


def set_event_cache(selected):
    """Write theme name to cache file"""

    with open(EVENT_CACHE, 'w') as f:
        f.write(selected)


def rofi_popup(txt_head, txt_body):
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
 - Hit a day to create a linked event.
(A day with attached event will appear yellow.)
 - Create multiple event type and with between them

There's somme shortcut too, type it in rofi prompt :

     help : display this help
 nn or -- : go to previous year
   n or - : go to previous month
   p or + : go to next month
 pp or ++ : go to next year
    event : display events of the month (first line)
   switch : switch events folder to display
    theme : show theme selector
     menu : display a selection menu (skip shortcuts)

There's some command line option too, dislay it with :
    ./naivecalendar -h

That's all :

press enter to continue...
"""

    rofi_popup("Help", txt)


# week days symbols : can be changed by locale
def set_locale_n_week_day_names(arg_locale):
    """ Set SYM_WEEK_DAYS constante given command line argument """

    if arg_locale:
        locale.setlocale(locale.LC_ALL, arg_locale)
    else:
        locale.setlocale(locale.LC_ALL, USER_LOCALE)

    if not SYM_WEEK_DAYS or len(SYM_WEEK_DAYS) == 1:

        def get_loc_day(day_num, lenght):
            """return locale day names truncated at lenght and titlized"""
            return locale.nl_langinfo(locale.DAY_1 + day_num)[:lenght].title()

        days_order = chain(range(FIRST_DAY_WEEK, 7), range(0, FIRST_DAY_WEEK))

        sym_week_days = [DAY_FORMAT.format(
            get_loc_day(day_num, DAY_ABBR_LENGHT)
        ) for day_num in days_order]

        return sym_week_days

if __name__ == "__main__":
    main()
