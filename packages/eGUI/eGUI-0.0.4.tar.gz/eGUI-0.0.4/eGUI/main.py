import PySimpleGUI as Sg
from .interface.登录 import 登录界面


def 主题列表():
    """界面主题列表"""
    return Sg.theme_list()


def 主题界面():
    """界面主题显示"""
    Sg.theme_previewer()
