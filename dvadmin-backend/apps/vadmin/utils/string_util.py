"""
封装字符串相关函数:UUID字符串,字符串加密解密
"""
import uuid as UUID
import base64

CHAR_SET = ("a", "b", "c", "d", "e", "f",
            "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
            "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
            "W", "X", "Y", "Z")


def uuid():
    """
    返回一个UUID对象
    :return:
    """
    return UUID.uuid4()


def uuid_36():
    """
    返回36字符的UUID字符串(十六进制,含有-)  bc5debab-95c3-4430-933f-2e3b6407ac30
    :return:
    """
    return str(UUID.uuid4())


def uuid_32():
    """
    返回32字符的UUID字符串(十六进制)  bc5debab95c34430933f2e3b6407ac30
    :return:
    """
    return uuid_36().replace('-', '')


def uuid_8():
    """
    返回8字符的UUID字符串(非进制)  3FNWjtlD
    :return:
    """
    s = uuid_32()
    result = ''
    for i in range(0, 8):
        sub = s[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += CHAR_SET[x % 0x3E]
    return result


def uuid_16():
    """
    返回16字符的UUID字符串(非进制)  3FNWjtlD3FNWjtlD
    :return:
    """
    return uuid_8() + uuid_8()


def bas64_encode_text(text):
    """
    base64加密字符串
    :param text:
    :return:
    """
    if isinstance(text, str):
        return str(base64.b64encode(text.encode('utf-8')), 'utf-8')
    return text


def bas64_decode_text(text):
    """
    base64解密字符串
    :param text:
    :return:
    """
    if isinstance(text, str):
        return str(base64.decodebytes(bytes(text, encoding="utf8")), 'utf-8')
    return text


def decode_text(text, crypto=""):
    """
    解密字符串
    :param text: 字符串
    :param crypto: 解密算法
    :return:
    """
    if crypto:
        if crypto.lower() == 'base64':
            text = bas64_decode_text(text)
        else:
            text = text
    return text


def encode_text(text, crypto=""):
    """
    加密字符串
    :param text: 字符串
    :param crypto: 加密算法
    :return:
    """
    if crypto:
        if crypto.lower() == 'base64':
            text = bas64_encode_text(text)
        else:
            text = text
    return text
