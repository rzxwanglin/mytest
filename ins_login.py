import sys, os
current_path = os.getcwd()

if "ins_login" in current_path:
    current_path = current_path.replace("ins_login", "")

sys.path.append(current_path)
sys.path.append(r"D:\project\tkspider")
import requests, time, traceback
import json, random, re, io, copy, platform, os
import email
import imaplib
from email.header import decode_header
from email.utils import parsedate_to_datetime

import speech_recognition as sr
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from loguru import logger
import config
from rhino_v2_utilis.handler.redis_handler import CRedisHandler
chrome_driver_path = os.path.join(current_path, "ins_login\\chromedriver.exe")
if platform.system() == 'Linux':
    chrome_driver_path = os.path.join(current_path, "ins_login/chromedriver_linux")
pro = random.choice(config.token_proxy_list)
os.environ.setdefault('HTTP_PROXY', f'http://' + pro)
os.environ.setdefault('HTTPS_PROXY', f'http://' + pro)
client = CRedisHandler(**config.cookies_redis_config)

class AliexpressSlider():
    def __init__(self, header=True):
        self.header = header
        self.chrome_driver = chrome_driver_path
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        # self.proxy = "http://10.11.203.70:50019"
        self.proxy = "http://127.0.0.1:7890"

    def get_proxy_ua(self):
        proxy_list = copy.deepcopy(config.token_proxy_list)
        ua_list = copy.deepcopy(config.user_agent_list)
        in_use_account_key = client.hkeys(config.token_cookie_hash)
        for cookie_key in in_use_account_key:
            cookie_detail = json.loads(client.hget(config.token_cookie_hash, cookie_key))
            if cookie_detail.get("proxy") in proxy_list:
                proxy_list.remove(cookie_detail.get("proxy"))  # 代理不重复在cookie中使用
            # if cookie_detail.get("user-agent") in ua_list:
            #     ua_list.remove(cookie_detail.get("user-agent"))  # 代理不重复在cookie中使用
        return proxy_list, ua_list, in_use_account_key

    def create_browser(self):
        logger.info("初始化 browser")
        chrome_options = webdriver.ChromeOptions()
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         'images': 2,  # 禁用图片的加载
        #         'javascript': 2  # 禁用js，可能会导致通过js加载的互动数抓取失效
        #     }
        # }
        # chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 无图模式
        # if self.header:
        #     chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--disable-gpu')  # 禁用gpu加速
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument("--auto-open-devtools-for-tabs")

        # if proxy_type == "short_proxy":
        #     chrome_options.add_argument('--proxy-server={}'.format("127.0.0.1:8080"))  # 短效代理
        # elif proxy_type == "local_proxy":
        #     pass
        # else:
        #     chrome_options.add_extension(self.get_chrome_proxy_extension(proxy=self.proxy))  # 长效代理
        chrome_options.add_argument("--user-agent=" + self.ua)
        # if "@" in self.proxy:
        #     chrome_options.add_argument(f'--proxy-server={"http://" + self.proxy.split("@")[1]}')
        #     chrome_options.add_argument(f'--proxy-auth={self.proxy.replace("http://", "").split("@")[0].split(":")[0]}:{self.proxy.replace("http://", "").split("@")[0].split(":")[1]}')
        # else:
        #     chrome_options.add_argument(f'--proxy-server={self.proxy}')

        # # 设置开发者模式启动，该模式下webself.driver属性为正常值
        try:
            self.browser = webdriver.Chrome(options=chrome_options, executable_path=binary_path)
        except:
            self.browser = webdriver.Chrome(options=chrome_options)
        script = 'Object.defineProperties(navigator,{webdriver:{get:() => undefined}});' \
                 'Object.defineProperty(navigator, "plugins", {get: () => [1, 2, 3],});'
        # 'Object.defineProperty(navigator, "languages", {get: () => ["en-US", "en"]});' \
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        script = 'Object.defineProperties(navigator,{webdriver:{get:() => undefined}});' \
                 'Object.defineProperty(navigator, "plugins", {get: () => [1, 2, 3],});'
        # 'Object.defineProperty(navigator, "languages", {get: () => ["en-US", "en"]});' \
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.wait = WebDriverWait(self.browser, 20)
        logger.info('启动浏览器')

    def cookie_login(self, cookie_str):
        for cook in cookie_str.split(";"):
            if not cook.strip():continue
            name = cook.split("=")[0].strip()
            value = cook.replace(name + "=", "").strip()
            cookie_dict = {
                'domain': 'instagram.com',
                'name': name,
                'value': value,
                "expires": "2025-12-30T08:53:52.782Z",
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            self.browser.add_cookie(cookie_dict)
        time.sleep(2)
        self.browser.get("https://www.instagram.com")
        time.sleep(2)

    def click_notice(self):
        page_source = self.browser.page_source
        html = etree.HTML(page_source)
        try:
            if html.xpath('//div[@class="_a9-z"]/button[2]'):
                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="_a9-z"]/button[2]'))).click()
        except:
            return

    def judge_page(self):
        page_source = self.browser.page_source
        html = etree.HTML(page_source)
        if (self.browser.current_url == "https://www.instagram.com/" or "https://www.instagram.com/?" in self.browser.current_url) and not html.xpath('//*[@id="loginForm"]'):
            return "账号正常"
        if "two_factor" in self.browser.current_url:
            return "二次验证"
        if "***" in page_source and "@" in page_source:
            return "邮箱验证"
        if "accounts/suspended" in self.browser.current_url:
            return "账号被封"
        if "自动化" in self.browser.page_source:
            return "出现验证"
        if html.xpath('//div[@class="wbloks_29"]'):
            if "challenge/action" in self.browser.current_url or ("***" in page_source and "@" in page_source):
                return "邮箱验证"
            if "/challenge/" in self.browser.current_url:
                return "出现验证"
        if html.xpath('//*[@class="_abya"]'):
            if html.xpath("//iframe"):
                return "谷歌验证"
            if "添加手机号即可重新登录" in self.browser.page_source:
                return "手机验证"
        if "login" in self.browser.current_url or html.xpath('//*[@id="loginForm"]'):
            return "账号掉线"
        return "未知异常"

    def click_verify(self):
        while True:
            try:
                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]'))).click()
            except:
                return "验证失败"
            time.sleep(2)
            message = self.judge_page()
            if message == "账号正常":
                return "验证成功"
            elif message == "账号掉线":
                return "账号掉线"
            elif message == "出现验证":
                time.sleep(5)
                continue
            else:
                return "账号异常"

    def input_text(self, xpath_path, text):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath_path))).clear()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath_path))).click()
        for i in text:
            ActionChains(self.browser).key_down(str(i)).perform()
            ActionChains(self.browser).key_up(str(i)).perform()
            # time.sleep(0.5)
        time.sleep(1)

    def get_email_verify_code(self, acc_hkey):
        """
        获取邮箱验证码
        :return:
        """
        email_address = acc_hkey.split(":")[2]
        password = acc_hkey.split(":")[3]
        imap_server = "imap." + email_address.split("@")[-1]
        imap_port = 993
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(email_address, password)
        mailbox = "INBOX"
        mail.select(mailbox)
        if email_address.split("@")[-1] == "gmx.com":
            status, messages = mail.search(None, 'FROM "no-reply@mail.instagram.com"')
            mail_ids = messages[0].split()
            for mail_id in mail_ids:
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # 获取邮件主题
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                if "code" not in subject:
                    continue
                date_string = msg.get("Date")
                if date_string:
                    date_parsed = parsedate_to_datetime(date_string)
                    time_stamp = int(date_parsed.timestamp())
                    if time_stamp < int(time.time() - 300):
                        continue
                # 获取邮件标题
                code = re.search("(\d{4,6})", subject).group(1)
                # 关闭 IMAP 连接
                mail.logout()
                return code
        else:
            status, messages = mail.search(None, 'all')
            mail_ids = messages[0].split()
            for mail_id in mail_ids[::-1]:
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # 获取邮件主题
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                if "验证帐户" not in subject and 'Verify your account' not in subject:
                    continue
                date_string = msg.get("Date")
                if date_string:
                    date_parsed = parsedate_to_datetime(date_string)
                    time_stamp = int(date_parsed.timestamp())
                    if time_stamp < int(time.time() - 300):
                        continue
                # 获取邮件验证码
                code = etree.HTML(msg.get_payload()).xpath("//font/text()")[0]
                # 关闭 IMAP 连接
                mail.logout()
                return code

    def email_verify(self, acc_hkey):
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="_ad-m"]//button'))).click()
        except:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@aria-label,"发送验证码")]'))).click()
        time.sleep(20)
        verify_code = self.get_email_verify_code(acc_hkey)
        try:
            self.input_text('//input[@id="security_code"]', verify_code)
        except:
            self.input_text('//input[@class="_aaye"]', verify_code)
        time.sleep(3)
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="_ad-m"]//button'))).click()
        except:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(@aria-label,"验证")]'))).click()
        time.sleep(10)
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(@aria-label,"是，正确无误")]'))).click()
        except:
            pass
        time.sleep(20)
        self.browser.get("https://www.instagram.com/")
        time.sleep(5)

    def login(self, acc_hkey):
        account = acc_hkey.split(":")[0]
        password = acc_hkey.split(":")[1]
        logger.info(f"开始账号密码登录...... account: {account}, password: {password}")
        # 输入账号
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="username"]'))).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="username"]'))).clear()
        for i in account:
            ActionChains(self.browser).key_down(str(i)).perform()
            ActionChains(self.browser).key_up(str(i)).perform()
        time.sleep(3)
        # 输入密码
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]'))).click()
        for i in password:
            ActionChains(self.browser).key_down(str(i)).perform()
            ActionChains(self.browser).key_up(str(i)).perform()
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()  # 点击登录
        time.sleep(10)

    def account_login(self, acc_hkey):
        self.login(acc_hkey)
        page_source = self.browser.page_source
        html = etree.HTML(page_source)
        if html.xpath('//div[@role="button"]'):
            try:
                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]'))).click()
            except:
                return
            time.sleep(5)
        message = self.judge_page()
        if message == "谷歌验证" or message == "未知异常":
            try:
                status = self.google_verify()
            except:
                status = False
            if not status:
                client.hset("instagram_google_verify_fail", acc_hkey, 1)
                logger.error("谷歌验证失败， tooken存入谷歌验证失败队列， 等待手动验证")


    # def convert_wav(self, mp3_binary_data):
    #     # 使用 BytesIO 将二进制数据包装成文件对象
    #     mp3_io = io.BytesIO(mp3_binary_data)
    #
    #     # 读取MP3文件
    #     audio = AudioSegment.from_mp3(mp3_io)
    #
    #     # 指定输出WAV文件名
    #     wav_file = "output.wav"
    #
    #     # 将MP3文件保存为WAV文件
    #     audio.export(wav_file, format="wav")
    #
    #     logger.info(f"已将MP3转换为{wav_file}")

    # def convert_text(self):
    #     try:
    #         # 转换音频格式
    #         sound = AudioSegment.from_mp3(r"output.wav")
    #         time.sleep(2)
    #         sound.export("audio.wav", format="wav")
    #
    #         # 读取音频文件
    #         r = sr.Recognizer()
    #         with sr.AudioFile('audio.wav') as source:
    #             audio_text = r.record(source)
    #             # 语音识别
    #             return r.recognize_google(audio_text, language='en-US')
    #     except:
    #         return


    def google_verify(self):
        self.browser.switch_to.frame(
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@id="recaptcha-iframe"]'))))
        time.sleep(1)
        self.browser.switch_to.frame(
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]'))))
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
        time.sleep(2)
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame(
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@id="recaptcha-iframe"]'))))
        time.sleep(1)
        self.browser.switch_to.frame(
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[contains(@title,"reCAPTCHA ")]'))))
        time.sleep(2)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="button-holder audio-button-holder"]/button'))).click()
        time.sleep(5)
        html = etree.HTML(self.browser.page_source)
        mp3_xpath = html.xpath('//div[@class="rc-audiochallenge-tdownload"]/a/@href')
        if mp3_xpath:
            mp3_link = mp3_xpath[0]
            logger.info("google验证音频地址：" + mp3_link)
        else:
            logger.error("谷歌验证失败")
        try:
            resp = requests.get(mp3_link, timeout=5, proxies={"http": self.proxy, "https": self.proxy})
        except:
            logger.error("获取google语音验证码mp3数据失败")
        self.convert_wav(resp.content)
        verify_code = self.convert_text()
        if not verify_code:
            logger.error("提取音频文字信息失败")
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div//input[@type="text"]'))).click()
        for i in verify_code:
            ActionChains(self.browser).key_down(str(i)).perform()
            ActionChains(self.browser).key_up(str(i)).perform()
            time.sleep(0.1)
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="verify-button-holder"]/button'))).click()
        self.browser.switch_to.default_content()
        time.sleep(5)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]'))).click()
        time.sleep(20)
        logger.info("google语音验证成功")
        return True


    def ins_login(self, acc_hkey):
        self.login(acc_hkey)
        page_source = self.browser.page_source
        html = etree.HTML(page_source)
        if html.xpath('//div[@role="button"]') and self.judge_page() != "谷歌验证":
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]'))).click()
            time.sleep(5)
        message = self.judge_page()
        if message == "谷歌验证" or message == "未知异常":
            try:
                self.google_verify()
            except:
                client.hset("instagram_google_verify_fail", acc_hkey, 1)
                logger.error("谷歌验证失败， tooken存入谷歌验证失败队列， 等待手动验证")

    def get_account(self):
        total_hkeys = client.hkeys(config.token_count_hash.format("total"))
        for acc_hkey in total_hkeys:
            data = json.loads(client.hget(config.token_count_hash.format("total"), acc_hkey))
            fail_count = data.get("fail_count")
            if fail_count > 3:
                logger.info(f"当前验证账号使用情况如下： {acc_hkey}, {json.dumps(data, ensure_ascii=False)}")
                cookie = client.hget("instagram_cookie_hash", acc_hkey)
                if client.hget("instagram_google_verify_fail", acc_hkey):
                    continue
                if cookie:
                    return acc_hkey, json.loads(cookie)
                else:
                    return acc_hkey, {
                            "cluster_id": data.get("cluster_id"),
                            "proxy": random.choice(config.token_proxy_list),
                            "user-agent": random.choice(config.user_agent_list),
                            "cookie": "",
                        }
        login_token = client.hkeys(config.login_token_account_hash)
        for acc_hkey in login_token:
            fail_hash = client.hget("instagram_cookie_fail_hash", acc_hkey)
            total_hash = client.hget(config.token_total_hash, acc_hkey)
            cookie_hash = client.hget(config.token_cookie_hash, acc_hkey)
            if fail_hash or total_hash or cookie_hash:
                continue
            if client.hget("instagram_google_verify_fail", acc_hkey):
                continue
            proxy, ua, _ = self.get_proxy_ua()
            cookie = {
                # "proxy": random.choice(proxy),
                "cluster_id": int(client.hget(config.login_token_account_hash, acc_hkey)),
                "user-agent": random.choice(ua),
                "cookie": "",
            }
            return acc_hkey, cookie
        if len(client.hkeys(config.token_total_hash)) < 20:
            acc_keys = client.hkeys(config.acc_pw_hash)
            if len(acc_keys) <= 0:
                logger.error("注册登录队列 账号不足")
                return "", {}
            acc_hkey = random.choice(acc_keys)
            proxy, ua, _ = self.get_proxy_ua()
            cookie = {
                # "proxy": random.choice(proxy),
                "cluster_id": int(client.hget(config.acc_pw_hash, acc_hkey)),
                "user-agent": random.choice(ua),
                "cookie": "",
            }
            if client.hget("instagram_google_verify_fail", acc_hkey):
                return "", {}
            return acc_hkey, cookie
        return "", {}

    def verify_2fa(self, acc_hkey):
        logger.info(f"开始instagram 2fa验证, {acc_hkey}")
        verify_str = acc_hkey.split(":")[-1]
        if verify_str == "olkQtEMAd":
            client.hset("instagram_google_verify_fail", acc_hkey, "2fa验证")
            return
        url = "https://2fa.run/app/2fa.php?secret=" + verify_str
        payload = {}
        headers = {
            'authority': '2fa.run',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://2fa.run/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            verify_code = json.loads(response.text)["newCode"]
        except:
            client.hset("instagram_google_verify_fail", acc_hkey, "2fa验证")
            logger.error(f"2fa验证获取验证码失败， {acc_hkey}")
            return
        # "//*[@id="mount_0_0_4k"]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[1]/div/label/input"
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="验证码"]'))).click()
        for i in verify_code:
            ActionChains(self.browser).key_down(str(i)).perform()
            ActionChains(self.browser).key_up(str(i)).perform()
            time.sleep(0.1)
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"确认")]'))).click()
        time.sleep(15)
        self.browser.refresh()
        time.sleep(5)


    def set_cookie(self, acc_hkey, cookie_info):
        if not cookie_info.get("cluster_id"):
            cookie_info["cluster_id"] = int(client.hget(config.login_token_account_hash, acc_hkey))
        if client.hget(config.token_count_hash.format("total"), acc_hkey):
            cookie_count_info = json.loads(client.hget(config.token_count_hash.format("total"), acc_hkey))
            cookie_count_info["fail_api"] = ""
            cookie_count_info["fail_count"] = 0
            cookie_count_info["fail_type"] = ""
            cookie_count_info["verify_times"] = int(cookie_count_info.get("verify_times", 0)) + 1
            client.hset(config.token_count_hash.format("total"), acc_hkey, json.dumps(cookie_count_info))
        if cookie_info.get("proxy"):
            cookie_info.pop("proxy")
        client.hset(config.token_total_hash, acc_hkey, json.dumps(cookie_info))
        client.hdel(config.token_cookie_hash, acc_hkey)
        client.hdel(config.acc_pw_hash, acc_hkey)
        client.hdel("instagram_google_verify_fail", acc_hkey)

    def set_fail_cookie(self, acc_hkey, cookie, message):
        if not client.hget("instagram_cookie_fail_hash", acc_hkey):
            cookie_count = json.loads(client.hget("instagram_cookie_total:count_hash", acc_hkey)) if client.hget(config.token_count_hash.format("total"), acc_hkey) else {}
            client.hset("instagram_cookie_fail_hash", acc_hkey, json.dumps({"message": message, "time_stamp": int(time.time()), "cookie": cookie, "cookie_count": cookie_count}, ensure_ascii=False))
        client.hdel(config.token_count_hash.format("total"), acc_hkey)
        client.hdel(config.token_cookie_hash, acc_hkey)
        client.hdel(config.acc_pw_hash, acc_hkey)
        client.hdel("instagram_google_verify_fail", acc_hkey)
        client.hset(config.fail_token_account_hash, acc_hkey, 4)

    def instagram_login(self, acc_hkey, cookie):
        try:
            self.create_browser()
            self.browser.get("https://www.instagram.com")
            time.sleep(3)
            if not cookie.get("cookie") or cookie.get("cookie") == "":        # cookie为空，则为账号密码登录
                cookie_str = ""
                self.ins_login(acc_hkey)
            else:                   # cookie不为空， 为注入cookie登录
                cookie_str = cookie.get("cookie", "")
                logger.info(f"开始注入cookie登录 account: {acc_hkey}")
                self.cookie_login(cookie_str)
            time.sleep(3)
            message = self.judge_page()
            if message == "二次验证":
                try:
                    self.verify_2fa(acc_hkey)
                except:
                    client.hset("instagram_google_verify_fail", acc_hkey, "2fa验证异常")
                    logger.error(f"2fa验证失败， error: {traceback.format_exc()}")

            self.browser.refresh()
            time.sleep(3)
            # 验证账号是否出现掉线，验证，被封情况
            message = self.judge_page()
            logger.info(f"账号状态为： {message}")
            if message == "账号掉线":
                self.account_login(acc_hkey)
                message = self.judge_page()
                logger.info(f"重新登录后账号状态为： {message}")
            if message == "二次验证":
                try:
                    self.verify_2fa(acc_hkey)
                except:
                    client.hset("instagram_google_verify_fail", acc_hkey, "2fa验证异常")
                    logger.error(f"2fa验证失败， error: {traceback.format_exc()}")
            elif message == "邮箱验证":
                html = etree.HTML(self.browser.page_source)
                email_addr = html.xpath('//*[contains(text(),"@")]/text()')[0].replace("邮箱：", "").strip()
                email_address = acc_hkey.split(":")[2]
                if email_addr[0] == email_address[0] and email_addr[-1] == email_address[-1] and email_addr.split("@")[-1][0] == email_address.split("@")[-1][0]:
                    try:
                        self.email_verify(acc_hkey)
                        logger.info("邮箱验证成功")
                    except:
                        logger.info("邮箱验证失败")
                else:
                    self.set_fail_cookie(acc_hkey, cookie, message)
            if message == "谷歌验证" or message == "未知异常":
                try:
                    self.google_verify()
                except:
                    client.hset("instagram_google_verify_fail", acc_hkey, 1)
                    logger.error("谷歌验证失败， tooken存入谷歌验证失败队列， 等待手动验证")
            if "accounts/onetap" in self.browser.current_url and "保存你的登录信息" in self.browser.page_source:
                self.browser.get("https://www.instagram.com")
                time.sleep(5)
            self.account_judge(acc_hkey, cookie)
        except:
            logger.info("error: " + traceback.format_exc())
        self.browser.quit()

    def account_judge(self, acc_hkey, cookie_info):
        cookie_str = ""
        message = self.judge_page()
        if message == "账号正常":
            # 点击 打开通知窗口
            self.click_notice()
            self.browser.refresh()
            time.sleep(5)
            for cookie_ in self.browser.get_cookies():
                cookie_str += cookie_["name"] + "=" + cookie_["value"] + "; "
            cookie_info["cookie"] = cookie_str
            self.set_cookie(acc_hkey, cookie_info)
        elif message == "账号掉线":  # 如果账号掉线，则循环到下次重新登录
            pass
        elif message == "出现验证":  # ins自动化验证， 点击账号自动化关闭按钮
            self.click_verify()
            time.sleep(5)
            self.click_notice()
            time.sleep(5)
            for cookie in self.browser.get_cookies():
                cookie_str += cookie["name"] + "=" + cookie["value"] + "; "
            cookie_info["cookie"] = cookie_str
            self.set_cookie(acc_hkey, cookie_info)
        elif message == "邮箱验证":  # ins账号邮箱验证， 获取邮箱验证码，并通过验证
            html = etree.HTML(self.browser.page_source)
            email_addr = html.xpath('//*[contains(text(),"@")]/text()')[0].replace("邮箱：", "").strip()
            email_address = acc_hkey.split(":")[2]
            # 判断邮箱是否正确， 不正确则判定账号失效
            if email_addr[0] == email_address[0] and email_addr[-1] == email_address[-1] and \
                    email_addr.split("@")[-1][0] == email_address.split("@")[-1][0]:
                try:
                    self.email_verify(acc_hkey)
                    time.sleep(5)
                    for cookie_ in self.browser.get_cookies():
                        cookie_str += cookie_["name"] + "=" + cookie_["value"] + "; "
                    cookie_info["cookie"] = cookie_str
                    self.set_cookie(acc_hkey, cookie_info)
                except: # 邮箱验证失败移入失败账号队列
                    self.set_fail_cookie(acc_hkey, cookie_info, message)
            else:
                self.set_fail_cookie(acc_hkey, cookie_info, message)
        elif message == "账号被封" or message == "手机验证":  # 账号被封或弹出绑定手机号判定为账号死号
            self.set_fail_cookie(acc_hkey, cookie_info, message)

        elif message == "二次验证":  # 二次验证存入谷歌验证队列
            client.hset("instagram_google_verify_fail", acc_hkey, "2fa验证")

        logger.info(f"登录完成后cookie: {acc_hkey}")
        time.sleep(5)

    def instagram_register(self, acc_hkey, cookie):
        try:
            self.create_browser()
            self.browser.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(3)
            email_address = acc_hkey.split(":")[0]
            email_password = acc_hkey.split(":")[1]
            account = email_address.split("@")[0] + str(random.randint(10000, 100000))
            password = email_password + "123"
            acc_hkeys = email_address + ":" + email_password + ":" + acc_hkey
            self.input_text('//input[@name="emailOrPhone"]', email_address)
            self.input_text('//input[@name="fullName"]', email_address.split("@")[0])
            self.input_text('//input[@name="username"]', account)
            self.input_text('//input[@name="password"]', password)
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()
            time.sleep(1)
            # 填写生日
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//span[@class="_aav3"][1]/select/option[@value="{str(random.randint(1,12))}"]'))).click()
            time.sleep(1)
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//span[@class="_aav3"][2]/select/option[@value="{str(random.randint(1,28))}"]'))).click()
            time.sleep(1)
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//span[@class="_aav3"][3]/select/option[@value="{str(random.randint(1970,2005))}"]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f'//button[@class=" _acan _acap _acaq _acas _aj1- _ap30"]'))).click()
            time.sleep(15)
            try:
                self.google_verify()
            except:
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f'//button[@class=" _acan _acap _acaq _acas _aj1- _ap30"]'))).click()
            time.sleep(20)
            email_verify_code = self.get_email_verify_code(acc_hkeys)
            self.input_text('//input[@name="email_confirmation_code"]', email_verify_code)
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f'//form[@method="POST"]/div/div/div[@role="button"]'))).click()
            time.sleep(30)
            client.hdel(config.acc_pw_hash, acc_hkey) # 删除账号密码队列邮箱账号，避免重复注册
            self.account_judge(acc_hkeys, cookie)
        except:
            logger.error("error: " + traceback.format_exc())
        self.browser.close()


    def run(self):
        acc_hkey, cookie = self.get_account()
        # acc_hkey, cookie = "camilaq6ph@gmx.com:Si5KSYCc50", {}
        if acc_hkey == "":
            logger.info("暂无token验证")
            return
        proxy = random.choice(["10.11.203.70:50002", "10.11.203.70:50025", "10.11.203.70:50014", "10.11.203.70:50005", "10.11.203.70:50023", "10.11.203.70:50028"])
        ua = cookie.get("user-agent", 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36')
        self.proxy = "http://" + proxy
        self.ua = ua
        logger.info(f"account: {acc_hkey}, proxy: {self.proxy}")
        if len(acc_hkey.split(":")) > 3:
            self.instagram_login(acc_hkey, cookie)
        # else:
        #     self.instagram_register(acc_hkey, cookie)



if __name__ == '__main__':
    num = 0
    while True:
        num += 1
        logger.info(f"第{str(num)}次循环")
        try:
            # ali_slider = AliexpressSlider(True)
            ali_slider = AliexpressSlider(False)
            ali_slider.run()
        except:
            logger.error(traceback.format_exc())
        time.sleep(30)

