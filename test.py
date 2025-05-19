import device_model
import time
import threading
import sounddevice as sd
import soundfile as sf

# List available devices
print(sd.query_devices())

# Select the desired output device ID
output_device_id = 0 # 2  # Replace with your device ID

# Load multi-channel audio file
audio_file = 'kaching.wav'
data, samplerate = sf.read(audio_file)
print(samplerate)
# Play the audio on the selected device
def playsound():
    sd.play(data, samplerate, device=output_device_id)
    sd.wait()

def playsound_inthread():
    t = threading.Thread(target=playsound, args=())
    t.start()

# 数据更新事件  Data update event
def updateData(DeviceModel):
    acc_z = DeviceModel.deviceData[0x50]['AccZ']
    if acc_z < -1.01:
        playsound()
        print("Ka-Chingggggggg! Acceleration in Z-Axis measured", DeviceModel.deviceData[0x50]['AccZ'])
    # 获得加速度x的值
    #print(DeviceModel.get("AccZ"))


if __name__ == "__main__":
    # 读取的modbus地址列表 List of Modbus addresses read
    addrLis = [0x50]
    # 拿到设备模型 Get the device model
    device = device_model.DeviceModel("Coin2", "/dev/ttyUSB0", 9600, addrLis, updateData)
    # 开启设备 Turn on the device
    device.openDevice()
    # 开启轮询 Enable loop reading
    device.startLoopRead()
