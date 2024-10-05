#!/usr/bin/python3
"""Deletes out-of-date archives.

Usage:
    fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu 
    > /dev/null 2>&1
"""

import os
from fabric.api import env, local, run, cd, lcd

env.hosts = ['52.23.237.49', '54.205.189.207']


def do_clean(number=0):
    """Delete out-of-date archives.

    This function removes old archives from the local versions
    directory and the remote server's web_static releases.

    Args:
        number (int): The number of archives to keep. 
            If number is 0 or 1, keeps only the most recent archive. 
            If number is 2, keeps the most and second-most recent archives,
            etc. Defaults to 0.

    Returns:
        None
    """
    number = 1 if int(number) == 0 else int(number)

    # List the archives in the local versions directory and sort them
    archives = sorted(os.listdir("versions"))

    # Remove old archives
    [archives.pop() for _ in range(number)]

    # Remove archives from the local versions directory
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Remove old web_static releases from the remote server
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]

        # Remove old web_static releases
        [archives.pop() for _ in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
