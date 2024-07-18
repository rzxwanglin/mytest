import requests
import urllib.parse

url = "https://www.instagram.com/graphql/query"

# Original payload string
payload = 'av=17841467445384268&__d=www&__user=0&__a=1&__req=1p&__hs=19922.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1014969124&__s=u06wne%3Azc0o5u%3Ayk12ho&__hsi=7392864625711762219&__dyn=7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEnxO1ywOwv89k2C1Fwc60AEC1TwQzXwae4UaEW2G0AEcobEaU2eUlwhEe87q7U1bobpEbUGdwtUd-2u2J0bS1LwTwKG1pg2fwxyo6O1FwlEcUed6goK2OubxKi2qi7ErwYCz8rwHw&__csr=gkMxMx2Yyf1lf9EYQ9ZRW5FYy9EyEN5raAjbnjbyfh6lkmQniJiGimV4nuF97hFvjJfKTiHzpk-OOdmm9V5HGaBJkjBy4dKmp5iz-qF4mujxqup6UDJaagybyrjCG8hVK8hoB2VuuqiuiupfxGi48xdeeg-amEynw05qBwZzFA9DAwHCo-2l0f65vwPwj2o3eg0gPw1HFxe310WhFT8dxgldwg86LEyx51i18w2TU62unk8G2l0Ezi0WxS8Upw5ixi0zCnBgG1Jw53Bxd025oG0xU2qwkcM725US00zS8&__comet_req=7&fb_dtsg=NAcM7GHys1foIT8KnRsIH-LQq87m6rVPa3Rt6XAeb-BLuPfQx6ith5Q%3A17854231342124680%3A1721285421&jazoest=26082&lsd=6LsNeBAifXat1-OhtPxgvy&__spin_r=1014969124&__spin_b=trunk&__spin_t=1721285429&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisProfilePostsTabContentDirectQuery_connection&variables=%7B%22after%22%3Anull%2C%22before%22%3Anull%2C%22data%22%3A%7B%22count%22%3A12%2C%22include_relationship_info%22%3Atrue%2C%22latest_besties_reel_media%22%3Atrue%2C%22latest_reel_media%22%3Atrue%7D%2C%22first%22%3A12%2C%22last%22%3Anull%2C%22username%22%3A%22georgerussell63%22%2C%22__relay_internal__pv__PolarisFeedShareMenurelayprovider%22%3Afalse%7D&server_timestamps=true&doc_id=8026303397430981'
# Convert the payload to a dictionary
payload_dict = dict(urllib.parse.parse_qsl(payload))


print(payload_dict)
