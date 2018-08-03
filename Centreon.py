#!/usr/bin/python

import requests
import json
import time
import os
import sys

def Centreon_Status():
  api_url = 'http://10.2.100.33/centreon/api/index.php'

  headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
  }

  params = (
      ('action', 'authenticate'),
  )

  data = [
    ('username', 'Tabata'),
    ('password', 'OtWDt87u'),
  ]


  json_authToken = requests.post(api_url, headers=headers, params=params, data=data)

  authToken = json_authToken.text[14:-2]


  header = {
      'Content-Type': 'application/json',
      'centreon-auth-token': authToken,
  }

  params_status = (
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

  json_status = requests.get(api_url, headers=header, params=params_status)
  json_hosts = requests.get(api_url, headers=header, params=params_hosts)

  status = json.loads(json_status.text)
  hosts = json.loads(json_hosts.text)

  lng_status = len(status)
  lng_hosts = len(hosts)

  host_problem = []
  service_problem = []


  if lng_status > 0 or lng_hosts > 0:
    for x in status:
      if (x['output'].find('CRITICAL') != -1) and ((int(time.time()) - int(x['last_state_change'])) >= 240) and ( (int(time.time()) - int(x['last_state_change'])) <= 900000):
        print("Les services " + x['name']  + " sont toujours indisponible")
        service_problem.append(x['name'])
    for y in hosts:
           if ( (int(time.time()) - int(y['last_state_change'])) >= 240 ) and ( (int(time.time()) - int(y['last_state_change'])) <= 900000):
             print("Les host  " + y['alias'] + ", est toujours inactif")
             host_problem.append(y['alias'])


  problems = []
  problems.append(host_problem)
  problems.append(service_problem)


  if not (len(host_problem) > 0 or len(service_problem) > 0):
    print "Pas de probleme avec les host ou les services"
  return problems


Centreon_Status()
