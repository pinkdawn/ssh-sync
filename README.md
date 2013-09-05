ssh-sync
========

sync git code to remote server using ssh

**Dependency**
* install python 2.7
* set `python_home` and `python_home/Scripts` to `PATH`
* `python doc/ez_setup.py`
* `easy_install paramiko`
* `easy_install pycrypto` 
 * or goto: `doc/pycrypto-2.3.1.win7x64-py2.7x64.7z` or find a win32 version yourself, uncompress it, copy to `python_home/Lib/site-packages`
 
**Run it**
* edit `config.py`
* goto `doc/run.cmd`, change the location to your `project_home`
* run `run.cmd`

**To Do**
* now only support using private key to ssh login, can easily modified to use username & password
