import jumpcoin
import pyglet

dime = {
    "coin_name": "Dime",
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "dime.wav",
    "io_pin": 4,
}
pizza_penny = {
    "coin_name": "Pizza Penny",
    "serial_port": "/dev/ttyUSB1",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "penny.wav",
    "io_pin": 27,
}
truck_penny = {
    "coin_name": "Truck Penny",
    "serial_port": "/dev/ttyUSB2",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "penny.wav",
    "io_pin":21,
}
nickel = {
    "coin_name": "Nickel",
    "serial_port": "/dev/ttyUSB3",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "nickel.wav",
    "io_pin":13,
}
quarter = {
    "coin_name": "Quarter",
    "serial_port": "/dev/ttyUSB4",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "quarter.wav",
    "io_pin":26,
}

coin_data = [
    dime,
    pizza_penny,
    truck_penny,
    nickel,
    quarter,
]
coins = []
if __name__ == "__main__":
    for coin_datum in coin_data:
        coins.append(
            jumpcoin.JumpCoin(
                coin_datum["coin_name"],
                coin_datum["serial_port"],
                coin_datum["baudrate"],
                coin_datum["modbus_addr"],
                coin_datum["audio_file"],
                coin_datum["io_pin"],
            )
        )
    print("Done initializing coins in main.py")
    pyglet.app.run()
