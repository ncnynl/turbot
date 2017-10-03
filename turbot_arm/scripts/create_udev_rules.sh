#!/bin/bash

echo "remap the device serial port(ttyUSBX) to turbot_arm"
echo "turbot_arm usb connection as /dev/arm , check it using the command : ls -l /dev|grep ttyUSB"
echo "start copy arm.rules to  /etc/udev/rules.d/"
echo "`rospack find turbot_arm`/scripts/arm.rules"
sudo cp `rospack find turbot_arm`/scripts/arm.rules  /etc/udev/rules.d
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish "
