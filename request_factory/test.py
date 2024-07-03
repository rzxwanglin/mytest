import requests
import json

proxy ={
   'http':'http://127.0.0.1:8800',
    'https':'http://127.0.0.1:8800'
}
def dz(Cookie_obj):
    # dianzam
    # Define the URL
    url = "https://www.instagram.com/graphql/query"
    print(Cookie_obj['cookie'])
    # Define the headers
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "1060",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie":str(Cookie_obj['cookie']),
        #"Cookie": "mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; wd=1020x604; csrftoken=wizJUqALLHashqTLJ4WjiP5O19Ay36O1; ds_user_id=67045065874; sessionid=67045065874%3AjuyYemzRhN7wXJ%3A11%3AAYcA63mwgzpf4kJ1FEqG4pgIJWEEEdkf7DQ7wbiwOw; shbid=\"16705\05467045065874\0541750759582:01f7162f81b050377930728836f1052b37975aed09acb9e66cd12d7aea9cffc4746e290a\"; shbts=\"1719223582\05467045065874\0541750759582:01f7e7a7cc10426915aeb8b07a877037b261789f55b55d41f8d6bf31352444df7c2457bb\"; rur=\"PRN\05467045065874\0541750759619:01f7bf54191315a40b15c564525a7148b3e23f0a28a574faacb0ee262ea7b66c267995bd\"",
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

        "User-Agent": str(Cookie_obj['user-agent']),
        "X-Asbd-Id": "129477",
        "X-Bloks-Version-Id": "213e4f338be29ab2c08f8071c4feb979c6b2fe37d4124f56e5c4b00e51a21aaf",
        "X-Csrftoken": Cookie_obj['csrf_token'],
        "X-Fb-Friendly-Name": "usePolarisLikeMediaLikeMutation",
        "X-Fb-Lsd": "zRjTA0fjlIwgmiCC2Y0ip0",
        "X-Ig-App-Id": "936619743392459"
    }

    # Define the payload
    payload = {
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
        "variables": "{\"media_id\":\"3397561855460766739\"}", #3393245210130807279  3397561855460766739 视频id instagram://media?id=3397561855460766739
        "server_timestamps": "true",
        "doc_id": "8244673538908708"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=payload,proxies=proxy)

    # Print the response
    print(response.status_code)
    print(response.text)

    """
    200
    {"data":{"xdt_api__v1__media__media_id__like":{"__typename":"XDTEmptyRecord"}},"extensions":{"is_final":true},"status":"ok"}
    """

def pl(Cookie_obj):
    # Define the URL
    url = "https://www.instagram.com/graphql/query"

    # Define the headers
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "1060",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": str(Cookie_obj['cookie']),
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

        "User-Agent": str(Cookie_obj['user-agent']),
        "X-Asbd-Id": "129477",
        "X-Bloks-Version-Id": "213e4f338be29ab2c08f8071c4feb979c6b2fe37d4124f56e5c4b00e51a21aaf",
        "X-Csrftoken": Cookie_obj['csrf_token'],
        "X-Fb-Friendly-Name": "usePolarisLikeMediaLikeMutation",
        "X-Fb-Lsd": "zRjTA0fjlIwgmiCC2Y0ip0",
        "X-Ig-App-Id": "936619743392459"
    }

    # Define the payload
    payload = {
        "av": "17841467016230633",
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "__req": "w",
        "__hs": "19898.HYP:instagram_web_pkg.2.1..0.1",
        "dpr": "1",
        "__ccg": "UNKNOWN",
        "__rev": "1014422660",
        "__s": "bi95c1:3c820x:kwi6yg",
        "__hsi": "7384010893272940246",
        "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEnxO1ywOwv89k2C1Fwc60D87u3ifK0EUjwGzEaE2iwNwKwHw8Xxm16wUwtEvw4JwJCwLyES1TwVwDwHg2ZwrUdUbGwmk0zU8oC1Iwqo5q3e3zhA6bwIDyUrAwHyokxK3OqcyU-2K",
        "__csr": "gjl1f4T116hnkQIn5Z9mDa_8lksPsLmDA9Ix4mVeEXCBGFvyAuiWV9XCBExaVvqlqhkEOql2FWiUx6JqCxJ4DBBDVVUCHjx6mAdx6bGmunWCxfAADyUkhpqyA8K9g8orGHK00kGah01buexmUfU4Wt2Fm0P8gwg9m04_U0s0EEOvyolaawGg534Diax8qzA0K47S1sw2D82Xw2TokP05wge85fw2YQ0K8gxS00Ajo",
        "__comet_req": "7",
        "fb_dtsg": "NAcNUan2ib-7AP2-rs3AIJMLv7DS9X8Z6Rep6vNdXaVCNhsyjp_L58w:17864970403026470:1719223576",
        "jazoest": "26060",
        "lsd": "Kk_PcR3_EMqT9Lwa2J305B",
        "__spin_r": "1014422660",
        "__spin_b": "trunk",
        "__spin_t": "1719224009",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PolarisPostCommentInputRevampedMutation",
        "variables": '{"connections":["client:root:__PolarisPostCommentsDirect__xdt_api__v1__media__media_id__comments__connection_connection(data:{} ,media_id:\"3393245210130807279\",sort_order:\"popular\")"],"request_data":{"comment_text":"cool"},"media_id":"3393245210130807279"}',
        "server_timestamps": "true",
        "doc_id": "7980226328678944"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=payload,proxies=proxy)

    # Print the response
    print(response.status_code)
    print(response.text)


    """
    200
{"errors":[{"message":"execution error","severity":"CRITICAL"}],"status":"ok"}
    """

#gz
def gz(Cookie_obj):
    user_id='63906350951'
    # Define the URL
    url = f"https://www.instagram.com/api/v1/friendships/create/{user_id}/"

    # Define the headers
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "1060",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": str(Cookie_obj['cookie']),
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

        "User-Agent": str(Cookie_obj['user-agent']),
        "X-Asbd-Id": "129477",
        "X-Bloks-Version-Id": "213e4f338be29ab2c08f8071c4feb979c6b2fe37d4124f56e5c4b00e51a21aaf",
        "X-Csrftoken": Cookie_obj['csrf_token'],
        "X-Fb-Friendly-Name": "usePolarisLikeMediaLikeMutation",
        "X-Fb-Lsd": "zRjTA0fjlIwgmiCC2Y0ip0",
        "X-Ig-App-Id": "936619743392459"
    }

    # Define the payload
    payload = {
        "container_module": "feed_timeline",
        "nav_chain": "PolarisFeedRoot:feedPage:3:topnav-link",
        "user_id": user_id
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=payload,proxies=proxy)

    # Print the response
    print(response.status_code)
    print(response.text)

res = requests.get('http://127.0.0.1:5003/api/get/cookie')
print(res.json())
dz(json.loads(res.json()))