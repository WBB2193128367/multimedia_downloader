from dlpackage import model_requests as dm
from dlpackage import requests_header
from dlpackage import setting_gui
from dlpackage import proxy_ip_pool
from dlpackage import share
import threadpool
import threading
import shutil
import os


# 定义的全局变量
video_path = None
url_path=None
cancel_flag = False
pause_flag = False
content_length = None  # 用来存储待下载文件的大小
start = [0, ]  # 用来存储断点续传的开始点
end = []  # 用来存储断点续传的结束点
download_fail_list1 = []  # 用来存储下载失败的视频的开始点，结束点，视频名称


# 计算已下载文件的总大小
def calculate(folder_path):
    full_size = 0
    for parent, dirs, files in os.walk(folder_path):
        full_size = sum(os.path.getsize(os.path.join(parent, file))
                        for file in files)
    return full_size

# def cancel_thread():
#     t = threading.Thread(
#         target=cancel,)
#     # 设置守护线程，进程退出不用等待子线程完成
#     t.setDaemon(True)
#     t.start()
# def cancel():
#     global thread_count
#     global cancel_flag
#     cancel_flag=True
#     while thread_count!=0:
#         time.sleep(1)
#     share.set_progress(0)
#     print(video_path)
#     shutil.rmtree(video_path)
#     cancel_flag=False
#     share.m3.show_info("取消成功！")

# 下载文件


def download_to_file1(start, end, file_name):
    global download_fail_list1
    response = dm.easy_download(
        url=url_path,
        stream=True,
        # proxies=proxy_ip_pool.get_proxy(),
        header=requests_header.get_user_agent2(
            start,
            end))
    if response is None:
        download_fail_list1.append(
            ([start, end, file_name], None))  # 将下载失败的视频连接加入列表
        return
    else:

        with open(file_name, 'wb') as file:
            file.write(response.content)
            print(share.get_save_path(file_name))
            p = (calculate(share.get_save_path(file_name)) / content_length) * 100
            print(p)
            share.set_progress(p)  # 设置进度条
            share.m3.str.set('%.2f%%' % p)


def try_again_download(start, end, file_name):
    global download_fail_list1
    share.m3.alert("正在尝试重新下载%s" % file_name)
    response = dm.easy_download(
        url=url_path,
        stream=True,
        # proxies=proxy_ip_pool.get_proxy(),
        header=requests_header.get_user_agent2(
            start,
            end),
        timeout=(18, 30))
    if response is None:
        # share.m3.alert("%s下载失败，请手动下载:\n%s" % (file_name))
        return
    else:
        download_fail_list1.remove(([start, end, file_name], None))
        with open(file_name, 'wb') as file:
            file.write(response.content)
            p = calculate(share.get_save_path(file_name)) / \
                content_length * 100
            share.set_progress(p)
            share.m3.str.set('%.2f%%' % p)

# 再次下载失败的文件


def download_fail_file1():
    global download_fail_list1
    if len(download_fail_list1) > 0:
        start_download_in_pool1(try_again_download, download_fail_list1)
        if len(download_fail_list1) == 0:
            share.log_content = {
                'time': share.get_time(),
                'link': url_path,
                'status': '下载成功'}
            t = threading.Thread(
                target=share.write, args=(share.log_content,))
            # 设置守护线程，进程退出不用等待子线程完成
            t.setDaemon(True)
            t.start()
            merge_file1(video_path)
            # 删除下载的视频片段
            shutil.rmtree(video_path)
            share.m3.alert("下载完成")
            share.set_progress(0)
            share.m3.str.set('')
            share.m3.clear_alert()
            share.running = False
        else:
            share.m3.alert("有部分文件没有下载完成，请点击重试！")
            share.m3.show_info("有部分文件没有下载完成，请点击重试！")
    else:
        share.m3.show_info("还没有下载失败的文件噢！")

# 进行文件的拼接


def merge_file1(dir_name):
    file_list = share.file_walker(dir_name)
    with open(dir_name + url_path[url_path.rfind('.'):url_path.rfind('.') + 4], 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())

    return True


# 进行参数的拼接
def get_download_params1(dir_name):
    i = 0
    params = []
    while i < len(end):
        index = "%05d" % i
        param = ([start[i], end[i], dir_name + "/" + index + ".ts"], None)
        params.append(param)
        i += 1
    return params


# 进行线程池的创建
def start_download_in_pool1(function, params):
    share.m3.alert("开始下载")
    # 设置线程池中线程的数量
    pool = threadpool.ThreadPool(setting_gui.threading_count)
    # 创建请求列表
    thread_requests = threadpool.makeRequests(function, params)
    # 将请求列表中的每个请求放入线程池中
    for req in thread_requests:
        pool.putRequest(req)

    pool.wait()


def file_divide(content_lenths):
    # if content_lenths <=209715200:
    #     divide_length=2097152
    # elif content_lenths >209715200 and content_lenths <=419430400:
    #     divide_length=4094304
    # elif content_lenths >419430400 and content_lenths <=629145600:
    #     divide_length = 6291456
    # elif content_lenths >629145600 and content_lenths <=838860800:
    #     divide_length = 8388608
    # elif content_lenths >838860800 and content_lenths <=1048576000:
    #     divide_length = 10485760
    # else:
    #     divide_length = 10485760
    for i in range(0, content_lenths, 1048576):
        if int(i) != 0:
            end.append(i)
    for i in end:
        if int(i) != 0:
            start.append(i + 1)
    if content_lenths >= start[len(start) - 1]:
        end.append(content_lenths)
    else:
        start.pop()


# 检查文件是否都下载完成
def check_file_count1(dir_name):
    path = dir_name
    file_num = 0
    for f_path, f_dir_name, f_names in os.walk(path):
        for name in f_names:
            if name.endswith(".ts"):
                file_num += 1
    return file_num


def start_one(content_size, video_name,m3u8_href):
    global content_length
    global download_fail_list1
    global start
    global end
    global video_path
    global url_path
    content_length = content_size
    video_name = share.check_video_name(video_name)
    video_name = setting_gui.path + "/" + video_name
    video_path = video_name
    url_path=m3u8_href
    link = share.m3.button_url.get().rstrip()
    if not os.path.exists(video_name):
        os.makedirs(video_name)
    # 对文件进行划分
    file_divide(content_size)
    # 进行参数的拼接
    params = get_download_params1(video_name)
    share.m3.alert('[文件大小]:%0.2f MB' % (content_size / 1024 / 1024))
    # 启动线程池进行下载
    start_download_in_pool1(download_to_file1, params)
    # while len(download_fail_list1)!=0:
    #     download_fail_file1()
    # 用来检查文件片段是否都下载完成
    if check_file_count1(video_name)== len(start):
        share.log_content = {
            'time': share.get_time(),
            'link': url_path,
            'status': '下载成功'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        # 合并视频
        merge_file1(video_name)
        # 删除下载的视频片段
        shutil.rmtree(video_name)

        share.m3.alert("下载完成")
        share.m3.show_info("下载完成")
        share.set_progress(0)
        share.m3.str.set('')
        share.m3.clear_alert()
        download_fail_list1 = []
        share.running = False
    else:
        share.m3.alert("有部分文件没有下载完成，请点击重试！")
        share.m3.show_info("有部分文件没有下载完成，请点击重试！")
    # 清空下载失败视频列表
    start = [0, ]
    end = []



def start_list(content_size, video_name,m3u8_href):
    global content_length
    global download_fail_list1
    global start
    global end
    global video_path
    global url_path
    content_length = content_size
    video_name = share.check_video_name(video_name)
    video_name = setting_gui.path + "/" + video_name
    video_path = video_name
    url_path = m3u8_href
    if not os.path.exists(video_name):
        os.makedirs(video_name)
    # 对文件进行划分
    file_divide(content_size)
    # 进行参数的拼接
    params = get_download_params1(video_name)
    share.m3.alert('[文件大小]:%0.2f MB' % (content_size / 1024 / 1024))
    # 启动线程池进行下载
    start_download_in_pool1(download_to_file1, params)
    while len(download_fail_list1)!=0:
        start_download_in_pool1(try_again_download, download_fail_list1)
    #用来检查文件片段是否都下载完成
    if check_file_count1(video_name)== len(start):
        share.log_content = {
            'time': share.get_time(),
            'link': url_path,
            'status': '下载成功'}
        t = threading.Thread(
            target=share.write, args=(share.log_content,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        # 合并视频
        merge_file1(video_name)
        # 删除下载的视频片段
        shutil.rmtree(video_name)

        share.m3.alert("下载完成")
        share.set_progress(0)
        share.m3.str.set('')
        share.m3.clear_alert()
        download_fail_list1 = []
        share.running = False
    # 清空下载失败视频列表
    start = [0, ]
    end = []
    return True