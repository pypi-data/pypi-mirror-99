import os
import sys
from distutils.sysconfig import get_python_lib
from setuptools import setup, find_packages


name="nxp_ls"
relative_site_packages = get_python_lib().split(sys.prefix + os.sep)[1]
data_files_relative_path = os.path.join(relative_site_packages, name)


setup(
    name=name,
    version="1.1.0",
    author="Larry Shen",
    author_email="larry.shen@nxp.com",
    license="MIT",

    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'lava_docker_slave = nxp_ls:main',
        ]
    },
    data_files=[(data_files_relative_path, ['lava_docker_slave'])],
)
