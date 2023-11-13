import json
import os

import network
import machine
import time
from umqtt.simple import MQTTClient

filename = "PrivateInfo.json"
if os.path.isfile( filename ):
  with open( filename, "r" ) as text_file:
    text_data_string = text_file.read()
    config = json.loads( text_data_string )
# WiFi credentials
wifi_ssid = config['wifi_ssid']
wifi_password = config['wifi_password']

# MQTT broker details
mqtt_broker = config['mqtt_broker']
mqtt_port = config['mqtt_port']
mqtt_topic = config['mqtt_topic']


# Connect to Wi-Fi
def connect_wifi():
  sta_if = network.WLAN( network.STA_IF )
  if not sta_if.isconnected():
    print( "Connecting to WiFi..." )
    sta_if.active( True )
    sta_if.connect( wifi_ssid, wifi_password )
    while not sta_if.isconnected():
      time.sleep( 0.01 )
  print( "Connected to WiFi" )


# Connect to MQTT broker
def connect_mqtt():
  client = MQTTClient( "rp2040_client", mqtt_broker, mqtt_port )
  client.connect()
  return client


# Get CPU temperature
def get_cpu_temperature():
  temperature = machine.cpu_temp()
  return temperature


def main():
  # Connect to Wi-Fi
  connect_wifi()

  # Connect to MQTT broker
  mqtt_client = connect_mqtt()

  try:
    while True:
      # Get CPU temperature
      temperature = get_cpu_temperature()

      # Publish temperature to MQTT
      mqtt_client.publish( mqtt_topic, str( temperature ) )

      # Wait for 20 seconds
      time.sleep( 20 )

  except KeyboardInterrupt:
    # Disconnect from MQTT
    mqtt_client.disconnect()
    print( "Disconnected from MQTT" )


if __name__ == "__main__":
  main()
