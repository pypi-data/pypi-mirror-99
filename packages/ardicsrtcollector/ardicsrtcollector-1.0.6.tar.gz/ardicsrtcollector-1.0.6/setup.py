import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as _in:
        return _in.read()

# This call to setup() does all the work
setup(
    name="ardicsrtcollector",
    # The version of this library.
    # Read this as
    #   - MAJOR VERSION 1
    #   - MINOR VERSION 0
    #   - MAINTENANCE VERSION 0
    version="1.0.6",
    description="Generates a dataset for the Turkish speech recognition.",
    # description and Project name| library name
    long_description=read('README.rst'),
    long_description_content_type="text/markdown",

    author="ARDIC R&D",
    author_email="yavuz.erzurumlu@ardictech.com",
    url="https://github.com/IoT-Ignite/ArdicSrtCollector",
     # These are the dependencies the library needs in order to run.
    install_requires=[
        'youtube-channel-transcript-api',
        'youtube_dl',
    ],

    py_modules=["ardicsrtcollector/*" ],
    packages=['ardicsrtcollector'],
    packages_dir={'': 'ardicsrtcollector'},

    include_package_data=True,

   
    entry_points={
        "console_scripts": [
            "ardicsrtcollector=ardicsrtcollector:get_all_srt_mp3_files",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers"
    ],

    # Here are the keywords of my library.
    keywords='dataset, speech recognition, srt, youtube srt',
    license="MIT",
)
