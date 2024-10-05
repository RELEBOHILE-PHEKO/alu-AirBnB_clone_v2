#!/usr/bin/python3
"""Fabric function sends archived static site to webservers"""
import os
from fabric.api import env, local, run, cd, lcd

env.hosts = ['52.23.237.49', '54.205.189.207']

def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.
            If number is 0 or 1, keeps only the most recent archive.
            If number is 2, keeps the most and second-most recent archives, etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    # Remove old archives
    [archives.pop() for _ in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        # Remove old web_static releases
        [archives.pop() for _ in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
