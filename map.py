import os
import configparser
import rtmidi

data_byte1 = 0  # Initialize data_byte1
midi_in = rtmidi.MidiIn()

CONFIG_FILE = "config.ini"
last_message = None


def create_config_file():
    config = configparser.ConfigParser()
    config.add_section("Commands")
    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)


def process_midi_message(message):
    global data_byte1, last_message
    if len(message) >= 3:
        status_byte = message[0]
        data_byte1 = message[1]
        data_byte2 = message[2]

        if status_byte == 144:  # Note On message
            if last_message == message:
                return

            last_message = message
            print("Pad", data_byte1, "pressed")
            user_command = input("Enter the command to associate with this key: ")

            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            config.set("Commands", str(data_byte1), user_command)
            with open(CONFIG_FILE, "w") as config_file:
                config.write(config_file)


def main():
    # Print the available MIDI input ports
    print("Available MIDI input ports:")
    for port_number, port_name in enumerate(midi_in.get_ports()):
        print(f"[{port_number}] {port_name}")

    # Choose the MIDI input port to listen to
    selected_port_number = int(input("Enter the port number of the MIDI input: "))

    # Open the selected MIDI input port
    midi_in.open_port(selected_port_number)

    print("Listening to MIDI input on", midi_in.get_port_name(selected_port_number))
    print("\nPress the key/pad you want to assign. Press ctrl+c to exit and save.")

    try:
        # Start an infinite loop to capture MIDI messages
        while True:
            message = midi_in.get_message()
            if message:
                message, _ = message  # Extract the MIDI message from the tuple
                process_midi_message(message)

                config = configparser.ConfigParser()
                config.read(CONFIG_FILE)
                command = config.get("Commands", str(data_byte1), fallback=None)

    except KeyboardInterrupt:
        os.system('clear')
        exit()


if __name__ == "__main__":
    if not os.path.isfile(CONFIG_FILE):
        create_config_file()

    main()
