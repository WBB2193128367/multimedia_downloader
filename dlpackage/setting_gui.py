import os
import json
import tkinter.filedialog
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from dlpackage import share
from PIL import ImageTk, Image

from dlpackage import right_kye


# 默认的媒体文件存储位置
path = os.path.abspath(os.path.join(os.getcwd(), "..")).replace('\\', '/') + '/downloads'
# 默认的线程数
threading_count = 60
download_model1 = '单例下载'
download_model = 0


# 关于的驱动方法

# 关于的事件


def guanyu():
    tkinter.messagebox.showinfo('关于', '该软件由WBB开发，仅供学习使用！！！')


# 生成线程数范围列表


def generate_list(arg):
    a = []
    for i in range(1, arg + 1):
        a.append(i)
    return a


# 点击确认按钮时的事件
def print_selection(root, button_url, button_video_name, top1, entry, combobox, combobox1, v):
    global path
    global threading_count
    global download_model
    global download_model1
    threading_count = int(combobox.get())
    if entry.get() == '':
        pass
    else:
        path = entry.get()
    if combobox1.get() == '列表下载':
        download_model = 1
        download_model1 = '列表下载'
        button_url['state'] = 'disabled'
        button_video_name['state'] = 'disabled'
    else:
        download_model = 0
        download_model1 = '单例下载'
        button_url['state'] = 'normal'
        button_video_name['state'] = 'normal'
    root.attributes("-alpha", 1 - v)
    top1.destroy()


# 浏览的事件
def liulan(str4):
    m = tkinter.filedialog.askdirectory()
    str4.set(m)


# 设置页面
def set(root, button_url, button_video_name):
    top1 = Toplevel(master=root)  # 创建弹出式窗体
    # top1.attributes("-toolwindow", 1)
    # top1.wm_attributes("-topmost", 1)
    top1.withdraw()
    top1.update()
    w = 400
    h = 320
    ws, hs = top1.winfo_screenwidth(), top1.winfo_screenheight()
    top1.geometry("%dx%d+%d+%d" %
                  (w, h, (ws / 2) - (w / 2), (hs / 2) - (h / 2)))
    top1.deiconify()
    # 使弹出窗口一直处于主窗口前面
    top1.transient(root)
    # 将top1设置为模式对话框，top1不关闭无法操作主窗口
    top1.grab_set()
    top1.title('设置页面')
    top1.iconbitmap(r'../image/设置窗口.ico')
    top1.configure(bg=color)

    # 设置透明度
    lb0 = Label(top1, text="透明度设置:", bg=color)
    lb0.place(x=3, y=10)
    lb2 = Label(top1, text="通过拖动下面滑块改变窗口透明度", bg=color)
    lb2.place(x=100, y=10)

    lb = Label(top1, text="清晰", bg=color)
    lb.place(x=100, y=40)
    lb1 = Label(top1, text="模糊", bg=color)
    lb1.place(x=290, y=40)
    S = Scale(
        top1,
        from_=0,
        to=0.8,
        resolution=0.1,
        showvalue=0,
        orient=HORIZONTAL,
        bg=color,
        fg=color,
        length=150)
    S.place(x=132, y=40)

    lb0 = Label(top1, text="下载目录:", bg=color)
    lb0.place(x=3, y=80)
    lb2 = Label(top1, text="使用指定的视频下载目录", bg=color)
    lb2.place(x=100, y=80)

    # 存储路径
    str3 = StringVar()
    str3.set(path)
    entry = Entry(top1, textvariable=str3, width=24)
    entry.place(x=100, y=110)
    menubar = Menu(top1, tearoff=False)
    # 将entry和rightkey事件绑定
    entry.bind("<Button-3>", lambda x: right_kye.rightKey(menubar, x, entry))
    load1 = Image.open("../image/9.png")
    render1 = ImageTk.PhotoImage(load1)
    img1 = Label(top1, image=render1, bg=color)
    img1.place(x=250, y=105)
    img1.bind("<Button-1>", lambda x: liulan(str3))
    # 线程数
    lb0 = Label(top1, text="线程数设置:", bg=color)
    lb0.place(x=3, y=150)
    lb2 = Label(top1, text="通过下面设置线程的最大数量", bg=color)
    lb2.place(x=100, y=150)
    lb3 = Label(top1, text="最大线程数为", bg=color)
    lb3.place(x=100, y=180)
    combobox = ttk.Combobox(top1, width=5)
    combobox.bind(
        "<Button-3>",
        lambda x: right_kye.rightKey(
            menubar,
            x,
            combobox))
    combobox['values'] = generate_list(100)
    combobox.current(threading_count - 1)
    combobox.place(x=180, y=180)
    lb3 = Label(top1, text="(1-100)", bg=color)
    lb3.place(x=238, y=180)

    # 下载模式设置
    lb4 = Label(top1, text="下载模式设置:", bg=color)
    lb4.place(x=3, y=220)
    combobox1 = ttk.Combobox(top1, width=10, state='readonly')
    combobox1['values'] = ['单例下载', '列表下载']
    combobox1.current(download_model)
    combobox1.place(x=100, y=225)

    # 确认按钮
    load = Image.open("../image/7.png")
    render = ImageTk.PhotoImage(load)
    img = Label(top1, image=render, bg=color)
    img.place(x=165, y=260)
    img.bind("<Button-1>",
             lambda x: print_selection(root, button_url, button_video_name, top1, entry, combobox, combobox1, S.get()))
    top1.mainloop()


def change_color():
    with open(r'../config.json', 'r+') as f:
        #m = f.readlines()
    #for i in range(len(m)):
        #n = json.loads(m[i])
        return json.load(f)
color=change_color()["bgcolor"]  #界面的颜色
color1=change_color()["ntcolor"]#notebook被选中的颜色

# data={"bgcolor": "green",
#   "ntcolor": "pink"}
#
#
# def change_config():
#     with open(r'../config.json', 'w') as f:
#         json.dump(data,f)