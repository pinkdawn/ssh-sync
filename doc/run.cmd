@ECHO OFF 
SETLOCAL
set PYTHONPATH=D:\py\ssh-sync
cd /d D:\py\ssh-sync\  
python sync.py %1 %2
ENDLOCAL
@ECHO ON