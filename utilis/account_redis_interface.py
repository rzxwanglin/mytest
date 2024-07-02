import config
from config import data_redis_client


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
        self.client =data_redis_client

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
        return cookie


