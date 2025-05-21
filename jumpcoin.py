import device_model
import time
import threading
import sounddevice as sd
import soundfile as sf
import pyglet

MIN_SECONDS_BETWEEN_SOUNDS = 1.0 # Fractional seconds before a coin can play another sound

############## JumpCoin

# For now, we'll keep the JumpCoin's separate, each to be run in a separate thread
# We could put them all on the same modbus and address them there,
# but the computer might be able to more effectively deal with five
# if each gets its own modbus and USB port and the computer uses
# one thread for each USB port.

class JumpCoin:
    # Data update event
    def updateData(self, DeviceModel):
        acc_z = DeviceModel.deviceData[self.modbus_addr]['AccZ']
        if acc_z < -1.015:
            if self.playing_sound == False:
                self.playsound()
            print("Acceleration in Z-Axis measured", acc_z)



    def __init__(self, coin_name, serial_port, baudrate, modbus_addr, audio_file):
        self.coin_name = coin_name
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.modbus_addr = modbus_addr
        self.audio_file = audio_file
        self.data, self.samplerate = sf.read(self.audio_file)
        self.playing_sound = False
        self.time_last_sound = time.monotonic()
        
        # Pyglet Sound
        self.sound_player = pyglet.resource.media(self.audio_file, streaming=False)
        #sound.play()

        #self.loaded_sound = pyglet.media.load(audio_file)
        #self.sound_player = pyglet.media.Player()
        #self.sound_player.queue(self.loaded_sound)

        self.accelerometer = device_model.DeviceModel(
                self.coin_name,
                self.serial_port,
                self.baudrate,
                [self.modbus_addr],
                self.updateData)
        self.accelerometer.openDevice()
        self.accelerometer.startLoopRead()

    def playsound_inthread(self):
        t = threading.Thread(target=self.playsound, args=())
        t.start()

    def playsound(self):
        self.sound_playing = True
        current_time = time.monotonic()
        if ((current_time - self.time_last_sound) > MIN_SECONDS_BETWEEN_SOUNDS):
            self.time_last_sound = time.monotonic()
            print("Kaching")
            self.sound_player.play()
        else:
            print(f"Too soon for another sound from {self.coin_name}")
            print(f"Current: {current_time} Last: {self.time_last_sound}")

