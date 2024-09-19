# ANT+ Weather Communication Project

This project demonstrates communication between a Python server and a C++ microcontroller using the ANT+ protocol. The server retrieves weather data and transmits it to the microcontroller, which displays it on an LCD screen.

## Hardware Requirements
- Microcontroller with ANT+ capabilities
- LCD screen
- Buttons

## Software Requirements
- Python 3.x
- [OpenANT library](https://github.com/Tigge/openant)
- Requests library (usually included with Python)
- C++ libraries for your specific microcontroller (refer to manufacturer documentation)

## Project Structure
- `ant_senddemo.py`: Python script for the server.
- `user_app1.c`: C++ code for the microcontroller.

## Python Script (`main.py`)

### Imports
- `requests`: For making HTTP requests to the weather API.
- `ctypes`: For converting signed bytes to unsigned bytes (used for temperature data).
- `logging`: For optional logging (commented out by default).
- `openant.easy.node`: Class for interacting with the ANT+ device.
- `openant.base.commons`: Utility functions for formatting data.

### Variable Definitions
- `NETWORK_KEY`: The network key used for ANT+ communication.
- `Device_Type`: The type of ANT+ device.
- `Device_Number`: The unique identifier for the ANT+ device.
- `Channel_Period`: The period (transmission interval) for the ANT+ channel.
- `Channel_Frequency`: The frequency for the ANT+ channel.

### AntSendDemo Class
- `__init__()`: Initializes the class variables.
- `Create_Next_DataPage()`: 
  - Retrieves weather data using the OpenWeatherMap API.
  - Converts temperature from Kelvin to Celsius.
  - Packs the weather type and temperature into an ANT+ message payload.
- `on_event_tx()`: Callback function triggered when data is transmitted. Prints the ANT+ message data.
- `OpenChannel()`: 
  - Sets up the ANT+ channel configuration.
  - Opens the ANT+ channel.
  - Catches keyboard interrupts for graceful shutdown.

### `main()` Function
- Creates an instance of `AntSendDemo`.
- Opens the ANT+ channel.
- Retrieves and displays weather data in a loop.

## C Code (`slave.c`)

### Includes
- Standard C libraries (`stdio.h`, `stdlib.h`, `string.h`)
- Configuration header for your microcontroller.

### Global Variables
- `G_u32UserApp1Flags`: Flags for the application state.
- Other global variables defined elsewhere may be used.

### Function Definitions
- `UserApp1Initialize()`: 
  - Initializes the state machine and ANT+ channel configuration.
  - Sets up LEDs for visual feedback.
  - Assigns the ANT+ channel information.
  - Initiates the state machine.
  
- `UserApp1RunActiveState()`: 
  - Calls the current state function in the state machine.

### State Machine Functions
- `UserApp1SM_WaitAntReady()`: Waits for the ANT+ channel to be configured.
- `UserApp1SM_Idle()`: Waits for a button press to open the channel.
- `UserApp1SM_WaitChannelOpen()`: Waits for the ANT+ channel to open.
- `UserApp1SM_ChannelOpen()`: 
  - Processes incoming ANT+ messages (weather data).
  - Updates the LCD display.
  - Waits for a button press to close the channel.
  - Handles channel closure events.

### Helper Functions
- Converts temperatures, formats strings, and other utility tasks as needed.

## License
This project is licensed under the MIT License.
