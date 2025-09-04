import gpiozero
import device_model
import time
import threading
import pyglet
from loguru import logger
import telemetry

# Pyglet Config, even though no display is used, GL is involved
pyglet.options['headless'] = True
pyglet.options.shadow_window = False
display = pyglet.display.get_display()
screen = display.get_default_screen()
config = screen.get_best_config()
config.opengl_api = "gles"
config.major_version = 3
config.minor_version = 0


G_THRESHOLD = -1.015    # how much g in z-axix triggers sound
                        # Negative because the sensor is upside down

LED_ON_TIME = 3 # Seconds to leave LED ring lit after trigger/jump

MIN_SECONDS_BETWEEN_SOUNDS = (
    0.5 # Fractional seconds before coin can play sound again
)

class JumpCoin:
    # Data update event
    def updateData(self, DeviceModel):
        acc_z = DeviceModel.deviceData[self.modbus_addr]["AccZ"]
        if acc_z < G_THRESHOLD:
            self.force = acc_z
            self.lit = True
            self.led.on()
            self.playsound()
        if self.lit:
            current_time = time.monotonic()
            if (current_time - self.time_last_sound) > LED_ON_TIME:
                self.led.off()
                self.lit = False

    def __init__(self, coin_name, serial_port, baudrate, modbus_addr, audio_file, io_pin):
        self.coin_name = coin_name
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.modbus_addr = modbus_addr
        self.time_last_sound = time.monotonic()
        self.sound_player = pyglet.resource.media(audio_file, streaming=False)
        self.force = 0 # Will later hold triggering g force for printing
        self.led = gpiozero.LED(io_pin)
        self.lit = False
        self.jumps = 0 # Track number of jumps before sending
        self.accelerometer = device_model.DeviceModel(
            self.coin_name,
            self.serial_port,
            self.baudrate,
            [self.modbus_addr],
            self.updateData,
        )
        self.accelerometer.openDevice()
        self.accelerometer.startLoopRead()

    def playsound_inthread(self):
        sound_thread = threading.Thread(target=self.playsound, args=())
        sound_thread.start()
    
    def light_led(self):
        self.led.on()
        time.sleep(LED_ON_TIME)
        self.led.off()

    def light_led_in_thread(self):
        led_thread = threading.Thread(target=self.light_led, args=())
        led_thread.start()

    def playsound(self):
        current_time = time.monotonic()
        if (current_time - self.time_last_sound) > MIN_SECONDS_BETWEEN_SOUNDS:
            self.time_last_sound = time.monotonic()
            self.jumps = self.jumps + 1
            logger.info(f"{self.coin_name} says Kaching after {self.force}g")
            self.sound_player.play()
            if self.jumps > 9:
                try:
                    telemetry.send_point_in_thread(self.coin_name, self.jumps)
                    logger.debug(f"{self.coin_name} sent {self.jumps} and reset counter")
                    self.jumps = 0
                except Exception as e:
                    logger.warning(e)
#        else:
#            logger.debug(f"Too soon for another sound from {self.coin_name}")
