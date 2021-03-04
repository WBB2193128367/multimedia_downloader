from tkinter import *


def cut(editor, event=None):
    editor.event_generate("<<Cut>>")


def copy(editor, event=None):
    editor.event_generate("<<Copy>>")


def paste(editor, event=None):
    editor.event_generate('<<Paste>>')


def rightKey(menubar, event, editor):
    menubar.delete(0, END)
    menubar.add_command(label='复制', command=lambda: copy(editor))
    menubar.add_command(label='剪切', command=lambda: cut(editor))
    menubar.add_command(label='粘贴', command=lambda: paste(editor))
    menubar.post(event.x_root, event.y_root)
