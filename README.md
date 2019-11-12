# RPI Radio
## About
A vintage radio retrofitted with a raspberry pi. Tuning dial controls station selection with static “between” stations.

See current functionality here: https://photos.app.goo.gl/TbV9LWXgRbATbLui6

[![rpi-radio](https://raw.githubusercontent.com/LesserChance/rpi-radio/master/assets/thumbnail.png)](https://photos.app.goo.gl/TbV9LWXgRbATbLui6
 "rpi-radio") 

## Setting up from Scratch
### Install Raspian Stretch Lite
https://www.raspberrypi.org/documentation/installation/installing-images/mac.md
1. `diskutil list`
1. `diskutil unmountDisk /dev/disk<disk# from diskutil>`
1. `sudo dd bs=1m if=image.img of=/dev/rdisk<disk# from diskutil> conv=sync`

### Set up Wifi
[`/boot/wpa_supplicant.conf`](https://raspberrypi.stackexchange.com/a/57023):

    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    network={
      ssid="MyWiFiNetwork"
      psk="MyPassword"
      key_mgmt=WPA-PSK
    }

### Enable ssh, Connect
1. `touch ssh`
1. plug in raspberry pi
1. find its IP: `sudo arp-scan --interface=en0 --localnet`
1. ssh in (u/p:pi/raspberry)

### Setup Raspberry Pi
1. `sudo raspi-config`
-- change password
-- enable SPI (interfacing options)
1. `sudo apt-get update`
1. `sudo apt-get upgrade -y`
1. `sudo apt-get install git`

### Setup Git
1. `ssh-keygen -t rsa -b 4096 -C “your@email.com”`
1. `eval "$(ssh-agent -s)"`
1. `ssh-add ~/.ssh/id_rsa`
1. `more ~/.ssh/id_rsa.pub` (copy to git)

### Checkout Repo
1. `git clone https://github.com/LesserChance/rpi-radio.git`
1. `cd rpi-radio`

### Install
1. `sudo bash ./install/install.sh`
1. optional reboot to confirm services come up automatically and cleanly from a reboot: `sudo shutdown -r now`

### Connect GPIO Pins
(pinout: https://pinout.xyz/)
#### OLED: https://www.adafruit.com/product/938
- Ground: 6 (gray)
- Vin: 1 (purple)
- CS: 24 (green)
- RST: 18 (yellow)
- SA0: 16 (orange)
- Clk: 23 (red)
- Data: 19 (brown)

#### Encoder: https://www.sparkfun.com/products/9117
TK

#### Power Switch: 
TK

#### Static LED: 
TK


