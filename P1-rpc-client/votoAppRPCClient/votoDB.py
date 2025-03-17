# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
"Interface with the dataabse"
from django.conf import settings
from xmlrpc.client import ServerProxy

def verificar_censo(censo_data):
    """ Esta funcion verifica si un votante esta registrado en el censo.
        Para comprobarlo, llama al servidor RPC

        :param censo_data: Diccionario que contiene los datos del votante
        :return: True si está registrado y es correcto
                 False en caso contrario
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.verificar_censo(censo_data)


def registrar_voto(voto_dict):
    """ Esta funcion registra un voto a traves del servidor RPC

    :param voto_dict: Diccionario con los datos del voto
    :return: Informacion del voto registrado si es exitoso
             None en caso de error.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.registrar_voto(voto_dict)


def eliminar_voto(idVoto):
    """ Esta funcion elimina un voto en el servidor RPC
    
    :param idVoto: ID del voto que se quiere eliminar
    :return: True si se ha eliminado correctamente
             False en caso contrario
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.eliminar_voto(idVoto)


def get_votos_from_db(idProcesoElectoral):
    """ Esta funcion obtiene los votos de un proceso electoral desde el servidor RPC
    
    :param idProcesoElectoral: ID del proceso electoral
    :return: Lista de votos encontrados para ese ID
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.get_votos_from_db(idProcesoElectoral)
