from tkinter import *
from tkinter import ttk
import json


def log_gui(root):
    top1 = Toplevel(master=root)  # 创建弹出式窗体
    # top1.attributes("-toolwindow", 1)
    # top1.wm_attributes("-topmost", 1)
    # 使弹出窗口一直处于主窗口前面
    top1.transient(root)
    # 将top1设置为模式对话框，top1不关闭无法操作主窗口
    top1.grab_set()
    top1.title('下载日志')
    top1.iconbitmap(r'../image/下载日志.ico')
    w = 400
    h = 300
    ws, hs = top1.winfo_screenwidth(), top1.winfo_screenheight()
    top1.geometry("%dx%d+%d+%d" %
                  (w, h, (ws / 2) - (w / 2), (hs / 2) - (h / 2)))
    #top1.resizable(0, 0)
    # 滚动条
    scrollBar = Scrollbar(top1)

    scrollBar.pack(side=RIGHT, fill=Y)
    # 定义表格界面
    tree_date = ttk.Treeview(
        top1,
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
    tree_date.pack(side=LEFT, fill=Y)
    # Treeview组件与垂直滚动条结合
    scrollBar.config(command=tree_date.yview)
    tree_date.config(yscrollcommand=scrollBar.set)
    # 将日志数据写入界面
    with open(r'../log.json', 'r+') as f:
        m = f.readlines()
    for i in range(len(m)):
        n = json.loads(m[i])
        tree_date.insert('', i, values=(n["time"], n["link"], n["status"]))

    top1.mainloop()
