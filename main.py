import time
import rtmidi
import os

data_byte1 = 0  # 
last_trigger_time = time.time()  # last trigger time

DEBOUNCE_DELAY = 0.5  # Debounce delay

def process_midi_message(message):
    global data_byte1
    if len(message) >= 3:
        status_byte = message[0]
        data_byte1 = message[1]
        data_byte2 = message[2]

        if status_byte == 144:  # Note On message
            # MIDI note number is data_byte1
            print("Pad", data_byte1, "pressed")
            # Velocity/intensity is data_byte2
            #print("Velocity:", data_byte2)

def macros(data_byte):
    global last_trigger_time
    current_time = time.time()
    if current_time - last_trigger_time >= DEBOUNCE_DELAY:
        """
        this is where your commands should go.
        ex.
        if data_byte == 112:
            os.system("gnome-terminal")
        elif data_byte == 113:
            os.system("firefox")
        elif data_byte == 114:
            os.system("steam")
        """
        last_trigger_time = current_time

def main():
    midi_in = rtmidi.MidiIn()

    # Print the available MIDI input ports
    print("Available MIDI input ports:")
    for port_number, port_name in enumerate(midi_in.get_ports()):
        print(f"[{port_number}] {port_name}")

    # Choose the MIDI input port to listen to
    selected_port_number = int(input("Enter the port number of the MIDI input: "))

    # Open the selected MIDI input port
    midi_in.open_port(selected_port_number)

    print("Listening to MIDI input on", midi_in.get_port_name(selected_port_number))

    # Start an infinite loop to capture MIDI messages
    while True:
        message = midi_in.get_message()
        if message:
            message, _ = message  # Extract the MIDI message from the tuple
            process_midi_message(message)
            macros(data_byte1)  # Pass data_byte1 to the function

if __name__ == "__main__":
    main()
