import rtmidi
import os

data_byte1 = 0  

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
            print("Velocity:", data_byte2)

def macros(data_byte):
    """  
    this is where your code goes.
    
    ex. 
    if data_byte == 112: os.system("gnome-terminal")
    if data_byte == 113: os.system("firefox")
    """

def main():
    midi_in = rtmidi.MidiIn()

    # Print ports
    print("Available MIDI input ports:")
    for port_number, port_name in enumerate(midi_in.get_ports()):
        print(f"[{port_number}] {port_name}")

    # Choose MIDI input port
    selected_port_number = int(input("Enter the port number of the MIDI input: "))


    midi_in.open_port(selected_port_number)

    print("Listening to MIDI input on", midi_in.get_port_name(selected_port_number))

    # capture 
    while True:
        message = midi_in.get_message()
        if message:
            message, _ = message  # Extract from tuple
            process_midi_message(message)
            macros(data_byte1)  # Pass data_byte1 to the function

if __name__ == "__main__":
    main()
