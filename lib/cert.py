import os

def remove(proc, path):
    proc.process("sudo rm %s/*.crt" % path)
    proc.process("sudo rm %s/*.key" % path)
    
def upload(proc, path, domain, crtFile, keyFile):
    with open(os.path.join(os.environ['PYTHONPATH'], crtFile)) as crt:
        target_crt = "%s/%s.crt" % (path, domain)
        proc.process("echo \"%s\" | sudo tee %s" % (crt.read(), target_crt))
        proc.process("sudo chmod 664 %s" % target_crt)
    with open(os.path.join(os.environ['PYTHONPATH'], keyFile)) as key:
        target_key = "%s/%s.key" % (path, domain)
        proc.process("echo \"%s\" | sudo tee %s" % (key.read(), target_key))
        proc.process("sudo chmod 664 %s" % target_key)

def replace(proc, path, domain, crt, key):
    proc.process("sudo /etc/init.d/nginx stop")
    
    remove(proc, path)
    upload(proc, path, domain, crt, key)
    
    proc.process("sudo /etc/init.d/nginx start")