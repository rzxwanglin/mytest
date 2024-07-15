import re

with open('data/account.txt','r+',encoding='utf8') as f:
    accounts= f.readlines()

for i in accounts:
    print(i.split('----'))
    username = i.split('----')[0].replace('登录账号:','')
    passwd = i.split('----')[1].replace('登录密码:','')
    email ='11@qq.com'
    pat = re.compile('2FA验证码（https://2fa.run/,复制这一串到这个网址获取验证码:(.*?) 登录教程：https://bit.ly/4dGuQrB')
    fcode =re.findall(pat,i.split('----')[2])[0]
    with open('data/account_info.txt','a+',encoding='utf-8') as f:
        f.write(username+':'+passwd+':'+email+':'+fcode+'\n')
