from distutils.core import setup

setup(
    name="chaojibaizhan", # 对外发布的模块名称
    version="1.0", # 版本号
    description='这是第一个对外发布的模块，里面是一些加减法，只用于测试',
    author="gaoqi", # 作者
    author_email='gaoqi110@163.com', # 作者邮箱
    py_modules=['chaojibaizhan.demo','chaojibaizhan.demo3']  # 要发布的模块

)