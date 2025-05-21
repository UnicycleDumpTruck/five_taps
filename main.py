import jumpcoin
import pyglet

dime = {
    "coin_name": "Dime",
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "kaching.wav",
}
pizza_penny = {
    "coin_name": "Pizza Penny",
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "kaching.wav",
}
truck_penny = {
    "coin_name": "Truck Penny",
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "kaching.wav",
}
nickel = {
    "coin_name": "Nickel",
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "kaching.wav",
}
quarter = {
    "coin_name": "Quarter",
    "serial_port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "modbus_addr": 0x50,
    "audio_file": "kaching.wav",
}

coin_data = [
    dime,
    #pizza_penny,
    #truck_penny,
    #nickel,
    #quarter,
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
            )
        )
    print("Done initializing coins in main.py")
    pyglet.app.run()
