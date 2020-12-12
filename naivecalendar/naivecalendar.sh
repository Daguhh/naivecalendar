#!/bin/bash

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

param="$@"
cmd="${BASH_SOURCE%/*}/naivecalendar.py $param"

if [[ " ${param[@]} " =~ " -h " ]] || [[ " ${param[@]} " =~ " --help " ]] ; then
    $cmd
    exit 0
fi

rofi -show calendar \
    -modi "calendar:$cmd" \
-hide-scrollbar true \
-matching-negate-char * \
-a 0,8,16,24,32,40,48 \
-lines 8 \
-line-padding 5 \
-padding 10 \
-width 320 \
-xoffset 320 -yoffset 25 \
-location 2 2 \
-columns 7 \
-color-enabled true \
-color-window "$BACKGROUND,$BORDER,$SEPARATOR" \
-color-normal "$BACKGROUND_ALT,$FOREGROUND,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" \
-color-active "$BACKGROUND,$BLUE,$BACKGROUND,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND" \
-color-urgent "$BACKGROUND,$YELLOW,$BACKGROUND_ALT,$HIGHLIGHT_BACKGROUND,$HIGHLIGHT_FOREGROUND"

if [[ " ${param[@]} " =~ " -p " ]] || [[ " ${param[@]} " =~ " --print " ]]; then
    FILE="$HOME/.cache/naivecalendar/pretty_print_cache.txt"
    cat $FILE
fi





