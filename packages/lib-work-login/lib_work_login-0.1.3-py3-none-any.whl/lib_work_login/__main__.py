#!/home/anon/env/bin/python3
# -*- coding: utf-8 -*-

"""Main file for entry points"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


from .work_login import WorkLogin

def main():
    WorkLogin().login()

def configure():
    WorkLogin().configure()
