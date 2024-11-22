#!/bin/bash
# RTS, march 2021
# update nov 2024
#-------------------------------------------
clear
echo "WELCOME - basics for AI in Ethnobotany - Return to Bali installaton "

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3-dev -y
sudo apt-get install build-essential python3-dev -y
sudo apt-get install python3-venv -y
sudo apt-get install ffmpeg -y
sudo apt-get install sox -y
sudo apt-get install libcurl4-openssl-dev

echo "installed python3, python3dev, python3-venv, ffmpeg, sox "

echo "hit ctrl d to close this session"
exit 0

