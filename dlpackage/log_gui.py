from tkinter import *
from tkinter import ttk
import threading
import json



#日志的界面
def log_gui(root):
    top1 = Toplevel(master=root)  # 创建弹出式窗体
    top1.withdraw()
    top1.update()
    # w = 400
    # h = 300
    # ws, hs = top1.winfo_screenwidth(), top1.winfo_screenheight()
    # top1.geometry("%dx%d+%d+%d" %
    #               (w, h, (ws / 2) - (w / 2), (hs / 2) - (h / 2)))
    ws, hs = root.winfo_rootx(), root.winfo_rooty()
    wss = ws + 125
    hss = hs + 65
    top1.geometry("400x320" + "+" + str(wss) + "+" + str(hss))
    top1.deiconify()
    # top1.attributes("-toolwindow", 1)
    # top1.wm_attributes("-topmost", 1)
    # 使弹出窗口一直处于主窗口前面
    top1.transient(root)
    # 将top1设置为模式对话框，top1不关闭无法操作主窗口
    top1.grab_set()
    top1.title('下载日志')
    top1.iconbitmap(r'../image/下载日志.ico')
    # 滚动条
    scrollBary = Scrollbar(top1, orient=VERTICAL)
    scrollBarx = Scrollbar(top1, orient=HORIZONTAL)
    scrollBary.pack(side=RIGHT, fill=Y)
    scrollBarx.pack(side=BOTTOM, fill=X)
    # 定义表格界面
    tree_date = ttk.Treeview(

        top1,
        style="myname.Treeview",
        columns=(
            'time',
            'link',
            'status'),
        show="headings")
    tree_date.pack()
    # 设置列宽度
    tree_date.column('time', width=100, anchor='center')
    tree_date.column('link', width=200, anchor='center')
    tree_date.column('status', width=80, anchor='center')
    # 添加列名
    tree_date.heading('time', text='下载时间')
    tree_date.heading('link', text='下载链接')
    tree_date.heading('status', text='下载状态')
    tree_date.pack(fill=BOTH, expand=True)
    # Treeview组件与垂直滚动条结合
    scrollBary.config(command=tree_date.yview)
    scrollBarx.config(command=tree_date.xview)
    tree_date.config(yscrollcommand=scrollBary.set)
    tree_date.config(xscrollcommand=scrollBarx.set)
    #读取日志的函数
    start_download(tree_date)
    top1.mainloop()




def read_log(tree_date):
    with open(r'../log.json', 'r+') as f:
        m = f.readlines()
    for i in range(len(m)):
        n = json.loads(m[i])
        tree_date.insert('', i, values=(n["time"], n["link"], n["status"]))



def start_download(tree_date):
    # 将日志数据写入界面(使用一个线程，防止日志界面卡死)
    t = threading.Thread(
        target=read_log, args=(
            tree_date,))
    # 设置守护线程，进程退出不用等待子线程完成
    t.setDaemon(True)
    t.start()
