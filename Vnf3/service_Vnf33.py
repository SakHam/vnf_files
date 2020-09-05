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


app = Flask(__name__)

#3 options, load, start and stop the new service 
@app.route('/check/',methods = ['GET'])
def check():
  print("the Detection Service 2 is up and Running")
  return "the Detection Service 2 is up and Running"

@app.route('/start/',methods = ['POST'])
def start():
  camera_name = request.args.get('camera_name','')
  network_url = request.args.get('network_url','')
  object_name = request.args.get('object_name','')  
  ports = request.args.get('ports','')  

  #global ports
  docker_ports1 = str(ports) + ':5000'
  #cmd = 'mkdir -m 777 "/home/camera/data_obj_detection/"' + camera_name
  cmd = 'sudo mkdir -m 777 "/home/ubuntu/object_detection/data/"' + camera_name
  os.system(cmd)
  #path = '/home/camera/data_obj_detection/' + camera_name
  path = '/home/ubuntu/object_detection/data/' + camera_name


  print("Run Object Detection Service  at Ports : " + str(ports))
  cmd = 'sudo docker run -d --name ' + camera_name + ' -p ' + docker_ports1 + ' yolo_video:v1'    
  os.system(cmd)
  time.sleep(5)
  cmd = "curl --location --request POST 'http://localhost:" + str(ports) + "/inputs/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "'"
  os.system(cmd)

  #ports = ports + 1
  #print("Update Ports : " + str(ports))

   
  return "Object Detection Service 2 for  " + camera_name + " Started"




#stop the service 
@app.route('/stop/',methods = ['POST'])
def stop():

  camera_name = request.args.get("camera_name","")

  #path = '/home/camera/data_obj_detection/' + camera_name + '/'
  path = '/home/ubuntu/object_detection/data/' + camera_name

  print("Remove frigate config file")
  #cmd = 'sudo rm -rf ' + path + 'config.yml'
  #os.system(cmd)
  
  print("Stop Container")

  print("Stop container service of " + camera_name)
  cmd = 'sudo docker rm -f ' + camera_name
  os.system(cmd)

  cmd = 'sudo rm -rf ' + path
  os.system(cmd)

  return "Object Detection Service 2 for  " + camera_name + " Stopped"
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5002)