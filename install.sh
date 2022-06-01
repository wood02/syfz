#!/bin/bash

echo " "
tput setaf 4;
echo "#########################################################################"
echo "Installing Docker..."
echo "#########################################################################"
if [ -x "$(command -v docker)" ]; then
  tput setaf 2; echo "Docker already installed, skipping."
else
  curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
  tput setaf 2; echo "Docker installed!!!"
fi


echo " "
tput setaf 4;
echo "#########################################################################"
echo "Installing docker-compose"
echo "#########################################################################"
if [ -x "$(command -v docker-compose)" ]; then
  tput setaf 2; echo "docker-compose already installed, skipping."
else
  curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
  tput setaf 2; echo "docker-compose installed!!!"
fi




#echo " "
#tput setaf 4;
#echo "#########################################################################"
#echo "Checking Docker status"
#echo "#########################################################################"
#if systemctl is-active docker >/dev/null 2>&1; then
#  tput setaf 4;
#  echo "Docker is running."
#else
#  tput setaf 1;
#  echo "Docker is not running. Please run docker and try again."
#  echo "You can run docker service using sudo systemctl start docker"
#  exit 1
#fi



echo " "
tput setaf 4;
echo "#########################################################################"
echo "Installing Syfz"
echo "#########################################################################"
docker-compose up -d

tput setaf 2; echo "Syfz is installed!!!"

sleep 3


tput setaf 2; echo "Thank you for installing Syfz, happy recon!!"