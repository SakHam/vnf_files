from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import socket
import os
import time, threading
import commands
import fileinput
import json
#import requests 


#global ports
#ports = 4500

app = Flask(__name__)

#3 options, load, start and stop the new service 
@app.route('/check/',methods = ['GET'])
def check():
  print("the Detection Service 1 is up and Running")
  return "the Detection Service 1 is up and Running"

@app.route('/start/',methods = ['POST'])
def start():
  if request.method == 'POST':
    print("POST")
  #global ports
  #args = request.args.get
  #print(args)
  camera_name = request.args.get("camera_name","")
  network_url = request.args.get('network_url','')
  object_name = request.args.get('object_name','')  
  ports = request.args.get('ports', type=int) 
  print("Camera name :")
  print(camera_name)

  docker_ports = str(ports) + ':' + str(ports)
  docker_ports1 = str(ports) + ':5000'
  print("Frigate Camera Settings Configurations")
  with open('/home/ubuntu/services/frigate/configs/config.yml', 'r') as file :
  #with open('/home/ubuntu/object_detection/frigate/configs/config.yml', 'r') as file :
    filedata = file.read()

    # Replace the target string
  filedata = filedata.replace('obj_name', object_name)
  filedata = filedata.replace('network_url', network_url)
  filedata = filedata.replace('name_cam', camera_name)
  filedata = filedata.replace('port_web', str(ports))
  cmd = 'mkdir -m 777 "/home/ubuntu/object_detection/"' + camera_name
  #cmd = 'mkdir -m 777 "/home/ubuntu/object_detection/data/"' + camera_name
  os.system(cmd)
  path = '/home/ubuntu/object_detection/' + camera_name
  #path = '/home/ubuntu/object_detection/data/' + camera_name
  # Write the file out again
  with open(path + '/config.yml', 'w') as file:
    file.write(filedata)
    


  time.sleep(1)

  print("Run Object Detection Service  at Ports : " + str(ports))
  cmd = 'sudo docker run -d --name ' + camera_name + ' --rm --privileged --shm-size=1g -v /dev/bus/usb:/dev/bus/usb -v ' + path  + ':/config:ro -p ' + docker_ports + ' -e RTSP_PASSWORD="admin" frigate2:latest'
  #cmd = 'sudo docker run -d --name ' + camera_name + ' -p ' + docker_ports1 + ' yolo_video:v0'    
  os.system(cmd)

  #ports = ports + 1
  #print("Update Ports : " + str(ports))

  return "Object Detection Service 1 for  " + camera_name + " Started"



#stop the service 
@app.route('/stop/',methods = ['POST'])
def stop():
  global ports
  camera_name = request.args.get("camera_name","")

  path = '/home/ubuntu/object_detection/' + camera_name + '/'
  #path = '/home/ubuntu/object_detection/data/' + camera_name + '/'

  print("Remove frigate config file")
  cmd = 'sudo rm -rf ' + path + 'config.yml'
  os.system(cmd)
  
  print("Stop Container")

  print("Stop container service of " + camera_name)
  cmd = 'sudo docker rm -f ' + camera_name
  os.system(cmd)


  return "Object Detection Service 1 for  " + camera_name + " Stopped"
  
if __name__ == '__main__':
    app.run(debug=True, host='192.168.79.18',port=5001)