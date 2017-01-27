import unittest
from requests import HTTPError
from skyscanner.skyscanner import Flights
import modules
import os
import time
import pickle
import sqlite3
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


class vuelaBotTest(unittest.TestCase):
    def test_busqueda_vuelo(self):
        self.result=modules.buscarvuelo_live('AGP', 'BCN', '2017-3-11', '2017-3-15')
        self.assertTrue(self.result is not None)
        self.assertTrue('Itineraries' in self.result)
        self.assertTrue(len(self.result['Itineraries']) > 0)

    def test_procesamiento_mensaje(self):
        salida=modules.separar_mensaje_busqueda('AGPBCN12/11/201623/12/2016')
        self.assertEquals(salida['origen'],'AGP')
        self.assertEquals(salida['destino'],'BCN')
        self.assertEquals(salida['fida'],'12/11/2016')
        self.assertEquals(salida['fvuelta'],'23/12/2016')

    def test_conversion_fecha(self):
        salida=modules.convertir_fechas('12/11/2016','23/12/2016')
        self.assertEquals(salida['fida'],'2016-11-12')
        self.assertEquals(salida['fvuelta'],'2016-12-23')


    def test_procesamiento_resultados(self):
        result_tests=load_obj('vuelos_test_results')
        salida=modules.procesar_resultados(result_tests)
        results_procesamiento=load_obj('test_resultado_mostrar')
        self.assertEquals(salida,results_procesamiento)


    def test_basedatos(self):

        con_bd =psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        c = con_bd.cursor()
        ciudad=('BCN', )

        c.execute('SELECT cod_aeropuerto FROM aeropuertos WHERE cod_aeropuerto=%s', ciudad)

        self.assertEquals(c.fetchone()[0],'BCN')
        con_bd.close()


if __name__ == '__main__':
    unittest.main()
