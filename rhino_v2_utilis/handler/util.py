# -*-coding:utf-8 -*-
"""
# File       : util.py
# Time       ：2023/5/18 15:13
# Author     ：caomengqi
# version    ：python 3.6
# Dec        :  一个常用的工具函数
"""
import json
import socket
from typing import Any
import requests
from loguru import logger
from requests.auth import AuthBase
from urllib3 import disable_warnings

disable_warnings()


def get_hostname():
    """
    获取本机的 hostname
    Returns:
    """
    return socket.gethostname()


def get_private_ip():
    """获取内网IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.gethostname()
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except BaseException as e:
        logger.error(e)
    finally:
        s.close()
    logger.info(f"获取内网ip为{ip}")
    return ip


def get_public_ip():
    """获取公网IP"""
    while True:
        text_urls = [
            "https://ifconfig.me",
            "https://checkip.amazonaws.com",
            "https://ident.me",
            "http://ip.42.pl/raw",
        ]
        json_urls = ["http://httpbin.org/ip", "https://api.ipify.org/?format=json"]
        for json_url in json_urls:
            try:
                res = requests.get(json_url, timeout=2).json()
                internet_ip = res.get("ip") or res.get("origin")
                internet_ip = internet_ip.strip()
                logger.info("get_public_ip ok! {}".format(internet_ip))
                return internet_ip
            except BaseException as e:
                logger.info(f"get public ip from {json_url} raise error:{e}")
        for text_url in text_urls:
            try:
                res = requests.get(text_url, timeout=2).text
                internet_ip = res.strip()
                logger.info("get_public_ip ok! {}".format(internet_ip))
                return internet_ip
            except BaseException as e:
                logger.info(f"get public ip from {text_url} raise error:{e}")


def is_port_open(ip, port):
    """
    判断是否连的通内网,是的话返回True
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)  # TODO 需要在 connect 方法之前 设置timeout
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except Exception as e:
        logger.warning(f"is_port_open raise a {e} error")
    return False


def modify_api_dict(data_dict: dict) -> dict:
    """
    对平台返回的接口进行修改，判断内网是否连的通，是的话使用内网配置
    :param data_dict:
    :return:
    """

    private_ip = data_dict.get("private_ip", None)
    private_port = data_dict.get("private_port", None)
    if is_port_open(private_ip, private_port):
        logger.warning("使用内网配置连接")
        data_dict.update(**{"ip": private_ip, "port": private_port})
    return data_dict


def download_web(
    open_url: str,
    method: str = "GET",
    dict_headers: dict = None,
    dict_params: dict = None,
    data: Any = None,
    dict_proxies: dict = None,
    verify: bool = False,
    auth: AuthBase = None,
    timeout: int = 20,
):
    """
    封装的下载函数
    :param open_url: 网页链接
    :param method: 请求方法
    :param dict_headers: 请求头
    :param dict_params: URL查询参数
    :param data: POST/PUT方法请求的数据
    :param dict_proxies: 代理配置
    :param timeout: 请求超时时间限制
    :param verify: 请求超时时间限制
    :param auth: 请求超时时间限制
    :return: requests.Response
    """
    response = None
    try:
        response = requests.request(
            method=method,
            url=open_url,
            headers=dict_headers,
            params=dict_params,
            data=data,
            proxies=dict_proxies,
            verify=verify,
            timeout=timeout,
            auth=auth,
        )
    except requests.RequestException as base_err:
        logger.error(
            f"Open url exception:[{str(base_err)}]. URL_info [{open_url}(params: {json.dumps(dict_params)})]"
        )
        return response

    if 200 != response.status_code:
        logger.error(
            f"Open url error:[code: {response.status_code}]. "
            f"URL_info [{open_url}(params: {json.dumps(dict_params)})]"
        )
        return response

    return response


# PUBLIC_IP = get_public_ip()
# PRIVATE_IP = get_private_ip()
# print("PUBLIC_IP:", PUBLIC_IP)
# print("PRIVATE_IP:", PRIVATE_IP)
