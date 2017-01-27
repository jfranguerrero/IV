from fabric.api import *

env.host = ['usuario:22']

def download():
    run ('sudo rm -rf IV')
    run ('sudo git clone https://github.com/jfranguerrero/IV')

def start():
    run ('sudo python IV/vuelaBot/vuelabot.py')

def stop():
    run ('kill -9 $(pidof python)')

def delete():
    run ('rm -rf IV')

def tests():
    run ('cd IV && make test')

def install():
run ('cd IV && make install')
