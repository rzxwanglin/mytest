#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/13 19:33
# @Author  : h1code2
# @File    : template.py
# @Software: PyCharm
import json
from urllib.parse import quote


class Template:

    @classmethod
    def template(cls):
        return {
            "liked": cls.liked_template(),
            "comment": cls.comment_template(),
            "post": cls.post_template(),
            "post_id": cls.post_id_template(),
            "user": cls.user_template(),
            "search": cls.search_template(),
            "follower": cls.follower_template(),
            "following": cls.following_template(),
            "hashtag": cls.hashtag_template(),
        }

    @classmethod
    def user_template(cls):
        return {
            "url": "https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}",
            "method": "GET",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'X-IG-App-ID': "936619743392459",
            },
        }

    @classmethod
    def post_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query/?doc_id=7571407972945935&variables={variables}",
            "method": "GET",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                # 'cookie': 'csrftoken={csrftoken}; mid=Zi2-pwALAAHLkpaZ8ZIKFKzIHGvK; ig_did=5EFB8B7F-54BF-4F88-AF86-D36A42AADE21; datr=p74tZpW_csvoDHFt4WF7WA_K; ps_n=1; ps_l=1; ig_nrcb=1; sessionid=63305878724%3ARMdu8FFCqYV8CD%3A21%3AAYe8mN8rO16HaOUSFsJwv5kUxtCQXyHicOc-LCHphRA; ds_user_id=63305878724;',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            },
        }

    @classmethod
    def post_id_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query",
            "method": "POST",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                # 'cookie': 'sessionid=65919192456%3ANdhFi0Igl4LtpM%3A13%3AAYeJJl0ZpJCVd5Q1c5-GA2e_JTbqNV1ubS_Elgr8tw',
                'dpr': '1',
                'origin': 'https://www.instagram.com',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com/',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'viewport-width': '979',
                # 'x-csrftoken': tok,
                # 'x-fb-lsd': lsd,
                'x-ig-app-id': '936619743392459'
            },
            "body": 'av=0&__d=www&__user=0&__a=1&__req=3&__hs=19860.HYP%3Ainstagram_web_pkg.2.1..0.0&dpr=1&__ccg=UNKNOWN&__rev=1013574538&__s=04k3vo%3A7dkurp%3Aiv0rv7&__hsi=7369806182333827548&__dyn=7xeUjG1mxu1syUbFp40NonwgU7SbzEdF8aUco2qwJw5ux609vCwjE1xoswaq0yE7i0n24oaEd86a3a1YwBgao6C0Mo2iyo2Ixe0EUjwGzEaE7622362W2K0zK5o4q3y1Sx-0iS2Sq2-azo7u1xwIw8O321LwTwKG1pg2Xwr86C1mwrd6goK68jxe6V89F8uxK3OqcyU-u&__csr=gV1vd6R8JNbdQJOnKHqaqFaX-FWGtGJAqqAAmAirWGHLCxO8yuEzihGAGEx7AAhQQVybHgGdxmnFlKWHAyGyWizeqVQqeiCzbAUDAGujz-umaBGbybzd1eaBgCuaBAUGFWDypaHxS26KUy00kx_w3pkEhg-jw2pk0N200M8x51mzk2C1nDDgAk0wE6J1G0edwfd06sim34i10wdC5U0g5wHw9et2H801_Ew1ci&__comet_req=7'
                    '&lsd={lsd}&jazoest=2880&__spin_r=1013574538&__spin_b=trunk&__spin_t=1715916717&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisPostActionLoadPostQueryQuery'
                    '&variables=%7B%22shortcode%22%3A%22{post_id}%22%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22child_comment_count%22%3A3%2C%22fetch_like_count%22%3A10%2C%22fetch_tagged_user_count%22%3Anull%2C%22fetch_preview_comment_count%22%3A2%2C%22has_threaded_comments%22%3Atrue%2C%22hoisted_comment_id%22%3Anull%2C%22hoisted_reply_id%22%3Anull%7D&server_timestamps=true&doc_id=24852649951017035'
        }

    @classmethod
    def search_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query/?query_hash=90cba7a4c91000cf16207e4f3bee2fa2&variables={variables}",
            "method": "GET",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            },
        }

    @classmethod
    def follower_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={variables}",
            "method": "GET",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            },
        }

    @classmethod
    def following_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={variables}",
            "method": "GET",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            },
        }

    @classmethod
    def hashtag_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query/?query_hash=e6306cc3dbe69d6a82ef8b5f8654c50b&variables={variables}",
            "method": "GET",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            },
        }

    @classmethod
    def liked_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query",
            "method": "POST",
            "headers": {
                'Connection': 'keep-alive',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                # 'cookie': 'sessionid=65919192456%3ANdhFi0Igl4LtpM%3A13%3AAYeJJl0ZpJCVd5Q1c5-GA2e_JTbqNV1ubS_Elgr8tw',
                'dpr': '1',
                'origin': 'https://www.instagram.com',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com/',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'viewport-width': '979',
                # 'x-csrftoken': tok,
                # 'x-fb-lsd': lsd,
                'x-ig-app-id': '936619743392459'
            },
            "body": 'av=17841463321743234&__d=www&__user=0&__a=1&__req=b8&__hs=19825.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1012724415&__s=gaj2vf%3Aw8viol%3Aw9hvty&__hsi=7356794386340420816&__dyn=7xeUjG1mxu1syUbFp40NonwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awt81s8hwGwQwoEcE7O2l0Fwqo31w9a9waO4U2zxe2GewGwso88cobEaU2eUlwhEe87q7U1bobpEbUGdwtU662O0z8c86-3u2WE5B0bK1Iwqo5q1IQp1yUoxeubxKi2qi9xi6U4e&__csr=glMrYAhkl12D4cQgyRYBbsHQnb9QYIZEx5y12pDOFd4JqjUGoyDybZqit4UyjgylaJ5jGKy2AXmfJamFd4iDGpAzkiFeQKUZ12US8WKp6gV2KexxemaBKmLUoUyExdotDrwu801g-62l03D85y1VP08e8wlU2cy80creTafg4QMocFQaP0cV0822i4o1JE12pYwO0DU2wwfR09u4EkP02eG80Ae0liaP3A0KES0m6cw0v780h2w&__comet_req=7&fb_dtsg=NAcN8Dc57gaS6RABySjJO2ZpUJIXVbk1mhTGFjB4cBOja3RyCp0uXdg%3A17843729647189359%3A1709207676&jazoest=26124' \
                    '&lsd={lsd}&__spin_r=1012724415&__spin_b=trunk&__spin_t=1712887171&qpl_active_flow_ids=1056839232&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisPostLikedByListDialogQuery' \
                    '&variables=%7B%22id%22%3A%22{post_id}%22%7D&server_timestamps=true&doc_id=7687108631341096'
        }

    @classmethod
    def comment_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query",
            "method": "POST",
            "headers": {
                'Connection': 'keep-alive',
                'dpr': '1',
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com/p/{seed}/',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.37',
                'viewport-width': '782',
                # 'x-fb-lsd': lsd,
            },
            "body": 'av=0&__d=www&__user=0&__a=1&__req=3&__hs=19823.HYP%3Ainstagram_web_pkg.2.1..0.0&dpr=1&__ccg=UNKNOWN&__rev=1012669602&__s=y3hblh%3A18tdeb%3Ao8rwco&__hsi=7356110657869292677&__dyn=7xeUjG1mxu1syUbFp40NonwgU29zEdF8aUco2qwJw5ux609vCwjE1xoswaq0yE7i0n24oaEd86a3a1YwBgao6C0Mo2iyo2Ixe0EUjwGzEaE7622362W2K0zK5o4q3y1Sx-0iS2Sq2-azo7u1xwIwbS1LwTwKG1pg2Xwr86C1mwrd6goK68jxe6V89F8uxK&__csr=j84Qeq2mAKyimJlPFLnhAZkWlf-J6ihLja4agycgiDiBAVUJaaxPVoy8qiDiKE-umWKENdpayubhqyK464ZpkVuSdxmaFAhuh1HzFqKUS-u4UWuFk4Xx2uqpebwgEyew053HBovCw11epi0ww5Kxi035yOS1lwFqVQaEE9o7m390uQ2y0c2w2Wj389k04wsU1KV807Se045U&__comet_req=7' \
                    '&lsd={lsd}&jazoest=2980&__spin_r=1012669602&__spin_b=trunk&__spin_t=1712727979&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisPostActionLoadPostQueryQuery' \
                    '&variables=%7B%22shortcode%22%3A%22{shortcode}%22%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22child_comment_count%22%3A3%2C%22fetch_like_count%22%3A10%2C%22fetch_tagged_user_count%22%3Anull%2C%22fetch_preview_comment_count%22%3A2%2C%22has_threaded_comments%22%3Atrue%2C%22hoisted_comment_id%22%3Anull%2C%22hoisted_reply_id%22%3Anull%7D&server_timestamps=true&doc_id=24852649951017035'
        }


if __name__ == '__main__':
    pass
