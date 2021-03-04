from dlpackage import multimedia_downloader_gui
from dlpackage import download_other_file
from dlpackage import model_requests as dm
from dlpackage import download_m3u8_file
from dlpackage import requests_header
from dlpackage import share
from dlpackage import right_kye
import webbrowser
import requests
import threading
import re


# 全局变量
content_size = None

# 利用正则表达式检查输入的地址是否正确


def check_href(m3u8_href):
    if re.match(
        r'^(http://|https://)?((?:[A-Za-z0-9]+-[A-Za-z0-9]+|[A-Za-z0-9]+)\.)+([A-Za-z]+)[/\?\:]?.*$',
        m3u8_href,
            re.S):
        return True
    else:
        return False


# 检验文件名是否为空
def check_video_name(video_name):
    if "" != video_name:
        return True
    else:
        return False


# 测试网络是否畅通
def test_network():
    try:
        share.m3.alert("正在测试网络是否畅通......")
        requests.get(url='https://www.baidu.com', timeout=5)
        return True
    except BaseException:
        t = threading.Thread(
            target=share.m3.waring_info, args=(
                '网络未连接！！！',))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        return False


# 用来检查用书输入的链接类型并作出响应
def inspect_user_input():
    m3u8_href = share.m3.button_url.get().rstrip()
    video_name = share.m3.button_video_name.get().rstrip()
    check = check_href(m3u8_href)
    check1 = check_video_name(video_name)

    # 当为m3u8文件时
    if check and check1 and re.match(r'^http.*?\.m3u8.*', m3u8_href):
        if test_network():
            # 开启线程执行耗时操作，防止GUI卡顿
            t = threading.Thread(
                target=download_m3u8_file.start, args=(
                    m3u8_href, video_name,))
            # 设置守护线程，进程退出不用等待子线程完成
            t.setDaemon(True)
            t.start()
        else:
            share.running = False
    # 当为其它类型的文件时
    elif check and check1:
        if test_network():
            response = dm.easy_download(
                url=m3u8_href,
                stream=True,
                header=requests_header.get_user_agent())
            if response is not None:
                content_size = int(response.headers['content-length'])
                t = threading.Thread(
                    target=download_other_file.start1, args=(
                        content_size, video_name,))
                # 设置守护线程，进程退出不用等待子线程完成
                t.setDaemon(True)
                t.start()
            else:
                pass
        else:
            share.running = False
    elif check == False and check1 == False:
        share.running = False
        t = threading.Thread(
            target=share.m3.show_info, args=(
                '地址不合法!\n文件名不能为空!', ))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
    elif check == False and check1 == True:
        share.running = False
        t = threading.Thread(
            target=share.m3.show_info, args=(
                '地址不合法', ))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()

    elif check and check1 == False:
        share.running = False
        t = threading.Thread(
            target=share.m3.show_info, args=(
                '文件名不能为空', ))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()


# 打开Githu链接
def open_github_url():
    webbrowser.open(
        'https://github.com/WBB2193128367/multimedia_downloader',
        new=0)

# 用来检查是否已经有任务开始下载


def check_tesk_repeat_open():
    # 如果没有任务执行
    if not share.running:
        share.running = True
        t = threading.Thread(
            target=inspect_user_input)
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()

    else:
        t = threading.Thread(
            target=share.m3.waring_info, args=(
                '正在下载中，请勿重复开启！',))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()


# 开始下载
def start_download():
    t = threading.Thread(
        target=check_tesk_repeat_open)
    # 设置守护线程，进程退出不用等待子线程完成
    t.setDaemon(True)
    t.start()


# 重试触发的事件
def try_again_download():
    m3u8_href = share.m3.button_url.get().rstrip()
    if re.match(r'^http.*?\.m3u8.*', m3u8_href):
        t = threading.Thread(
            target=download_m3u8_file.download_fail_file)
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
    else:
        t = threading.Thread(
            target=download_other_file.download_fail_file1)
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()


def run():

    share.m3 = multimedia_downloader_gui.Multimedia_Downloader()
    # 绑定点击事件
    #
    share.m3.rb1.bind(
        "<Button-1>",
        lambda x: download_m3u8_file.order_type(False))
    #share.m3.button_cancel.bind('<Button-1>',lambda x:download_small_other_file.cancel_thread())
    #share.m3.button_pause.bind('<Button-1>', lambda x: download_small_other_file.pause_or_continue())
    share.m3.rb2.bind(
        "<Button-1>",
        lambda x: download_m3u8_file.order_type(True))
    # 点击将进行源文件的保存
    share.m3.cb.bind("<Button-1>", lambda x: download_m3u8_file.save_source())
    # 开始下载的事件
    share.m3.button_start.bind("<Button-1>", lambda x: start_download())
    share.m3.button_again.bind("<Button-1>", lambda x: try_again_download())
    share.m3.label1.bind("<Button-1>", lambda x: open_github_url())
    share.m3.button_url.bind(
        "<Button-3>",
        lambda x: right_kye.rightKey(
            share.m3.menubar,
            x,
            share.m3.button_url))
    share.m3.button_video_name.bind(
        "<Button-3>",
        lambda x: right_kye.rightKey(
            share.m3.menubar,
            x,
            share.m3.button_video_name))
    #share.m3.button_exit.bind("<Button-1>", lambda x: e())
    # 手动加入消息队列
    share.m3.root.mainloop()


if __name__ == "__main__":
    run()
