from distutils.core import setup
from setuptools import setup, find_packages
setup(
    name = 'qobs',
    version = '0.0.2',
    keywords = ('obs', 'huaweiyun'),
    description = 'self module for quickly uploading or downloading folders from ali oss',
    license = 'MIT License',
    author = 'zwy',
    python_require=">=3.5",
    install_requires=['huawei-obs','tqdm'],
    author_email = 'zuowangyang@foxmail.com',
    packages = find_packages("./src"),# 需要打包的package,使用find_packages 来动态获取package，exclude参数的存在，使打包的时候，排除掉这些文件
    platforms = 'any',
    package_dir={"":"src"},
    include_package_data = True,
)