# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
"Interface with the dataabse"
#from votoAppWSClient.models import Censo, Voto
import requests
from django.conf import settings


def verificar_censo(censo_data):
    """ Check if the voter is registered in the Censo
    :param censo_dict: dictionary with the voter data
                       (as provided by CensoForm)
    :return True or False if censo_data is not valid
    """
    response = requests.post(settings.RESTAPIBASEURL + "censo/", json=censo_data)
    if response.status_code != 200:
        return False
    return True


def registrar_voto(voto_dict):
    """ Register a vote in the database
    :param voto_dict: dictionary with the vote data (as provided by VotoForm)
      plus de censo_id (numeroDNI) of the voter
    :return new voto info if succesful, None otherwise
    """
    response = requests.post(settings.RESTAPIBASEURL + "voto/", json=voto_dict)
    # get default values from voto
    voto = response.json()
    if response.status_code != 200:        
        return None
    return voto


def eliminar_voto(idVoto):
    """ Delete a vote in the database
    :param idVoto: id of the vote to be deleted
    :return True if succesful,
     False otherwise
     """
    response = requests.delete(settings.RESTAPIBASEURL + "voto/"+idVoto+"/")
    if response.status_code != 200:
        return False
    return True



def get_votos_from_db(idProcesoElectoral):
    """ Gets votes in the database correspondint to some electoral processs
    :param idProcesoElectoral: id of the vote to be deleted
    :return list of votes found
     """
    response = requests.get(settings.RESTAPIBASEURL + "testbd/getvotos/" + idProcesoElectoral)
    if response.status_code != 200:
        return None 
    return response.json()
