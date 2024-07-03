import random, copy, string, json
from typing import Any
from scrapy import Request, FormRequest
from request_factory.template import Template
from urllib.parse import urlencode, quote
from rhino_v2_utilis.config import ConfigHandler

class RequestFactory:
    """
    请求对象制造机
    """
    base_url = "https://api.bnnapp.com/__proxy_host/api.ok.ru/api/batch/executeV2"

    @classmethod
    def make_request(cls, task_info: dict, spider_self: Any, seed: str, task: str, meta: dict, **kwargs):
        request = cls.factory().get(task)(task_info, task, seed, meta, spider_self, **kwargs)
        return request

    @classmethod
    def factory(cls):
        return {
            "user": cls.make_user_request,
            "post": cls.make_post_request,
            "post_id": cls.make_post_id_request,
            "search": cls.make_search_request,
            "follower": cls.make_follower_request,
            "following": cls.make_following_request,
            "hashtag": cls.make_hashtag_request,
            "liked": cls.make_liked_request,
            "comment": cls.make_comment_request,
            "like_inter":cls.make_request_like_inter,
            "comment_inter":cls.make_request_comment_inter,
            "click_inter":cls.make_request_click_inter,
        }

    @classmethod
    def make_user_request(cls, task_info: dict, task: any, user_name: string, meta: dict, spider_self: Any):
        req_info = copy.deepcopy(Template.template().get(task))
        req_info["url"] = req_info["url"].format(**{"user_name": user_name})
        return Request(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def make_post_request(cls, task_info: dict, task: any, user_id: string, meta: dict, spider_self: Any):
        req_info = copy.deepcopy(Template.template().get(task))
        variables = '{"id":"' + user_id + '","include_clips_attribution_info":false,"first":50}'
        if task_info.get("sub_page", 1) > 1:
            after = task_info.get("sub_end_cursor")
            variables = '{"id":"' + user_id + '","include_clips_attribution_info":false,"first":50,"after":"' + after + '"}'
        req_info["url"] = req_info["url"].format(**{"variables": quote(variables)})
        return Request(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def make_post_id_request(cls, task_info: dict, task: any, post_id: string, meta: dict, spider_self: Any):
        req_info = copy.deepcopy(Template.template().get(task))
        lsd = cls.get_lsd()
        csrftoken = cls.get_csrftoken()
        req_info["body"] = req_info["body"].format(**{
            "lsd": lsd,
            "post_id": post_id
        })
        req_info["headers"]["x-csrftoken"] = csrftoken
        req_info["headers"]["x-fb-lsd"] = lsd
        return FormRequest(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def make_search_request(cls, task_info: dict, task: any, keyword: string, meta: dict, spider_self: Any):
        lsd = cls.get_lsd()
        csrftoken = cls.get_csrftoken()
        req_info = copy.deepcopy(Template.template().get(task))
        req_info["url"] = "https://www.instagram.com/api/v1/tags/web_info/?tag_name=" + keyword
        after = task_info.get("sub_end_cursor")
        if task_info.get("sub_page", 1) > 1:
            variables = '{"tag_name":"' + keyword + '","first":50,"after":"' + after + '"}'
            req_info["url"] = "https://www.instagram.com/graphql/query/?query_hash=90cba7a4c91000cf16207e4f3bee2fa2&variables=" + quote(variables)
        req_info["headers"]["x-fb-lsd"] = lsd
        req_info["headers"]["X-IG-App-ID"] = "936619743392459"
        req_info["headers"]["x-csrftoken"] = csrftoken
        return Request(
            dont_filter=True,
            meta=meta,
            **req_info
        )


    @classmethod
    def make_follower_request(cls, task_info: dict, task: any, user_id: string, meta: dict, spider_self: Any):
        lsd = cls.get_lsd()
        req_info = copy.deepcopy(Template.template().get(task))
        after = task_info.get("sub_end_cursor")
        variables = '{"include_reel":false,"fetch_mutual":true,"first":50,"id":"' + user_id + '"}'
        if task_info.get("sub_page", 1) > 1:
            variables = '{"include_reel":false,"fetch_mutual":true,"first":50,"id":"' + user_id + '","after":"' + after + '"}'
        req_info["url"] = req_info["url"].format(**{"variables": quote(variables)})
        req_info["headers"]["x-fb-lsd"] = lsd
        return Request(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def make_following_request(cls, task_info: dict, task: any, user_id: string, meta: dict, spider_self: Any):
        lsd = cls.get_lsd()
        req_info = copy.deepcopy(Template.template().get(task))
        after = task_info.get("sub_end_cursor")
        variables = '{"include_reel":false,"fetch_mutual":true,"first":50,"id":"' + user_id + '"}'
        if task_info.get("sub_page", 1) > 1:
            variables = '{"include_reel":false,"fetch_mutual":true,"first":50,"id":"' + user_id + '","after":"' + after + '"}'
        req_info["url"] = req_info["url"].format(**{"variables": quote(variables)})
        req_info["headers"]["x-fb-lsd"] = lsd
        return Request(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def make_hashtag_request(cls, task_info: dict, task: any, user_id: string, meta: dict, spider_self: Any):
        lsd = cls.get_lsd()
        req_info = copy.deepcopy(Template.template().get(task))
        variables = '{"id":"' + user_id + '"}'
        req_info["url"] = req_info["url"].format(**{"variables": quote(variables)})
        req_info["headers"]["x-fb-lsd"] = lsd
        return Request(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def make_liked_request(cls, task_info: dict, task: any, post_id: string, meta: dict, spider_self: Any):
        req_info = copy.deepcopy(Template.template().get(task))
        lsd = cls.get_lsd()
        csrftoken = cls.get_csrftoken()
        req_info["body"] = req_info["body"].format(**{
            "lsd": lsd,
            "post_id": post_id
        })
        req_info["headers"]["x-csrftoken"] = csrftoken
        req_info["headers"]["x-fb-lsd"] = lsd
        return FormRequest(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def make_comment_request(cls, task_info: dict, task: any, seed: string, meta: dict, spider_self: Any):
        req_info = copy.deepcopy(Template.template().get(task))
        lsd = cls.get_lsd()
        req_info["body"] = req_info["body"].format(**{
            "lsd": lsd,
            "shortcode": seed
        })
        req_info["headers"]["x-fb-lsd"] = lsd
        req_info["headers"]["referer"] = req_info["headers"]["referer"].format(**{"seed":seed})
        meta["dont_merge_cookies"] = True
        return FormRequest(
            dont_filter=True,
            meta=meta,
            **req_info
        )

    @classmethod
    def get_lsd(cls):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(9))

    @classmethod
    def get_csrftoken(cls):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


    @classmethod
    def make_request_like_inter(cls, task, cookie_obj: Any,task_contain):
        req_info = copy.deepcopy(Template.template().get(task))
        req_info["body"]['variables'] = req_info["body"]['variables'].replace("{media_id}",task_contain['media_id'])
        req_info["headers"]["Cookie"] = cookie_obj['cookie']
        req_info["headers"]["User-Agent"] = cookie_obj['user-agent']
        req_info["headers"]["X-Csrftoken"] =cookie_obj['csrf_token']

        return req_info

    @classmethod
    def make_request_comment_inter(cls, task, cookie_obj: Any,task_contain):
        req_info = copy.deepcopy(Template.template().get(task))
        req_info["body"]['comment_text'] = req_info["body"]['comment_text'].replace("{text}", task_contain['text'])
        req_info['url'] = req_info['url'].replace("{media_id}", task_contain['media_id'])
        req_info["headers"]["Cookie"] = cookie_obj['cookie']
        req_info["headers"]["User-Agent"] = cookie_obj['user-agent']
        req_info["headers"]["X-Csrftoken"] = cookie_obj['csrf_token']

        return req_info

    @classmethod
    def make_request_click_inter(cls, task, cookie_obj: Any,task_contain):
        req_info = copy.deepcopy(Template.template().get(task))
        req_info["body"]['user_id'] = req_info["body"]['user_id'].replace("{user_id}", task_contain['user_id'])
        req_info["url"] =req_info["url"].replace("{user_id}", task_contain['user_id'])
        req_info["headers"]["Cookie"] = cookie_obj['cookie']
        req_info["headers"]["User-Agent"] = cookie_obj['user-agent']
        req_info["headers"]["X-Csrftoken"] = cookie_obj['csrf_token']

        return req_info
