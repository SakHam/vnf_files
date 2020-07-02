from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import socket
import os
import time, threading
import commands
import fileinput
import json
import requests 



app = Flask(__name__)


@app.route('/check/',methods = ['GET'])
def check():
  print("the Service is up and Running")
  
  URL1 = "http://192.168.79.18:5000/check"
  
  r_object_detect = requests.get(url = URL1) 
  
  data_obj_det = r_object_detect.json() 
 
  URL2 = "http://192.168.79.10:5000/check"
  r_monitoring = requests.get(url = URL2) 
  
  data_monitoring = r_monitoring.json() 
  
  
  print(data_obj_det)
  print(data_monitoring)
  
  
  
  return "Send the check requests : " + data_obj_det + data_monitoring

#3 options, load, start and stop the new service 

@app.route('/start/',methods = ['POST'])
def start():
  camera_name = request.args.get('camera_name','')
  network_url = request.args.get('network_url','')
  object_name = request.args.get('object_name','')  
  PARAMS = {'camera_name':camera_name, 'network_url':network_url, 'object_name':object_name} 
  
  URL1 = "http://192.168.79.18:5000/start"
  
  r_object_detect = requests.post(url = URL1, data = PARAMS) 
  
  data_obj_det = r_object_detect.text() 
 
  URL2 = "http://192.168.79.10:5000/start"
  r_monitoring = requests.post(url = URL2, data = PARAMS) 
  
  data_monitoring = r_monitoring.text() 
  
  
  print(data_obj_det)
  print(data_monitoring)
  
  
  
  return "Send the start requests : " + data_obj_det + data_monitoring




#stop the service 
@app.route('/stop/',methods = ['POST'])
def stop():
  camera_name = request.args.get("camera_name","")
  PARAMS = {'camera_name':camera_name} 
  
  URL1 = "http://192.168.79.18:5000/stop"
  r_object_detect = requests.post(url = URL1, data = PARAMS) 
  
  data_obj_det = r_object_detect.text() 
 
  URL2 = "http://192.168.79.10:5000/stop"
  r_monitoring = requests.post(url = URL2, data = PARAMS) 
  
  data_monitoring = r_monitoring.text() 
  
  
  print(data_obj_det)
  print(data_monitoring)
  
  
  
  return "Send the stop requests : " + data_obj_det + data_monitoring
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
