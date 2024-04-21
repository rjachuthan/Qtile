#!/bin/bash

wal -R & 
syncthing --no-browser &
syncthingtray &
qtile run-cmd -g 1 thorium-browser &
qtile run-cmd -g 2 logseq &
qtile run-cmd -g 8 anki &
# qtile run-cmd -g 3 qutebrowser www.youtube.com &
picom &

# starting utility applications at boot time
# picom --config $HOME/.config/picom/picom.conf --vsync &
/usr/libexec/polkit-gnome-autentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &
playerctld daemon &
xhost +si:localuser:$USER &
# ~/.fehbg &
