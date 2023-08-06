"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
RFF 3：Fixed Length Transfer Protocol(FLP)
Authors: jdh99 <jdh821@163.com>
"""

import unittest

from crcmodbus import crc16

# 版本
FLP_VERSION_NAME = '1.2'

# 最大尾缀长度
FLP_SUFFIX_LEN_MAX = 0x7FF


def bytes_to_flp_frame(data: bytearray, is_need_crc: bool, fixed_len: int) -> bytearray:
    """字节流转换为FLP帧.fixedLen为0表示不是固定长度帧,不需要尾缀"""
    frame_len = 2 + len(data)
    if is_need_crc:
        frame_len += 2

    suffix_len = 0
    if frame_len < fixed_len:
        suffix_len = fixed_len - frame_len
        if suffix_len > FLP_SUFFIX_LEN_MAX:
            suffix_len = FLP_SUFFIX_LEN_MAX

    frame = bytearray()
    # 尾缀长度
    suffix_len_value = suffix_len
    if is_need_crc:
        suffix_len_value |= 0x8000

    frame.append((suffix_len_value >> 8) & 0xff)
    frame.append(suffix_len_value & 0xff)

    # crc校验
    if is_need_crc:
        frame.append(0)
        frame.append(0)

    # 正文
    frame += data
    # 尾缀
    frame += bytearray(suffix_len)

    if is_need_crc:
        crc = crc16.checksum(data)
        frame[2] = (crc >> 8) & 0xff
        frame[3] = crc & 0xff
    return frame


def flp_frame_to_bytes(frame: bytearray) -> bytearray:
    """FLP帧转换为字节流.字节流是FLP帧的数据正文.转换失败返回None"""
    size = len(frame)
    if size < 2:
        return None

    suffix_len_value = (frame[0] << 8) + frame[1]
    suffix_len = suffix_len_value & 0x7FFF
    is_need_crc = (suffix_len_value >> 15) == 0x1

    # 判断帧最小长度是否正确
    calc_frame_min_size = suffix_len + 2
    if is_need_crc:
        calc_frame_min_size = suffix_len + 2
    if size < calc_frame_min_size:
        return None

    if is_need_crc:
        crc_get = (frame[2] << 8) + frame[3]
        crc_calc = crc16.checksum(frame[4:size - suffix_len])
        if crc_get != crc_calc:
            return None
        return frame[4:size - suffix_len]
    else:
        return frame[2:size - suffix_len]


class _UnitTest(unittest.TestCase):
    def test_flp_header(self):
        data = bytearray([1, 2, 3, 4, 5])
        frame1 = bytes_to_flp_frame(data, True, 15)
        frame2 = bytes_to_flp_frame(data, False, 15)
        self.print_hex(frame1)
        self.print_hex(frame2)
        self.assertEqual(frame1, bytearray(
            [0x80, 0x06, 0x2a, 0xbb, 0x01, 0x02, 0x03, 0x04, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        self.assertEqual(frame2, bytearray(
            [0x00, 0x08, 0x01, 0x02, 0x03, 0x04, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

        data1 = flp_frame_to_bytes(frame1)
        data2 = flp_frame_to_bytes(frame2)
        self.print_hex(data1)
        self.print_hex(data2)
        self.assertEqual(data1, bytearray([0x01, 0x02, 0x03, 0x04, 0x05]))
        self.assertEqual(data2, bytearray([0x01, 0x02, 0x03, 0x04, 0x05]))

    @staticmethod
    def print_hex(data: bytearray):
        for i in data:
            print('0x%02x, ' % i, end='')
        print()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
