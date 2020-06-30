#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python -y
sudo apt-get install python-pip -y
sudo pip install -U Flask
sudo pip install flask-restful
