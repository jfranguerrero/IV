# -*- coding: utf-8 -*-
import sys
import telebot
from telebot import types
import time
from skyscanner.skyscanner import Flights
from requests.exceptions import HTTPError
import os
import modules
import psycopg2
import pickle
import urlparse


reload(sys)
sys.setdefaultencoding('utf8')


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])



TOKEN =os.environ['token_vuelabot']


bot = telebot.TeleBot(TOKEN)

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            print "[" + str(cid) + "]: " + m.text


bot.set_update_listener(listener)

@bot.message_handler(commands=['start', 'help', 'ayuda'])
def command_ayuda(m):
    cid = m.chat.id

    salida="Funcinamiento de vuelaBot\n\n\nPara buscar un vuelo:\n/buscarvuelo Cod_Aeropuerto_Origen Cod_Aeropuerto_Destino Fecha_ida Fecha_vuelta\n\nMostrar códigos aeropuertos Españoles:\n /aeropuertos"
    bot.send_message(cid,salida)


@bot.message_handler(commands=['contacto'])
def command_contacto(m):
    cid = m.chat.id
    salida="Para cualquier duda, problema o sujerencia.\nEmail: jfranguerrero@gmail.com\nTelegram: @Jfguerrero"

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
            bot.send_message(cid, resultado, parse_mode="Markdown")


        except HTTPError as e:
            bot.send_message(cid,"Error en Código aeropuerto o fechas inválidas")


    except ValueError:
        bot.send_message(cid,"Fecha incorrecta, Debe ser DD/MM/AAAA. Los códigos de aeropuerto deben de tener 3 caracteres")

@bot.message_handler(commands=['aeropuertos'])
def command_aeropuertos(m):


    cid = m.chat.id
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    c = conn.cursor()

    salida=''
    c.execute("""SELECT * from aeropuertos""")
    rows =c.fetchall()
    for row in rows:
        salida+="País: "+row[2]+', Ciudad: '+row[1]+", Código aeropuerto: "+row[0]+'\n'

    bot.send_message(cid,salida)
    c.close()
    conn.close()


bot.polling(none_stop=True)
