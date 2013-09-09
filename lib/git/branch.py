
def current(proc):
    cmd = 'git branch'
    out, _ = proc.process(cmd)
    for line in out:
        if line and line.startswith('*'):
            return line[1:].strip()
        
    return ''

def switch(proc, to):
    cmd = 'git checkout -f %s' % to
    proc.process(cmd)
    
    print 'switch to branch [%s]' % to
    
def revert(proc):
    cmd = 'git checkout .'
    proc.process(cmd)
    
    cmd = 'git clean -f -d'    # remove un-versioned files
    proc.process(cmd)
    
    print 'reverted old changes'
    
def track(proc, name):
    cmd = 'git checkout --track origin/%s' % name
    proc.process(cmd)
    
    print 'pull branch [%s] from master' % name
    
def create(proc, name):
    cmd = 'git checkout -b %s' % name
    proc.process(cmd)
    
    print 'create branch [%s]' % name

def delete(proc, name):
    cmd = 'git branch -D %s' % name
    proc.process(cmd)
    
    print 'deleted branch [%s]' % name

def pull(proc):
    cmd = 'git pull'    
    proc.process(cmd)

def forceRevert(proc):
    revert(proc)
    pull(proc)

def forceSwitch(proc, name):
    switch(proc, name)
    if current(proc) != name:
        track(proc, name)
    if current(proc) != name:
        create(proc, name)
        
    forceRevert(proc)
    
def forceReCreate(proc, name):
    if name == 'master': return False
    revert(proc)
    switch(proc, 'master')
    pull(proc)
    delete(proc, name)
    track(proc, name)
    return current(proc) == name