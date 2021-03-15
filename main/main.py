from dlpackage import multimedia_downloader_gui
from dlpackage import download_other_file
from dlpackage import model_requests as dm
from dlpackage import download_m3u8_file
from dlpackage import requests_header
from dlpackage import download_list_manage
from dlpackage import share
from dlpackage import setting_gui
from dlpackage import right_kye
import webbrowser
import requests
import threading
import re


# 全局变量
running1=False
content_size = None

# 利用正则表达式检查输入的地址是否正确





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
        share.m3.waring_info("网络未连接!!!")
        share.m3.clear_alert()
        return False



def inspect_user_input1():
    global running1
    count=0
    error=0
    success_list=[]
    error_list=[]
    for i in download_list_manage.id_list:
        share.exeing_id=i
        video_name=download_list_manage.name[i].strip()
        share.m3.c.set(video_name)
        m3u8_href=download_list_manage.url[i].strip()
        check1 = check_video_name(video_name)

        # 当为m3u8文件时
        if check1 and re.match(r'^http.*?\.m3u8.*', m3u8_href):
            if test_network():
                if download_m3u8_file.start_list1(m3u8_href, video_name)==True:
                    download_list_manage.delete_item(share.m3.tree_date,i)
                    download_list_manage.name.pop(i)
                    download_list_manage.url.pop(i)
                    success_list.append(i)
                    count+=1
                else:
                    error+=1
                    error_list.append(i)
            else:
                break
        # 当为其它类型的文件时
        elif check1:
            #测试网络是否畅通
            if test_network():
                response = dm.easy_download(
                    url=m3u8_href,
                    stream=True,
                    header=requests_header.get_user_agent())
                if response is not None:
                    content_size = int(response.headers['content-length'])
                    if download_other_file.start_list(content_size, video_name,m3u8_href)==True:
                        download_list_manage.delete_item(share.m3.tree_date, i)
                        download_list_manage.name.pop(i)
                        download_list_manage.url.pop(i)
                        success_list.append(i)
                        count += 1
                    else:
                        error_list.append(i)
                        error+=1
            else:
                break
    share.m3.c.set('')
    running1=False
    if count==len(download_list_manage.id_list) and error==0:
        download_list_manage.id_list = []
        share.m3.show_info('所有的链接已经下载完成!')
    elif count!=len(download_list_manage.id_list) and error!=0:
        download_list_manage.id_list=error_list
        share.m3.show_info('列表中有部分链接下载失败，详情请查看下载日志!')
    else:
        if len(success_list)!=0:
            for i in success_list:
                if i in download_list_manage.id_list:
                    download_list_manage.id_list.remove(i)
        else:
            pass



# 用来检查用书输入的链接类型并作出响应
def inspect_user_input():
    m3u8_href = share.m3.button_url.get().strip()
    video_name = share.m3.button_video_name.get().strip()
    check = share.check_href(m3u8_href)
    check1 = check_video_name(video_name)

    # 当为m3u8文件时
    if check and check1 and re.match(r'^http.*?\.m3u8.*', m3u8_href):
        if test_network():
            download_m3u8_file.start_one1(m3u8_href, video_name)
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
                download_other_file.start_one(content_size, video_name, m3u8_href)
            else:
                pass
        else:
            share.running = False
    elif check == False and check1 == False:
        share.running = False
        share.m3.show_info('地址不合法!\n文件名不能为空!')
    elif check == False and check1 == True:
        share.running = False
        share.m3.show_info('地址不合法')

    elif check and check1 == False:
        share.running = False
        share.m3.show_info('文件名不能为空')


# 打开Githu链接
def open_github_url():
    webbrowser.open(
        'https://github.com/WBB2193128367/multimedia_downloader',
        new=0)

# 用来检查是否已经有任务开始下载


def check_tesk_repeat_open():
    global running1
    # 如果没有任务执行
    if setting_gui.download_model1=='单例下载':

        if not share.running:
            share.running = True
            inspect_user_input()

        else:
            share.m3.waring_info('正在下载中，请勿重复开启!')
    elif setting_gui.download_model1=='列表下载':
         if running1==False:
             if len(download_list_manage.name)!=0:
                 running1=True
                 inspect_user_input1()

             else:
                 share.m3.show_info('下载列表为空！')
         else:
             share.m3.show_info('列表已经开始下载,请勿重复开启!')
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
    share.m3.button1.bind("<Button-1>", lambda x: download_list_manage.add_url(share.m3.root,share.m3.tree_date))
    share.m3.button2.bind("<Button-1>", lambda x: download_list_manage.delete_thread())
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
