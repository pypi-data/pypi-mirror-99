import PySimpleGUI as Sg


def 登录界面(窗口标题: str, 用户名_密码_字典: dict, 主题: str = "Python"):
    """简单登录界面

    :param 窗口标题: 窗口标题名称
    :param 用户名_密码_字典: 查询字典
    :param 主题: 默认使用Python主题
    :return: 返回登录的用户名和密码
    """
    Sg.theme(主题)
    login_layout = [
        [Sg.Frame(layout=[
            [Sg.Text('账户'), Sg.Input(key="username")],
            [Sg.Text('密码'), Sg.Input(key="password", password_char="*")],
            [Sg.Button("登录")]
        ], title="登录账户")],
    ]
    login_window = Sg.Window(窗口标题, login_layout)
    while True:
        event, values = login_window.read()
        if event == Sg.WIN_CLOSED:
            break
        elif event == "登录":
            for i in 用户名_密码_字典:
                user = values['username']
                password = values['password']
                if user == i and password == 用户名_密码_字典[i]:
                    Sg.popup('登录成功!')
                    login_window.close()
                    return user, password
            else:
                Sg.popup('用户名或登录失败!', text_color='red')
                login_window['password'].update("")

