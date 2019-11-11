#!/bin/bash
# creates the rpi_radio service file
BASE_DIR="$(dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )")"
cat <<-EOF | sudo tee /etc/systemd/system/radio.service >/dev/null
[Unit]
Description=radio
After=network-online.target
Wants=network-online.target

[Service]
# Command to execute when the service is started
ExecStart=$BASE_DIR/radio
Restart=on-failure
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=RADIO

[Install]
WantedBy=multi-user.target
EOF
