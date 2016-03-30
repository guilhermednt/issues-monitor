#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

RESULT=`SCREEN=:0 DISPLAY=:0 XAUTHORITY=$HOME/.Xauthority $DIR/issues_monitor.py -c $DIR/config.ini 2>&1`

if [[ $RESULT != *"Another instance is already running, quitting."* ]]; then
	printf "$RESULT \n\n" >>$DIR/issues_monitor.log
fi
