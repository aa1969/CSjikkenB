import smbus
import time
import mcp3424

i2c = smbus.SMBus(1)
addr = 0x68

while True:
    config = (mcp3424.cfg_read | mcp3424.cfg_ch3 | mcp3424.cfg_once |
              mcp3424.cfg_12bit | mcp3424.cfg_PGAx1)
    # Update I2C configuration and start conversion
    data = i2c.write_byte(addr, config)
    time.sleep(1 / mcp3424.sps_12bit)
    while True:
        data = i2c.read_i2c_block_data(addr, 0, 3)  # Read the current value
        # Check if a value has been updated: 0 indicates updated
        if data[2] >> 7 == 0:
            break
        # If the value hasn't been updated, wait a while and reload it
        time.sleep(0.001)

    volt = mcp3424.to_volt(data, 12)
    print(volt)
    time.sleep(0.005)