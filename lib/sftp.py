import paramiko, os


class sftp(object):
    def __init__(self, host, user, pwd, pkey):
        self.t = paramiko.Transport((host, 22))
        key = paramiko.RSAKey.from_private_key_file(pkey, pwd)
        self.t.connect(username=user, pkey=key)
        self._sftp = paramiko.SFTPClient.from_transport(self.t)
        print 'SFTP connected'
        
    def put(self, src, dest):
        self._sftp.put(src, dest)
        print 'put: [%s]' % dest

    def remove(self, path):
        self._sftp.remove(path)
        print 'remove: [%s]' % path

    def chdir(self, path):
        self._sftp.chdir(path)
        print 'cd: [%s]' % path

    def mkdir(self, path):
        self._sftp.mkdir(path)
        print 'mkdir: [%s]' % path

    def mkdirs(self, path):
        try:
            self.mkdir(path)
        except:
            self.mkdirs(os.path.dirname(path))
            self.mkdir(path)

    def __enter__(self):
        return self     
        
    def __exit__(self, _type, _value, _traceback):
        self.t.close()
        print 'SFTP disconnected'