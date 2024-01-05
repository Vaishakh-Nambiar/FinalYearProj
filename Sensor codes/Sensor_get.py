import smbus
import time

# I2C address of the SEN0433 sensor
SEN0433_ADDRESS = 0x68

# Register addresses for accelerometer data
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

# Initialize the I2C bus
bus = smbus.SMBus(1)  # 1 indicates the I2C bus number


def read_acceleration_data():
    # Read raw accelerometer data
    x_raw = bus.read_i2c_block_data(SEN0433_ADDRESS, ACCEL_XOUT_H, 2)
    y_raw = bus.read_i2c_block_data(SEN0433_ADDRESS, ACCEL_YOUT_H, 2)
    z_raw = bus.read_i2c_block_data(SEN0433_ADDRESS, ACCEL_ZOUT_H, 2)

    # Convert raw data to acceleration values
    x_accel = (x_raw[0] << 8 | x_raw[1]) / 16384.0  # Sensitivity: +/- 2g
    y_accel = (y_raw[0] << 8 | y_raw[1]) / 16384.0
    z_accel = (z_raw[0] << 8 | z_raw[1]) / 16384.0

    return {
        "x_acceleration": x_accel,
        "y_acceleration": y_accel,
        "z_acceleration": z_accel,
    }


while True:
    # Read Acceleration Sensor Data
    acceleration_data = read_acceleration_data()

    print(f"Acceleration Data: {acceleration_data}")

    time.sleep(1)  # Read data every 1 second (adjust as needed)
