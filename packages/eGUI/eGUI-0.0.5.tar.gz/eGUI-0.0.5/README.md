# eGUI
[![pypi version](https://aliplayervideo.oss-cn-beijing.aliyuncs.com/GitHub%E5%9B%BE%E7%89%87/%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9logo.png)](https://space.bilibili.com/365335499)

基于Python的GUI界面，函数使用中文命名，使用简单，界面丰富，上手方便，持续更新。

## 安装
***
```python
pip install eGUI
```
## 界面效果
***
![](https://aliplayervideo.oss-cn-beijing.aliyuncs.com/GitHub%E5%9B%BE%E7%89%87/1.png)

![](https://aliplayervideo.oss-cn-beijing.aliyuncs.com/GitHub%E5%9B%BE%E7%89%87/2.png)
## 运行效果

![](https://aliplayervideo.oss-cn-beijing.aliyuncs.com/GitHub%E5%9B%BE%E7%89%87/4.png)

![](https://aliplayervideo.oss-cn-beijing.aliyuncs.com/GitHub%E5%9B%BE%E7%89%87/5.png)

## 主题效果
***
![](https://aliplayervideo.oss-cn-beijing.aliyuncs.com/GitHub%E5%9B%BE%E7%89%87/3.png)


## 代码
***

```python
import eGUI

""" 用户登录 """
用户密码字典 = {"123": "456", "789": "654"}  # 用户名密码为文本类型
登录返回结果 = eGUI.登录界面("我的登录", 用户密码字典)
print(登录返回结果)

""" 切换登录界面 """
用户密码字典 = {"123": "456", "789": "654"}  # 用户名密码为文本类型
登录返回结果 = eGUI.登录界面("我的登录", 用户密码字典, 主题="Black")
print(登录返回结果)

""" 界面主题查询 """
print(eGUI.主题列表())
eGUI.主题界面()

```
***
### 0.0.5版本 2021年3月20日更新

- 1.登录界面
- 2.主题列表
- 3.主题界面视图

修改部分引导错误