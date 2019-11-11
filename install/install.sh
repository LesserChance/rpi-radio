#!/bin/bash
set -x

BASE_DIR="$(dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )")"

# syslog
sudo mkdir -p /var/log/radio
sudo touch /var/log/radio/radio.log
sudo cp "$BASE_DIR"/install/*_syslog.conf /etc/rsyslog.d
sudo systemctl restart rsyslog

# systemd
sudo bash $BASE_DIR/install/radio_service.sh
sudo chown root:root /etc/systemd/system/radio.service
sudo chmod 644 /etc/systemd/system/radio.service
sudo systemctl enable /etc/systemd/system/radio.service
sudo systemctl daemon-reload
sudo systemctl restart $(ls /etc/systemd/system/radio.service | cut -d'/' -f5)

# dependencies
sudo apt-get update
sudo apt-get install vim python3-pip mpd mpc libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5 -y
sudo apt-get -y dist-upgrade
sudo pip3 install RPi.GPIO Adafruit_GPIO Adafruit_SSD1306 Pillow
cp install/radio.m3u /var/lib/mpd/playlists/
