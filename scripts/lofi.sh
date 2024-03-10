#!/bin/bash

# List of Lofi Musics
lofi_links=(
    "https://www.youtube.com/watch?v=jfKfPfyJRdk&pp=ygUEbG9maQ%3D%3D"
    "https://www.youtube.com/watch?v=JqLIV9QzYt8&pp=ygUEbG9maQ%3D%3D"
    "https://www.youtube.com/watch?v=MZhivjxcF-M&pp=ygUEbG9maQ%3D%3D"
    "https://www.youtube.com/watch?v=ZjM2Ybr8YfE&pp=ygUEbG9maQ%3D%3D"
    "https://www.youtube.com/watch?v=iubb8g2R694&pp=ygUEbG9maQ%3D%3D"
    "https://www.youtube.com/watch?v=KRA26LhuTP4&pp=ygUObG9maSBib2xseXdvb2Q%3D"
    "https://www.youtube.com/watch?v=Ik0YeuQHBCI&pp=ygUObG9maSBib2xseXdvb2Q%3D"
    "https://www.youtube.com/watch?v=uFrYFfcnPwA&pp=ygUObG9maSBib2xseXdvb2Q%3D"
)

# Randomly select a link
random_link=${lofi_links[$RANDOM % ${#lofi_links[@]}]}

title=$(yt-dlp --get-title "$random_link")

# Send a notification
notify-send -t 3000 --app-name="Lofi Music" "Playing Lofi Music" "$title"

# Play the selected link using MPV
mpv "$random_link"
