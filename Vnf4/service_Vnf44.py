from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import socket
import os
import time, threading
import commands
import fileinput
import json
import requests 


#global ports
#ports = 4500
global automation_id
automation_id = 0


app = Flask(__name__)

@app.route('/check/',methods = ['GET'])
def check():
  print("the Monitoring Service is up and Running")
  return "the Monitoring Service is up and Running"
#3 options, load, start and stop the new service 
@app.route('/start/',methods = ['POST'])
def start():
 
  global automation_id
  camera_name = request.args.get('camera_name','')
  network_url = request.args.get('network_url','')
  object_name = request.args.get('object_name','')  
  ports = request.args.get('ports','')  
  time.sleep(2)

  cmd = 'mkdir -m 777 "/home/ubuntu/monitoring/data/"' + camera_name
  path = '/home/camera/data_obj_detection/' + camera_name
  #path = '/home/ubuntu/monitoring/data/' + camera_name
  print("Create mqttInfluxDb service")
  #Create ,write  MqttInfluxDB.py file
  with open('/home/camera/MqqtInfluxDb/MqttInfluxDB.py', 'r') as file :
  #with open('/home/ubuntu/monitoring/Mqttinfluxdb/MqttInfluxDB.py', 'r') as file :
    filedata = file.read()
    filedata = filedata.replace('person', object_name)
    filedata = filedata.replace('cam_name', camera_name)
  cmd = 'touch ' + path + '/MqttInfluxDB_' + camera_name + '.py'
  os.system(cmd)
  with open(path + '/MqttInfluxDB_' + camera_name + '.py', 'w') as file:
    file.write(filedata)
  time.sleep(1)

  print("Run mqttInfluxDb service")
  # run the MqttInfluxDB.py file
  cmd = 'python ' + path + '/MqttInfluxDB_' + camera_name + '.py &'
  os.system(cmd) 

  time.sleep(1)
  print("Upadate Grafana Dashboard")
  #create new dashboard for grafana
  with open('/home/camera/grafana_dashboards/panel.json', 'r') as file :
  #with open('/home/ubuntu/monitoring/grafan/panel.json', 'r') as file :
    filedata = file.read()
    filedata = filedata.replace('000', str(automation_id))
    filedata = filedata.replace('cam_name', camera_name)
    filedata = filedata.replace('ports', str(ports))
  cmd = 'touch ' + path + '/panel_' + camera_name + '.json'
  os.system(cmd)

  
  with open(path + '/panel_' + camera_name + '.json', 'w') as file:
    file.write(filedata)
  cmd = 'curl -X POST -H "Content-Type: application/json" -d @' + path + '/panel_' + camera_name + '.json http://admin:admin@localhost:3000/api/dashboards/db'
  os.system(cmd)

  #ports = ports + 1
  automation_id = automation_id + 1
  print("automation_id  : " + str(automation_id))

  return "Monitoring for  " + camera_name + " Started"


@app.route('/stop/',methods = ['POST'])
def stop():
  #global automation_id
  camera_name = request.args.get("camera_name","")

  path = '/home/camera/data_obj_detection/' + camera_name + '/'
  #path = '/home/ubuntu/monitoring/data/' + camera_name + '/'
  print("Stop Mqqt Infuxdb")
  cmd = 'sudo pkill -9 -f MqttInfluxDB_' + camera_name + '.py'
  os.system(cmd) 
  cmd = 'sudo rm -rf ' + path + 'MqttInfluxDB_' + camera_name + '.py'
  os.system(cmd)

  
  with open(path + 'panel_' + camera_name + '.json', 'r') as file:
    panel_conf  = json.load(file)
  uid = str(panel_conf["dashboard"]["uid"])
  cmd = 'sudo rm -rf ' + path + 'panel_' + camera_name + '.json'
  os.system(cmd)
  
  print("Remove Dashboard")
  cmd = 'curl -X DELETE -H "Content-Type: application/json" http://admin:admin@localhost:3000/api/dashboards/uid/' + uid
  os.system(cmd)
  cmd = 'sudo rm -rf ' + path + camera_name + '.json'
  os.system(cmd)  

  return "Monitoring for  " + camera_name + " Stopped"
  
if __name__ == '__main__':
    app.run(debug=True, host='192.168.79.4',port=5003)


