# -*- coding: utf-8 -*-

from config import *
from lib.cmd import cmd
from lib.sftp import sftp
from lib.ssh import ssh
from lib import git
import os

os.chdir(local_git)
local = cmd()
local_branch = git.branch.current(local)

remote = ssh(host, user, pwd, pkey)
remote.precall('cd %s' % remote_git)

ftp = sftp(host, user, pwd, pkey)
ftp.chdir(remote_git)

if local_branch != git.branch.current(remote):
    git.branch.force_switch(remote, local_branch)

changed, added, deleted = git.status.ls(local)

# upload changed files
for f in changed:
    ftp.put(f, f)

# remove deleted files
for f in deleted:
    ftp.remove(f)

# upload added files, if exception, try create directory first
for f in added:
    try:
        ftp.put(f, f)
    except:
        ftp.mkdirs(os.path.split(f)[0])
        ftp.put(f, f)

ftp.close()
remote.close()

    