

setting up a joycon test:

kernel driver:
First, install dkms-hid-nintendo:

Update: hid-nintendo is present on Linux's Kernel starting from 5.10! If your kernel is 5.10 or above, skip this step.

git clone https://github.com/nicman23/dkms-hid-nintendo
cd dkms-hid-nintendo
sudo dkms add .
sudo dkms build nintendo -v 3.0
sudo dkms install nintendo -v 3.0

userspace:
Then, install joycond:

git clone https://github.com/DanielOgorchock/joycond
cd joycond
sudo apt install cmake libevdev-dev
cmake .
sudo make install
sudo systemctl enable --now joycond



udev rules:
/etc/udev/rules.d/50-nintendo-switch.rules
```
# Switch Joy-con (L) (Bluetooth only)
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", KERNELS=="0005:057E:2006.*", MODE="0666"

# Switch Joy-con (R) (Bluetooth only)
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", KERNELS=="0005:057E:2007.*", MODE="0666"

# Switch Pro controller (USB and Bluetooth)
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="057e", ATTRS{idProduct}=="2009", MODE="0666"
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", KERNELS=="0005:057E:2009.*", MODE="0666"

# Switch Joy-con charging grip (USB only)
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="057e", ATTRS{idProduct}=="200e", MODE="0666"
```


now to get the info in python. First need to id the combined device:

1) pair by holding the battery level buttons
2) press L+R to create combined device

python3 ./.local/lib/python3.8/site-packages/evdev/evtest.py







