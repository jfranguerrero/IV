FROM ubuntu:14.04
MAINTAINER Jose Francisco Guerrero Collantes <jfranguerrero@gmail.com>
#instalamos git
RUN apt-get -y update
RUN apt-get install -y git

#Clonamos repositorio
RUN sudo git clone https://github.com/jfranguerrero/IV

#Instalamos herramientas
RUN sudo apt-get -y update
RUN sudo apt-get install -y python-setuptools
RUN sudo apt-get -y install python-dev
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install python-psycopg2
RUN sudo apt-get -y install libpq-dev
RUN sudo easy_install3 pip
RUN sudo pip install --upgrade pip

ENV token_vuelabot="250787379:AAFbu2eez-nF0_a-hLPWbqM3Vqd_uWR9eqE"
ENV DATABASE_URL="postgres://nplqfozzkewmas:2Qjia0d5phK20qOE53hcYWGJtA@ec2-23-21-238-76.compute-1.amazonaws.com:5432/ddf30htb3vtksc"
ENV api_skyscanner="st701826977373404435621936935426"

RUN cd IV/ && make install
