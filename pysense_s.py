#
# Based on the code "tmpl7.py" by Marco Rainone <mrainone@libero.it>
#

# Example of use:
# 
# import pysense_s
# a = pysense_s.reader()
# print(a.get_temp())
# print(a.get_pressure())
# print(a.get_altitude())

from machine import I2C
import time

MPL3115Address = 0x60                         # address MPL3115A2

class reader:

    def __init__(self):
        # =================================
        #
        # https://docs.pycom.io/pycom_esp32/library/machine.I2C.html
        # i2c.init(mode, *, baudrate=100000, pins=(SDA, SCL))
        # i2c = I2C(0, I2C.MASTER, baudrate=100000)
        # i2c = I2C(0, I2C.MASTER, baudrate=100000, pins=('P22', 'P21'))      # Initialize the I2C bus
        self.i2c = I2C(0, I2C.MASTER, pins=('P22', 'P21'))      # Initialize the I2C bus

        wr = bytearray(1)
        # MPL3115A2 address, 0x60(96)
        # Select control register, 0x26(38)
        #       0xB9(185)   Active mode, OSR = 128, Altimeter mode
        wr[0] = 0xB9
        self.i2c.writeto_mem(MPL3115Address, 0x26, wr)
        # MPL3115A2 address, 0x60(96)
        # Select data configuration register, 0x13(19)
        #       0x07(07)    Data ready event enabled for altitude, pressure, temperature
        wr[0] = 0x07
        self.i2c.writeto_mem(MPL3115Address, 0x13, wr)
        # MPL3115A2 address, 0x60(96)
        # Select control register, 0x26(38)
        #       0xB9(185)   Active mode, OSR = 128, Altimeter mode
        wr[0] = 0xB9
        self.i2c.writeto_mem(MPL3115Address, 0x26, wr)

    def get_temp(self, type="C"):
        # type: "F" for Fahrenheit; anything else for Celsius

        data = bytearray(2)
        data = self.i2c.readfrom_mem(MPL3115Address, 0x04, 2)

        # Convert the data to 20-bits
        temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
        cTemp = temp / 16.0

        if type == "F":
            return (cTemp * 1.8 + 32)
        else:
            return cTemp

    def get_pressure(self):
        # MPL3115A2 address, 0x60(96)
        # Select control register, 0x26(38)
        #       0x39(57)    Active mode, OSR = 128, Barometer mode

        wr = bytearray(1)
        wr[0] = 0x39
        self.i2c.writeto_mem(MPL3115Address, 0x26, wr)
        time.sleep(1)

        # MPL3115A2 address, 0x60(96)
        # Read data back from 0x00(00), 4 bytes
        # status, pres MSB1, pres MSB, pres LSB
        data2 = bytearray(3)
        data2 = self.i2c.readfrom_mem(MPL3115Address, 0x01, 3)

        # Convert the data2 to 20-bits
        pres = ((data2[0] * 65536) + (data2[1] * 256) + (data2[2] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000.0
        return pressure

    def get_altitude(self):
        # MPL3115A2 address, 0x60(96)
        # Select control register, 0x26(38)
        #       0x39 | 0x80    Active mode, OSR = 128, Barometer mode
        wr = bytearray(1)
        wr[0] = 0xB9
        self.i2c.writeto_mem(MPL3115Address, 0x26, wr)
        time.sleep(1)

        # MPL3115A2 address, 0x60(96)
        # Read data back from 0x00(00), 4 bytes
        # status, pres MSB1, pres MSB, pres LSB
        data2 = bytearray(3)
        data2 = self.i2c.readfrom_mem(MPL3115Address, 0x01, 3)
        height = ((data2[0] * 65536) + (data2[1] * 256) + (data2[2] & 0xF0)) / 16
        altitude = float(height) / 16.0
        return altitude

