import network
import machine as m
from time import sleep
import time
import ubinascii
import ustruct
import socket
import urequests as requests
from machine import Pin
from i2c_lcd import I2cLcd
from lcd_api import LcdApi

# LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = m.I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
  
lcd.clear()
lcd.move_to(0,0)
lcd.putstr("Connecting...")

# Default pin configuration
DEFAULT_PINS = {
    "SDA": 0,
    "SCL": 1
}

def split_string(string):
    max_chars_per_line = 32
    lines = []
    current_line = ""

    for word in string.split():
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += word + " "
        else:
            # Find the last space in the current line
            last_space_index = current_line.rfind(" ")
            if last_space_index != -1:
                lines.append(current_line[:last_space_index].strip())
                current_line = current_line[last_space_index+1:] + word + " "
            else:
                # No space found, break the word
                lines.append(current_line.strip())
                current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines

def write_auto_move(message):
    if True:
        if len(message) > 16 and len(message) <= 32:
            lcd.clear()
            lcd.putstr(message)
        elif len(message) > 32:
            lcd.clear()
            lines_to_write = split_string(message)
            for line in lines_to_write:
                lcd.putstr(line)
                sleep(4)
                lcd.clear()

# Microphone

ck = 1
ws = 2
da = 3
record_button = m.Pin(18, m.Pin.IN, m.Pin.PULL_UP)
button_enabled = False
mic_pin = m.ADC(26)
audio_buffer = bytearray()
is_recording = False  # Start with recording stopped
audio_ready_to_send = False


def toggle_recording():
    global is_recording, audio_ready_to_send, button_enabled
    if is_recording:
        print("Stopping recording...")
        is_recording = False
        audio_ready_to_send = True
        button_enabled = False
        lcd.clear()
        lcd.putstr("Recording stopped.")
    else:
        print("Starting recording...")
        is_recording = True
        audio_ready_to_send = False  # Reset the flag when starting a new recording
        lcd.clear()
        lcd.putstr("Recording...")


def encode_to_b64(audio_data):
    return ubinascii.b2a_base64(audio_data).decode('utf-8')

# WiFi
SERVER_ENDPOINT = "http://glowworm-charmed-jointly.ngrok-free.app/"
ssid = "Galaxy S9+8aac"
password = "svanik1234"
headers = {"ngrok-skip-browser-warning": "yes"}

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected to WLAN. IP address - {ip}")
    # print("Attempting to visit server website...")
    # r = requests.get(SERVER_ENDPOINT, headers=headers)
    # print(r.text)


def format_and_display_received_tests():
    tests = requests.get(f"{SERVER_ENDPOINT}get-tests", headers=headers)
    tests_list = list(tests.text)
    tests = ["The tests to be conducted are ", tests_list[0][1], " and ", tests_list[1][1]]
    sleep(3)
    for n in range(int(len(f"{tests[0]}{tests[1]}{tests[2]}{tests[3]}"))):
        final_string = ""
        for i in tests:
            final_string += str(i)
        
        if len(final_string) > 32:
            global s1, s2
            # Find the last comma within the first 32 characters
            last_comma_index = final_string[:32].rfind(',')
            
            if last_comma_index != -1:
                # Create a new string up to the last comma
                s1 = final_string[:last_comma_index]
                # Create another variable holding the remaining value
                s2 = final_string[last_comma_index + 1:]
            else:
                # If no comma is found, return the original string and an empty remaining value
                s1 = final_string[:32]
                s2 = final_string[32:]
        
        write_auto_move(s1)
        sleep(5)
        write_auto_move(s2)
        sleep(5)


def send():
    global is_recording, button_enabled
    lcd.clear()
    lcd.putstr("Sending data. Please wait...")
    button_enabled = False
    is_recording = False
    print("Sending data. Making GET request.")
    reply = requests.get(f"{SERVER_ENDPOINT}post-recording", data=encode_to_b64(audio_data=audio_buffer), headers=headers)
    if str(reply.text).startswith("ask"):
        write_auto_move(str(reply.text).removeprefix("ask/"))
    elif str(reply.text).startswith("result"):
        write_auto_move(str(reply.text).removeprefix("result/"))
        sleep(5)
        format_and_display_received_tests()
        specialist = requests.get(f"{SERVER_ENDPOINT}get-specialist", headers=headers).text
        write_auto_move(f"You should visit {specialist}")
        sleep(3)
        write_string("Cleaning up...")
        sleep(2)
        requests.get(f"{SERVER_ENDPOINT}reset", headers=headers)
        m.soft_reset()

# Mainloop
connect_to_wifi()
lcd.clear()
  
lcd.putstr("Connection established!")
sleep(3)
    
lcd.clear()

lcd.putstr("Press the button to record.")

sleep(3)
lcd.clear()
    
lcd.putstr("What is your age?")
    
sleep(3)
    
button_enabled = True

while True:
    if button_enabled:
            # Check for button press (when pin reads low)
        if record_button.value() == 0:
            toggle_recording()
                
        sleep(0.2)
                
        # If recording, capture audio data
    if is_recording:
        data = mic_pin.read_u16()
        audio_buffer.extend(ustruct.pack('<H', data))
    elif audio_ready_to_send:
        button_enabled = False
        print(f"Captured data: \n\n\n\n{audio_buffer}")
        try:
            send()
        except:
            lcd.clear()
            lcd.putstr("Server connection error!")
            break;