sudo cp fliplock.service /etc/systemd/system/fliplock.service
sudo cp tablet.desktop /usr/share/applications/
sudo systemctl daemon-reload
sudo systemctl enable --now fliplock.service
