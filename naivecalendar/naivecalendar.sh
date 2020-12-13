#!/bin/bash

param="$@"
cmd="${BASH_SOURCE%/*}/naivecalendar.py $param"

if [[ " ${param[@]} " =~ " -h " ]] || [[ " ${param[@]} " =~ " --help " ]] ; then
    $cmd
    exit 0
fi

THEME="${BASH_SOURCE%/*}/themes/classic_dark.rasi"
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

rofi -show calendar \
    -modi "calendar:$cmd" \
    -theme $THEME \
    -hide-scrollbar true \
    -x-offset 0 \
    -y-offset 55 \
    -location 3 \


if [[ " ${param[@]} " =~ " -p " ]] || [[ " ${param[@]} " =~ " --print " ]]; then
    FILE="$HOME/.cache/naivecalendar/pretty_print_cache.txt"
    cat $FILE
fi





