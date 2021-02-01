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
THEME_SOURCE_PATH="${BASH_SOURCE%/*}/themes"
if [[ " ${param[@]} " =~ " -t " ]] || [[ " ${param[@]} " =~ " --theme " ]] ; then
    while [[ $# -gt 0 ]] ; do
        key="$1"
        case $key in
            -t|--theme)
            OPT_THEME="$2"
            shift # past argument
            ;;
        esac
        shift # past value
    done
    THEME="$THEME_USER_PATH/$OPT_THEME).rasi"
    if ! test -f "$THEME"; then
        THEME="$THEME_SOURCE_PATH/$OPT_THEME.rasi"
    fi
    if ! test -f "$THEME"; then
        echo "theme '$OPT_THEME' doesn't exist"
        exit 0
    fi

elif test -f "$THEME_CACHE_FILE"; then
    # look in user path, then in source path
    THEME="$THEME_USER_PATH/$(cat $THEME_CACHE_FILE).rasi"
    if ! test -f "$THEME"; then
        THEME="$THEME_SOURCE_PATH/$(cat $THEME_CACHE_FILE).rasi"
    fi
    if ! test -f "$THEME"; then
        echo "*************************************************************************"
        echo "* '$(cat $THEME_CACHE_FILE)' theme doesn't exist anymore, "     
        echo "*    - please remove $THEME_CACHE_FILE    "
        echo "* or                                                                    *" 
        echo "*    - force a theme with -t|--theme argument,                          *"
        echo "*      then switch again to an existing theme to override cache file    *"
        echo "*************************************************************************"
        exit 0
    fi
    printf "%-25s  %-25s  %-25s  %-25s\n"$PARAM_LIST

else
    THEME="$THEME_SOURCE_PATH/classic_dark.rasi"
fi

# launch rofi
output="$(rofi -show calendar \
    -modi "calendar:$cmd" \
    -theme-str '@theme "'$THEME'"' \
    -hide-scrollbar true \
    -x-offset 0 \
    -y-offset 55 \
    -location 3 2>&1)"

# print date to stdout
if [[ " ${param[@]} " =~ " -p " ]] || [[ " ${param[@]} " =~ " --print " ]]; then
    FILE="$HOME/.cache/naivecalendar/pretty_print_cache.txt"
    printf "%s" "$(cat $FILE)"
fi





