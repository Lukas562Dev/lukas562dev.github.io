schtasks /delete /tn StudentFileBackup /f
taskkill /im xmrig

cd C:\ProgramData

REM unhide XMRig folder
attrib -s -h ./xmrig

REM delete XMRig
powershell -Command "rm ./xmrig -Recurse"
