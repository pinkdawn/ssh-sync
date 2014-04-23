# -*- coding: utf-8 -*-

from config import *
from lib.cmd import cmd
from lib.sftp import sftp
from lib.ssh import ssh
from lib.cache import ModifyCache
from lib import git, cert
from datetime import datetime

import os, sys

def setupSsh():
    remote = ssh(host, user, pwd, pkey)
    remote.precall('cd %s' % remote_git)
    return remote

def setupLocal():
    os.chdir(local_git)
    return cmd()  
    
def syncBranch(local_branch, remote):
    git.branch.revert(remote)
    if local_branch != git.branch.current(remote):
        git.branch.forceSwitch(remote, local_branch)

def modified(file):
    try:
        return os.path.getmtime(file)
    except:
        return 0

def getNewFiles(files, cache):
    return [x for x in files if cache.set(x, modified(x))]

def syncNewFiles(changed, added, deleted):
    _added = []
    _deleted = []
    _changed = []

    with ModifyCache('added') as cache:
        _added += getNewFiles(added, cache)
        for x in cache.allKeys():
            if x not in _added and cache.set(x, modified(x)):
                _deleted.append(x)
                cache.removeKey(x)

    with ModifyCache('changed') as cache:
        _changed += getNewFiles(changed, cache)
        for x in cache.allKeys():
            if x not in _changed and cache.set(x, modified(x)):
                _changed.append(x)
                cache.removeKey(x)

    with ModifyCache('deleted') as cache:
        _deleted += getNewFiles(deleted, cache)
        for x in cache.allKeys():
            if x not in _deleted and cache.set(x, modified(x)):
                _added.append(x)
                cache.removeKey(x)

    syncFiles(_changed, _added, _deleted)

def syncFiles(changed, added, deleted):
    with sftp(host, user, pwd, pkey) as ftp:
        for f in changed:
            ftp.put(f, remote_git + '/' +f)

        for f in deleted:
            try:
                ftp.remove(remote_git + '/' +f)
            except:
                pass # already removed

        for f in added:
            try:
                ftp.put(f, remote_git + '/' +f)
            except:  # should check whether it's directory exception
                ftp.mkdirs(os.path.split(remote_git + '/' +f)[0])
                ftp.put(f, remote_git + '/' +f)

def clearCache():
    ModifyCache.clear('added')
    ModifyCache.clear('changed')
    ModifyCache.clear('deleted')

if __name__=="__main__":
    local = setupLocal()
    print 'Start at --------- ' + str(datetime.now())[:19]

    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        syncNewFiles(*git.status.ls(local))
    else:
        with setupSsh() as remote:
            local_branch = git.branch.current(local)

            if len(sys.argv) == 1:
                syncBranch(local_branch, remote)
                syncFiles(*git.status.ls(local))
                clearCache()
            elif len(sys.argv) > 1 and sys.argv[1] == '-r':
                git.branch.forceReCreate(remote, local_branch)
                clearCache()
            elif len(sys.argv) > 1 and sys.argv[1] == '-s':
                cert.replace(remote, ssl_path, ssl_domain, ssl_crt, ssl_key)
