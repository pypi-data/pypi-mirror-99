import setuptools

setuptools.setup(
    name = 'chinese_chess',     #库文件的名字
    version = '0.0.1',       #库的版本
    author = 'Young_shool',    #我的姓名
    author_eamil = 'cxy_ypp@stud.tjut.edu.cn',   #邮箱
    description = 'This is my college project',   #简介
    url = 'https://github.com',
    packages = setuptools.find_packages(),
    #license = 'MIT License',
    include_packet_data = True,
    install_requires = [],
)