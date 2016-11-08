# -*- coding: utf-8 -*-
from skyscanner.skyscanner import Flights
import datetime
import sys
import psycopg2
reload(sys)
sys.setdefaultencoding('utf8')


def buscarvuelo_live( origen, destino, fecha_ida, fecha_vuelta):
    flights_service = Flights(os.environ['api_skyscanner'])
    result = flights_service.get_result(
            errors='graceful',
            country='ES',
            currency='EUR',
            locale='es-ES',
            originplace=origen+'-sky',
            destinationplace=destino+'-sky',
            outbounddate=fecha_ida,
            inbounddate=fecha_vuelta,
            adults=1).parsed

    return result


def separar_mensaje_busqueda(mensaje):
    mensaje = ''.join(mensaje.split())
    origen=mensaje[0:3]
    destino=mensaje[3:6]
    fida=mensaje[6:16]
    fvuelta=mensaje[16:26]
    return {'origen':origen, 'destino':destino ,'fida':fida , 'fvuelta':fvuelta }


def convertir_fechas(ida, vuelta):
    datetime.datetime.strptime(ida, '%d/%m/%Y')
    datetime.datetime.strptime(vuelta, '%d/%m/%Y')
    fida=datetime.datetime.strptime(ida, '%d/%m/%Y').strftime('%Y-%m-%d')
    fvuelta=datetime.datetime.strptime(vuelta, '%d/%m/%Y').strftime('%Y-%m-%d')
    return {'fida':fida , 'fvuelta':fvuelta }


def procesar_resultados( result):
    try:

        resultado='Precio: *'+str(result['Itineraries'][0]['PricingOptions'][0]['Price'])+' €*\n\n'
        cod_ida=result['Itineraries'][0]['OutboundLegId']
        cod_vuelta=result['Itineraries'][0]['InboundLegId']

        for item in result['Legs']:
            if (item['Id']==cod_ida):
                hora_salida=item['Departure']
                cod_aero=item['Carriers'][0]
                resultado+='IDA:\nHora de salida: '+hora_salida+'\n'
                for item2 in result['Carriers']:
                    if(item2['Id']==cod_aero):
                        nombre_aero=item2['Name']
                        resultado+='Aerolinea: *'+nombre_aero+'*\n\n'

        for item in result['Legs']:
            if (item['Id']==cod_vuelta):
                hora_salida=item['Departure']
                cod_aero=item['Carriers'][0]
                resultado+='VUELTA:\nHora de salida: '+hora_salida+'\n'
                for item2 in result['Carriers']:
                    if(item2['Id']==cod_aero):
                        nombre_aero=item2['Name']
                        resultado+='Aerolinea: *'+nombre_aero+'*\n\n'

        link=result['Itineraries'][0]['PricingOptions'][0]['DeeplinkUrl']

        resultado+='[Reservar Aquí]('+link+')'

        return resultado
    except (NameError, TypeError, IndexError):
        return "No se han encontrado resultados."
