import serial
import pynmea2

# Global variables to store GPS data
latitude = 0.0
longitude = 0.0
speed = 0.0
heading = 0.0
fix = 0  # Initialize heading with a default value

# Function to parse NMEA sentence and update global variables
def parse_nmea_message(nmea_sentence):
    global latitude, longitude, speed, heading, fix

    try:
        msg = pynmea2.parse(nmea_sentence)

        if isinstance(msg, pynmea2.GGA):
            latitude = msg.latitude
            longitude = msg.longitude
            fix = msg.gps_qual
           

        elif isinstance(msg, pynmea2.RMC):
            if msg.true_course is not None:
                speed = msg.spd_over_grnd
                heading = msg.true_course

        # Print parsed data for debugging
        print(f"Latitude: {latitude}, Longitude: {longitude}, Speed: {speed}, Heading: {heading}")
        print(fix)
    except pynmea2.ParseError as e:
        print(f"Error parsing NMEA sentence: {e}")


# Open a serial connection to the GPS module
with serial.Serial('COM5', 9600, timeout=1) as ser:
    print("Connected to GPS module")
    while True:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()

        # Check if the line contains a valid NMEA sentence
        if line.startswith('$'):
            # Parse the NMEA sentence
            parse_nmea_message(line)

