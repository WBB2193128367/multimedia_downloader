import requests
from dlpackage import share
from dlpackage import proxy_ip_pool


def easy_download(
        url,
        stream,
        header,
        proxies=None,
        timeout=(
            12,
            30),
        max_retry_time=5):
    i = 0
    while i <= max_retry_time:
        try:
            share.m3.alert("连接:%s" % url)
            res = requests.get(
                url=url,
                stream=stream,
                headers=header,
                proxies=proxies,
                timeout=timeout)
            if res.status_code == 200 or res.status_code == 206:
                return res
            else:
                return None
        except requests.exceptions.ConnectionError:
            share.m3.alert("请求连接异常！")
            i += 1
            # return None
        except requests.exceptions.Timeout:
            share.m3.alert("请求超时！")
            i += 1
        except Exception as e:
            share.m3.alert("出现其它异常！")
            i += 1
    return None
