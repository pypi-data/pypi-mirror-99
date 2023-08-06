from setuptools import find_packages,setup
setup(
    name = 'sanic_rest_framework',
    version = '0.0.1',
    packages = find_packages(),
    description="Sanic rest api framework Similar to DRF ",
    author="WangLaoSi",
    author_email='103745315@qq.com',
    url="https://gitee.com/Wang_LaoSi/sanic_rest_framework",
    download_url='https://gitee.com/Wang_LaoSi/sanic_rest_framework/repository/archive/master.zip',
    install_requires = ['sainc','tortoise-orm']
)