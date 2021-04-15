import os
import re
import shutil
import threading
import threadpool
from Crypto.Cipher import AES
from dlpackage import model_requests as dm
from dlpackage import requests_header
from dlpackage import setting_gui
from dlpackage import share

# 定义的全局变量
video_path = None
link = None
download_fail_list = []
url_list = []
order_increase = False
exit_flag = False
save_source_file = False
url_host = None
url_path = None
key = None  # 用来存储秘钥，用于视频的解码
iv = None
downloaded_clip = 0


def try_again_download(url, file_name):
    global download_fail_list
    global downloaded_clip
    share.m3.alert("正在尝试重新下载%s" % file_name)
    response = dm.easy_download(
        url=url, stream=False, header=requests_header.get_user_agent(),
        timeout=(18, 30))
    if response is None:
        # share.m3.alert("%s下载失败，请手动下载:\n%s" % (file_name, url))
        return
    else:
        download_fail_list.remove(([url, file_name], None))
        with open(file_name, 'wb') as file:
            file.write(response.content)
            downloaded_clip += 1
            m = (downloaded_clip / len(url_list)) * 100
            share.set_progress(m)
            share.m3.str.set('%.2f%%' % m)


# 重复下载失败的.ts文件
def download_fail_file():
    global download_fail_list
    global downloaded_clip
    if len(download_fail_list) > 0:
        start_download_in_pool(try_again_download, download_fail_list)
        if len(download_fail_list) == 0:
            share.log_content = {
                'time': share.get_time(),
                'link': link,
                'status': '下载成功'}
            t = threading.Thread(
                target=share.write, args=(share.log_content,))
            # 设置守护线程，进程退出不用等待子线程完成
            t.setDaemon(True)
            t.start()
            if merge_file(video_path):
                if save_source_file is False:
                    # 删除文件夹
                    shutil.rmtree(video_path)
                share.m3.alert("下载完成")
                share.m3.show_info("下载完成")

                share.set_progress(0)
                share.m3.str.set('')
                share.m3.clear_alert()
                downloaded_clip=0
                share.running = False
            else:
                share.m3.alert("视频文件合并失败,请查看消息列表")
        else:
            share.m3.alert("有部分文件没有下载完成，请点击重试！")
            share.m3.show_info("有部分文件没有下载完成，请点击重试！")
    else:
        share.m3.show_info("还没有下载失败的文件噢！")


# 合并.ts文件片段


def merge_file(dir_name):
    global iv
    global key
    # 根据文件名对.ts文件进行排序
    file_list = share.file_walker(dir_name)
    with open(dir_name + ".mp4", 'wb+') as fw:
        for i in range(len(file_list)):
            if key is not None and iv is None:
                cryptor = AES.new(key, AES.MODE_CBC, key)
                fw.write(cryptor.decrypt(open(file_list[i], 'rb').read()))
            elif key is not None and iv is not None:
                cryptor = AES.new(key, AES.MODE_CBC, iv)
                fw.write(cryptor.decrypt(open(file_list[i], 'rb').read()))
            else:
                fw.write(open(file_list[i], 'rb').read())
    iv = None
    key = None
    return True


# 拼接下载用的参数
def get_download_params(head, dir_name):
    global url_list
    i = 0
    params = []
    while i < len(url_list):
        index = "%05d" % i
        param = ([head + url_list[i], dir_name + "/" + index + ".ts"], None)
        params.append(param)
        i += 1
    return params


# 设置线程池开始下载
def start_download_in_pool(function, params):
    # 线程数
    share.m3.alert("已确认正确地址，开始下载")
    pool = threadpool.ThreadPool(setting_gui.threading_count)
    thread_requests = threadpool.makeRequests(function, params)
    [pool.putRequest(req) for req in thread_requests]
    pool.wait()


# 检查.ts文件是否都下载完成
# def check_file(dir_name):
#     path = dir_name
#     file_num = 0
#     for f_path, f_dir_name, f_names in os.walk(path):
#         for name in f_names:
#             if name.endswith(".ts"):
#                 file_num += 1
#     return file_num


# 测试拼接的下载地址是否正确
def test_download_url(url):
    share.m3.alert("尝试使用%s下载视频" % url)
    res = dm.easy_download(
        url,
        stream=False,
        header=requests_header.get_user_agent(),
        max_retry_time=5)
    return res


# 进行速度优先和画质优先的触发事件


def order_type(type_):
    global order_increase
    order_increase = type_
    if type_:
        share.m3.alert("设置速度优先")
    else:
        share.m3.alert("设置画质优先")


# 获取域名


def get_host(url):
    url_param = url.split("//")
    return url_param[0] + "//" + url_param[1].split("/")[0] + "/"


def get_dir(url):
    host = get_host(url)
    url = url.replace(host, '')
    return ("/" + url[0:url.rfind("/")] + "/").replace("//", "/")


# 获取带宽
def get_band_width(info):
    info_list = info.split("\n")[0].split(",")
    for info in info_list:
        if info.startswith("BANDWIDTH"):
            return int(info.split("=")[1])
    return 0


# 排序
def order_list(o_type, o_list):
    o_list.sort(key=get_band_width, reverse=o_type)
    return o_list


# 获得域名路径


def get_path(url):
    if url.rfind("/") != -1:
        return url[0:url.rfind("/")] + "/"
    else:
        return url[0:url.rfind("\\")] + "\\"


# 获得.ts文件列表
def get_ts_add(m3u8_href):
    global key
    global url_path
    global url_host
    global iv
    share.m3.alert("获取ts下载地址，m3u8地址:\n%s" % m3u8_href)
    url_host = get_host(m3u8_href)
    url_path = get_path(m3u8_href)
    response = dm.easy_download(
        url=m3u8_href,
        stream=False,
        header=requests_header.get_user_agent())
    if response is not None:
        response = response.text
    else:
        return []
    share.m3.alert("响应体:\n%s\n" % response)
    response_list = response.split("#")
    ts_add = []
    m3u8_href_list_new = []
    count = 1
    for res_obj in response_list:
        # 说明m3u8文件加密
        if res_obj.startswith("EXT-X-KEY"):
            # 利用正则表达式获得秘钥链接
            url = re.findall(r'URI=\"(.*?)\"', res_obj, re.S)[0]
            if len(re.findall(r'IV=(.*?)', res_obj, re.S)) != 0:
                iv = re.findall(r'IV=(.*?)', res_obj, re.S)[0]
            else:
                iv = None

            if url.startswith('key'):
                response = dm.easy_download(
                    url_path + url,
                    stream=False,
                    header=requests_header.get_user_agent())
                key = response.content
            elif url.startswith('http'):
                response = dm.easy_download(
                    url, stream=False, header=requests_header.get_user_agent())
                key = response.content

        # 说明有二级m3u8文件
        elif res_obj.startswith("EXT-X-STREAM-INF"):
            # m3u8 作为主播放列表（Master Playlist），其内部提供的是同一份媒体资源的多份流列表资源（Variant Stream）
            # file_add = res_obj.split("\n")[1]
            file = res_obj.split(":")[1]
            m3u8_href_list_new.append(file)
        elif res_obj.startswith("EXTINF"):
            # 当 m3u8 文件作为媒体播放列表（Media Playlist），其内部信息记录的是一系列媒体片段资源
            file = res_obj.split("\n")[1]
            ts_add.append(file)
    if len(m3u8_href_list_new) > 0:
        # 根据画质优先/速度优先排序
        m3u8_href_list_new = order_list(order_increase, m3u8_href_list_new)
        file = m3u8_href_list_new[0].split("\n")[1]
        # 递归调用get_ts_add()方法
        ts_add = get_ts_add(url_path + file)
        if len(ts_add) == 0:
            ts_add = get_ts_add(url_host + file)
            if len(ts_add) == 0:
                ts_add = get_ts_add(file)

    return ts_add


# 是否保存源文件的事件


def save_source():
    global save_source_file
    if share.m3.cb_status.get() == 0:
        save_source_file = True
        share.m3.alert("下载完成后保存源文件")
    else:
        save_source_file = False
        share.m3.alert("下载完成后删除源文件")


# 下载视频并保存为文件
def download_to_file(url, file_name):
    global download_fail_list
    global url_list
    global downloaded_clip
    response = dm.easy_download(
        url=url,
        stream=False,
        header=requests_header.get_user_agent())
    if response is None:
        download_fail_list.append(([url, file_name], None))  # 将下载失败的视频连接加入列表
        return
    else:
        with open(file_name, 'wb') as file:
            file.write(response.content)
            downloaded_clip += 1
            m = (downloaded_clip / len(url_list)) * 100
            share.set_progress(m)  # 设置进度条
            share.m3.str.set('%.2f%%' % m)


def start_one1(m3u8_href, video_name):
    global link
    global key
    global download_fail_list
    global url_list
    global url_path
    global url_host
    global video_path
    global downloaded_clip
    # 清空消息框中的消息
    share.m3.clear_alert()
    # 进度条归零
    share.set_progress(0)
    link = m3u8_href
    # 格式化文件名
    video_name = share.check_video_name(video_name)
    # 获取所有ts视频下载地址
    url_list = get_ts_add(m3u8_href)
    if len(url_list) == 0:
        share.m3.waring_info("获取地址失败!")
        share.m3.clear_alert()
        share.log_content = {
            'time': share.get_time(),
            'link': link,
            'status': '下载失败'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        share.running = False  # 重置任务开始标志
        return
    video_name = setting_gui.path + "/" + video_name
    video_path = video_name
    if not os.path.exists(video_name):
        os.makedirs(video_name)
    share.m3.alert("总计%s个视频" % str(len(url_list)))
    # 拼接正确的下载地址开始下载
    if test_download_url(url_host + url_list[0]):
        # 获取.ts文件的链接和命名
        params = get_download_params(head=url_host, dir_name=video_name)
        # 获得参数后线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)
    elif test_download_url(url_path + url_list[0]):
        params = get_download_params(head=url_path, dir_name=video_name)
        # 线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)
    elif test_download_url(url_list[0]):
        params = get_download_params('', dir_name=video_name)
        # 线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)

    else:
        share.m3.waring_info("地址连接失败!")
        share.log_content = {
            'time': share.get_time(),
            'link': link,
            'status': '下载失败'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        share.running = False
        return
    # 重新下载先前下载失败的.ts文件
    # while len(download_fail_file())!=0:
    #     download_fail_file()
    # 检查ts文件总数是否对应
    if downloaded_clip == len(url_list):
        share.log_content = {
            'time': share.get_time(),
            'link': link,
            'status': '下载成功'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        # 合并视频
        if merge_file(video_name):
            if save_source_file is False:
                # 删除文件夹
                shutil.rmtree(video_name)
            share.m3.alert("下载完成")
            share.m3.show_info("下载完成")
            share.set_progress(0)
            share.m3.str.set('')
            share.m3.clear_alert()
            share.running = False
            downloaded_clip = 0
            # 清空下载失败视频列表
            url_list = []
            download_fail_list = []
        else:
            share.m3.alert("视频文件合并失败,请查看消息列表")
            share.m3.show_info("视频文件合并失败,请查看消息列表")
    else:
        share.m3.alert("有部分文件没有下载完成，请点击重试！")
        share.m3.show_info("有部分文件没有下载完成，请点击重试！")

    # 重置任务开始标志


def start_list1(m3u8_href, video_name):
    global link
    global key
    global download_fail_list
    global url_list
    global url_path
    global url_host
    global video_path
    global downloaded_clip
    # 清空消息框中的消息
    share.m3.clear_alert()
    # 进度条归零
    share.set_progress(0)
    link = m3u8_href
    # 格式化文件名
    video_name = share.check_video_name(video_name)
    # 任务开始标志，防止重复开启下载任务
    # 获取所有ts视频下载地址
    url_list = get_ts_add(m3u8_href)
    if len(url_list) == 0:
        share.m3.alert("获取地址失败!")
        share.log_content = {
            'time': share.get_time(),
            'link': link,
            'status': '下载失败'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        return False
    video_name = setting_gui.path + "/" + video_name
    video_path = video_name
    if not os.path.exists(video_name):
        os.makedirs(video_name)
    share.m3.alert("总计%s个视频" % str(len(url_list)))
    # 拼接正确的下载地址开始下载
    if test_download_url(url_host + url_list[0]):
        # 获取.ts文件的链接和命名
        params = get_download_params(head=url_host, dir_name=video_name)
        # 获得参数后线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)
    elif test_download_url(url_path + url_list[0]):
        params = get_download_params(head=url_path, dir_name=video_name)
        # 线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)
    elif test_download_url(url_list[0]):
        params = get_download_params('', dir_name=video_name)
        # 线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)
    elif test_download_url(url_list[0]):
        params = get_download_params('', dir_name=video_name)
        # 线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)
    elif test_download_url(url_list[0]):
        params = get_download_params(head='', dir_name=video_name)
        # 线程池开启线程下载视频
        start_download_in_pool(download_to_file, params)
    else:
        share.m3.alert("地址连接失败!")
        share.log_content = {
            'time': share.get_time(),
            'link': link,
            'status': '下载失败'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        return False
    # 重新下载先前下载失败的.ts文件
    while len(download_fail_list) != 0:
        start_download_in_pool(try_again_download, download_fail_list)
    # 检查ts文件总数是否对应
    if downloaded_clip == len(url_list):
        share.log_content = {
            'time': share.get_time(),
            'link': link,
            'status': '下载成功'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        # 合并视频
        if merge_file(video_name):
            if save_source_file is False:
                # 删除文件夹
                shutil.rmtree(video_name)
            share.m3.alert("下载完成!")
            share.set_progress(0)
            share.m3.str.set('')
            share.m3.clear_alert()
            share.running = False
            downloaded_clip = 0
            # 清空下载失败视频列表
            url_list = []
            download_fail_list = []
        else:
            share.m3.alert("视频文件合并失败,请查看消息列表")
    else:
        share.m3.alert("有部分文件没有下载完成，请点击重试！")
    # 重置任务开始标志
    return True
