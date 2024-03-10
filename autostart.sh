#!/bin/bash

wal -R & 
syncthing --no-browser &
syncthingtray &
qtile run-cmd -g 1 thorium-browser &
qtile run-cmd -g 2 logseq &
picom &

# starting utility applications at boot time
# picom --config $HOME/.config/picom/picom.conf --vsync &
# /usr/libexec/polkit-gnome-autentication-agent-1 &
# /usr/lib/xfce4/notifyd/xfce4-notifyd &
# playerctld daemon &
# xhost +si:localuser:$USER &
# ~/.fehbg &
