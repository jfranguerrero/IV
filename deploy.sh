#!/bin/bash

sudo apt-get update

wget https://releases.hashicorp.com/vagrant/1.8.7/
sudo dpkg -i vagrant_1.8.7_x86_64.deb

sudo vagrant plugin install vagrant-azure

# Instalación Ansible
sudo apt-get install ansible


# Despliegue en Azure
sudo vagrant up --provider=azure

# Despliegue de la aplicación con Fabric
sudo pip install fabric

fab -p N1_n2n3n4_N5 -H usuario@vuelabot.cloudapp.net nohup
