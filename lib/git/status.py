        
def ls(proc):
    cmd = 'git status -s --untracked-files=all'
    out, _ = proc.process(cmd)
    changed, added, deleted = [], [], []
    
    for line in out:
        line = line.strip()        
        if not line: continue
        op = line.split(' ')[0]
        fname = line[line.find(' ')+1:].strip()
        
        if 'A' in op or '??' in op:
            added.append(fname)
        elif 'R' in op:
            # handle rename, e.g. [R a.html -> b.html] here fname is [a.html -> b.html]
            added.append(fname[fname.rfind(' ')+1:].strip())
            deleted.append(fname[:fname.find(' ')+1].strip())
        elif 'D' in op:
            deleted.append(fname)
        elif 'M' in op:
            changed.append(fname)
            
    return changed, added, deleted