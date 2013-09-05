import subprocess

class cmd(object):
    def __init__(self):
        pass
        
    def process(self, cmd):
        p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
        out, err = p.communicate()
        return out.split('\n'), err
