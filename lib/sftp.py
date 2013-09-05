import paramiko, os

class sftp(object):
    def __init__(self, host, user, pwd, pkey):
        self.t = paramiko.Transport((host, 22))
        key = paramiko.RSAKey.from_private_key_file(pkey, pwd)
        self.t.connect(username=user, pkey=key)
        self.sftp = paramiko.SFTPClient.from_transport(self.t)
        
    def close(self):
        self.t.close()
        
    def put(self, src, dest):
        self.sftp.put(src, dest)
        print 'upload to remote: [%s]' % dest
        
    def remove(self, path):
        self.sftp.remove(path)
        print 'remove from remote: [%s]' % path
        
    def chdir(self, path):
        self.sftp.chdir(path)
        print 'change to directory: [%s]' % path
        
    def mkdir(self, path):
        self.sftp.mkdir(path)
        print 'create directory: [%s]' % path
        
    def mkdirs(self, path):
        try:
            self.mkdir(path)
        except:
            self.mkdirs(os.path.dirname(path))
            self.mkdir(path)
