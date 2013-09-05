@ECHO OFF 
set PYTHONPATH=D:\py\ssh-sync\ 
setlocal 
cd /d D:\py\ssh-sync\  
python sync.py %1 %2
@ECHO ON