"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
RFF 1：Network Layer Version 1(NLv1)
Authors: jdh99 <jdh821@163.com>
"""

import utzpy.common as common

import unittest

# 协议族版本号
PROTOCOL_VERSION = 1

# 协议版本
NLV1_VERSION_NAME = "1.1"

# 头部长度
NLV1_HEAD_LEN = 22

# 特殊地址
# 未指定地址
IA_INVALID = 0x0
# 回环地址
IA_LOOPBACK = 0x1
# 广播地址
IA_BROADCAST = 0xFFFFFFFFFFFFFFFF

# IA地址字节数
IA_LEN = 8


class StandardHeader:
    """标准头部"""

    def __init__(self):
        self.version = 0
        self.frame_index = 0
        self.payload_len = 0
        self.next_head = 0
        self.hops_limit = 0
        self.src_ia = 0
        self.dst_ia = 0


_generate_frame_index = 0


def bytes_to_standard_header(data: bytearray) -> (StandardHeader, int):
    """
    字节流转换为标准头部.字节流是大端
    :param data: 字节流必须大于头部长度
    :return: 返回头部以及头部字节数.头部为None或者字节数为0表示转换失败
    """
    if len(data) < NLV1_HEAD_LEN:
        return None, 0

    header = StandardHeader()
    j = 0
    header.version = data[j]
    j += 1
    header.frame_index = data[j]
    j += 1
    header.payload_len = (data[j] << 8) + data[j + 1]
    j += 2
    header.next_head = data[j]
    j += 1
    header.hops_limit = data[j]
    j += 1
    header.src_ia = common.bytes_to_ia(data[j:])
    j += IA_LEN
    header.dst_ia = common.bytes_to_ia(data[j:])
    j += IA_LEN
    return header, j


def standard_header_to_bytes(header: StandardHeader) -> bytearray:
    """标准头部转换为字节流.字节流是大端"""
    data = bytearray()
    data.append(header.version)
    data.append(header.frame_index)
    data.append((header.payload_len >> 8) & 0xff)
    data.append(header.payload_len & 0xff)
    data.append(header.next_head)
    data.append(header.hops_limit)
    data += common.ia_to_bytes(header.src_ia)
    data += common.ia_to_bytes(header.dst_ia)
    return data


def is_global_ia(ia: int) -> bool:
    """是否是全球单播地址"""
    return ((ia >> 61) & 0xff) == 0x1


def is_constant_ia(ia: int) -> bool:
    """是否是固定单播地址"""
    return ((ia >> 61) & 0xff) == 0x2


def is_unique_local_ia(ia: int) -> bool:
    """是否是唯一本地地址"""
    return ((ia >> 57) & 0xff) == 0xfe


def generate_frame_index() -> int:
    """生成帧序号"""
    global _generate_frame_index

    _generate_frame_index += 1
    if _generate_frame_index > 0xff:
        _generate_frame_index = 0
    return _generate_frame_index


class _UnitTest(unittest.TestCase):
    def test_bytes_to_standard_header(self):
        data = bytearray(
            [0x01, 0x05, 0x00, 0x06, 0x07, 0x08, 0x12, 0x34, 0x56, 0x78, 0x12, 0x34, 0x56, 0x78, 0x87, 0x65, 0x43, 0x21,
             0x87, 0x65, 0x43, 0x21])
        header, offset = bytes_to_standard_header(data)
        self.assertEqual(offset, NLV1_HEAD_LEN)
        self.assertEqual(header.version, PROTOCOL_VERSION)
        self.assertEqual(header.frame_index, 5)
        self.assertEqual(header.payload_len, 6)
        self.assertEqual(header.next_head, 7)
        self.assertEqual(header.hops_limit, 8)
        self.assertEqual(header.src_ia, 0x1234567812345678)
        self.assertEqual(header.dst_ia, 0x8765432187654321)

    def test_standard_header_to_bytes(self):
        header = StandardHeader()
        header.version = PROTOCOL_VERSION
        header.frame_index = 5
        header.payload_len = 6
        header.next_head = 7
        header.hops_limit = 8
        header.src_ia = 0x1234567812345678
        header.dst_ia = 0x8765432187654321
        data = standard_header_to_bytes(header)
        self.assertEqual(data, bytearray(
            [0x01, 0x05, 0x00, 0x06, 0x07, 0x08, 0x12, 0x34, 0x56, 0x78, 0x12, 0x34, 0x56, 0x78, 0x87, 0x65, 0x43, 0x21,
             0x87, 0x65, 0x43, 0x21]))

    def test_ia(self):
        self.assertEqual(is_global_ia(0x2140000000000401), True)
        self.assertEqual(is_global_ia(0x4001000000000401), False)
        self.assertEqual(is_constant_ia(0x2140000000000401), False)
        self.assertEqual(is_constant_ia(0x4001000000000401), True)

    @staticmethod
    def print_hex(data: bytearray):
        for i in data:
            print('%02x ' % i, end='')
        print()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
