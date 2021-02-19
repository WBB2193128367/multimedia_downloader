from tkinter import messagebox
import tkinter.filedialog
from tkinter import ttk
from tkinter import *


# 默认的媒体文件存储位置
path = '../videos'
# 默认的线程数
threading_count = 60

# 关于的驱动方法

#关于的事件
def guanyu():
    tkinter.messagebox.showinfo('提示', '该软件由WBB开发，仅供学习使用！！！')

#生成线程数范围列表
def generate_list(arg):
    a=[]
    for i in range(1,arg+1):
        a.append(i)
    return a


#点击确认按钮时的事件
def print_selection(root, top1, entry, combobox, v):
    global path
    global threading_count
    threading_count = int(combobox.get())
    if entry.get() == '':
        pass
    else:
        path = entry.get()
    root.attributes("-alpha", 1 - v)
    top1.destroy()



#浏览的事件
def liulan(str4):
    m = tkinter.filedialog.askdirectory()
    str4.set(m)


# 设置页面
def set(root):
    top1 = Toplevel(master=root)  # 创建弹出式窗体
    # top1.attributes("-toolwindow", 1)
    # top1.wm_attributes("-topmost", 1)
    #使弹出窗口一直处于主窗口前面
    top1.transient(root)
    #将top1设置为模式对话框，top1不关闭无法操作主窗口
    top1.grab_set()
    top1.title('设置页面')
    top1.iconbitmap(r'../image/设置窗口.ico')
    w = 400
    h = 300
    ws, hs = top1.winfo_screenwidth(), top1.winfo_screenheight()
    top1.geometry("%dx%d+%d+%d" %
                  (w, h, (ws / 2) - (w / 2), (hs / 2) - (h / 2)))
    top1.resizable(0, 0)
    # 设置透明度
    lb0 = Label(top1, text="透明度设置:")
    lb0.place(x=3, y=10)
    lb2 = Label(top1, text="通过拖动下面滑块改变窗口透明度")
    lb2.place(x=100, y=10)

    lb = Label(top1, text="清晰")
    lb.place(x=100, y=40)
    lb1 = Label(top1, text="模糊")
    lb1.place(x=290, y=40)
    S = Scale(
        top1,
        from_=0,
        to=0.8,
        resolution=0.1,
        showvalue=0,
        orient=HORIZONTAL,
        length=150)
    S.place(x=132, y=40)

    lb0 = Label(top1, text="下载目录:")
    lb0.place(x=3, y=80)
    lb2 = Label(top1, text="使用指定的视频下载目录")
    lb2.place(x=100, y=80)
    # 存储路径
    str3 = StringVar()
    str3.set(path)
    entry = Entry(top1, textvariable=str3, width=14)
    entry.place(x=100, y=110)
    btn2 = Button(
        top1,
        text="选择目录",
        bg="purple",
        width=8,
        height=1,
        cursor='pirate',
        command=lambda: liulan(str3))
    btn2.place(x=210, y=107)
    # 线程数
    lb0 = Label(top1, text="线程数设置:")
    lb0.place(x=3, y=150)
    lb2 = Label(top1, text="通过下面设置线程的最大数量")
    lb2.place(x=100, y=150)
    lb3 = Label(top1, text="最大线程数为")
    lb3.place(x=100, y=180)
    combobox = ttk.Combobox(top1, width=5, state='readonly')
    combobox['values'] = generate_list(100)
    combobox.current(threading_count-1)
    combobox.place(x=180, y=180)
    lb3 = Label(top1, text="(1-100)")
    lb3.place(x=238, y=180)
    # 确认按钮
    btn = Button(
        top1,
        text="确认",
        bd=5,
        bg="purple",
        cursor='pirate',
        relief="raised",
        fg='black',
        width=5,
        height=1,
        compound=tkinter.CENTER,
        command=lambda: print_selection(root, top1, entry, combobox, S.get()))
    btn.place(x=170, y=230)
    top1.mainloop()
