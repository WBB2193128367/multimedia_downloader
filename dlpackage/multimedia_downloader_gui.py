from dlpackage import share
from dlpackage import log_gui
from dlpackage import setting_gui
from dlpackage import floating_window
import tkinter.messagebox
from tkinter import ttk
from tkinter import *
import tkinter.font as tf
from PIL import ImageTk, Image

class Multimedia_Downloader:
    def __init__(self, title="多媒体下载器"):
        #########################################      对主窗口的设置     ###############################################################
        self.root = Tk()
        self.root.withdraw()
        self.root.update()
        self.w = 650
        self.h = 550
        ws, hs = self.root.winfo_screenwidth(), self.root.winfo_screenheight()  # 获取屏幕的的大小
        self.root.geometry('%dx%d+%d+%d' % (self.w,
                                            self.h,
                                            (ws / 2) - (self.w / 2),
                                            (hs / 2) - (self.h / 2)))  # 设置主窗口的大小和默认显示位置
        self.root.deiconify()
        self.title = title  # 主窗口的标题
        self.root.title("%s" % (self.title))
        self.root.configure( bg='#bbdefb')
        self.root.iconbitmap(r'../image/主窗口.ico')  # 对主窗口图标进行设置
        self.root.resizable(0, 0)  # 固定主窗口的大小
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: share.close_windows(
                self.root))  # 关闭窗口时进行提示是否关闭，防止误操作
        self.style = ttk.Style(self.root)
######################################################################################################################################


####################################################   对菜单栏的设计   #################################################################
        self.menubar = Menu(self.root)  # 定义一个菜单栏
        #self.file = Menu( self.menubar,tearoff=0)
        self.menubar.add_cascade(
            label='设置',
            command=lambda: setting_gui.set(
                self.root,self.button_url,self.button_video_name))
        self.menubar.add_cascade(
            label='日志',
            command=lambda: log_gui.log_gui(
                self.root))
        self.menubar.add_cascade(label='关于', command=setting_gui.guanyu)
        self.root.config(menu=self.menubar)
#######################################################################################################################################



#################################################    对主界面的布局    ###################################################################


        self.style.theme_create("wbb", parent="alt", settings={
            "TNotebook.Tab": {
                "configure": {"padding": [10, 10], "background":"#bbdefb",'font':'仿宋'},
                "map": {"background": [("selected","#00FFFF")],"font": [("selected", '黑体')],
                        }
            },
            "Treeview":{
                "map": {"background": [("selected","#00FFFF")],"font": [("selected", '黑体')],}
            },
        })


        self.style.theme_use("wbb")

        self.style.configure('my.TNotebook', tabposition='wn',background='#bbdefb')
        self.style.configure("Treeview", background="white",
                        foreground="black", )
        self.notebook = ttk.Notebook(
            self.root,
            padding=2,
            style='my.TNotebook',
            width='470',
            height='425')
        self.notebook.pack(fill=tkinter.BOTH,expand=True)
########################################################################################################################################



################################################   首页的界面         ####################################################################
        self.f1 = Frame(self.notebook, bg='#bbdefb')
        self.label = Label(
            self.f1,
            text="多媒体下载器",
            bg='#bbdefb',
            font=(
                '华文彩云',
               40))
        self.label.place(x=115, y=95)
        self.label = Label(
            self.f1,
            text="作者:王保保",
            bg='#bbdefb',
            font=(
                '方正舒体',
                18))
        self.label.place(x=300, y=285)
        self.label = Label(
            self.f1,
            text="指导老师:李慧旻",
            bg='#bbdefb',
            font=(
                '方正舒体',
                18))
        self.label.place(x=300, y=320)


        self.notebook.add(self.f1, text='首页')
#########################################################################################################################################




##############################################   下载页面           #######################################################################

############################    功能区界面的设计     ###########################
        self.f2 = Frame(self.notebook, bg='#bbdefb')
        self.frm = LabelFrame(
            self.f2,
            width=528,
            height=260,
            bg='#bbdefb',
            padx=10,
            text="功能区",
            font = (
            "黑体",10)
               )
        self.frm.place(x=7, y=258)
        self.label7 = Label(
            self.frm,

            text="多媒体地址:",
            bg='#bbdefb',
            font=(
                "黑体",
                11)).place(
            x=0,
            y=15)
        self.button_url =Entry(self.frm, width=50)
        self.button_url.place(x=0, y=40)

        self.label8 = Label(
            self.frm,

            bg='#bbdefb',
            text="媒体命名为:(无需后缀名)",
            font=(
                "黑体",
                11)).place(
            x=0,
            y=80)
        self.button_video_name = Entry(self.frm, width=50)
        self.button_video_name.place(x=0, y=105)

        self.v = IntVar()
        self.cb_status = IntVar()
        self.v.set(1)
        self.rb1 = Radiobutton(
            self.frm,
            text='速度优先',
            bg='#bbdefb',
            variable=self.v,
            value=1,
            font=(
                "黑体",
                11))
        self.rb2 = Radiobutton(
            self.frm,
            text='画质优先',
            bg='#bbdefb',
            variable=self.v,
            value=2,
            font=(
                "黑体",
                11))
        self.cb = Checkbutton(
            self.frm,
            text='保存源文件',
            bg='#bbdefb',
            variable=self.cb_status,
            font=(
                "黑体",
                11))
        self.rb1.place(x=0, y=140)
        self.rb2.place(x=100, y=140)
        self.cb.place(x=200, y=140)
        self.m = StringVar()
        self.button_pause = Button(
            self.frm, textvariable=self.m, width=8, font=(
                "Lucida Grande", 11), bg='blue')
        self.m.set('暂停下载')
        # self.button_pause.place(x=330, y=15)


        #开始下载按钮
        self.load = Image.open("../image/3.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self.frm, image=self.render,bg='#bbdefb')
        self.img.place(x=380, y=23)

        self.button_cancel = Button(
            self.frm, text="取消下载", width=8, font=(
                "Lucida Grande", 11), bg='cadetblue')
        # self.button_cancel.place(x=330, y=77)

        self.load1 = Image.open("../image/4.png")
        self.render1 = ImageTk.PhotoImage(self.load1)
        self.img1 = Label(self.frm, image=self.render1, bg='#bbdefb')
        self.img1.place(x=398, y=83)

        Label(
            self.frm,
            text="下载进度:",
            bg='#bbdefb',
            font=(
                "黑体",
                11)).place(
            x=0,
            y=175)
        self.c = StringVar()
        Label(
            self.frm,
            bg='#bbdefb',
            fg='blue',
            textvariable=self.c,
            font=(
                "黑体",
                11)).place(
            x=78,
            y=175)
        self.progress = ttk.Progressbar(
            self.frm,
            orient="horizontal",
            length=430,
            mode="determinate")
        self.progress.place(x=0, y=200)
        self.progress["maximum"] = 100
        self.progress["value"] = 0
        self.str = StringVar()
        self.lb = Label(self.frm, textvariable=self.str, bg='#bbdefb',fg='blue', font=(
            "黑体",
            11))
        self.lb.place(x=440, y=200)
##########################################################################

#####################    消息区界面的设计   #################################

        self.message_frm = LabelFrame(
            self.f2,
            bg='#bbdefb',
            width=528,
            height=255,
            padx=10,
            font=(
                "黑体",
                10),
            text="消息")
        self.message_frm.place(x=7, y=3)

        self.scrollbar = Scrollbar(self.message_frm)
        self.scrollbar.pack(side='right', fill='y')
        self.message_v = StringVar()
        self.message_s = ""
        self.message_v.set(self.message_s)

        self.message = Text(self.message_frm, width=69, height=18)
        self.message.insert('insert', self.message_s)
        self.message.pack(side='left', fill='y')
        # 以下两行代码绑定text和scrollbar
        self.scrollbar.config(command=self.message.yview)
        self.message.config(yscrollcommand=self.scrollbar.set)
        self.message.config(state=DISABLED)
########################################################################

        self.notebook.add(self.f2,text='下载页面')
############################################################################################################################



################################################    列表管理界面的设计   ######################################################
        self.ff = Frame(self.notebook, bg='#bbdefb')
        # 定义表格界面
        self.tree_date = ttk.Treeview(
            self.ff,
            style="myname.Treeview",
            columns=(
                'name',
                'url',),
            height=33,
            show="headings")
        # 滚动条
        self.scrollBary = Scrollbar(self.tree_date, orient=VERTICAL)
        self.scrollBarx = Scrollbar(self.tree_date, orient=HORIZONTAL)
        self.scrollBary.pack(side=RIGHT, fill=Y)
        self.scrollBarx.pack(side=BOTTOM, fill=X)
        # 设置列宽度
        self.tree_date.column('name', width=40,anchor='center')
        self.tree_date.column('url', width=260, anchor='center')
        # 添加列名
        self.tree_date.heading('name', text='文件名称')
        self.tree_date.heading('url', text='下载链接')
        self.tree_date.pack(fill=BOTH,ipady=190)
        # Treeview组件与垂直滚动条结合
        self.scrollBary.config(command=self.tree_date.yview)
        self.scrollBarx.config(command=self.tree_date.xview)
        self.tree_date.config(yscrollcommand=self.scrollBary.set)
        self.tree_date.config(xscrollcommand=self.scrollBarx.set)
        self.load2 = Image.open("../image/6.png")
        self.render2 = ImageTk.PhotoImage(self.load2)
        self.img2 = Label(self.ff, image=self.render2, bg='#bbdefb')
        self.img2.place(x=145, y=450)
        self.load3 = Image.open("../image/5.png")
        self.render3 = ImageTk.PhotoImage(self.load3)
        self.img3 = Label(self.ff, image=self.render3, bg='#bbdefb')
        self.img3.place(x=315, y=450)

        self.notebook.add(self.ff, text='列表管理')

########################################################################################################################



############################################    源码地址界面的设计      ####################################################
        self.f3 = Frame(self.notebook ,bg='#bbdefb')
        self.load5 = Image.open("../image/左.jpg").resize((150, 150))
        self.render5= ImageTk.PhotoImage(self.load5)
        self.img5 = Label(self.f3, image=self.render5, bg='#bbdefb')
        floating_window.CreateToolTip(self.img5, text='Github')
        self.img5.place(x=40, y=140)


        self.load6 = Image.open("../image/右.jpg").resize((150, 150))
        self.render6 = ImageTk.PhotoImage(self.load6)
        self.img6 = Label(self.f3, image=self.render6, bg='#bbdefb')
        floating_window.CreateToolTip(self.img6, text='Github')
        self.img6.place(x=355, y=150)


        self.load7 = Image.open("../image/链接.png").resize((150, 150))
        self.render7 = ImageTk.PhotoImage(self.load7)
        self.img7 = Label(self.f3, image=self.render7, bg='#bbdefb')
        self.img7.place(x=190, y=120)
        self.notebook.add(self.f3, text='源码地址')
        floating_window.CreateToolTip(self.img7, text='点我/扫我')
########################################################################################################################


###########################################    问题反馈界面的设计        ###################################################
        self.f4 = Frame(self.notebook, bg='#bbdefb')
        self.load4 = Image.open("../image/微信.png").resize((100,100))
        self.render4 = ImageTk.PhotoImage(self.load4)
        self.img4 = Label(self.f4, image=self.render4, bg='#bbdefb')
        floating_window.CreateToolTip(self.img4, text='微信:wbb2193128367')
        self.img4.place(x=120, y=150)

        self.load8 = Image.open("../image/QQ.png").resize((100, 100))
        self.render8 = ImageTk.PhotoImage(self.load8)
        self.img8 = Label(self.f4, image=self.render8, bg='#bbdefb')
        floating_window.CreateToolTip(self.img8, text='QQ:2193128367')
        self.img8.place(x=320, y=150)


        self.load9= Image.open("../image/0.png").resize((30, 30))
        self.render9 = ImageTk.PhotoImage(self.load9)
        self.img9 = Label(self.f4, image=self.render9, bg='#bbdefb')
        floating_window.CreateToolTip(self.img9, text='邮箱:2193128367@qq.com')
        self.img9.place(x=440, y=470)
        self.notebook.add(self.f4, text='问题反馈')

#######################################################################################################################

        #右键点击弹出框
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
