
from setuptools import setup, find_packages  

setup(  
    name = 'Pyomic',  
    version = '1.0.1',
    # keywords = ('chinesename',),  
    description = 'A python module that could analysis the ERGs',  
    license = 'MIT License',  
    install_requires = ['ERgene','numpy','pandas','matplotlib','sklearn','scipy','networkx','seaborn','datetime'],  
    packages = ['Pyomic'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'ZehuaZeng',  
    author_email = 'Starlitnightly@163.com',
    url = 'https://github.com/Starlitnightly/Pyomic',
    # packages = find_packages(include=("*"),),  
)  
