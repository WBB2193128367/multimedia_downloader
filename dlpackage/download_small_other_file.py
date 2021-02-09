from dlpackage import model_download as dm
from dlpackage import requests_header
from dlpackage import setting_gui
from dlpackage import share
import threading
import time
import os





# 定义的全局变量
pause_flag = False            #暂停标志
cancel_flag = False           #取消下载标志
length = None                 #用来保存已经下载文件的长度
mode = None                   #用来保存文件的存储模式
file_status = False           #用来保存文件的打开或关闭状态
file_path_name = None         #用来保存文件的存储路径


# 暂停/继续下载
def pause_or_continue():

    global pause_flag
    if share.m3.m.get() == '暂停下载':
        share.m3.m.set('继续下载')
        pause_flag = True
    else:
        share.m3.m.set('暂停下载')
        pause_flag = False
        m3u8_href = share.m3.button_url.get().rstrip()
        video_name = share.m3.button_video_name.get().rstrip()
        t = threading.Thread(
            target=download_mp4, args=(
                m3u8_href, video_name,))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()

#取消下载的线程
def cancel_thread():
    t = threading.Thread(
        target=cancel)
    # 设置守护线程，进程退出不用等待子线程完成
    t.setDaemon(True)
    t.start()


# 取消下载
def cancel():
    global pause_flag
    global cancel_flag
    global file_status
    global file_path_name
    if not pause_flag:
        cancel_flag = True
        # 判断download_mp4(）中打开的文件是否关闭，file_path_name是否被赋值，如果没有就再给它一点时间
        while file_status == False or file_path_name == None:
            time.sleep(1)
        #移除已经下载完成的部分文件
        os.remove(file_path_name)
        #进度条归零
        share.set_progress(0)
        share.m3.str.set('')
        share.m3.show_info("取消成功！")
        cancel_flag = False
        file_status = False
        file_path_name = None

    else:
        os.remove(file_path_name)
        share.set_progress(0)
        share.m3.str.set('')
        share.m3.m.set('暂停下载')
        pause_flag = False
        share.m3.show_info("取消成功！")


# 下载除去m3u8外的其它媒体文件


def download_mp4(m3u8_href, video_name):
    global length
    global cancel_flag
    global mode
    global file_path_name
    global file_status
    share.m3.clear_alert()
    video_name = share.check_video_name(video_name)
    video_name = setting_gui.path + "/" + video_name  # 将保存路径与文件名称进行拼接
    video_name = video_name + share.m3.button_url.get()[share.m3.button_url.get(
    ).rfind('.'):share.m3.button_url.get().rfind('.') + 4]  # 将文件的后缀与整体路径进行拼接
    chunk_size = 512
    # 当这个文件已经下载过
    if os.path.exists(
            video_name):

        # response=requests.get(url=m3u8_href, stream=True,headers=Model_http_header.get_user_agent1(os.path.getsize(video_name)))
        # print(response.status_code)
        response = dm.easy_download(
            url=m3u8_href,
            stream=True,
            #请求头中加入'Range': 'bytes'参数实现断点续传
            header=requests_header.get_user_agent1(
                os.path.getsize(video_name)))
        mode = 'ab'
        size = os.path.getsize(video_name)
        content_size = length
    else:
        response = dm.easy_download(
            url=m3u8_href,
            stream=True,
            header=requests_header.get_user_agent())
        mode = 'wb'
        size = 0
        content_size = int(response.headers['content-length'])
    share.m3.alert('[文件大小]:%0.2f MB' % (content_size / 1024 / 1024))
    with open(video_name, mode) as f:
        for data in response.iter_content(chunk_size=chunk_size):

                #如果既没有暂停也没有取消下载就正常下载
                if pause_flag == False and cancel_flag == False:
                    f.write(data)
                    size = size + len(data)
                    p = (size / content_size) * 100
                    share.set_progress(p)
                    share.m3.str.set('%.2f%%' % float(p))
                #如果取消下载
                elif cancel_flag:
                    f.close()
                    file_status = f.closed
                    file_path_name = video_name
                    break
                #如果暂停下载
                elif pause_flag:
                    f.close()
                    length = content_size
                    file_path_name = video_name
                    break
    if size == content_size:
        share.m3.alert('下载完成！')
        share.m3.show_info("下载完成！")
        share.set_progress(0)
