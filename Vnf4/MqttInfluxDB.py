import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
INFLUXDB_ADDRESS = '192.168.17.7'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'mqtt'

MQTT_ADDRESS = '192.168.17.7'
MQTT_USER = 'mqtt'
MQTT_PASSWORD = 'mqtt'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

MQTT_TOPIC = 'frigate/cam_name/person/sum'
#MQTT_TOPIC1 = 'frigate/camera1/person'
location = 'cam_name'
#sensor_data = 0
#influxdb_client = InfluxDBClient(host=INFLUXDB_ADDRESS, port=3004)

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

#influxdb_client.create_database('example')


print(influxdb_client.get_list_database())


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def _parse_mqtt_message(topic, payload):
    return payload



def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    print(type(sensor_data))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(int(sensor_data))

def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': 'event',
            'tags': {
                'location': location
            },
            'fields': {
                'value': sensor_data
            }
        }
    ]
    influxdb_client.write_points(json_body)



def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def main():
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
