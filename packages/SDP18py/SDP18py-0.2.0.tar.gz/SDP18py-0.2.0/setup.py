from setuptools import setup, find_packages
import os
import glob
import sys

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]


thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


def files(folder):
    for path in glob.glob(folder+'/*'):
        if os.path.isfile(path):
            yield path

data_files=[
            ('.', glob.glob(sys.prefix+'/DLLs/tix84*.dll')),
            ('tcl/tix8.4.3', files(sys.prefix+'/tcl/tix8.4.3/')),
            ('tcl/tix8.4.3/bitmaps', files(sys.prefix+'/tcl/tix8.4.3/bitmaps/')),
            ('tcl/tix8.4.3/pref', files(sys.prefix+'/tcl/tix8.4.3/pref/')),
           ]
setup(
	name='SDP18py',
	version='0.2.0',
	description='This package schedules surgeries using metaheurisitcs. It is a project done for in NUS for Systems Design Project (SDP):Metaheuristic Surgery Scheduling for Operating Theatre Scheduling',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/lwq96/NewProject',
	author='SDP18',
	author_email='e0176071@u.nus.edu',
	license='MIT',
	classifiers=classifiers,
	keywords='metaheuristic, surgery, scheduling',
	packages=find_packages(),
	install_requires=install_requires,
	data_files=data_files
)