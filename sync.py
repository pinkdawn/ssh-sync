# -*- coding: utf-8 -*-
# easy_install pycrypto
# easy_install paramiko

from lib.cmd import cmd
from lib.sftp import sftp
from lib.ssh import ssh
from lib import git
import os

local_git = 'd:/php/refinery29'

host = 'suryani.dev.rf29.net'
pkey = 'C:/Users/ben.zhuang/.ssh/id_rsa'
pwd = '850202'
user = 'devuser'
remote_git = '/var/refinery29'

os.chdir(local_git)
local_branch = git.branch.current(cmd())

# switch to same branch, and clean it
remote = ssh(host, user, pwd, pkey)
remote.precall('cd %s' % remote_git)
if local_branch != git.branch.current(remote):
    git.branch.revert(remote)
    git.branch.force_switch(remote, local_branch)
git.branch.revert(remote)

# make the same changes as local
changed, added, deleted = git.status.ls(cmd())
ftp = sftp(host, user, pwd, pkey)
ftp.chdir(remote_git)
for f in changed:
    ftp.put(f, f)
for f in deleted:
    ftp.remove(f)
for f in added:
    try:
        ftp.put(f, f)
    except:
        ftp.mkdirs(os.path.split(f)[0])
        ftp.put(f, f)

ftp.close()
remote.close()

    