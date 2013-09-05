
def current(proc):
    cmd = 'git branch'
    out, _ = proc.process(cmd)
    for line in out:
        if line and line.startswith('*'):
            return line.replace('*', '').strip()
        
    return ''

def switch(proc, to):
    cmd = 'git checkout -f %s' % to
    proc.process(cmd)
    
    print 'switch to branch [%s]' % to
    
def revert(proc):
    cmd = 'git checkout .'
    proc.process(cmd)
    
    cmd = 'git clean -f'    # remove un-versioned files
    proc.process(cmd)
    
def track(proc, name):
    cmd = 'git checkout --track origin/%s' % name
    proc.process(cmd)
    
    print 'pull branch [%s] from master' % name
    
def create(proc, name):
    cmd = 'git checkout -b %s' % name
    proc.process(cmd)
    
    print 'create branch [%s]' % name
    
def force_switch(proc, name):
    revert(proc, name)
    switch(proc, name)
    if current(proc) != name:
        track(proc, name)
    if current(proc) != name:
        create(proc, name)
    revert(proc, name)