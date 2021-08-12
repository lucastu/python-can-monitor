# Files

**Dashboard_main.py**  => main script contain everything 

**alert.py** => exemple of multiple windows grammar

**interface.ui** => XML file that contains the mainwindow graphical setup

**launcher.sh** => bash file to launch main script if it's not open, else it put the window in front

**notif.py** => ancien script of display a notif base of what I need to write 

**ombre.py** => empty window that is supposed to open fullscreen and with transparency

**sound_level.py** => contain the class of the sound_level display script

**source_handler** => contain what I need to handler the data from the arduino

# Dependancys
## pour demarrer le gestionnaire de fenetre au demarrage
```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
Edit the file to add  :

> picom -b --config /config2-picom.conf

Ex :
```
    @lxpanel --profile LXDE-pi
    @pcmanfm --desktop --profile LXDE-pi
    @xscreensaver -no-splash
    @picom -b --config /config2-picom.conf
    point-rpi
    xset s off
    xset s noblank
    xset -dpms
    /usr/local/bin/openauto
    /usr/local/bin/controller_service_watchdog.sh
```

## Pour la barre de chargement du volume
```
sudo apt install cmake build-essential tcl-dev tk-dev python3-tk
python -m pip install scikit-build
python setup.py install

sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3

sudo apt-get install -y python-pil.imagetk
sudo pip3 install tksvg

sudo apt install cmake meson git pkg-config asciidoc libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev libdbus-1-dev libconfig-dev libgl1-mesa-dev  libpcre2-dev  libevdev-dev uthash-dev libev-dev libx11-xcb-dev
git clone https://github.com/yshui/picom
cd picom
git submodule update --init --recursive
meson --buildtype=release . build
ninja -C build
sudo ninja -C build install


sudo apt-get install python3-pyqt5
```