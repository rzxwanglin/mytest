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
            "click_inter": cls.click_inter(),
            "like_inter": cls.liked_inter(),
            "comment_inter": cls.comment_inter()
        }

    @classmethod
    def user_template(cls):
        return {
            "url": "https://www.instagram.com/api/v1/users/web_profile_info/?username=",
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
                'Cookie': ''
            },
        }

    @classmethod
    def post_template(cls):
        return {
            "url": "https://www.instagram.com/graphql/query",
            "method": "POST",
            "headers": {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'sec-ch-ua-model': '""',
                'x-ig-app-id': '936619743392459',
                'sec-ch-ua-mobile': '?0',
                'x-bloks-version-id': '213c82555f99bb0cecb045c627a22f08209d7a699fc238c7e73a0482e70267f9',
                'x-fb-lsd': '6UrRZwaUXr24urfM08N1Zb',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'x-fb-friendly-name': 'PolarisProfilePostsTabContentDirectQuery_connection',
                'x-asbd-id': '129477',
                'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"',
                'sec-ch-prefers-color-scheme': 'light',
                'X-Csrftoken': '14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL',
                'sec-ch-ua-platform': '"Windows"',
                'origin': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.instagram.com/leomessi/',
                'accept-language': 'zh-CN,zh;q=0.9',
                'priority': 'u=1, i',
                'Cookie': 'mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL; ds_user_id=66881971457; shbid="3441\\05466881971457\\0541752544811:01f7a6c74b853375ad25c9e687be530eec06197f673ca3d78e4bddb3ca8d0b14fffa4eb1"; shbts="1721008811\\05466881971457\\0541752544811:01f74ea4bd4f2d3c92b4b3cf8fb860d26c641fd7096946e9efe64481a3fab7351a7fc475"; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYfuOxpOKttsAb5y03fQEpsehxGDNDNEPSwM0eS8Iaw; wd=1224x675; rur="CCO\\05466881971457\\0541752732472:01f7909d08d1f1d8a827220c9fc20a5f4e5f038bc6aa285dc522dc04916ac4f44a034a13"; csrftoken=NcpnPEpVnHl4lU0VdfF3r7GaYbLSgJxe; ds_user_id=66881971457; ig_did=4A4975E2-6FB1-49DE-964C-364FFEBBAAB6; ig_nrcb=1; mid=ZmpVpQALAAHbZz7Di09C11gTIg8a; rur="CCO\\05466881971457\\0541752804738:01f7ea21cb6afca72448b6a93f1ca5cdc7efaf8b564f8dc42673c78c3c036467a798d5a9"; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYcLBFHeW22Bq9T3yMuwnlxMy1dc2YIL8OxJ02s-vu4; shbid="3441\\05466881971457\\0541752737312:01f7ad0e6b8709af249bb17e3ddd71875e2520dce922ec14f5e525c7c1a463268822f50d"; shbts="1721201312\\05466881971457\\0541752737312:01f74f45c18eab648167a3192e8c95a97778b8ef861b5c7d19e754ab61ed75242b394acc"'
            },
            "body": {
                "av": "17841466823730246",
                "__d": "www",
                "__user": "0",
                "__a": "1",
                "__req": "t",
                "__hs": "19921.HYP:instagram_web_pkg.2.1..0.1",
                "dpr": "1",
                "__ccg": "UNKNOWN",
                "__rev": "1014938391",
                "__s": "qocp3g:epr8y9:6767kz",
                "__hsi": "7392482544959070897",
                "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEnxO1ywOwv89k2C1Fwc60D87u3ifK0EUjwGzEaE2iwNwKwHw8Xxm16wUwtEvw4JwJCwLyES1TwTU9UaQ0Lo6-3u2WE5B08-269wr86C1mwPwUQp1yUb9UK6V89F8uxK3OqcxK2K",
                "__csr": "gjR1D5PPOgxkQAciFZYjkYT4WtideHetlaCy-OVfBHunVJoxvKWh9biAF9rAiAK_h5FquV5y9pii6Q8l5yLjyVpp-mi8GqmQGVEC49qKqVVG-EyqtfD-cBG48gGVUhB8FWGFUy9Bx2iFKu6WCWzFoCFU_g01mP8O5A7o8Ha7E3bwjp4U5Gut0erw3W80qswli0NqyA84Pe2l0EVVQy4y40E8gwAgd80I60EpNcF89k2x5sUswzBxq2505Zwtoqe1UweR0WU0z1068w-e2l0xw09oK",
                "__comet_req": "7",
                "fb_dtsg": "NAcO2XG2d1pE_m2pnQkpVDiDYN2f9QkPlSSaw_pQo0DKQm18o26TS8w:17843696212148243:1719912508",
                "jazoest": "26115",
                "lsd": "6UrRZwaUXr24urfM08N1Zb",
                "__spin_r": "1014938391",
                "__spin_b": "trunk",
                "__spin_t": "1721196469",
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "PolarisProfilePostsTabContentDirectQuery_connection",
                "variables": '{"after":null,"before":null,"data":{"count":10,"include_relationship_info":true,"latest_besties_reel_media":true,"latest_reel_media":true},"first":10,"last":null,"username":"{username}","__relay_internal__pv__PolarisFeedShareMenurelayprovider":false}',
                "server_timestamps": "true",
                "doc_id": "7962794617130896"
            }
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
                 'x-csrftoken': 'tok',
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
                'cookie': 'mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; shbid="3441\05466881971457\0541752820702:01f7305537ca37ee6ffb0ed0d96d35a71355631dff8d7036c05c3576c465ab9b1a4b9817"; shbts="1721284702\05466881971457\0541752820702:01f76319f9e89e7168f409bbe26d6f1fa0dbf46c1a12889dec1a4ae74e78226f6c0326b0"; ds_user_id=67554144179; csrftoken=9Jz2OAPTgBcLUoApxh9NbT70fuFEWUvg; sessionid=67554144179%3AMcVbWHHEnnPTkE%3A26%3AAYdT03HyIMkhfXEEwIZNO88gyv2XoP3V8ZC0OCZLfA; wd=1920x919; rur="NHA\05467554144179\0541752827062:01f7a59817276ee277778b58425dccde91094bca7d27614e7dd5bce88063dea60e1c111d"',
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
                'cookie':'mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; shbid="3441\05466881971457\0541752820702:01f7305537ca37ee6ffb0ed0d96d35a71355631dff8d7036c05c3576c465ab9b1a4b9817"; shbts="1721284702\05466881971457\0541752820702:01f76319f9e89e7168f409bbe26d6f1fa0dbf46c1a12889dec1a4ae74e78226f6c0326b0"; ds_user_id=67554144179; csrftoken=9Jz2OAPTgBcLUoApxh9NbT70fuFEWUvg; sessionid=67554144179%3AMcVbWHHEnnPTkE%3A26%3AAYdT03HyIMkhfXEEwIZNO88gyv2XoP3V8ZC0OCZLfA; wd=1920x919; rur="NHA\05467554144179\0541752827062:01f7a59817276ee277778b58425dccde91094bca7d27614e7dd5bce88063dea60e1c111d"',
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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'sec-ch-ua-model': '""',
                'x-ig-app-id': '936619743392459',
                'sec-ch-ua-mobile': '?0',
                'x-bloks-version-id': '213c82555f99bb0cecb045c627a22f08209d7a699fc238c7e73a0482e70267f9',
                'x-fb-lsd': '6UrRZwaUXr24urfM08N1Zb',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'x-fb-friendly-name': 'PolarisProfilePostsTabContentDirectQuery_connection',
                'x-asbd-id': '129477',
                'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"',
                'sec-ch-prefers-color-scheme': 'light',
                'X-Csrftoken': '14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL',
                'sec-ch-ua-platform': '"Windows"',
                'origin': 'https://www.instagram.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.instagram.com/leomessi/',
                'accept-language': 'zh-CN,zh;q=0.9',
                'priority': 'u=1, i',
                'Cookie': 'mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL; ds_user_id=66881971457; shbid="3441\\05466881971457\\0541752544811:01f7a6c74b853375ad25c9e687be530eec06197f673ca3d78e4bddb3ca8d0b14fffa4eb1"; shbts="1721008811\\05466881971457\\0541752544811:01f74ea4bd4f2d3c92b4b3cf8fb860d26c641fd7096946e9efe64481a3fab7351a7fc475"; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYfuOxpOKttsAb5y03fQEpsehxGDNDNEPSwM0eS8Iaw; wd=1224x675; rur="CCO\\05466881971457\\0541752732472:01f7909d08d1f1d8a827220c9fc20a5f4e5f038bc6aa285dc522dc04916ac4f44a034a13"; csrftoken=NcpnPEpVnHl4lU0VdfF3r7GaYbLSgJxe; ds_user_id=66881971457; ig_did=4A4975E2-6FB1-49DE-964C-364FFEBBAAB6; ig_nrcb=1; mid=ZmpVpQALAAHbZz7Di09C11gTIg8a; rur="CCO\\05466881971457\\0541752804738:01f7ea21cb6afca72448b6a93f1ca5cdc7efaf8b564f8dc42673c78c3c036467a798d5a9"; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYcLBFHeW22Bq9T3yMuwnlxMy1dc2YIL8OxJ02s-vu4; shbid="3441\\05466881971457\\0541752737312:01f7ad0e6b8709af249bb17e3ddd71875e2520dce922ec14f5e525c7c1a463268822f50d"; shbts="1721201312\\05466881971457\\0541752737312:01f74f45c18eab648167a3192e8c95a97778b8ef861b5c7d19e754ab61ed75242b394acc"'
            },
            "body": {
                "av": "17841466823730246",
                "__d": "www",
                "__user": "0",
                "__a": "1",
                "__req": "u",
                "__hs": "19921.HYP:instagram_web_pkg.2.1..0.1",
                "dpr": "1",
                "__ccg": "UNKNOWN",
                "__rev": "1014938391",
                "__s": "r2rs8i:vxq40u:fzi2zl",
                "__hsi": "7392485916952636128",
                "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEnxO1ywOwv89k2C1Fwc60D87u3ifK0EUjwGzEaE2iwNwKwHw8Xxm16wUwtEvw4JwJCwLyES1TwTU9UaQ0Lo6-3u2WE5B08-269wr86C1mwPwUQp1yUb9UK6V89F8uxK3OqcxK2K",
                "__csr": "gjM8kYYaRd934GvsQBjPtjqtideHetlaCy-PA-mJV-rgGLKWh8xaiABKhaiXt4mBFXAm8BB98rgxkmaZebBBDVpeqFFriHCyogBGVHDCHWy9FQ-vUOmEgx3jDx548FWGFUy9Bx2iFKu6WCWzFoCFU_jw05qowLz8mghyU8Ha7E3bwjp4U5Gut0erw3W80qswli0NqyA823wBgaeut8x8x0a248943i0b1wa6sjai2l0Ehne788Vomwxg1vo7m6zwu83JgeK08Mg1y8fzwBg8o02mbw",
                "__comet_req": "7",
                "fb_dtsg": "NAcPGrqwV3upgiFmFkDGVUyPzMD1M247cSnNxrwtfTxOx_fk_dB9IPg:17843696212148243:1719912508",
                "jazoest": "26478",
                "lsd": "8LMJiqLdeuTsnc6q8pM2cm",
                "__spin_r": "1014938391",
                "__spin_b": "trunk",
                "__spin_t": "1721197254",
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "PolarisPostCommentsPaginationDirectQuery",
                # cached_comments_cursor 游标 media_id帖子 pk id
                "variables": '{"after":"{"cached_comments_cursor": "", "bifilter_token": "KHkAZGGnvpcfQADFrUyQxixAAObkgDsr-j8AR_tbhnwrQADIUFEwWANAAOfpP4sGM0AASmOH69KwPwCo4bOxGo8_AK8AEJ2Y8z8A9_PT3UaFQQCVZISc_3Q_ABe1zZjiEkAAu9yFCW82QADeR8VPBwlAAH-T-VAxiD8AAA=="}","before":null,"first":10,"last":null,"media_id":"{media_id}","sort_order":"popular"}',
                "server_timestamps": "true",
                "doc_id": "8059165620761059"
            }

        }

    @classmethod
    def liked_inter(cls):
        return {
            "url": "https://www.instagram.com/graphql/query",
            "method": "POST",
            "headers": {
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Length": "1060",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "{cookie}",
                # "Cookie": "mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; wd=1020x604; csrftoken=wizJUqALLHashqTLJ4WjiP5O19Ay36O1; ds_user_id=67045065874; sessionid=67045065874%3AjuyYemzRhN7wXJ%3A11%3AAYcA63mwgzpf4kJ1FEqG4pgIJWEEEdkf7DQ7wbiwOw; shbid=\"16705\05467045065874\0541750759582:01f7162f81b050377930728836f1052b37975aed09acb9e66cd12d7aea9cffc4746e290a\"; shbts=\"1719223582\05467045065874\0541750759582:01f7e7a7cc10426915aeb8b07a877037b261789f55b55d41f8d6bf31352444df7c2457bb\"; rur=\"PRN\05467045065874\0541750759619:01f7bf54191315a40b15c564525a7148b3e23f0a28a574faacb0ee262ea7b66c267995bd\"",
                "Origin": "https://www.instagram.com",
                "Priority": "u=1, i",
                "Referer": "https://www.instagram.com/",
                "Sec-Ch-Prefers-Color-Scheme": "light",
                "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
                "Sec-Ch-Ua-Full-Version-List": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.114\", \"Google Chrome\";v=\"126.0.6478.114\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Model": "\"\"",
                "Sec-Ch-Ua-Platform": "\"Windows\"",
                "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "{user-agent}",
                "X-Asbd-Id": "129477",
                "X-Bloks-Version-Id": "213e4f338be29ab2c08f8071c4feb979c6b2fe37d4124f56e5c4b00e51a21aaf",
                "X-Csrftoken": "{csrf_token}",
                "X-Fb-Friendly-Name": "usePolarisLikeMediaLikeMutation",
                "X-Fb-Lsd": "zRjTA0fjlIwgmiCC2Y0ip0",
                "X-Ig-App-Id": "936619743392459"
            },
            "body": {
                "av": "17841467016230633",
                "__d": "www",
                "__user": "0",
                "__a": "1",
                "__req": "x",
                "__hs": "19898.HYP:instagram_web_pkg.2.1..0.1",
                "dpr": "1",
                "__ccg": "UNKNOWN",
                "__rev": "1014422660",
                "__s": "s5v8mi:3c820x:jimn0s",
                "__hsi": "7384009069877920886",
                "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEnxO1ywOwv89k2C1Fwc60AEC1TwQzXwae4UaEW2G0AEcobEaU2eUlwhEe87q7U1bobpEbUGdwtUeo9UaQ0Lo6-3u2WE5B08-269wr86C1mwPwUQp1yUb9UK6V89F8C58rwYCz8KfwHw",
                "__csr": "gjl1f4Og_6hnkQIn5Z9mDa_8lksO9bRlV2r8h4jJi3KqGGK_ymiAXHgKXGmyqHBZFlF5izeil7GtkKiQqRGq6Qh6Bzuuu9GQUhBF3ohyWBDB-FEjV99UK54mmdgyUB3EixKGKU01iEF404JUW5rw_wjFQaBo721rx210Bo0j_w1M2yz9-9xkEG2F0kcit8G4xzzA0K47S1sw2D82Xw29UG0GEkP05wge85fw2YQ0K8gxS00Ajo",
                "__comet_req": "7",
                "fb_dtsg": "NAcO2rlejkPZgWnpP-eC3L1BPWCuCTsKKUZLRxdSgPFBwMF3A0Kom7Q:17864970403026470:1719223576",
                "jazoest": "26130",
                "lsd": "zRjTA0fjlIwgmiCC2Y0ip0",
                "__spin_r": "1014422660",
                "__spin_b": "trunk",
                "__spin_t": "1719223584",
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "usePolarisLikeMediaLikeMutation",
                "variables": "{\"media_id\":\"{media_id}\"}",
                # 3393245210130807279  3397561855460766739 视频id instagram://media?id=3397561855460766739
                "server_timestamps": "true",
                "doc_id": "8244673538908708"
            }
        }

    @classmethod
    def comment_inter(cls):
        return {
            "url": "https://www.instagram.com/api/v1/web/comments/{media_id}/add/",
            "method": "POST",
            "headers": {
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Length": "1060",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "{cookie}",
                # "Cookie": "mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; wd=1020x604; csrftoken=wizJUqALLHashqTLJ4WjiP5O19Ay36O1; ds_user_id=67045065874; sessionid=67045065874%3AjuyYemzRhN7wXJ%3A11%3AAYcA63mwgzpf4kJ1FEqG4pgIJWEEEdkf7DQ7wbiwOw; shbid=\"16705\05467045065874\0541750759582:01f7162f81b050377930728836f1052b37975aed09acb9e66cd12d7aea9cffc4746e290a\"; shbts=\"1719223582\05467045065874\0541750759582:01f7e7a7cc10426915aeb8b07a877037b261789f55b55d41f8d6bf31352444df7c2457bb\"; rur=\"PRN\05467045065874\0541750759619:01f7bf54191315a40b15c564525a7148b3e23f0a28a574faacb0ee262ea7b66c267995bd\"",
                "Origin": "https://www.instagram.com",
                "Priority": "u=1, i",
                "Referer": "https://www.instagram.com/",
                "Sec-Ch-Prefers-Color-Scheme": "light",
                "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
                "Sec-Ch-Ua-Full-Version-List": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.114\", \"Google Chrome\";v=\"126.0.6478.114\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Model": "\"\"",
                "Sec-Ch-Ua-Platform": "\"Windows\"",
                "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "{user-agent}",
                "X-Asbd-Id": "129477",
                "X-Bloks-Version-Id": "213e4f338be29ab2c08f8071c4feb979c6b2fe37d4124f56e5c4b00e51a21aaf",
                "X-Csrftoken": "{csrf_token}",
                "X-Fb-Friendly-Name": "usePolarisLikeMediaLikeMutation",
                "X-Fb-Lsd": "zRjTA0fjlIwgmiCC2Y0ip0",
                "X-Ig-App-Id": "936619743392459"
            },
            "body": {
                "comment_text": "{text}"
            }
        }

    @classmethod
    def click_inter(cls):
        return {
            "url": "https://www.instagram.com/api/v1/friendships/create/{user_id}/",
            "method": "POST",
            "headers": {
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Length": "1060",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": "{cookie}",
                # "Cookie": "mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; wd=1020x604; csrftoken=wizJUqALLHashqTLJ4WjiP5O19Ay36O1; ds_user_id=67045065874; sessionid=67045065874%3AjuyYemzRhN7wXJ%3A11%3AAYcA63mwgzpf4kJ1FEqG4pgIJWEEEdkf7DQ7wbiwOw; shbid=\"16705\05467045065874\0541750759582:01f7162f81b050377930728836f1052b37975aed09acb9e66cd12d7aea9cffc4746e290a\"; shbts=\"1719223582\05467045065874\0541750759582:01f7e7a7cc10426915aeb8b07a877037b261789f55b55d41f8d6bf31352444df7c2457bb\"; rur=\"PRN\05467045065874\0541750759619:01f7bf54191315a40b15c564525a7148b3e23f0a28a574faacb0ee262ea7b66c267995bd\"",
                "Origin": "https://www.instagram.com",
                "Priority": "u=1, i",
                "Referer": "https://www.instagram.com/",
                "Sec-Ch-Prefers-Color-Scheme": "light",
                "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
                "Sec-Ch-Ua-Full-Version-List": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.114\", \"Google Chrome\";v=\"126.0.6478.114\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Model": "\"\"",
                "Sec-Ch-Ua-Platform": "\"Windows\"",
                "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "{user-agent}",
                "X-Asbd-Id": "129477",
                "X-Bloks-Version-Id": "213e4f338be29ab2c08f8071c4feb979c6b2fe37d4124f56e5c4b00e51a21aaf",
                "X-Csrftoken": "{csrf_token}",
                "X-Fb-Friendly-Name": "usePolarisLikeMediaLikeMutation",
                "X-Fb-Lsd": "zRjTA0fjlIwgmiCC2Y0ip0",
                "X-Ig-App-Id": "936619743392459"
            },
            "body": {
                "container_module": "feed_timeline",
                "nav_chain": "PolarisFeedRoot:feedPage:3:topnav-link",
                "user_id": '{user_id}'
            }
        }


if __name__ == '__main__':
    pass
