#!/usr/bin/python
# -*-coding:Latin-1 -*

import requests
import json
import time
import os
import sys

def Centreon_Status():
    #Cette fonction permet de recuperer tous les hosts ainsi que les services que Centreon gere et qui sont soit dans un etat "CRITICAL" ou bien "down"
  api_url = 'http://10.2.100.33/centreon/api/index.php'

  # Header et params servent à l'authentification et retourne un token valable 10 minutes
  headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
  }
  params = (
      ('action', 'authenticate'),
  )
  # data contient le contient utliser pour recuperer toutes les informations
  data = [
    ('username', 'Tabata'),
    ('password', 'OtWDt87u'),
  ]

  # On envoie la requête avec les informations header, params et data et on recupere le token de la session que l'on stocke dans authToken
  json_authToken = requests.post(api_url, headers=headers, params=params, data=data)
  authToken = json_authToken.text[14:-2]

  # A partir d'ici on recupere tous les services et hosts qui sont en etat CRITICAL ou down
  header = {
      'Content-Type': 'application/json',
      'centreon-auth-token': authToken,
  }
  # Apres plusieurs test, on recupere tous les services que l'on triera plus tard
  params_services = (
      ('object', 'centreon_realtime_services'),
      ('action', 'list'),
      ('viewType', 'problems'),
      ('limit', '500'),
  )
  params_hosts = (
      ('object', 'centreon_realtime_hosts'),
      ('action', 'list'),
      ('status', 'down'),
  )

  # On stock les services et les hosts dans deux variables
  json_status = requests.get(api_url, headers=header, params=params_services)
  json_hosts = requests.get(api_url, headers=header, params=params_hosts)

  status = json.loads(json_status.text)
  hosts = json.loads(json_hosts.text)

  lng_status = len(status)
  lng_hosts = len(hosts)

  host_problem = []
  service_problem = []

  # On trie les services en etat "CRITICAL"
  # On laisse 5 minutes aux services et aux hosts pour leur laisser la possibiliter de se resoudre seul
  # Sinon on affiche le probleme et si le probleme persiste plus de 15 minutes, on l'ignore puisque qu'il aura dejà ete annonce
  # On prepare ce que Nikita lira lors de la commande vocal
  if lng_status > 0 or lng_hosts > 0:
    for x in status:
        if x['output'].find('CRITICAL') != -1:
            service_problem.append(x['name'])
        if (x['output'].find('CRITICAL') != -1) and ((int(time.time()) - int(x['last_state_change'])) >= 300) and ( (int(time.time()) - int(x['last_state_change'])) <= 840):
            print("Les services " + x['name']  + " sont toujours indisponible")
    for y in hosts:
        host_problem.append(y['alias'])
        if ( (int(time.time()) - int(y['last_state_change'])) >= 300 ) and ( (int(time.time()) - int(y['last_state_change'])) <= 840):
             print("Les host  " + y['alias'] + ", est toujours inactif")
  else:
      print("Aucun probleme avec Centreon")


  # On retourne ensuite les problemes des services et des hosts dans un array pour que l'interface puisse les afficher
  problems = []
  problems.append(host_problem)
  problems.append(service_problem)

  return problems


Centreon_Status()
