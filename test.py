import device_model
import time


# 数据更新事件  Data update event
def updateData(DeviceModel):
    acc_z = DeviceModel.deviceData[0x50]['AccZ']
    if acc_z < -1.01:
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
