from setuptools import setup, find_packages

from os import path
this_directory=path.abspath(path.dirname(__file__))
with open(path.join(this_directory,'README.md'),encoding='utf-8') as f:
	long_description=f.read()

setup(
	name='socpipe',
	version='0.0.6',
	description='very simple way of inter-process communication',
	long_description=long_description,
	long_description_content_type='text/markdown',
	maintainer='R. Nakano',
	maintainer_email='yukiakari@ichigo.me',
	url='https://github.com/kana-lab/socpipe/',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers'
	],
	keywords='inter-process, multi process, communication, マルチプロセス, プロセス間通信, rpc',
	package_dir={'':'src'},
	packages=find_packages(where='src'),
	python_requires='>=3.6, <4'
)
