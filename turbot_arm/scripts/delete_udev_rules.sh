#!/bin/bash

echo "delete remap the device serial port(ttyUSBX) to turbot_arm"
echo "sudo rm   /etc/udev/rules.d/arm.rules"
sudo rm   /etc/udev/rules.d/arm.rules
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish  delete"
