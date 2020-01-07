from setuptools import setup

setup(
    name='hachinai_search',
    version='0.01',
    packages=['hachinai_search'],
    url='https://github.com/kibehiro/hachinai-search',
    license='MIT',
    author='KIBE',
    description='ハチナイのカードデータを検索できるWebアプリ',
    install_requires=['flask', 'python-dotenv']
)
