from machine import ADC, Pin
import time
import struct

# Initialize the ADC pin (e.g., ADC0 on GP26)
mic = ADC(Pin(26))

# Set the recording duration in seconds
record_duration = 3
sample_rate = 10000  # Sample rate in Hz (adjust as needed)

# List to store the byte data
byte_data = bytearray()

start_time = time.time()
while time.time() - start_time < record_duration:
    # Read the analog value from the microphone
    mic_value = mic.read_u16()
    
# Convert the value to bytes and store in the bytearray
    byte_data.extend(struct.pack('<H', mic_value))
    
    # Delay to match the sample rate
    time.sleep(1 / sample_rate)

print("Recording complete!")
print("Collected byte data length:", len(byte_data))

print(f"Data recorded: \n\n\n\n {byte_data}")