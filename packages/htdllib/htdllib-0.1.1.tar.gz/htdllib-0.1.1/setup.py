import setuptools
setuptools.setup(
    name='htdllib',#库名
    version='0.1.1',#版本号，建议一开始取0.0.1
    author='haowen zhang',#你的名字，名在前，姓在后，例：张一一 Yiyi Zhang
    author_email='806670753@qq.com',#你的邮箱（任何邮箱都行，只要不是假的）
    description='又一次……',#库介绍
    long_descripition_content_type="text/markdown",
    url='https://github.com/',
    packages=setuptools.find_packages(),
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent" ,
    ],
)