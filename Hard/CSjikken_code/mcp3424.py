cfg_read = 0b10000000
cfg_stop = 0b00000000
cfg_ch1 = 0b00000000
cfg_ch2 = 0b00100000
cfg_ch3 = 0b01000000
cfg_ch4 = 0b01100000
cfg_once = 0b00000000
cfg_seq = 0b00001000
cfg_18bit = 0b00001100
cfg_16bit = 0b00001000
cfg_14bit = 0b00000100
cfg_12bit = 0b00000000
cfg_PGAx1 = 0b00000000
cfg_PGAx2 = 0b00000001
cfg_PGAx4 = 0b00000010
cfg_PGAx8 = 0b00000011

volt_ref = 2.048
vmax_18bit = 0x01FFFF
vmax_16bit = 0x7FFF
vmax_14bit = 0x1FFF
vmax_12bit = 0x07FF

sps_18bit = 3.75
sps_16bit = 15
sps_14bit = 60
sps_12bit = 240


def parse_int(data, resolution):
    # M is MSB since the value style is two's complement
    if resolution == 18:
        # ******MD DDDDDDDD DDDDDDDD
        x = int(((data[0] << 16) & 0x030000) |
                ((data[1] << 8) & 0x00FF00) | data[1])
        return (-(x & 0x020000) | (x & 0x01FFFF))
    elif resolution == 16:
        # MDDDDDDD DDDDDDDD
        x = int(((data[0] << 8) & 0xFF00) | data[1])
        return (-(x & 0x8000) | (x & 0x7FFF))
    elif resolution == 14:
        # **MDDDDD DDDDDDDD
        x = int(((data[0] << 8) & 0x3F00) | data[1])
        return (-(x & 0x2000) | (x & 0x1FFF))
    elif resolution == 12:
        # ****MDDD DDDDDDDD
        x = int(((data[0] << 8) & 0x0F00) | data[1])
        return (-(x & 0x0800) | (x & 0x07FF))


def to_volt(data, resolution):
    x = parse_int(data, resolution)
    if resolution == 18:
        return (round(volt_ref * x / vmax_18bit, 9))  # LSB: 0.000015625 V
    elif resolution == 16:
        return (round(volt_ref * x / vmax_16bit, 7))  # LSB: 0.0000625 V
    elif resolution == 14:
        return (round(volt_ref * x / vmax_14bit, 5))  # LSB: 0.00025 V
    elif resolution == 12:
        return (round(volt_ref * x / vmax_12bit, 3))  # LSB: 0.001 V