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
  print("Service is Up & Running")
  return "Service is responding"
    
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
### configure input number 

  with open('/usr/share/hassio/homeassistant/configuration.yaml', 'r+') as output, open('/home/camera/frigate/configs/input_number_template.yaml', 'rb') as input:
    fileinput = input.read() 
    fileinput = fileinput.replace('camer_name', camera_name)

    filedataout = output.read() 
    filedataout = filedataout.replace('input_number:', 'input_number:\n' + str(fileinput))

  with open('/home/camera/frigate/' + camera_name + '/input_number.yaml', 'w') as file:
    file.write(fileinput)

  with open('/usr/share/hassio/homeassistant/configuration.yaml', 'w') as file:
    file.write(filedataout)
### configure input number 

  print("Home-Assitant Camera Settings Configurations")


  with open('/usr/share/hassio/homeassistant/configuration.yaml', 'a') as output, open('/home/camera/frigate/configs/cameras.yaml', 'rb') as input:
    filedata = input.read()
    filedata = filedata.replace('camer_name', camera_name)
    filedata = filedata.replace('id_name', camera_name)
    filedata = filedata.replace('topic_camera', 'frigate/' + camera_name + '/' + object_name + '/snapshot')
    filedata = filedata.replace('id_unq', 'image.' + camera_name)
    filedata = filedata.replace('stat_topic', 'frigate/' + camera_name + '/' + object_name)
    filedata = filedata.replace('stat_topc_event', 'frigate/' + camera_name + '/' + object_name)
    filedata = filedata.replace('id_unq_event', camera_name + ".event")
    filedata = filedata.replace('id_name_event', camera_name + ".event")
    filedata = filedata.replace('events_unit', camera_name + ".event")
    filedata = filedata.replace('sum_topic', 'frigate/' + camera_name + '/' + object_name + '/sum')
    filedata = filedata.replace('objn', object_name)    
    output.write('\n')	
    output.write(filedata)

  with open('/home/camera/frigate/' + camera_name + '/cameras.yaml', 'w') as file:
    file.write(filedata)

  time.sleep(2)
  print("Home-Assitant Camera Automation Configurations")
  with open('/usr/share/hassio/homeassistant/automations.yaml', 'a') as output, open('/home/camera/frigate/configs/automation.yaml', 'rb') as input:
    filedata = input.read()
    filedata = filedata.replace('id_number', "'" + str(automation_id) + "'")
    filedata = filedata.replace('objn', object_name)    
    filedata = filedata.replace('camer_name', camera_name)    
    output.write('\n')	
    output.write(filedata)
  automation_id = automation_id + 1
  with open('/home/camera/frigate/' + camera_name + '/automation.yaml', 'w') as file:
    file.write(filedata)





  print("Home-Assitant Cards Camera Settings Configurations")

## Configure Cards_stream
  with open('/home/camera/frigate/configs/Cards_stream', 'r') as file :
    filedata = file.read()

# Replace the target string
  filedata = filedata.replace('name_cam', camera_name)
  filedata = filedata.replace('ports', str(ports))


# Write the file out again
  with open('/home/camera/frigate/' + camera_name + '/Cards_stream', 'w') as file:
    file.write(filedata)

## Configure Cards_image
  with open('/home/camera/frigate/configs/Cards_image', 'r') as file :
    filedata = file.read()

# Replace the target string
  filedata = filedata.replace('name_cam', camera_name)
  filedata = filedata.replace('objn', object_name)

# Write the file out again
  with open('/home/camera/frigate/' + camera_name + '/Cards_image', 'w') as file:
    file.write(filedata)

## Configure Cards_event
  with open('/home/camera/frigate/configs/Cards_event', 'r') as file :
    filedata = file.read()

# Replace the target string
  filedata = filedata.replace('name_cam', camera_name)


# Write the file out again
  with open('/home/camera/frigate/' + camera_name + '/Cards_event', 'w') as file:
    file.write(filedata)

## Configure Cards_sum
  with open('/home/camera/frigate/configs/Cards_sum', 'r') as file :
    filedata = file.read()

# Replace the target string
  filedata = filedata.replace('name_cam', camera_name)
  filedata = filedata.replace('objn', object_name)

# Write the file out again
  with open('/home/camera/frigate/' + camera_name + '/Cards_sum', 'w') as file:
    file.write(filedata)

  time.sleep(2)


  print("Update Lovelace file")


  with open(r'/home/camera/frigate/configs/lovelace') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    HA_configs  = json.load(file)




  with open(r'/home/camera/frigate/' + camera_name + '/Cards_stream') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    card_configs1  = json.load(file)

  with open(r'/home/camera/frigate/' + camera_name + '/Cards_image') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    card_configs2  = json.load(file)
  with open(r'/home/camera/frigate/' + camera_name + '/Cards_event') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    card_configs3  = json.load(file)

  with open(r'/home/camera/frigate/' + camera_name + '/Cards_sum') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    card_configs4  = json.load(file)

  HA_configs['data']['config']['views'][0]['cards'].append(card_configs1)
  #HA_configs['data']['config']['views'][0]['cards'].append(card_configs2)
  HA_configs['data']['config']['views'][0]['cards'].append(card_configs3)
  HA_configs['data']['config']['views'][0]['cards'].append(card_configs4)
  json_output = json.dumps(HA_configs)
  

  with open('/usr/share/hassio/homeassistant/.storage/lovelace', 'w') as file:
    file.write(json_output)

  cmd = 'sudo cp /usr/share/hassio/homeassistant/.storage/lovelace /home/camera/frigate/configs/lovelace'
  os.system(cmd)

  time.sleep(2)



  print("Restart Home-Assitant")

  cmd = 'sudo docker restart 425674f5d108'
  os.system(cmd)

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


  with open('/usr/share/hassio/homeassistant/configuration.yaml', 'rb') as output, open('/home/camera/frigate/' + camera_name + '/cameras.yaml', 'rb') as input:
    filedata_in = input.read()
    fifledata_out = output.read()
    fifledata_out = fifledata_out.replace(filedata_in, '')
  with open('/usr/share/hassio/homeassistant/configuration.yaml', 'w') as file:
    file.write(fifledata_out)


  with open('/usr/share/hassio/homeassistant/configuration.yaml', 'rb') as output, open('/home/camera/frigate/' + camera_name + '/input_number.yaml', 'rb') as input:
    filedata_in = input.read()
    fifledata_out = output.read()
    fifledata_out = fifledata_out.replace(filedata_in, '')
  with open('/usr/share/hassio/homeassistant/configuration.yaml', 'w') as file:
    file.write(fifledata_out)



  with open('/usr/share/hassio/homeassistant/automations.yaml', 'rb') as output, open('/home/camera/frigate/' + camera_name + '/automation.yaml', 'rb') as input:
    filedata_in = input.read()
    fifledata_out = output.read()
    fifledata_out = fifledata_out.replace(filedata_in, '')
  automation_id = automation_id - 1

  with open('/usr/share/hassio/homeassistant/automations.yaml', 'w') as file:
    file.write(fifledata_out)



  with open('/usr/share/hassio/homeassistant/.storage/lovelace', 'r') as file:
    HA_configs  = json.load(file)
 

  keep_going = True
  index = 0
  for x in range(3):
    keep_going = True
    index = 0
    while keep_going:
      temp = str(HA_configs['data']['config']['views'][0]['cards'][index])
      if (temp.find(camera_name) != -1): 
        print("Find name : " + camera_name) 
        print("At index : ")
        print(index)
        HA_configs['data']['config']['views'][0]['cards'].pop(index)
        keep_going = False
      else:
        index = index + 1
  





  json_output = json.dumps(HA_configs) 

  with open('/usr/share/hassio/homeassistant/.storage/lovelace', 'w') as file:
    file.write(json_output)



  cmd = 'sudo cp /usr/share/hassio/homeassistant/.storage/lovelace /home/camera/frigate/configs/lovelace'
  os.system(cmd)


  print("Restart Home-Assitant")

  cmd = 'sudo docker restart 425674f5d108'
  os.system(cmd) 

  time.sleep(30)

  print("Stop container service of " + camera_name)
  cmd = 'sudo docker rm -f ' + camera_name
  os.system(cmd)
  return "Service " + camera_name + " Stopped"
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
