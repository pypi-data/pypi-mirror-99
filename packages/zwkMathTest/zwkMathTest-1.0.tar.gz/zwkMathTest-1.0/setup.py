from distutils.core import setup
setup(
    name='zwkMathTest', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='zwk', # 作者
    author_email='18235140257@163.com', py_modules=['zwkMathTest.test1','zwkMathTest.test2'] # 要发布的模块
)