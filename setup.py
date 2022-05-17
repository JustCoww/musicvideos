from setuptools import setup, find_packages

VERSION = '0.6.3'
DESCRIPTION = 'Old slowedvideos now musicvideos, Various scripts from justcow.'

# Setting up
setup(
    name="musicvideos",
    version=VERSION,
    author="JustCow",
    author_email="<justcow@pm.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['moviepy', 'pydub', 'pedalboard', 'yt_dlp', 'pillow', 'soundfile', 'requests', 'google-api-python-client', 'google-auth-oauthlib', 'google-auth-httplib2'],
    keywords=['python', 'video', 'audio', 'justcow'],
    include_package_data=True ,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
