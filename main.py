# ANT+ - Stride Based Speed and Distance Sensor Example
#
# SDM demo working with OpenAnt Library (https://github.com/Tigge/openant)
# using feature of:
# - acting as Transmitting Device (TX-Broadcast)
# - gracefully close ANT-Channels

import requests
import ctypes

import logging
import time

from openant.easy.node import Node
from openant.easy.channel import Channel
from openant.base.commons import format_list

# Definition of Variables
NETWORK_KEY = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
Device_Type = 123
Device_Number = 12345
Channel_Period = 8134
Channel_Frequency = 57



##########################################################################


class AntSendDemo:
    def __init__(self):

        self.ANTMessageCount = 0
        self.ANTMessagePayload = [0, 0, 0, 0, 0, 0, 0, 0]

        self.TimeProgramStart = time.time()
        self.LastTimeEvent = time.time()

    def Create_Next_DataPage(self):

        self.ANTMessageCount += 1

        weather_data = get_calgary_weather("fb8ac4fefdc9bb18cb7a4fbdf854b4b4")
    
        if weather_data:

            weather = weather_data['weather']
            temp = weather_data['temperature']
            print("Weather: " + weather)
            print("Temperature: " + str(temp))

        encodedWeatherOutput = 0

        match weather:
            case 'Clear':
                encodedWeatherOutput = 1
            case 'Few Clouds':
                encodedWeatherOutput = 2
            case 'Scattered Clouds':
                encodedWeatherOutput = 3
            case 'Broken Clouds':
                encodedWeatherOutput = 4
            case 'Shower Rain':
                encodedWeatherOutput = 5
            case 'Rain':
                encodedWeatherOutput = 6
            case 'Thunderstorm':
                encodedWeatherOutput = 7
            case 'Snow':
                encodedWeatherOutput = 8
            case 'Mist':
                encodedWeatherOutput = 9
            case 'Clouds':
                encodedWeatherOutput = 10

        if self.ANTMessageCount != None:

            class Converter(ctypes.Union):
                _fields_ = [("ui", ctypes.c_ubyte), ("si", ctypes.c_byte)]

            # Very rare case of union being used
            # The class converts a signed byte to an unsigned byte in python using the ctypes library.

            convertedOutput = int(Converter(si=temp).ui)
            self.ANTMessagePayload[0] = 0
            self.ANTMessagePayload[1] = 0
            self.ANTMessagePayload[2] = 0
            self.ANTMessagePayload[3] = 0
            self.ANTMessagePayload[4] = 0
            self.ANTMessagePayload[5] = 0
            self.ANTMessagePayload[6] = convertedOutput
            self.ANTMessagePayload[7] = encodedWeatherOutput


        return self.ANTMessagePayload

    # TX Event
    def on_event_tx(self, data):
        ANTMessagePayload = self.Create_Next_DataPage()
        self.ActualTime = time.time() - self.TimeProgramStart

        self.channel.send_broadcast_data(
            self.ANTMessagePayload
        )  # Final call for broadcasting data
        print(
            self.ActualTime,
            "TX:",
            Device_Number,
            ",",
            Device_Type,
            ":",
            format_list(ANTMessagePayload),
        )

    # Open Channel
    def OpenChannel(self):

        self.node = Node()  # initialize the ANT+ device as node

        # CHANNEL CONFIGURATION
        self.node.set_network_key(0x00, NETWORK_KEY)  # set network key
        self.channel = self.node.new_channel(
            Channel.Type.BIDIRECTIONAL_TRANSMIT, 0x00, 0x00
        )  # Set Channel, Master TX
        self.channel.set_id(
            Device_Number, Device_Type, 1
        )  # set channel id as <Device Number, Device Type, Transmission Type>
        self.channel.set_period(Channel_Period)  # set Channel Period
        self.channel.set_rf_freq(Channel_Frequency)  # set Channel Frequency

        # Callback function for each TX event
        self.channel.on_broadcast_tx_data = self.on_event_tx

        try:
            self.channel.open()  # Open the ANT-Channel with given configuration
            self.node.start()
        except KeyboardInterrupt:
            print("Closing ANT+ Channel...")
            self.channel.close()
            self.node.stop()
        finally:
            pass


###########################################################################################################################
def get_calgary_weather(api_key):
  """
  This function retrieves the current weather and temperature for Calgary, Canada
  using the OpenWeatherMap API.

  Args:
      api_key (str): Your OpenWeatherMap API key.

  Returns:
      dict: A dictionary containing weather description, temperature, and other weather data 
          if successful, or None if there's an error.
  """

  url = f"https://api.openweathermap.org/data/2.5/weather?q=Calgary,ca&appid=" + api_key



  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    weather = data['weather'][0]['main']
    temp = data['main']['temp'] - 273.15  # Convert Kelvin to Celsius

    return {
      'weather': weather,
      'temperature': round(temp)
    }
  else:
    print(f"Error: {response.status_code}")
    return None


def main():

    # logging.basicConfig(
    #     filename="example.log", level=logging.DEBUG
    # )  # just for Debugging purpose, outcomment this in live version

    ant_senddemo = AntSendDemo()

    try:
        ant_senddemo.OpenChannel()  # start
    except KeyboardInterrupt:
        print("Closing ANT+ Channel!")
    finally:
        print("Finally...")
        logging.shutdown()  # Shutdown Logger

    print("Close demo...")

    print("Starting weather API test")

    weather_data = get_calgary_weather("fb8ac4fefdc9bb18cb7a4fbdf854b4b4")

    if weather_data:

        weather = weather_data['weather']
        temp = weather_data['temperature']
        print("Weather: " + weather)
        print("Temperature: " + str(temp))
    else:
        print("Error retrieving weather data.")

if __name__ == "__main__":
    main()
