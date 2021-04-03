from dlpackage import setting_gui
import tkinter.messagebox
from PIL import Image, ImageTk
import json
import time
import re
import os


# 定义的全局变量
exeing_id=None #用来保存下载链表中正在下载链接的id
m3 = None  # 定义的一个Multimedia_Downloader的对象
running = False  # 开始下载的标志
log_content = {}  # 用来存储给日志文件中写入的内容


# 对下载的.ts文件进行排序
def file_walker(path):
    file_list = []
    for root, dirs, files in os.walk(path):  # 生成器
        files.sort(key=lambda x: int(x[0:-3]))
        for fn in files:
            p = str(root + "/" + fn)
            file_list.append(p)
    return file_list


# 获取视频文件数量
def count_file(file_name):
    video_name = get_save_path(file_name)
    file_num = 0
    for f_path, f_dir_name, f_names in os.walk(video_name):
        for name in f_names:
            if name.endswith(".ts"):
                file_num += 1
    return file_num


# 返回一个经过出处理的文件名
def check_video_name(name):
    return name.replace("\t", "").replace("\n", "")


# 得到文件的保存路径，不包括文件名
def get_save_path(video_name):
    if video_name.rfind("/") != -1:
        return video_name[0:video_name.rfind("/")]
    else:
        return video_name[0:video_name.rfind("\\")]

# 设置进度条


def set_progress(v):
    m3.progress["value"] = v
    m3.root.update()


# 关闭主窗口时进行提示
def close_windows(root):
    if os.path.exists(
        setting_gui.path +
        '/' +
            m3.button_video_name.get().strip()) and m3.button_video_name.get().strip() != '':
        if tkinter.messagebox.askokcancel('退出', '已经下载部分文件，确认退出吗？'):
            root.destroy()
    else:

        if tkinter.messagebox.askokcancel('退出', '确认要退出吗？'):
            root.destroy()

# 获取当前电脑上的时间，并且进行格式话


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 将log_content中临时存储的日志信息写入json文件中
def write(file):
    ff = json.dumps(file)  # 将字典转换为字符串
    with open(r'../log.json', 'a+') as f:
        f.write(ff)
        f.write('\n')


#检验用户输入的网址是否正确
def check_href(m3u8_href):
    if re.match(
        r'^([hH][tT]{2}[pP]://|[hH][tT]{2}[pP][sS]://)([A-Za-z0-9]|-)+\.([A-Za-z0-9]|-)+\.([A-Za-z0-9]|-)+/(.*?)$',
        m3u8_href,
            re.S):
        return True
    else:
        return False

def get_image(filename, width, height):
    im =Image.open(filename).resize((width, height))
    return ImageTk.PhotoImage(im)