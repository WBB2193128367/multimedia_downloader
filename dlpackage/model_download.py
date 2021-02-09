import requests

def easy_download(
        url,
        stream,
        header,
        timeout=(
            10,
            30),
        max_retry_time=3):
    i = 1
    while i <= max_retry_time:
        try:
            print("连接:%s" % url)
            res = requests.get(
                url=url,
                stream=stream,
                headers=header,
                timeout=timeout)
            if res.status_code != 200 and res.status_code !=206:
                return None
            return res
        except Exception as e:
            print(e)
            i += 1
    return None
