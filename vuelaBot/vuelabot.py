# -*- coding: utf-8 -*-
import sys
import telebot
from telebot import types
import time
from skyscanner.skyscanner import Flights
from requests.exceptions import HTTPError
import os
import sqlite3
import modules

reload(sys)
sys.setdefaultencoding('utf8')



TOKEN =os.environ['token_vuelabot']


bot = telebot.TeleBot(TOKEN)

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            print "[" + str(cid) + "]: " + m.text


bot.set_update_listener(listener)

@bot.message_handler(commands=['buscarvuelo'])
def command_buscarvuelo(m):
    cid = m.chat.id
    mensaje = m.text[13:]
    dic_datos=modules.separar_mensaje_busqueda(mensaje)


    try:
        fechas=modules.convertir_fechas(dic_datos['fida'], dic_datos['fvuelta'])
        try:
            result = modules.buscarvuelo_live(dic_datos['origen'], dic_datos['destino'], fechas['fida'], fechas['fvuelta'])

            bot.send_message(cid, "Buscando vuelos a " +dic_datos['destino'] +" con origen "+dic_datos['origen'])
            resultado=modules.procesar_resultados(result)
            bot.send_message(cid, resultado)


        except HTTPError as e:
            bot.send_message(cid,"Error en Código aeropuerto o fechas inválidas")


    except ValueError:
        bot.send_message(cid,"Fecha incorrecta, Debe ser DD/MM/AAAA. Los códigos de aeropuerto deben de tener 3 caracteres")

@bot.message_handler(commands=['aeropuertos'])
def command_aeropuertos(m):
    cid = m.chat.id
    con_bd = sqlite3.connect('vuelabot.db')
    c = con_bd.cursor()

    salida=''
    for row in c.execute('SELECT * FROM aeropuertos'):
        salida+="País: "+row[2]+', Ciudad: '+row[1]+", Código aeropuerto: "+row[0]+'\n'

    bot.send_message(cid,salida)
#    con_bd.commit()
    con_bd.close()


bot.polling(none_stop=True)
