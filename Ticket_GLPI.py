#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import os
import sys

def New_Ticket():
  # Authentification au compte stagiaire.info afin de recuperer le token de session
  app_token = '0ak4H1pmTmzj4yANaMlC2OU5ZvXL92WA7ipLlItB'
  url ='http://glpi/glpi/apirest.php/initSession'

  headers = {
      'Content-Type':'application/json',
      'Authorization': 'Basic c3RhZ2lhaXJlLmluZm86aXQxNTBr',
      'App-Token':'0ak4H1pmTmzj4yANaMlC2OU5ZvXL92WA7ipLlItB'
  }

  response = requests.get('http://glpi/glpi/apirest.php/initSession', headers = headers)


  Init_session = json.loads(response.text)

  token = Init_session['session_token']

  # Recuperation des tickets
  headers_ticket = {
      'Content-Type':'application/json',
      'Session-Token' : token,
      'App-Token':'0ak4H1pmTmzj4yANaMlC2OU5ZvXL92WA7ipLlItB'
  }

  response = requests.get('http://glpi/glpi/apirest.php/Ticket/?order=DESC&expand_drodpowns=true', headers = headers_ticket)
  # On stock tous les tickets
  all_ticket = json.loads(response.text)
  global new_ticket
  new_ticket = []

  lng_new_ticket = 0
  # On verifie leurs status
  # 1 = Nouveau
  for ticket in all_ticket:
    if ticket["status"] == 1:
      lng_new_ticket += 1
      new_ticket.append(ticket)
  # On retourne la phrase que Nikita lira lors d'une demande vocal
  if lng_new_ticket != 0:
    print("La pause est terminer messieurs")
    print("Vous avez %s nouveaux tickets" % lng_new_ticket)
  else:
    print("Vous n'avez aucun nouveaux ticket")

  return new_ticket

#Definir une fonction qui retournera le nombre de nouveau ticket au GUI

New_Ticket()
