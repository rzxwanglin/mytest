import re
class InsCookieMiddleware(object):
    """cookie"""
    def process_request(self, request, task):
        cookie_dict = request.meta.get("cookie_dict")
        cookie = ""
        if task in ["liked", "comment"]:
            cookie_str = cookie_dict.get("cookie", "")
            if re.search("sessionid=(.*?);", cookie_str):
                session_id = re.search("sessionid=(.*?);", cookie_str).group(1)
                ds_user_id = re.search("ds_user_id=(.*?);", cookie_str).group(1)
                if "@" in cookie_dict.get("proxy"):
                    cookie = "sessionid=" + session_id + ";"
                else:
                    cookie = "sessionid=" + session_id + "; ds_user_id=" + ds_user_id + ";"
        else:
            cookie = cookie_dict.get("cookie", "")
        # request.headers["cookie"] = cookie
        return cookie