from setuptools import setup, find_packages

VERSION = '0.2.3'
DESCRIPTION = 'NBA2-lite-server'
LONG_DESCRIPTION = 'Interface to the NBA2-lite to be replace with any other server handler'

# Setting up
setup(
    name="NBA2LiteServer",
    version=VERSION,
    author="Test1",
    author_email="byhouse1@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'psutil', 'paramiko', 'Flask', 'Flask-Cors', 'furl'],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)