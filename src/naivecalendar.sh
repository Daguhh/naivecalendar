#!/bin/bash

param="$@"
cmd="${BASH_SOURCE%/*}/naivecalendar.py $param"

# display help msg
if [[ " ${param[@]} " =~ " -h " ]] || [[ " ${param[@]} " =~ " --help " ]] ; then
    $cmd
    exit 0
fi

# display version msg
if [[ " ${param[@]} " =~ " -v " ]] || [[ " ${param[@]} " =~ " --version " ]] ; then
    $cmd
    exit 0
fi

# load theme file
THEME_CACHE_FILE="$HOME/.cache/naivecalendar/theme_cache.txt"
THEME_USER_PATH="$HOME/.config/naivecalendar/themes"
if test -f "$THEME_CACHE_FILE"; then
    THEME="$THEME_USER_PATH/$(cat $THEME_CACHE_FILE).rasi"
    if ! test -f "$THEME"; then
        THEME="${BASH_SOURCE%/*}/themes/$(cat $THEME_CACHE_FILE).rasi"
    fi
else
    THEME="${BASH_SOURCE%/*}/themes/classic_dark.rasi"
fi

if [[ " ${param[@]} " =~ " -t " ]] || [[ " ${param[@]} " =~ " --theme " ]] ; then
    while [[ $# -gt 0 ]] ; do
        key="$1"
        case $key in
            -t|--theme)
            THEME="$2"
            shift # past argument
            shift # past value
            ;;
        esac
    done
    THEME="${BASH_SOURCE%/*}/themes/$THEME.rasi"
fi

# launch rofi
rofi -show calendar \
    -modi "calendar:$cmd" \
    -theme-str '@theme "'$THEME'"' \
    -hide-scrollbar true \
    -x-offset 0 \
    -y-offset 55 \
    -location 3 \


# print date to stdout
if [[ " ${param[@]} " =~ " -p " ]] || [[ " ${param[@]} " =~ " --print " ]]; then
    FILE="$HOME/.cache/naivecalendar/pretty_print_cache.txt"
    cat $FILE
fi





