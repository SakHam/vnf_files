from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import socket
import os
import time, threading
import commands
import fileinput
import json
import requests 
## importing socket module
import socket
## getting the hostname by socket.gethostname() method
#global ip_address

## getting the IP address using socket.gethostbyname() method
#ip_address = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
## printing the hostname and ip_address

#print("IP Address: ")
#print(ip_address)

#hostname = 'DESKTOP-JANREBS'
## getting the IP address using socket.gethostbyname() method
#ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address


global camera_names
global counter
global ports
camera_names = []
counter = 0
ports = 4500
app = Flask(__name__)


@app.route('/check/',methods = ['GET'])
def check():
  print("the Service is up and Running")
  
  URL1 = "http://192.168.79.18:5000/check/"
  URL2 = "http://192.168.79.10:5000/check/"
  URL3 = "http://192.168.79.4:5000/check/"
  r_object_detect1 = requests.get(url = URL1)
  r_object_detect2 = requests.get(url = URL2)
  r_monitoring = requests.get(url = URL3) 

  
  
  if r_object_detect1.status_code == 200:
    print('The Detection Service 1 is up and Running!')
  else:
    print('The Detection Service 1 not responding')

  if r_object_detect2.status_code == 200:
    print('The Detection Service 2 is up and Running!')
  else:
    print('The Detection Service 2 not responding')

  if r_monitoring.status_code == 200:
    print('The Monitoring Service is up and Running!')
  else:
    print('The Monitoring Service not responding')   
  

  

#3 options, load, start and stop the new service 

@app.route('/start/',methods = ['POST'])
def start():

  global camera_names,counter,ports
  camera_name = request.args.get('camera_name','')
  network_url = request.args.get('network_url','')
  object_name = request.args.get('object_name','')  
  print(camera_name)
  print(ports)
  find = 0

  print("Search if Camera Name is already exists")
  for i in camera_names:
    if i == camera_name:
      find = 1
      print("camera name is already exists")
      break

  if find == 1:
    print("Camera Name Found")
    if object_name != "person":
      
      print("Stop object Detection Service 1\n")
      cmd = "curl --location --request POST 'http://192.168.79.18:5001/stop/?camera_name=" + camera_name + "'"
      os.system(cmd)
      cmd = "curl --location --request POST 'http://192.168.79.4:5003/stop/?camera_name=" + camera_name + "'"
      os.system(cmd)  
      
      print("Start object Detection 2\n")
      cmd = "curl --location --request POST 'http://192.168.79.10:5002/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)
      cmd = "curl --location --request POST 'http://192.168.79.4:5003/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)  
      ports = ports + 1
      return "Service " + camera_name + " Started"

    else:
      print("Stop object Detection Service 2\n")
      cmd = "curl --location --request POST 'http://192.168.79.10:5002/stop/?camera_name=" + camera_name + "'"
      os.system(cmd)
      cmd = "curl --location --request POST 'http://192.168.79.4:5003/stop/?camera_name=" + camera_name + "'"
      os.system(cmd)  
      
      print("Start object Detection 1\n")
      cmd = "curl --location --request POST 'http://192.168.79.18:5001/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)
      cmd = "curl --location --request POST 'http://192.168.79.4:5003/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)
      ports = ports + 1
      return "Service " + camera_name + " Started"
 
  else:
    camera_names.append(camera_name)
    counter = counter + 1
    print(camera_names)
    if object_name == "person":
      
      print("Start object Detection Service 1")
     
      cmd = "curl --location --request POST 'http://192.168.79.18:5001/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)
      
      cmd = "curl --location --request POST 'http://192.168.79.4:5003/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)
      ports = ports + 1
      return "Service " + camera_name + " Started"

    else:
      print("Start object Detection Service 2")
      cmd = "curl --location --request POST 'http://192.168.79.10:5002/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)
      cmd = "curl --location --request POST 'http://192.168.79.4:5003/start/?camera_name=" + camera_name + "&network_url=" + network_url + "&object_name=" + object_name + "&ports=" + str(ports) + "'"
      os.system(cmd)
      ports = ports + 1
      return "Service " + camera_name + " Started"

  



#stop the service 
@app.route('/stop/',methods = ['POST'])
def stop():

  global camera_names,counter
  camera_name = request.args.get("camera_name","")
  object_name = request.args.get('object_name','')  
  camera_names.remove(camera_name)
  print(camera_names)
  counter = counter - 1
  PARAMS = {'camera_name':camera_name} 
  
  if object_name == "person":
    cmd = "curl --location --request POST 'http://192.168.79.18:5001/stop/?camera_name=" + camera_name + "'"
    os.system(cmd)
    cmd = "curl --location --request POST 'http://localhost:5003/stop/?camera_name=" + camera_name + "'"
    os.system(cmd)  
  else:
    cmd = "curl --location --request POST 'http://localhost:5002/stop/?camera_name=" + camera_name + "'"
    os.system(cmd)
    cmd = "curl --location --request POST 'http://localhost:5003/stop/?camera_name=" + camera_name + "'"
    os.system(cmd)

  return "Service " + camera_name + " Stopped"
  

  
if __name__ == '__main__':
    app.run(debug=True, host='192.168.79.9', port=5000)