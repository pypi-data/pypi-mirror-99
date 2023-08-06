import os
from setuptools import setup, find_packages
from shutil import copy


name = "nxp_ls"
script = "lava_docker_slave"

try:
    copy(script, name)
except:
    pass

setup(
    name=name,
    version="1.1.4",
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

    package_data={'': [script]},
)

#try:
#    os.remove(os.path.join(name, script))
#except:
#    pass
