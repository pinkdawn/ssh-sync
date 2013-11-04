# -*- coding: utf-8 -*-

from config import *
from lib.cmd import cmd
from lib.sftp import sftp
from lib.ssh import ssh
from datetime import datetime

from lib import git, cert
import os, sys, pickle, tempfile

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

def loadLastModified():
    try:
        f = os.path.join(tempfile.gettempdir(), 'last_modified')
        return pickle.load(open( f, "rb"))
    except IOError:
        return {}

def saveLastModified(last_modifed):
    f = os.path.join(tempfile.gettempdir(), 'last_modified')
    pickle.dump(last_modifed, open(f, "wb"))

def getNewFiles(files, last_modified):
    result = []
    for f in files:
        if (f not in last_modified or last_modified[f] != os.path.getmtime(f)):
            result.append(f)
            last_modified[f] = os.path.getmtime(f)
    return result

def syncNewFiles(changed, added, deleted):
    last_modifed = loadLastModified()

    syncFiles(getNewFiles(changed, last_modifed),
              getNewFiles(added, last_modifed),
              getNewFiles(deleted, last_modifed),
              )

    saveLastModified(last_modifed)

def syncFiles(changed, added, deleted):
    with sftp(host, user, pwd, pkey) as ftp:
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
            elif len(sys.argv) > 1 and sys.argv[1] == '-r':
                git.branch.forceReCreate(remote, local_branch)
                saveLastModified({})
            elif len(sys.argv) > 1 and sys.argv[1] == '-s':
                cert.replace(remote, ssl_path, ssl_domain, ssl_crt, ssl_key)
