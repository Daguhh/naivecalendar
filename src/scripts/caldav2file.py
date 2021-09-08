#!/usr/bin/env python3

"""
Still in dev. Put me in $HOME/.config/naivecalendar/scripts/

This script get caldav events from an online account (1) and
save it into files so it can shown up in naivecalendar

(1) : launch this script to create a config file at::

    "$HOME/.naivecalendar/caldav_user.json"

and fill it with your account infos::


    {
        "url": "url,
        "user": "user",
        "password": "password",
        "calendar_name": "calendar_name"   <-- optional (keep empty)
    }


Launch it again tu download your events.
"""

import os
import sys
import json

import caldav


class default:
    def __init__(self):
        self.value = ""
DEFAULT = [default()]

def err_msg(txt):
    print(len(txt)*'*', f'\n{txt}\n', len(txt)*'*', file=sys.stderr)

def tab(s):
    """indent multiline text"""
    s = s.split("\n")
    s = [f" {l}" for l in s]
    s = "\n".join(s)
    return s

#######################
### Get caldav conf ###
#######################

HOME = os.getenv("HOME")
conf_path = f"{HOME}/.config/naivecalendar/caldav_user.json"

event_path = f"{HOME}/.naivecalendar_events/CalDav"

if os.path.exists(conf_path):
    with open(conf_path, "r") as f:
        conf = json.load(f)
else:
    default_conf = {"url": "", "user": "", "password": "", "calendar_name": ""}
    with open(conf_path, "w") as f:
        conf = f.write(json.dumps(default_conf, indent=4))

    err_msg(f"please fill {conf_path} to connect your caldav account")
    exit(0)


########################################
### Ask caldav server and get events ###
########################################

try:
    client = caldav.DAVClient(
        url=conf["url"], username=conf["user"], password=conf["password"]
    )
    my_principal = client.principal()
    my_cals = my_principal.calendars()
    ind_cal = 0
    if conf["calendar_name"]:
        ind_cal = [c.name for c in my_cals].index(conf["calendar_name"])
    my_cal = my_cals[ind_cal]
    my_events = my_cal.events()

except Exception as e:
    err_msg(f"Please check your caldav account informations at:\n{conf_path}")
    raise e


#####################
### Format events ###
#####################

events_by_day = dict()

for event in my_events:
    my_vobj = event.vobject_instance
    my_contents = my_vobj.contents["vevent"][0].contents

    event_dct = dict()

    event_dct["summary"] = my_contents.setdefault("summary", DEFAULT)[0].value
    event_dct["description"] = my_contents.setdefault("description", DEFAULT)[0].value
    event_dct["location"] = my_contents.setdefault("location", DEFAULT)[0].value

    dtstart = my_contents["dtstart"][0].value
    event_dct["day_start"] = dtstart.strftime("%y-%m-%d")
    event_dct["time_start"] = dtstart.strftime("%Hh%M")

    # dtend = my_contents['dtend'][0].value
    # event_dct['day_end'] = dtend.strftime('%y-%m-%d')
    # event_dct['time_end'] = dtend.strftime('%Hh%M')

    events_by_day[event_dct["day_start"]] = events_by_day.setdefault(
        event_dct["day_start"], []
    ) + [event_dct]

######################
### write to files ###
######################


for day, event_list in events_by_day.items():

    event_list_sorted = sorted(event_list, key=lambda k: k["time_start"])

    text = ""
    for event in event_list_sorted:
        text += f"[{event['time_start']}] {event['summary']}\n"
        if event["location"]:
            text += f"location :\n{tab(event['location'])}\n"
        if event["description"]:
            text += f"description :\n{tab(event['description'])}\n"
        text += "\n"

    with open(f"{event_path}/{event['day_start']}.txt", "w") as f:
        f.write(text)
