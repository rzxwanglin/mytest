#!/bin/env  python3
# cython: language_level=3

'''
python 在 Windows下使用AES时要安装的是pycryptodome 模块 pip install pycryptodome
python 在 Linux下使用AES时要安装的是pycrypto模块 pip install pycrypto
其实安装pip install Crypto也可以,可能安装完以后会出现
ModuleNotFoundError: No module named 'Crypto'的错误
这时需要去python的根目录下/Lib/site-packages/找到crypto 、crypto-1.4.1.dist-info 目录，将crypto 首字母改为大写，即修改名称为 Crypto、 Crypto-1.4.1.dist-info .就可以了


因为本脚本含有密钥,需要编译成.so放在在安装包中,如下:
pythonInclude=$(dirname $(which python3))/../include/python3.6m
cython=$(find  $(dirname $(which python3))/../ -name cython.py)
python3 $cython ./crypt.py
gcc -shared -fPIC -I${pythonInclude} ./crypt.c -o ./crypt.so
'''

import argparse
import pdb
import base64
from Crypto.Cipher import AES

tk = "ENCRYPTED|"
# 即rzx@1218在小端机器上的二进制值
key = '7a72407832313831'


# 填充函数
def add_to_16(value):
    while True:
        val = value.encode('utf-8')
        l = len(val)
        if l < 16 or l % 16 != 0:
            value += '\x00'  # 补全, 明文和key都必须是16的倍数
            continue
        break
    return value.encode('utf-8')


# 加密
def Encrypt(text):
    global key
    iv = add_to_16("")
    print("iv",iv.decode("utf-8"))
    mode = AES.MODE_CBC
    key = add_to_16(key)
    print("key",key.decode("utf-8"))
    print("add_to_16(text)",add_to_16(text).decode("utf-8"))

    aes = AES.new(key=key, mode=mode, IV=iv)
    encryptedstr = aes.encrypt(add_to_16(text))  # 加密后得到的字节数据
    # 结果: b'\x8f#\x10\xeb\xf8\x13\xb4\xb5\x11\x9d\x185'
    en_str = base64.b64encode(encryptedstr).decode()  # 以base64编码方式解码, 得到加密字符串!
    # 结果:yMQ6/gTtLURnRg1Iu2ZMiix79u8jsVHHFA2qKs28aQ=
    # en_str = b2a_hex(encryptedstr).decode()  # 以hex编码方式解码, 得到加密字符串
    # 结果:8f2310ebf813b4b5119d183522ed993228b1efdbbc8ec5471c5036a8ab36f1a4
    return en_str  # 把加密后的字节数据返回


# 解密
def Decrypt(en_str):
    global key
    iv = add_to_16("")
    # 解密时必须重新构建aes对象
    aes = AES.new(key=add_to_16(key), mode=AES.MODE_CBC, IV=iv)
    # 先把密文转换成字节型, 再解密, 最后把之前填充的'\x00' 去掉
    decryptedstr = aes.decrypt(base64.decodebytes(en_str.encode())).decode().strip('\x00')
    # decryptedstr = aes.decrypt(a2b_hex(en_str)).decode().strip('\x00') # 对应上面的hex编码
    return decryptedstr


def DecodeText(text):
    # 加密内容格式:
    # ENCRYPTED|<密文>
    global tk
    pos = text.find(tk)
    if pos >= 0:
        try:
            c = text[len(tk):]
            decode = Decrypt(c)
            return decode
        except:
            return "Bad!"
    else:
        return text


if __name__ == '__main__':
    print(Encrypt("minioadmin"))
    # print(Decrypt("5qjAbMTNA+ZN+r2mBIsoxw=="))
    exit()

    parser = argparse.ArgumentParser(description="encode/decode tools")
    parser.add_argument("-d", "--decode", nargs='?', default='encode',
                        help="decode the text", dest='code')
    parser.add_argument("-t", "--text", nargs="+",
                        help="the text to de/en code", type=str, dest='text')

    # pdb.set_trace()
    args = parser.parse_args()
    print(args.text)
    text = args.text[0]

    if args.code == 'encode':
        en_str = Encrypt(text)
        print(en_str)
    else:
        # pdb.set_trace()
        try:
            if text.find(tk) >= 0:
                de_str = DecodeText(text)
            else:
                de_str = Decrypt(text)
            print(de_str)
        except:
            print("Bad args!")
