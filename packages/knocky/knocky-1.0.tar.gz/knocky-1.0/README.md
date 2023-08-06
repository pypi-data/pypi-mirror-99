# knocky

## 介绍
knocky包用于通信时帧头和帧正文处理解耦。

帧正文处理函数注册成knocky包的服务，帧头处理调用服务，调用knocky服务获取响应数据。

本软件包已上传到pypi，可输入命令直接安装。
```python
pip install knocky
```

## 示例
```python
import knocky as knock


def main():
    knock.register(0, 5, service1)
    print(knock.call(0, 5, bytearray([4, 5])))


def service1(req: bytearray, *args) -> (bytearray, bool):
    print('service1 get req:', req, args)
    return bytearray([1, 2, 3]), True


if __name__ == '__main__':
    main()
```

输出:
```text
service1 get req: bytearray(b'\x04\x05') ()
resp: (bytearray(b'\x01\x02\x03'), True)
```
