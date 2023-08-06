"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
knocky包用于通信时帧头和帧正文处理解耦
帧正文处理函数注册成knock包的服务,帧头处理调用服务,调用knock服务获取响应数据
Authors: jdh99 <jdh821@163.com>
"""

import unittest

_services = dict()


def call(protocol: int, cmd: int, req: bytearray, *args) -> (bytearray, bool):
    """Call 同步调用.返回值是应答字节流和是否需要应答标志"""
    global _services

    rid = cmd + (protocol << 16)
    if rid not in _services:
        return None, False
    return _services[rid](req, *args)


def register(protocol: int, cmd: int, callback):
    """
    注册服务回调函数
    callback是回调函数,格式:func(req: bytearray, *args) -> (bytearray, bool)
    回调函数的返回值是应答数据和应答标志.应答标志为false表示不需要应答
    """
    global _services

    rid = cmd + (protocol << 16)
    _services[rid] = callback


call(0, 1, bytearray([2, 3]), 4, 5)


class _UnitTest(unittest.TestCase):
    def test_case1(self):
        register(0, 1, self.service1)
        resp, result = call(0, 1, bytearray([4, 5]))
        print('resp:', resp, result)
        self.assertEqual(resp, bytearray([1, 2, 3]))
        self.assertEqual(result, True)

        resp, result = call(0, 2, bytearray([4, 5]))
        print(resp, result)
        self.assertEqual(resp, None)
        self.assertEqual(result, False)

        resp, result = call(1, 1, bytearray([4, 5]))
        print(resp, result)
        self.assertEqual(resp, None)
        self.assertEqual(result, False)

        register(0, 2, self.service2)
        resp, result = call(0, 2, bytearray([4, 5]), 'args1', ['a', 'b'])
        print(resp, result)
        self.assertEqual(resp, bytearray([6, 7, 8, 9]))
        self.assertEqual(result, True)

    @staticmethod
    def service1(req: bytearray, *args) -> (bytearray, bool):
        print('service1 get req:', req, args)
        return bytearray([1, 2, 3]), True

    @staticmethod
    def service2(req: bytearray, *args) -> (bytearray, bool):
        print('service2  get req:', req, args)
        return bytearray([6, 7, 8, 9]), True


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(_UnitTest("test_case1"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
