from dlpackage import share
from dlpackage import log_gui
from dlpackage import setting_gui
from dlpackage import download_list_manage
import tkinter.messagebox
from tkinter import ttk
from tkinter import *
import tkinter.font as tf


class Multimedia_Downloader:
    def __init__(self, title="多媒体下载器"):
        #########################################      对主窗口的设置     ############
        self.root = Tk()
        self.root.withdraw()
        self.root.update()
        self.w = 550
        self.h = 450
        ws, hs = self.root.winfo_screenwidth(), self.root.winfo_screenheight()  # 获取屏幕的的大小
        self.root.geometry('%dx%d+%d+%d' % (self.w,
                                            self.h,
                                            (ws / 2) - (self.w / 2),
                                            (hs / 2) - (self.h / 2)))  # 设置主窗口的大小和默认显示位置
        self.root.deiconify()
        self.title = title  # 主窗口的标题
        self.root.title("%s" % (self.title))
        self.root.iconbitmap(r'../image/主窗口.ico')  # 对主窗口图标进行设置

        self.root.resizable(0, 0)  # 固定主窗口的大小
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: share.close_windows(
                self.root))  # 关闭窗口时进行提示是否关闭，防止误操作
##########################################################################


####################################################   对菜单栏的设计   #########
        self.menubar = Menu(self.root)  # 定义一个菜单栏
        #self.file = Menu( self.menubar,tearoff=0)
        self.menubar.add_cascade(
            label='设置',
            command=lambda: setting_gui.set(
                self.root))
        self.menubar.add_cascade(
            label='日志',
            command=lambda: log_gui.log_gui(
                self.root))
        self.menubar.add_cascade(label='关于', command=setting_gui.guanyu)
        self.root.config(menu=self.menubar)
##########################################################################


##################################################   对界面进行布局    ##########
        style = ttk.Style(self.root)
        style.configure('lefttab.TNotebook', tabposition='wn')
        self.notebook = ttk.Notebook(
            self.root,
            style='lefttab.TNotebook',
            width='450',
            height='425')
        self.f1 = Frame(self.notebook)
        self.label = Label(
            self.f1,
            text="多媒体下载器\n作者：WBB\n指导老师:李慧旻",
            font=(
                '华为宋体',
                20))
        self.label.place(x=110, y=150)
        self.f2 = Frame(self.notebook)
        self.ff=Frame(self.notebook)
        self.f3 = Frame(self.notebook)
        self.f4 = Frame(self.notebook)
        self.notebook.add(self.f1, text='首页')
        self.notebook.add(self.f2, text='下载页面')
        self.notebook.add(self.ff, text='列表管理')


        # 滚动条
        self.scrollBary = Scrollbar(self.ff, orient=VERTICAL)
        self.scrollBarx = Scrollbar(self.ff, orient=HORIZONTAL)
        self.scrollBary.pack(side=RIGHT, fill=Y)
        self.scrollBarx.pack(side=BOTTOM, fill=X)
        # 定义表格界面
        self.tree_date = ttk.Treeview(
            self.ff,
            columns=(
                'name',
                'url',),
            height=17,
            show="headings")
        self.tree_date.pack()
        # 设置列宽度
        self.tree_date.column('name', width=40,anchor='center')
        self.tree_date.column('url', width=260, anchor='center')
        # 添加列名
        self.tree_date.heading('name', text='文件名称')
        self.tree_date.heading('url', text='下载链接')
        self.tree_date.pack(fill=BOTH)
        # Treeview组件与垂直滚动条结合
        self.scrollBary.config(command=self.tree_date.yview)
        self.scrollBarx.config(command=self.tree_date.xview)
        self.tree_date.config(yscrollcommand=self.scrollBary.set)
        self.tree_date.config(xscrollcommand=self.scrollBarx.set)
        self.button1 = Button(
            self.ff, text='添加链接', width=8, font=(
                "Lucida Grande", 11), bg='blue')
        self.button1.place(x=120,y=375)
        self.button2 = Button(
            self.ff, text='删除链接', width=8, font=(
                "Lucida Grande", 11), bg='blue')
        self.button2.place(x=250, y=375)
        # 将日志数据写入界面(使用一个线程，防止日志界面卡死)


        self.notebook.add(self.f3, text='源码地址')
        self.label = Label(self.f3, text='Github地址:', font=('华为宋体', 15))
        self.ft = tf.Font(family='华为宋体', size=15, underline=1)
        self.label1 = Label(
            self.f3,
            cursor='plus',
            text='https://github.com/\nWBB2193128367/\nmultimedia_downloader',
            font=self.ft,
            justify='left',
            fg='blue')
        self.label.place(x=60, y=150)
        self.label1.place(x=170, y=150)
        self.notebook.add(self.f4, text='问题反馈')
        self.label = Label(
            self.f4,
            text="邮箱地址:2193128367@qq.com",
            font=(
                '华为宋体',
                15))
        self.label.place(x=90, y=150)
        self.notebook.pack()
##########################################################################


################################################    功能区界面的设计    ##########

        self.frm = LabelFrame(
            self.f2,
            width=430,
            height=205,
            padx=10,
            text="功能区")
        self.frm.place(x=10, y=5)
        self.label7=Label(
            self.frm,
            text="多媒体地址:",
            font=(
                "Lucida Grande",
                11)).place(
            x=0,
            y=0)
        self.button_url = Entry(self.frm, width=45)
        self.button_url.place(x=0, y=25)

        self.label8=Label(
            self.frm,
            text="媒体命名为:(无需后缀名)",
            font=(
                "Lucida Grande",
                11)).place(
            x=0,
            y=50)
        self.button_video_name = Entry(self.frm, width=45)
        self.button_video_name.place(x=0, y=75)

        self.v = IntVar()
        self.cb_status = IntVar()
        self.v.set(1)
        self.rb1 = Radiobutton(
            self.frm,
            text='速度优先',
            variable=self.v,
            value=1,
            font=(
                "Lucida Grande",
                11))
        self.rb2 = Radiobutton(
            self.frm,
            text='画质优先',
            variable=self.v,
            value=2,
            font=(
                "Lucida Grande",
                11))
        self.cb = Checkbutton(
            self.frm,
            text='保存源文件',
            variable=self.cb_status,
            font=(
                "Lucida Grande",
                11))
        self.rb1.place(x=0, y=95)
        self.rb2.place(x=100, y=95)
        self.cb.place(x=200, y=95)
        self.m = StringVar()
        self.button_pause = Button(
            self.frm, textvariable=self.m, width=8, font=(
                "Lucida Grande", 11), bg='blue')
        self.m.set('暂停下载')
        #self.button_pause.place(x=330, y=15)

        self.button_start = Button(
            self.frm, text="开始下载", width=8, font=(
                "Lucida Grande", 11), bg='blue')
        self.button_start.place(x=330, y=23)

        self.button_cancel = Button(
            self.frm, text="取消下载", width=8, font=(
                "Lucida Grande", 11), bg='blue')
        #self.button_cancel.place(x=330, y=77)

        self.button_again = Button(
            self.frm, text="重试", width=8, font=(
                "Lucida Grande", 11), bg='blue')
        self.button_again.place(x=330, y=73)

        Label(
            self.frm,
            text="下载进度:",
            font=(
                "Lucida Grande",
                11)).place(
            x=0,
            y=125)
        self.c=StringVar()
        Label(
            self.frm,
            fg='blue',
            textvariable=self.c,
            font=(
                "Lucida Grande",
                11)).place(
            x=70,
            y=125)
        self.progress = ttk.Progressbar(
            self.frm,
            orient="horizontal",
            length=355,
            mode="determinate")
        self.progress.place(x=0, y=150)
        self.progress["maximum"] = 100
        self.progress["value"] = 0
        self.str = StringVar()
        self.lb = Label(self.frm, textvariable=self.str)
        self.lb.place(x=357, y=150)
##########################################################################


###########################################################   消息界面的设计   ##

        self.message_frm = LabelFrame(
            self.f2,
            width=400,
            height=200,
            padx=10,
            text="消息")
        self.message_frm.place(x=10, y=210)

        self.scrollbar = Scrollbar(self.message_frm)
        self.scrollbar.pack(side='right', fill='y')
        self.message_v = StringVar()
        self.message_s = ""
        self.message_v.set(self.message_s)

        self.message = Text(self.message_frm, width=55, height=14)
        self.message.insert('insert', self.message_s)
        self.message.pack(side='left', fill='y')
        # 以下两行代码绑定text和scrollbar
        self.scrollbar.config(command=self.message.yview)
        self.message.config(yscrollcommand=self.scrollbar.set)
        self.message.config(state=DISABLED)
#########################################################################点

        self.menubar = Menu(self.root, tearoff=False)

    # 给消息框输入消息并且保证消息一直在底部

    def alert(self, m):
        print("%s" % m)
        if m:
            self.message.config(state=NORMAL)
            self.message.insert(END, m + "\n")
            # 确保scrollbar在底部
            self.message.see(END)
            self.message.config(state=DISABLED)
        self.root.update()

    # 清空消息框
    def clear_alert(self):
        self.message.config(state=NORMAL)
        self.message.delete('1.0', 'end')
        self.message.config(state=DISABLED)
        self.root.update()

    # 弹出提示框

    def show_info(self, m):
        tkinter.messagebox.showinfo("提示", m)
    # 弹出警告框

    def waring_info(self, m):
        tkinter.messagebox.showwarning('警告！', m)
