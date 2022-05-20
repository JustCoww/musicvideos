from setuptools import setup, find_packages

VERSION = '1.0.7'
DESCRIPTION = 'Old slowedvideos now musicvideos, Various scripts from justcow.'

# Setting up
setup(
    name="musicvideos",
    version=VERSION,
    author="JustCow",
    author_email="<justcow@pm.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['moviepy', 'pedalboard', 'pillow', 'soundfile'],
    keywords=['python', 'video', 'audio', 'justcow'],
    include_package_data=True ,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
