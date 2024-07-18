from utilis.account_redis_interface import AccountRedisInterface
import re
with open('data.txt', 'r+',encoding='utf-8') as f:
    users = f.readlines()

for i in users:
    """
    登录账号:(.*?)----登录密码:(.*?)----2FA验证码（https://2fa.run/,复制这一串到这个网址获取验证码:(.*?) 登录教程：https://bit.ly/4dGuQrB----改密、换绑邮箱手机号教程：https://bit.ly/4bj54YP

    
    """
    account = i.split('----')[0].replace('登录账号:','')
    password = i.split('----')[1].replace('登录密码:','')
    email = '718'
    fa = i.split('----')[2].split('网址获取验证码:')[1].split(' 登录教程')[0]
    accountinfo = account+":"+password+":"+email+":"+fa
    print(accountinfo)
    # 1 需要登陆 2 登陆完成 4 失效
    AccountRedisInterface().add_account(accountinfo,1)




