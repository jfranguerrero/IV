from fabric.api import *
import os

env.host = ['usuario:22']

def download():
    run ('sudo rm -rf IV')
    run ('sudo git clone https://github.com/jfranguerrero/IV')

def nohup():
    with shell_env(api_skyscanner=os.environ['api_skyscanner'], DATABASE_URL=os.environ['DATABASE_URL'], token_vuelabot=os.environ['token_vuelabot']):
        run("nohup python IV/vuelaBot/vuelabot.py >& /dev/null < /dev/null &",pty=False)

def start():
    with shell_env(api_skyscanner=os.environ['api_skyscanner'], DATABASE_URL=os.environ['DATABASE_URL'], token_vuelabot=os.environ['token_vuelabot']):
        run ('python IV/vuelaBot/vuelabot.py')

def stop():
    run ('kill -9 $(pidof python)')

def delete():
    run ('rm -rf IV')

def tests():
    run ('cd IV && make test')

def install():
    run ('cd IV && make install')
