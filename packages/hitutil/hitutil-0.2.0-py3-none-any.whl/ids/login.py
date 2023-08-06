from requests import Session
import re
from .utils import encrypt, rds
from bs4 import BeautifulSoup


def idslogin(username, password):
    s = Session()
    # get pwdDefaultEncryptSalt
    r1 = s.get('http://ids.hit.edu.cn/authserver/login')
    pwd_default_encrypt_salt = re.compile(
        'pwdDefaultEncryptSalt = "(.*)"').search(r1.text).groups()[0]
    passwordEncrypt = encrypt(
        rds(64).encode()+password.encode(), pwd_default_encrypt_salt.encode())
    # Detect Captcha
    r2 = s.get(
        'http://ids.hit.edu.cn/authserver/needCaptcha.html?username=%s&pwdEncrypt2=pwdEncryptSalt' % username)
    if r2.text == 'true':
        raise Exception('Captcha needed')
    soup = BeautifulSoup(r1.text, 'html.parser')
    r = s.post(r1.url, data={
        "username": username,
        "password": passwordEncrypt,
        "captchaResponse": None,
        "lt": soup.find('input', {'name': 'lt'})['value'],
        "dllt": soup.find('input', {'name': 'dllt'})['value'],
        "execution": soup.find('input', {'name': 'execution'})['value'],
        "_eventId": soup.find('input', {'name': '_eventId'})['value'],
        "rmShown": soup.find('input', {'name': 'rmShown'})['value'],
        "pwdDefaultEncryptSalt": pwd_default_encrypt_salt
    })
    if r.url != 'http://ids.hit.edu.cn/authserver/index.do':
        raise Exception('Fail to login')
    return s