#!/bin/bash
echo 461 > /sys/class/gpio/export                #Motor pins 
echo "out" > /sys/class/gpio/gpio461/direction   #A0 for Output Arduino
echo 487 > /sys/class/gpio/export 
echo "out" > /sys/class/gpio/gpio487/direction   #A1 for Output Arduino

echo 337 > /sys/class/gpio/export                #Input LED Pins
echo "out" > /sys/class/gpio/gpio337/direction   #A0 for Input Arduino
echo 501 > /sys/class/gpio/export 
echo "out" > /sys/class/gpio/gpio501/direction   #A1 for Input Arduino

