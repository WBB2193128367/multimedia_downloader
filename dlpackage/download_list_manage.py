from tkinter import *
from dlpackage import share
from dlpackage import right_kye
import tkinter.messagebox
import threading

#定义的一些全局变量
name={}
id_list=[]
url={}
i=1



def add_url(root,tree_date):
    top1 = Toplevel(master=root)  # 创建弹出式窗体
    top1.withdraw()
    top1.update()
    w = 250
    h = 180
    ws, hs = top1.winfo_screenwidth(), top1.winfo_screenheight()
    top1.geometry("%dx%d+%d+%d" %
                  (w, h, (ws / 2) - (w / 2), (hs / 2) - (h / 2)))
    top1.deiconify()
    # 使弹出窗口一直处于主窗口前面
    top1.transient(root)
    # 将top1设置为模式对话框，top1不关闭无法操作主窗口
    top1.grab_set()
    top1.title('添加链接')
    top1.iconbitmap(r'../image/主窗口.ico')
    label1=Label(top1,text='媒体名称:')
    label1.place(x=10,y=20)
    entry1=Entry(top1)
    entry1.place(x=70,y=20)
    label2 = Label(top1, text='URL:')
    label2.place(x=10, y=70)
    entry2 = Entry(top1)
    entry2.place(x=70, y=70)
    button=Button(top1,text='确认添加',bg='blue')
    button.place(x=95,y=125)
    button.bind("<Button-1>", lambda x:add(top1,tree_date,entry1,entry2) )
    menubar = Menu(top1, tearoff=False)
    # 将entry和rightkey事件绑定
    entry1.bind("<Button-3>", lambda x: right_kye.rightKey(menubar, x, entry1))
    entry2.bind("<Button-3>", lambda x: right_kye.rightKey(menubar, x, entry2))
    top1.mainloop()




def add(top1,tree_date,entry1,entry2):
    global name
    global url
    global i
    global id_list
    if entry1.get()=='' or entry2.get()=='':
        t = threading.Thread(
            target=share.m3.waring_info, args=(
                '媒体名称和URI不能为空哦!',))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        return
    if share.check_href(entry2.get().strip())==False:
        t = threading.Thread(
                target=share.m3.waring_info, args=(
                    'URL不合法哦!',))
        # 设置守护线程，进程退出不用等待子线程完成
        t.setDaemon(True)
        t.start()
        return

    name['I%03d' %i]=entry1.get().strip()
    url['I%03d'%i]=entry2.get().strip()
    id_list.append('I%03d' %i)
    tree_date.insert('', i, values=(entry1.get().strip(),entry2.get().strip()))
    i+=1
    top1.destroy()



def delete(tree_date):
    global name
    global url
    global id_list
    selection=tree_date.selection()
    if selection==():
        share.m3.waring_info("还没有选中的数据哦！")
    else:
        flag=tkinter.messagebox.askyesno('提示信息','确认删除选中数据吗？')
        if flag:
            for item in selection:
                if share.exeing_id==item:
                    share.m3.waring_info(name[share.exeing_id]+'正在下载中，不能删除噢!')
                else:
                    tree_date.delete(item)
                    name.pop(item)
                    url.pop(item)
                    id_list.remove(item)


def delete_item(tree_date,item):
    selection = tree_date.get_children()
    for i in selection:
        if i==item:
           tree_date.delete(i)


def delete_thread():
    thread=threading.Thread(target=delete,args=(share.m3.tree_date,))
    thread.setDaemon(True)
    thread.start()