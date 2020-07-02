from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import socket
import os
import time, threading
import commands
import fileinput
import json
#import settings


ports = 4500
automation_id = 1584118258158
app = Flask(__name__)

#3 options, load, start and stop the new service 
@app.route('/check/',methods = ['GET'])
def check():
  print("the DetectionService is up and Running")
  return "the Detection Service Service is up and Running"

@app.route('/start/',methods = ['POST'])
def start():
  camera_name = request.args.get('camera_name','')
  network_url = request.args.get('network_url','')
  object_name = request.args.get('object_name','')  


  global ports, automation_id
  docker_ports = str(ports) + ':' + str(ports)
  print("Frigate Camera Settings Configurations")
  with open('/home/camera/frigate/configs/config.yml', 'r') as file :
    filedata = file.read()

# Replace the target string
  filedata = filedata.replace('person', object_name)
  filedata = filedata.replace('network_url', network_url)
  filedata = filedata.replace('name_cam', camera_name)
  filedata = filedata.replace('port_web', str(ports))
  cmd = 'mkdir -m 777 "/home/camera/frigate/"' + camera_name
  os.system(cmd)

# Write the file out again
  with open('/home/camera/frigate/' + camera_name + '/config.yml', 'w') as file:
    file.write(filedata)


  time.sleep(2)

  time.sleep(30)
  print("Run Object Detection Service  at Ports : " + str(ports))
  cmd = 'sudo docker run -d --name ' + camera_name + ' --rm --privileged --shm-size=1g -v /dev/bus/usb:/dev/bus/usb -v /home/camera/frigate/' + camera_name + ':/config:ro -p ' + docker_ports + ' -e RTSP_PASSWORD="admin" frigate2:latest'
  os.system(cmd)

  ports = ports + 1
  print("Update Ports : " + str(ports))
  time.sleep(2)


  return "Service " + camera_name + " Started"




#stop the service 
@app.route('/stop/',methods = ['POST'])
def stop():
  camera_name = request.args.get("camera_name","")

  global ports, automation_id


  print("Stop container service of " + camera_name)
  cmd = 'sudo docker rm -f ' + camera_name
  os.system(cmd)
  return "Service " + camera_name + " Stopped"
  
if __name__ == '__main__':
    app.run(debug=True, host='192.168.79.18')
