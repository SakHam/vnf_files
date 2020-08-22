from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import socket
import os
import time, threading
import commands
import fileinput
import json
#import settings


global ports
ports = 4500
global automation_id
automation_id = 0
global camera_back_up
camera_back_up = "NONE"

app = Flask(__name__)

#3 options, load, start and stop the new service 

@app.route('/check/',methods = ['GET'])
def check():
  print("Service is Up & Running")

@app.route('/start/',methods = ['POST'])
def start():

  global ports, automation_id, camera_back_up
  camera_name = request.args.get('camera_name','')
  network_url = request.args.get('network_url','')
  object_name = request.args.get('object_name','')  


  if object_name == "person" :
    print(object_name)
    docker_ports = str(ports) + ':' + str(ports)
    docker_ports1 = str(ports) + ':5000'
    print("Frigate Camera Settings Configurations")
    with open('/home/camera/frigate/configs/config.yml', 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('obj_name', object_name)
    filedata = filedata.replace('network_url', network_url)
    filedata = filedata.replace('name_cam', camera_name)
    filedata = filedata.replace('port_web', str(ports))
    cmd = 'mkdir -m 777 "/home/camera/data_obj_detection/"' + camera_name
    os.system(cmd)
    path = '/home/camera/data_obj_detection/' + camera_name
    # Write the file out again
    with open(path + '/config.yml', 'w') as file:
      file.write(filedata)
    


    time.sleep(1)


    print("Create mqttInfluxDb service")
    #Create ,write  MqttInfluxDB.py file
    with open('/home/camera/MqqtInfluxDb/MqttInfluxDB.py', 'r') as file :
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
      filedata = file.read()
      filedata = filedata.replace('000', str(automation_id))
      filedata = filedata.replace('cam_name', camera_name)
      filedata = filedata.replace('ports', str(ports))
    cmd = 'touch ' + path + '/panel_' + camera_name + '.json'
    os.system(cmd)

  
    with open(path + '/panel_' + camera_name + '.json', 'w') as file:
      file.write(filedata)
    cmd = 'curl -X POST -H "Content-Type: application/json" -d @' + path + '/panel_' + camera_name + '.json http://root:root@localhost:3000/api/dashboards/db'
    os.system(cmd)


    automation_id = automation_id + 1
    print("automation_id  : " + str(automation_id))


    print("Run Object Detection Service  at Ports : " + str(ports))
    cmd = 'sudo docker run -d --name ' + camera_name + ' --rm --privileged --shm-size=1g -v /dev/bus/usb:/dev/bus/usb -v ' + path  + ':/config:ro -p ' + docker_ports + ' -e RTSP_PASSWORD="admin" frigate2:latest'
    #cmd = 'sudo docker run -d --name ' + camera_name + ' -p ' + docker_ports1 + ' yolo_video:v0'    
    os.system(cmd)

    ports = ports + 1
    print("Update Ports : " + str(ports))
    time.sleep(2)


    return "Service " + camera_name + " Started"
  else:

    print(object_name)
    docker_ports1 = str(ports) + ':5000'
    cmd = 'mkdir -m 777 "/home/camera/data_obj_detection/"' + camera_name
    os.system(cmd)
    path = '/home/camera/data_obj_detection/' + camera_name

    print("Create mqttInfluxDb service")
    #Create ,write  MqttInfluxDB.py file
    with open('/home/camera/MqqtInfluxDb/MqttInfluxDB.py', 'r') as file :
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
      filedata = file.read()
      filedata = filedata.replace('000', str(automation_id))
      filedata = filedata.replace('cam_name', camera_name)
      filedata = filedata.replace('ports', str(ports))
    cmd = 'touch ' + path + '/panel_' + camera_name + '.json'
    os.system(cmd)

  
    with open(path + '/panel_' + camera_name + '.json', 'w') as file:
      file.write(filedata)
    cmd = 'curl -X POST -H "Content-Type: application/json" -d @' + path + '/panel_' + camera_name + '.json http://root:root@localhost:3000/api/dashboards/db'
    os.system(cmd)


    automation_id = automation_id + 1
    print("automation_id  : " + str(automation_id))


    print("Run Object Detection Service  at Ports : " + str(ports))
    cmd = 'sudo docker run -d --name ' + camera_name + ' -p ' + docker_ports1 + ' yolo_video:v1'    
    os.system(cmd)
    time.sleep(10)
    cmd = "curl --location --request POST 'http://localhost:" + str(ports) + "/inputs/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "'"
    os.system(cmd)

    ports = ports + 1
    print("Update Ports : " + str(ports))
    time.sleep(2)
    
    #cmd = 'curl --data "camera_name=' + camera_name + '&network_url=' + network_url + '&object_name=' + object_name  + '" -X POST http://localhost:4500/inputs/'
    


    return "Service " + camera_name + " Started"




#stop the service 
@app.route('/stop/',methods = ['POST'])
def stop():
  camera_name = request.args.get("camera_name","")

  global ports, automation_id, camera_back_up
  path = '/home/camera/data_obj_detection/' + camera_name + '/'
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
  cmd = 'curl -X DELETE -H "Content-Type: application/json" http://root:root@localhost:3000/api/dashboards/uid/' + uid
  os.system(cmd)
  cmd = 'sudo rm -rf ' + path + camera_name + '.json'
  os.system(cmd)

  print("Remove frigate config file")
  cmd = 'sudo rm -rf ' + path + 'config.yml'
  os.system(cmd)
  
  print("Stop Container")

  print("Stop container service of " + camera_name)
  cmd = 'sudo docker rm -f ' + camera_name
  os.system(cmd)


  return "Service " + camera_name + " Stopped"
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
