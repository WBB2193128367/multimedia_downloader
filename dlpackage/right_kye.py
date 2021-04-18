from tkinter import *

#剪切功能的实现
def cut(editor, event=None):
    editor.event_generate("<<Cut>>")

#复制功能的实现
def copy(editor, event=None):
    editor.event_generate("<<Copy>>")

#粘贴功能的实现
def paste(editor, event=None):
    editor.event_generate('<<Paste>>')

#右键帮定的函数
'''
使用的时候定义一个Menubar控件，然后将其传给rightkey()函数
'''
def rightKey(menubar, event, editor):
    menubar.delete(0, END)
    menubar.add_command(label='复制', command=lambda: copy(editor))
    menubar.add_separator()
    menubar.add_command(label='剪切', command=lambda: cut(editor))
    menubar.add_separator()
    menubar.add_command(label='粘贴', command=lambda: paste(editor))
    menubar.post(event.x_root, event.y_root)
