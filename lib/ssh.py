import paramiko

class ssh(object):
    def __init__(self, host, user, pwd, pkey, debug=False):
        self.user = user
        self.host = host
        self.debug = debug
        
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=user, password=pwd, key_filename=pkey)
        self.prefix = ''
        
        print 'SSH connected'
    
    def precall(self, cmd):
        if self.prefix:
            self.prefix = '%s && %s' % (self.prefix, cmd) 
        else:
            self.prefix = cmd

    def process(self, cmd):
        if self.prefix:
            if self.debug: print '%s && %s' % (self.prefix, cmd)
            stdin, stdout, stderr = self.client.exec_command('%s && %s' % (self.prefix, cmd))
        else:
            if self.debug: print cmd
            stdin, stdout, stderr = self.client.exec_command(cmd)
            
        return stdout.readlines(), stderr
    
    def close(self):
        self.client.close()       
