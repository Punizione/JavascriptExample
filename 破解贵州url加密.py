from Crypto.Cipher import AES
import base64


class EnAES(object):
    def __init__(self):
        # self.BS的值为16
        self.BS = AES.block_size
        self.key = b'qnbyzzwmdgghmcnm'
        self.cipher = AES.new(self.key, AES.MODE_ECB)   # 初始化AES实例， 使用ECB模式，源码加密模式就是这样子，key也是一样的

    def pad(self, s):
        """
        PKCS 7 填充方法
        放回的是16倍数长度字符串，填充值是待填充个数，字符串长度必须是16或者是16的倍数 如:
        01 01 01 01 01 01 01 01 长度为8
        填充之后为
        01 01 01 01 01 01 01 01 08 08 08 08 08 08 08 08

        如果传入长度为16 需再填充16个， 如：
        01 01 01 01 01 01 01 01 08 08 08 08 08 08 08 08
        填充之后为
        01 01 01 01 01 01 01 01 08 08 08 08 08 08 08 08 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
        :param s: 待填充值
        :return: 16倍数长度字符串
        """
        # 填充为16进制 以空白来填充
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

    def aes_encrypt(self, text):
        """
        text为待破解的数字
        下面的代码是多个语句放在一起
        拆开来就是
        pad_text = self.pad(text)   # 填充
        b_text = bytearray(pad_text, encoding='utf-8')    # 转为byte
        encrypt_text = self.cipher.encrypt(b_text)      # 加密
        encrypt_text_utf-8 = base64.standard_b64encode(encrypt_text).decode('utf-8')[:-2]
            # 将二进制转为utf-8，同时去掉加密字符最后两位俩个等号
        encrypt_text_utf-8_url = encrypt_text_utf-8.replace('/', '^').replace('\\', '^')
            # 替换字符，源码如此
        """
        # return base64.standard_b64encode(self.cipher.encrypt(bytearray(self.pad(text), encoding='utf-8'))
        #                                  ).decode('utf-8')[:-2].replace('/', '^').replace('\\', '^')
        # return base64.standard_b64encode(self.cipher.encrypt(self.pad(text))
        #                          ).decode('utf-8')[:-2].replace('/', '^').replace('\\', '^')
        pad_text = self.pad(text)
        print('pad_text : ', pad_text)
        encrypt_text = self.cipher.encrypt(pad_text)
        print('encrypt_text : ', encrypt_text)
        encrypt_text_utf8 = base64.standard_b64encode(encrypt_text).decode('utf-8')
        encrypt_text_utf8 = base64.b64encode(encrypt_text).decode('utf-8')
        print('encrypt_text_utf-8 : ', encrypt_text_utf8.encode())
        print('encrypt_text_utf-8 : ', encrypt_text_utf8)
        return encrypt_text_utf8[:-2]

    def url_encrypt(self, url):
        url_id = url.split('/')[-1].split('.')[0]
        print('url_id : ', url_id)
        encrypt_id = self.aes_encrypt(url_id)  # 获取url中的数字"20825",并调用aes_encrypt解密
        url = url.split('/')
        url[-1] = encrypt_id+'.'+url[-1].split('.')[1]
        return "/".join(url)


def main():
    url_1 = 'http://ggzy.gzlps.gov.cn/jyxxzczb/20825.jhtml'
    # url_2 = 'http://ggzy.gzlps.gov.cn:80/jyxxzczb/20827.jhtml'
    aes = EnAES()
    """
    在调用之前先初始化这个实例
    后面每一次获取加密链接至需要调用aes.url_encrypt(url)即可
    """

    print(aes.url_encrypt(url_1))
    # print(aes.url_encrypt(url_2))


if __name__ == '__main__':
    main()
