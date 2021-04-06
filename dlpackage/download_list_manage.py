from tkinter import *
from dlpackage import share
from dlpackage import right_kye
import tkinter.messagebox
import threading
from PIL import ImageTk, Image
#定义的一些全局变量
name={}
id_list=[]
url={}
i=1
m=[]


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
    top1.configure(bg='#bbdefb')
    label1=Label(top1,text='媒体名称:',bg='#bbdefb')
    label1.place(x=10,y=20)
    entry1=Entry(top1)
    entry1.place(x=70,y=20)
    label2 = Label(top1, text='URL:',bg='#bbdefb')
    label2.place(x=10, y=70)
    entry2 = Entry(top1)
    entry2.place(x=70, y=70)
    load3 = Image.open("../image/8.png")
    render3 = ImageTk.PhotoImage(load3)
    img3 = Label(top1, image=render3,bg='#bbdefb')
    img3.place(x=90, y=120)
    img3.bind("<Button-1>", lambda x:add(top1,tree_date,entry1,entry2) )
    menubar = Menu(top1, tearoff=False)
    # 将entry和rightkey事件绑定
    entry1.bind("<Button-3>", lambda x: right_kye.rightKey(menubar, x, entry1))
    entry2.bind("<Button-3>", lambda x: right_kye.rightKey(menubar, x, entry2))
    top1.mainloop()



# def treeviewClick(tree):  # 单击
#     global m
#     for item in tree.selection():
#         item_text = tree.item(item, "tags")
#         if item_text[0] not in m:
#             tree.tag_configure(item_text[0], background='purple')
#             m.append(item_text[0])
#         elif item_text[0] in m:
#             tree.tag_configure(item_text[0], background='white')
#             m.remove(item_text[0])


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
    # tree_date.tag_bind(i, '<Button-1>', lambda x:treeviewClick(tree_date))
    i+=1
    top1.destroy()



def delete(tree_date):
    global name
    global url
    global m
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
            m=[]

def delete_item(tree_date,item):
    selection = tree_date.get_children()
    for i in selection:
        if i==item:
           tree_date.delete(i)


def delete_thread():
    thread=threading.Thread(target=delete,args=(share.m3.tree_date,))
    thread.setDaemon(True)
    thread.start()

