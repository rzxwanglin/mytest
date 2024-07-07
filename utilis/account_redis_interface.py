import config
import time
from config import account_redis_client


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class AccountRedisInterface:
    def __init__(self):
        self.client = account_redis_client

    def get_account(self):
        account = self.client.keys(config.login_token_account_hash)
        return account

    def get_cookie(self):
        """
        获取账号，应该用zset source 来维护cookie ，单个账号被调用次数同时不能超过5次，然后休眠10秒
        login_token_account_hash 中注册是，应该往 zset中添加信息跟新信息
        每次获取最下面的账号使用，并且统计次数
        :return:
        """
        cookie = self.client.zpopmin(config.cookie_total_zset)
        if not cookie:
            return None
        acc_hkey = cookie[0][0]
        self.client.zadd(config.cookie_total_zset, {str(acc_hkey): time.time() + 1})
        cookie_obj = self.client.hget(config.cookie_total_hash, str(acc_hkey))

        # 统计 cookie 被获取多次数
        acc_hkey_count = self.client.hget(config.cookie_total_count_hash, acc_hkey)
        if not acc_hkey_count:
            requests_count = 1
        else:
            requests_count = acc_hkey_count.get('requests_count', 0) + 1
        self.client.hset(config.cookie_total_count_hash, acc_hkey_count, {'requests_count': requests_count})
        return cookie_obj


