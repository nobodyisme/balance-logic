import os
from setuptools import setup

PACKAGE = "BalanceLogic"

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = PACKAGE,
    version = __import__("balancelogic").__version__,
    author = "Vitaly Kapustian",
    author_email = "vkap@yandex-team.ru",
    description = ("A library implementing balance logic for distributed key-value storages."),
    license = "LGPL",
    keywords = "balancelogic distributed storage",
    url = "http://github.com/vkap/balance-logic",
    packages=['balancelogic'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Database",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    ],
)
