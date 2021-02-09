from dlpackage import model_download as dm
from dlpackage import requests_header
from dlpackage import setting_gui
from dlpackage import share
import threadpool
import shutil
import os






# 定义的全局变量
video_path=None
cancel_flag=False
pause_flag=False
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
            url=share.m3.button_url.get().rstrip(),
            stream=True,
            header=requests_header.get_user_agent2(
                start,
                end))
    if response is None:
            download_fail_list1.append((start, end, file_name,))  # 将下载失败的视频连接加入列表
            return
    else:

        with open(file_name, 'wb') as file:
            file.write(response.content)
            print(share.get_save_path(file_name))
            p = (calculate(share.get_save_path(file_name)) / content_length ) * 100
            print(p)
            share.set_progress(p)  # 设置进度条
            share.m3.str.set('%.2f%%' % p)




# 再次下载失败的文件
def download_fail_file1():
    global download_fail_list1
    if len(download_fail_list1) > 0:
        for info in download_fail_list1:
            start = info[0]
            end = info[1]
            file_name = info[2]
            share.m3.alert("正在尝试重新下载%s" % file_name)
            response = dm.easy_download(
                url=share.m3.button_url.get().rstrip(),
                stream=True,
                header=requests_header.get_user_agent2(
                    start,
                    end),
                max_retry_time=50)
            if response is None:
                share.m3.alert("%s下载失败，请手动下载:\n%s" % (file_name))
                continue
            with open(file_name, 'wb') as file:
                file.write(response.content)
                p = calculate(share.get_save_path(file_name)) / content_length * 100
                share.set_progress(p)


# 进行文件的拼接
def merge_file1(dir_name):
    file_list = share.file_walker(dir_name)
    with open(dir_name + share.m3.button_url.get()[share.m3.button_url.get().rfind('.'):share.m3.button_url.get().rfind('.') + 4], 'wb+') as fw:
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
def start_download_in_pool1(params):
    share.m3.alert("开始下载")
    # 设置线程池中线程的数量
    pool = threadpool.ThreadPool(setting_gui.threading_count)
    # 创建请求列表
    thread_requests = threadpool.makeRequests(download_to_file1, params)
    # 将请求列表中的每个请求放入线程池中
    for req in thread_requests:
        pool.putRequest(req)

    pool.wait()


# 将大于5MB的文件进行划分
def file_divide(content_lenths):
    if content_lenths <=209715200:
        divide_length=2097152
    elif content_lenths >209715200 and content_lenths <=419430400:
        divide_length=4094304
    elif content_lenths >419430400 and content_lenths <=629145600:
        divide_length = 6291456
    elif content_lenths >629145600 and content_lenths <=838860800:
        divide_length = 8388608
    elif content_lenths >838860800 and content_lenths <=1048576000:
        divide_length = 10485760
    else:
        divide_length = 10485760
    for i in range(0, content_lenths, divide_length):
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
    return file_num == len(start)


def start1(content_size, video_name):
    global content_length
    global download_fail_list1
    global start
    global end
    global video_path
    content_length = content_size
    video_name = share.check_video_name(video_name)
    video_name = setting_gui.path + "/" + video_name
    video_path=video_name
    if not os.path.exists(video_name):
        os.makedirs(video_name)
    # 对文件进行划分
    file_divide(content_size)
    # 进行参数的拼接
    params = get_download_params1(video_name)
    share.m3.alert('[文件大小]:%0.2f MB' % (content_size / 1024 / 1024))
    # 启动线程池进行下载
    start_download_in_pool1(params)
    while len(download_fail_list1)!=0:
        download_fail_file1()
    # 用来检查文件片段是否都下载完成
    if check_file_count1(video_name):
        # 合并视频
        merge_file1(video_name)
        # 删除下载的视频片段
        shutil.rmtree(video_name)

        share.m3.alert("下载完成")
        share.m3.show_info("下载完成")
        share.set_progress(0)
    else:
        share.m3.alert("下载失败！")
        share.m3.show_info("下载失败！")
    # 清空下载失败视频列表
    download_fail_list1 = []
    start = [0, ]
    end = []
    content_length = None
    share.m3.str.set('')
