output=$(curl -sS localhost:4244/toggle 2>&1)
notify-send -i /opt/fliplock/tablet.png "Toggle Tablet Mode" "$output"
